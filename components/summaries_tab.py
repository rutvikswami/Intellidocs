"""
Summaries tab component
"""

import streamlit as st

def render_summaries_tab():
    """Render the summaries tab"""
    st.header("📊 Document Summaries & FAQs")
    
    if not st.session_state.rag_system.documents:
        st.info("Upload documents to generate summaries!")
    else:
        doc_list = st.session_state.rag_system.get_document_list()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Generate Summary")
            if doc_list:
                selected_doc = st.selectbox("Select document for summary", doc_list)
                
                if st.button("🔄 Generate Summary"):
                    with st.spinner("Generating summary..."):
                        summary = st.session_state.rag_system.generate_document_summary(selected_doc)
                        st.session_state.current_summary = summary
                
                if hasattr(st.session_state, 'current_summary'):
                    st.markdown(f'<div class="summary-box">{st.session_state.current_summary}</div>', 
                              unsafe_allow_html=True)
        
        with col2:
            st.subheader("❓ Generate FAQ")
            if doc_list:
                selected_doc_faq = st.selectbox("Select document for FAQ", doc_list, key="faq_doc")
                
                if st.button("🔄 Generate FAQ"):
                    with st.spinner("Generating FAQ..."):
                        faq = st.session_state.rag_system.generate_document_faq(selected_doc_faq)
                        st.session_state.current_faq = faq
                
                if hasattr(st.session_state, 'current_faq'):
                    st.markdown(f'<div class="summary-box">{st.session_state.current_faq}</div>', 
                              unsafe_allow_html=True)