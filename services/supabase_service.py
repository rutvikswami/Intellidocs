"""
Supabase service for IntelliDocs
Handles logging and analytics
"""

import os
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
import streamlit as st

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("⚠️ Supabase not installed. Logging features disabled.")

class SupabaseService:
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client"""
        if not SUPABASE_AVAILABLE:
            return
        
        try:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            
            if supabase_url and supabase_key:
                self.client = create_client(supabase_url, supabase_key)
            else:
                st.info("ℹ️ Supabase credentials not found. Running without logging.")
        except Exception as e:
            st.warning(f"⚠️ Supabase connection failed: {str(e)}")
            self.client = None
    
    def log_chat_interaction(self, query: str, response: str, sources: List[str], 
                           user_id: str = 'demo_user', response_time_ms: int = None) -> bool:
        """Log chat interaction to Supabase"""
        if not self.client:
            return False
        
        try:
            # Generate session_id if not in session state
            if 'session_id' not in st.session_state:
                st.session_state.session_id = str(uuid.uuid4())
            
            data = {
                'query': query,
                'response': response,
                'sources': sources,
                'user_id': user_id,
                'session_id': st.session_state.session_id,
                'response_time_ms': response_time_ms,
                'document_count': len(sources)
            }
            
            result = self.client.table('chat_logs').insert(data).execute()
            return True
        except Exception as e:
            st.warning(f"Failed to log interaction: {str(e)}")
            return False
    
    def log_document_upload(self, file_name: str, file_type: str, file_size: int,
                           chunk_count: int, processing_time_ms: int = None,
                           user_id: str = 'demo_user') -> bool:
        """Log document upload to Supabase"""
        if not self.client:
            return False
        
        try:
            data = {
                'file_name': file_name,
                'file_type': file_type,
                'file_size': file_size,
                'chunk_count': chunk_count,
                'processing_time_ms': processing_time_ms,
                'user_id': user_id,
                'upload_status': 'success',
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('document_uploads').insert(data).execute()
            return True
        except Exception as e:
            st.warning(f"Failed to log upload: {str(e)}")
            return False
    
    def log_analytics_event(self, event_type: str, event_data: Dict[str, Any] = None,
                           user_id: str = 'demo_user') -> bool:
        """Log analytics event to Supabase"""
        if not self.client:
            return False
        
        try:
            # Generate session_id if not in session state
            if 'session_id' not in st.session_state:
                st.session_state.session_id = str(uuid.uuid4())
                
            data = {
                'event_type': event_type,
                'event_data': event_data or {},
                'user_id': user_id,
                'session_id': st.session_state.session_id
            }
            
            result = self.client.table('usage_analytics').insert(data).execute()
            return True
        except Exception as e:
            st.warning(f"Failed to log analytics: {str(e)}")
            return False
    
    def get_chat_history(self, user_id: str = 'demo_user', limit: int = 50) -> List[Dict]:
        """Get chat history for user"""
        if not self.client:
            return []
        
        try:
            result = self.client.table('chat_logs')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data
        except Exception as e:
            st.warning(f"Failed to get chat history: {str(e)}")
            return []
    
    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Get analytics data for dashboard"""
        if not self.client:
            return {}
        
        try:
            # Get recent activity
            recent_queries = self.client.table('chat_logs')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(10)\
                .execute()
            
            # Get document upload stats
            upload_stats = self.client.table('document_uploads')\
                .select('*')\
                .order('created_at', desc=True)\
                .execute()
            
            # Get usage analytics
            analytics = self.client.table('analytics_dashboard')\
                .select('*')\
                .limit(30)\
                .execute()
            
            return {
                'recent_queries': recent_queries.data,
                'upload_stats': upload_stats.data,
                'daily_analytics': analytics.data
            }
        except Exception as e:
            st.warning(f"Failed to get analytics: {str(e)}")
            return {}
    
    def get_connection_status(self) -> bool:
        """Check if Supabase connection is working"""
        if not self.client:
            return False
        
        try:
            # Simple query to test connection
            result = self.client.table('chat_logs').select('count').limit(1).execute()
            return True
        except Exception as e:
            return False