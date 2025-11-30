"""
Sidebar component for document management
"""

import streamlit as st
import tempfile
import os

def render_sidebar():
    """Render the document management sidebar"""
    with st.sidebar:
        st.header("📄 Document Management")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF, DOCX, or TXT files"
        )
        
        if uploaded_files:
            st.subheader("Processing Documents...")
            
            for uploaded_file in uploaded_files:
                # Get file type
                file_type = uploaded_file.name.split('.')[-1].lower()
                
                # Process document
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    success, message = st.session_state.rag_system.process_document(
                        uploaded_file.getvalue(),
                        uploaded_file.name,
                        file_type
                    )
                
                if success:
                    st.success(f"✅ {uploaded_file.name}")
                else:
                    st.error(f"❌ {uploaded_file.name}: {message}")
        
        st.divider()
        
        # Document stats
        document_count = len(st.session_state.rag_system.documents)
        unique_docs = len(st.session_state.rag_system.get_document_list())
        st.metric("📊 Document Chunks", document_count)
        st.metric("📁 Unique Documents", unique_docs)
        
        # Document list
        if st.session_state.rag_system.documents:
            st.subheader("📋 Uploaded Documents")
            for doc_name in st.session_state.rag_system.get_document_list():
                st.text(f"• {doc_name}")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()