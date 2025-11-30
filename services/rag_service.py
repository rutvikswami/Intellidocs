"""
IntelliDocs RAG Service
Core functionality for document processing and AI interactions
"""

import streamlit as st
import os
from datetime import datetime
import tempfile
import traceback
from pathlib import Path
from typing import List, Dict, Optional

# Core imports
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np
from .supabase_service import SupabaseService

# Document processing imports
import PyPDF2
try:
    from docx import Document as docx_Document
    DOCX_AVAILABLE = True
except ImportError:
    try:
        import python_docx
        from python_docx import Document as docx_Document
        DOCX_AVAILABLE = True
    except ImportError:
        DOCX_AVAILABLE = False

# Load environment variables
load_dotenv()

# Configure Gemini API
if os.getenv('GEMINI_API_KEY'):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class IntelliDocsRAG:
    def __init__(self):
        self.embedding_model = None
        self.documents = []  # Simple in-memory storage
        self.embeddings = []
        
        # Initialize Supabase service
        self.supabase_service = SupabaseService()
        
        # Initialize Gemini only if API key is available
        try:
            if os.getenv('GEMINI_API_KEY'):
                self.gemini_model = genai.GenerativeModel('gemini-pro-latest')
            else:
                self.gemini_model = None
                st.warning("⚠️ Gemini API key not found. AI responses will be limited.")
        except Exception as e:
            self.gemini_model = None
            st.error(f"Error initializing Gemini: {str(e)}")
    
    @st.cache_resource
    def load_embedding_model(_self):
        """Load sentence transformer model"""
        try:
            return SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            st.error(f"Error loading embedding model: {str(e)}")
            return None
    
    def initialize_vectordb(self):
        """Initialize simple vector storage"""
        if self.embedding_model is None:
            self.embedding_model = self.load_embedding_model()
    
    def process_document(self, file_content: bytes, file_name: str, file_type: str) -> tuple[bool, str]:
        """Process uploaded document and add to simple storage"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            try:
                # Read document based on file type
                text = ""
                if file_type.lower() == 'pdf':
                    text = self._extract_pdf_text(tmp_file_path)
                elif file_type.lower() == 'docx':
                    text = self._extract_docx_text(tmp_file_path)
                elif file_type.lower() == 'txt':
                    text = self._extract_txt_text(tmp_file_path)
                else:
                    return False, f"Unsupported file type: {file_type}"
                
                if not text or not text.strip():
                    return False, "No text content found in document"
                
                # Simple text splitting
                chunks = self.split_text(text, chunk_size=800, overlap=100)
                
                if not chunks:
                    return False, "No chunks created from document"
                
                # Generate embeddings and store
                if self.embedding_model is None:
                    return False, "Embedding model not available"
                
                chunks_added = 0
                for i, chunk in enumerate(chunks):
                    if chunk.strip():
                        try:
                            embedding = self.embedding_model.encode([chunk])[0]
                            
                            self.documents.append({
                                "text": chunk,
                                "source": file_name,
                                "chunk_id": i,
                                "id": f"{file_name}_{i}"
                            })
                            self.embeddings.append(embedding)
                            chunks_added += 1
                        except Exception as e:
                            st.warning(f"Error processing chunk {i}: {str(e)}")
                            continue
                
                # Log document upload to Supabase
                self.supabase_service.log_document_upload(
                    file_name=file_name,
                    file_type=file_type,
                    file_size=len(file_content),
                    chunk_count=chunks_added
                )
                
                return True, f"Successfully processed {chunks_added} chunks from {file_name}"
                
            finally:
                # Clean up temp file
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
            
        except Exception as e:
            error_msg = f"Error processing document: {str(e)}"
            st.error(error_msg)
            st.error(f"Traceback: {traceback.format_exc()}")
            return False, error_msg
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n[Page {page_num + 1}]\n{page_text}\n"
                    except Exception as e:
                        st.warning(f"Error reading page {page_num + 1}: {str(e)}")
                        continue
            return text
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            if not DOCX_AVAILABLE:
                raise Exception("python-docx library not available")
            
            doc = docx_Document(file_path)
            text_parts = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            return "\n".join(text_parts)
        except Exception as e:
            raise Exception(f"DOCX extraction error: {str(e)}")
    
    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            # First check if file exists and is readable
            if not os.path.exists(file_path):
                raise Exception(f"File does not exist: {file_path}")
            
            if not os.path.isfile(file_path):
                raise Exception(f"Path is not a file: {file_path}")
            
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                        if content and content.strip():
                            return content
                except (UnicodeDecodeError, UnicodeError):
                    continue
                except Exception as e:
                    st.warning(f"Error reading with encoding {encoding}: {str(e)}")
                    continue
            
            # If all encodings fail, try binary read and decode manually
            try:
                with open(file_path, 'rb') as file:
                    raw_content = file.read()
                    # Try to detect encoding
                    content = raw_content.decode('utf-8', errors='replace')
                    return content
            except Exception as e:
                raise Exception(f"Binary read failed: {str(e)}")
            
        except Exception as e:
            raise Exception(f"TXT extraction error: {str(e)}")
    
    def split_text(self, text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        """Simple text splitter"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            if end > text_length:
                end = text_length
            
            chunk = text[start:end]
            actual_end = end
            
            # Try to end at a sentence or paragraph boundary
            if end < text_length:
                # Look for sentence endings
                for boundary in ['. ', '.\n', '!\n', '?\n']:
                    boundary_pos = chunk.rfind(boundary)
                    if boundary_pos > chunk_size * 0.7:  # At least 70% of chunk size
                        chunk = chunk[:boundary_pos + len(boundary)]
                        actual_end = start + boundary_pos + len(boundary)
                        break
            
            if chunk.strip():
                chunks.append(chunk.strip())
            
            # Move start position correctly
            start = actual_end - overlap
            if start <= start or start < 0:
                start = actual_end
            
            if start >= text_length:
                break
                
        return [chunk for chunk in chunks if chunk.strip()]
    
    def search_documents(self, query: str, n_results: int = 3) -> Optional[Dict]:
        """Search for relevant document chunks using cosine similarity"""
        try:
            if not self.documents or self.embedding_model is None:
                return None
            
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Calculate cosine similarities
            similarities = []
            for doc_embedding in self.embeddings:
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                similarities.append(similarity)
            
            # Get top results
            top_indices = np.argsort(similarities)[-n_results:][::-1]
            
            results = {
                "documents": [[self.documents[i]["text"] for i in top_indices]],
                "metadatas": [[{
                    "source": self.documents[i]["source"],
                    "chunk_id": self.documents[i]["chunk_id"]
                } for i in top_indices]],
                "distances": [[1 - similarities[i] for i in top_indices]]
            }
            
            return results
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            return None
    
    def generate_answer(self, query: str, context_docs: List[Dict]) -> str:
        """Generate answer using Gemini with context"""
        try:
            if not self.gemini_model:
                return "AI model not available. Please check your Gemini API key configuration."
            
            # Prepare context
            context = "\n\n".join([
                f"[Source: {doc['source']}]\n{doc['document']}"
                for doc in context_docs
            ])
            
            # Prepare prompt
            prompt = f"""
You are IntelliDocs, an AI knowledge assistant. Answer the user question using ONLY the provided context.

CONTEXT:
{context}

QUESTION: {query}

INSTRUCTIONS:
- Answer based only on the provided context
- If the answer is not in the context, say "This information is not available in the uploaded documents"
- Provide specific citations like [Source: filename.pdf]
- Be concise but complete

ANSWER:
"""
            
            # Generate response
            response = self.gemini_model.generate_content(prompt)
            
            # Log chat interaction to Supabase
            sources = [doc['source'] for doc in context_docs]
            self.supabase_service.log_chat_interaction(
                query=query,
                response=response.text,
                sources=sources
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def generate_document_summary(self, file_name: str) -> str:
        """Generate auto-summary for uploaded document"""
        try:
            if not self.gemini_model:
                return "AI model not available for summary generation."
            
            # Get all chunks for this document
            doc_chunks = [doc for doc in self.documents if doc["source"] == file_name]
            if not doc_chunks:
                return "No content available for summary."
            
            # Combine text (limit to avoid token limits)
            combined_text = "\n".join([chunk["text"] for chunk in doc_chunks])
            if len(combined_text) > 8000:
                combined_text = combined_text[:8000] + "..."
            
            prompt = f"""
Create a comprehensive summary of this document. Include:

1. MAIN TOPIC: What this document is about
2. KEY POINTS: 3-5 most important points  
3. IMPORTANT DETAILS: Specific policies, procedures, or requirements
4. WHO SHOULD READ THIS: Target audience

Document Content:
{combined_text}

Provide a clear, structured summary:
"""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def generate_document_faq(self, file_name: str) -> str:
        """Generate FAQ from document"""
        try:
            if not self.gemini_model:
                return "AI model not available for FAQ generation."
            
            # Get all chunks for this document
            doc_chunks = [doc for doc in self.documents if doc["source"] == file_name]
            if not doc_chunks:
                return "No content available for FAQ."
            
            # Combine text
            combined_text = "\n".join([chunk["text"] for chunk in doc_chunks])
            if len(combined_text) > 8000:
                combined_text = combined_text[:8000] + "..."
            
            prompt = f"""
Based on this document, create a FAQ with 5-8 common questions employees might ask.
Format as Q: [Question] A: [Answer]

Document Content:
{combined_text}

Generate practical FAQ:
"""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating FAQ: {str(e)}"
    
    def compare_documents(self, doc1_name: str, doc2_name: str) -> str:
        """Compare two documents and highlight differences"""
        try:
            if not self.gemini_model:
                return "AI model not available for document comparison."
            
            # Get chunks for both documents
            doc1_chunks = [doc for doc in self.documents if doc["source"] == doc1_name]
            doc2_chunks = [doc for doc in self.documents if doc["source"] == doc2_name]
            
            if not doc1_chunks or not doc2_chunks:
                return "One or both documents not found."
            
            # Combine text for each document
            doc1_text = "\n".join([chunk["text"] for chunk in doc1_chunks])[:6000]
            doc2_text = "\n".join([chunk["text"] for chunk in doc2_chunks])[:6000]
            
            prompt = f"""
Compare these two documents and provide:

1. SIMILARITIES: What's the same between them
2. DIFFERENCES: Key changes or variations
3. NEW ADDITIONS: What's in Document 2 that's not in Document 1
4. REMOVED CONTENT: What's in Document 1 that's not in Document 2
5. SUMMARY: Overall comparison conclusion

Document 1 ({doc1_name}):
{doc1_text}

Document 2 ({doc2_name}):
{doc2_text}

Provide structured comparison:
"""
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error comparing documents: {str(e)}"
    
    def get_document_list(self) -> List[str]:
        """Get list of unique document names"""
        return list(set([doc["source"] for doc in self.documents]))
    
    def get_document_preview(self, file_name: str, max_chars: int = 2000) -> str:
        """Get preview of document content"""
        doc_chunks = [doc for doc in self.documents if doc["source"] == file_name]
        if not doc_chunks:
            return "Document not found."
        
        # Get first few chunks for preview
        preview_text = "\n".join([chunk["text"] for chunk in doc_chunks[:3]])
        
        if len(preview_text) > max_chars:
            preview_text = preview_text[:max_chars] + "..."
        
        return preview_text