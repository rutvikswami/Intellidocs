"""
Document comparison tab component
"""

import streamlit as st

def render_compare_tab():
    """Render the document comparison tab"""
    st.header("🔍 Multi-Document Comparison")
    
    if len(st.session_state.rag_system.get_document_list()) < 2:
        st.warning("Upload at least 2 documents to use comparison feature!")
    else:
        doc_list = st.session_state.rag_system.get_document_list()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Document 1")
            doc1 = st.selectbox("Select first document", doc_list, key="doc1")
            
            if doc1:
                preview1 = st.session_state.rag_system.get_document_preview(doc1, 1000)
                st.markdown(f'<div class="doc-preview">{preview1}</div>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("📄 Document 2")
            remaining_docs = [d for d in doc_list if d != doc1] if 'doc1' in locals() else doc_list
            doc2 = st.selectbox("Select second document", remaining_docs, key="doc2") if remaining_docs else None
            
            if doc2:
                preview2 = st.session_state.rag_system.get_document_preview(doc2, 1000)
                st.markdown(f'<div class="doc-preview">{preview2}</div>', unsafe_allow_html=True)
        
        # Comparison section
        if 'doc1' in locals() and 'doc2' in locals() and doc1 and doc2:
            st.divider()
            
            if st.button("🔍 Compare Documents", type="primary"):
                with st.spinner("Analyzing differences..."):
                    comparison = st.session_state.rag_system.compare_documents(doc1, doc2)
                    st.session_state.comparison_result = comparison
            
            if hasattr(st.session_state, 'comparison_result'):
                st.subheader("📊 Comparison Results")
                st.markdown(f'<div class="comparison-box">{st.session_state.comparison_result}</div>', 
                          unsafe_allow_html=True)
        
        # Quick comparison suggestions
        st.divider()
        st.subheader("💡 Suggested Comparisons")
        
        comparison_examples = [
            "Policy V1 vs Policy V2 - Version differences",
            "Employee Handbook vs Remote Work Policy - Overlapping guidelines", 
            "Training Manual vs Quick Reference - Depth comparison",
            "Draft vs Final - Change tracking"
        ]
        
        for example in comparison_examples:
            st.info(f"📌 {example}")
    
    # Example queries for comparison
    st.divider()
    st.subheader("🔥 Try These Comparison Questions")
    st.markdown("""
    - "What changed between the old policy and new policy?"
    - "Which document has more detailed guidelines?"
    - "What requirements are the same in both documents?"
    - "What new rules were added in the updated version?"
    """)