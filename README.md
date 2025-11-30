# 🧠 IntelliDocs - AI Document Intelligence Agent

Transform how you interact with documents using advanced AI technology. Upload documents, ask questions, get intelligent answers with citations.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.42%2B-red) ![AI](https://img.shields.io/badge/AI-Google%20Gemini-green)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation
```bash
# 1. Clone and setup
git clone <your-repo-url>
cd yalo
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here

# 3. Run the application
streamlit run app.py
```

**🎉 That's it! Open http://localhost:8501 and start uploading documents.**

---

## 🎯 What is IntelliDocs?

IntelliDocs is an **intelligent document processing agent** that uses Retrieval-Augmented Generation (RAG) to help you:

- **Chat with your documents** using natural language
- **Get accurate answers** with source citations  
- **Generate summaries** and FAQs automatically
- **Compare documents** to find differences
- **Track analytics** on document usage

### How It Works
1. 📄 **Upload** → Documents are processed and indexed
2. 🤖 **Ask** → AI searches and retrieves relevant content  
3. ✅ **Get Answers** → Contextual responses with citations

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📄 **Multi-Format Support** | PDF, DOCX, TXT file processing |
| 🤖 **AI Chat Interface** | Natural language Q&A with citations |
| 📊 **Document Summaries** | Auto-generated content overviews |
| ❓ **FAQ Generation** | Automatic question-answer pairs |
| 🔍 **Document Comparison** | Side-by-side difference analysis |
| 📈 **Analytics Dashboard** | Usage tracking and metrics |
| 🔒 **Secure Processing** | Privacy-focused document handling |
| ⚡ **Real-time Responses** | Streaming AI with source references |

### Limitations
- Files >10MB may process slowly
- Optimized for English content
- Requires internet for AI processing

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Frontend** | Streamlit | Web application framework |
| **AI Engine** | Google Gemini Pro | Text generation & chat responses |
| **Embeddings** | Sentence Transformers | Semantic search (local) |
| **Vector DB** | ChromaDB | Document similarity matching |
| **Database** | Supabase (optional) | Analytics & chat history |
| **Processing** | PyPDF2, python-docx | Document parsing |

### Required APIs
- **Google Gemini API**: Get free key at [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Supabase** (optional): For persistent storage and analytics

## 💡 Usage

1. **Upload Documents**: Use the sidebar to upload PDF, DOCX, or TXT files
2. **Wait for Processing**: Documents are automatically chunked and indexed
3. **Ask Questions**: Type natural language queries in the chat interface
4. **Explore Features**: Try different tabs for summaries, comparisons, and analytics
5. **Check Sources**: Every AI response includes document citations

### Example Questions
- "What are the key benefits mentioned in the document?"
- "Summarize the main points of section 3"
- "What policies apply to remote work?"

---

## 📚 Additional Resources

- 📖 **[Streamlit Deployment Guide](STREAMLIT_DEPLOYMENT.md)** - Step-by-step deployment instructions
- 🏗️ **[Architecture Diagram](ARCHITECTURE_DIAGRAM_PROMPT.md)** - System design visualization
- 🗄️ **[Database Setup](SUPABASE_SETUP.md)** - Optional Supabase configuration
- ⚙️ **[Configuration](.env.example)** - Environment variables template

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**🎉 Ready to start your intelligent document journey!**

*Built with ❤️ using Streamlit, Google AI, and modern Python technologies*
