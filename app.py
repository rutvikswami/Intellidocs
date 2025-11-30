"""
IntelliDocs - AI Knowledge Base Agent
Main Streamlit Application
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from services.rag_service import IntelliDocsRAG
from components.sidebar import render_sidebar
from components.chat_tab import render_chat_tab
from components.documents_tab import render_documents_tab
from components.summaries_tab import render_summaries_tab
from components.compare_tab import render_compare_tab
from utils.ui_helpers import load_custom_css

def main():
    # Page config
    st.set_page_config(
        page_title="IntelliDocs - AI Knowledge Base",
        page_icon="📚",
        layout="wide"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize RAG system
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = IntelliDocsRAG()
        st.session_state.rag_system.initialize_vectordb()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Header
    st.title("📚 IntelliDocs")
    st.markdown("**AI Knowledge Base Agent** - Upload documents and chat with your company knowledge")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📄 Documents", "📊 Summaries", "🔍 Compare"])
    
    # Sidebar
    render_sidebar()
    
    # Tab content
    with tab1:
        render_chat_tab()
    
    with tab2:
        render_documents_tab()
    
    with tab3:
        render_summaries_tab()
    
    with tab4:
        render_compare_tab()

if __name__ == "__main__":
    main()