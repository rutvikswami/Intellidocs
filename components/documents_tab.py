"""
Documents management tab component
"""

import streamlit as st

def render_documents_tab():
    """Render the documents management tab"""
    st.header("📄 Document Management & Previews")
    
    if not st.session_state.rag_system.documents:
        st.info("Upload documents using the sidebar to get started!")
    else:
        doc_list = st.session_state.rag_system.get_document_list()
        
        for doc_name in doc_list:
            with st.expander(f"📄 {doc_name}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader("Content Preview")
                    preview = st.session_state.rag_system.get_document_preview(doc_name, 3000)
                    st.markdown(f'<div class="doc-preview">{preview}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.subheader("Document Stats")
                    doc_chunks = [doc for doc in st.session_state.rag_system.documents if doc["source"] == doc_name]
                    st.metric("Chunks", len(doc_chunks))
                    st.metric("Total Characters", sum(len(chunk["text"]) for chunk in doc_chunks))