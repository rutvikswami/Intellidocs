"""
Chat tab component
"""

import streamlit as st

def render_chat_tab():
    """Render the chat interface tab"""
    # Right column: Help and document preview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat with Documents")
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat['query'])
            
            with st.chat_message("assistant"):
                st.write(chat['response'])
                if chat.get('sources'):
                    st.caption(f"📎 Sources: {', '.join(chat['sources'])}")
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            if not st.session_state.rag_system.documents:
                st.error("Please upload documents first!")
                return
            
            # Add user message to chat
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Search for relevant documents
                    search_results = st.session_state.rag_system.search_documents(prompt)
                    
                    if search_results and search_results['documents']:
                        # Prepare context documents
                        context_docs = []
                        sources = []
                        
                        for i, doc in enumerate(search_results['documents'][0]):
                            metadata = search_results['metadatas'][0][i]
                            context_docs.append({
                                'document': doc,
                                'source': metadata['source']
                            })
                            if metadata['source'] not in sources:
                                sources.append(metadata['source'])
                        
                        # Generate answer
                        response = st.session_state.rag_system.generate_answer(prompt, context_docs)
                        
                        # Display response
                        st.write(response)
                        st.caption(f"📎 Sources: {', '.join(sources)}")
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            'query': prompt,
                            'response': response,
                            'sources': sources
                        })
                        
                    else:
                        response = "I couldn't find relevant information in the uploaded documents. Please make sure you've uploaded documents and try rephrasing your question."
                        st.write(response)
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            'query': prompt,
                            'response': response,
                            'sources': []
                        })
    
    with col2:
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        **1. Upload Documents**
        - Use the sidebar to upload files
        - Get automatic processing
        
        **2. Ask Questions** 
        - Natural language queries
        - Source citations included
        
        **3. Premium Features**
        - Auto-generated summaries
        - Document comparison
        - Visual previews
        """)
        
        # Document preview
        if st.session_state.rag_system.documents:
            st.subheader("📄 Document Preview")
            doc_list = st.session_state.rag_system.get_document_list()
            if doc_list:
                selected_doc = st.selectbox("Select document", doc_list)
                
                if selected_doc:
                    preview = st.session_state.rag_system.get_document_preview(selected_doc)
                    st.markdown(f'<div class="doc-preview">{preview}</div>', unsafe_allow_html=True)