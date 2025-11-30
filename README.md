# 🧠 IntelliDocs - AI-Powered Document Intelligence Agent

**IntelliDocs** is an advanced AI agent that transforms how you interact with documents. Upload PDFs, Word documents, or text files and engage in intelligent conversations using state-of-the-art Retrieval-Augmented Generation (RAG) technology.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42%2B-red)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-green)
![Database](https://img.shields.io/badge/Database-Supabase-orange)

## 🎯 Agent Overview

IntelliDocs is an **intelligent document processing agent** that combines multiple AI technologies to create a seamless document interaction experience. The agent processes documents through advanced chunking algorithms, creates semantic embeddings, and uses retrieval-augmented generation to provide contextually accurate answers with source citations.

### 🤖 How the Agent Works End-to-End

1. **Document Ingestion**: Users upload documents → Agent processes and chunks content → Creates vector embeddings → Stores in searchable database
2. **Query Processing**: User asks questions → Agent performs semantic search → Retrieves relevant context → Generates AI-powered responses
3. **Advanced Analysis**: Agent can summarize documents, generate FAQs, compare multiple documents, and provide analytics
4. **Continuous Learning**: All interactions are logged for analytics and system improvement

## ✨ Features & Limitations

### 🚀 **Core Features**
- ✅ **Multi-format Document Support**: PDF, DOCX, TXT files
- ✅ **Intelligent Chat Interface**: Natural language queries with citations
- ✅ **Advanced AI Processing**: Document summaries, FAQ generation, comparisons
- ✅ **Real-time Responses**: Streaming AI responses with source references
- ✅ **Document Preview**: Syntax-highlighted content preview
- ✅ **Session Management**: Persistent chat history and user sessions
- ✅ **Analytics Dashboard**: Usage tracking and performance metrics
- ✅ **Secure Processing**: Privacy-focused document handling

### 🎯 **Advanced Capabilities**
- ✅ **Retrieval-Augmented Generation (RAG)**: Context-aware AI responses
- ✅ **Semantic Search**: Vector-based document similarity matching
- ✅ **Document Comparison**: AI-powered difference analysis
- ✅ **Auto-generated Summaries**: Intelligent content condensation
- ✅ **FAQ Generation**: Automatic question-answer pair creation
- ✅ **Audit Logging**: Complete interaction tracking for compliance

### ⚠️ **Current Limitations**
- ❌ **Document Size**: Large files (>10MB) may have processing delays
- ❌ **Language Support**: Optimized for English content (other languages may work but not guaranteed)
- ❌ **Image Processing**: Text extraction from images in PDFs not supported
- ❌ **Real-time Collaboration**: Single-user sessions (no multi-user document editing)
- ❌ **Version Control**: No built-in document versioning system
- ❌ **Offline Mode**: Requires internet connection for AI processing

## 🛠️ Tech Stack & APIs Used

### **Frontend & User Interface**
- **Streamlit 1.42+**: Modern web application framework
- **Custom CSS**: Enhanced UI components and responsive design
- **Session State Management**: Persistent user interactions

### **AI & Machine Learning Stack**
- **Google Gemini Pro API**: Advanced language model for text generation
  - Used for: Chat responses, summaries, FAQ generation, document comparison
  - Rate Limits: Follows Google AI Studio quotas
- **Sentence Transformers**: Local embedding generation
  - Model: `all-MiniLM-L6-v2` for semantic similarity
  - Runs locally for privacy and speed
- **ChromaDB**: Vector database for semantic search
  - In-memory storage for development
  - Persistent storage option available

### **Document Processing**
- **PyPDF2**: PDF text extraction and parsing
- **python-docx**: Microsoft Word document processing
- **Text Processing**: Custom chunking algorithms for optimal context

### **Database & Analytics**
- **Supabase (PostgreSQL)**: Cloud database for persistence
  - Tables: `chat_logs`, `document_uploads`, `chat_sessions`, `usage_analytics`
  - Features: Row Level Security, real-time subscriptions, REST API
- **SQLAlchemy**: Database ORM and connection management

### **Development & Deployment**
- **Python 3.8+**: Core programming language
- **Poetry/pip**: Dependency management
- **Streamlit Cloud**: Deployment platform (ready)
- **Docker**: Containerization support

### **Security & Configuration**
- **Environment Variables**: Secure API key management
- **Row Level Security (RLS)**: Database access control
- **Input Validation**: Document upload safety checks

## 🚀 Setup & Run Instructions

### **Prerequisites**
```bash
# System Requirements
Python 3.8 or higher
pip (Python package manager)
4GB+ RAM (for embedding models)
Internet connection (for AI APIs)
```

### **Step 1: Clone & Install**
```bash
# Clone the repository
git clone <your-repository-url>
cd yalo

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add required keys
nano .env
```

**Required Environment Variables:**
```env
# Required - Get from Google AI Studio
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - For data persistence and analytics
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### **Step 3: Get API Keys**

#### **Google Gemini API (Required)**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Create new API key
4. Copy key to `.env` file as `GEMINI_API_KEY`

#### **Supabase Database (Optional)**
1. Visit [Supabase](https://supabase.com) and create account
2. Create new project
3. Go to Settings → API → Copy URL and anon key
4. Run SQL setup from `database/supabase_setup.sql`
5. Add credentials to `.env` file

### **Step 4: Run the Application**
```bash
# Start the Streamlit application
streamlit run app.py

# Alternative: Run with specific port
streamlit run app.py --server.port 8501

# Alternative: Run in headless mode
streamlit run app.py --server.headless true
```

### **Step 5: Usage Instructions**
1. **Access the app**: Open browser to `http://localhost:8501`
2. **Upload documents**: Use sidebar to upload PDF, DOCX, or TXT files
3. **Start chatting**: Ask questions about your uploaded documents
4. **Explore features**: Try summaries, FAQs, and document comparison
5. **Monitor analytics**: View usage statistics (if Supabase configured)

### **Development Setup** (Optional)
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Check code formatting
black . --check
flake8 .
```

### **Docker Deployment** (Optional)
```bash
# Build Docker image
docker build -t intellidocs .

# Run container
docker run -p 8501:8501 --env-file .env intellidocs
```

### **Troubleshooting**

**Common Issues:**
- **Import errors**: Run `pip install -r requirements.txt` again
- **API key errors**: Verify Gemini API key in `.env` file
- **Memory issues**: Reduce chunk size or restart application
- **Port conflicts**: Change port with `--server.port 8502`

**Performance Optimization:**
- Use SSD storage for faster document processing
- Allocate 4GB+ RAM for embedding models
- Use persistent vector storage for large document sets

### **Production Deployment**

For production deployment, consider:
- Use environment-specific configuration
- Enable Supabase for data persistence
- Configure proper security headers
- Set up monitoring and logging
- Use cloud deployment (Streamlit Cloud, AWS, etc.)

---

**🎉 Ready to start your intelligent document journey!**

For detailed setup guides, check out:
- 📖 [Supabase Setup Guide](SUPABASE_SETUP.md)
- 🏗️ [Architecture Diagram Prompt](ARCHITECTURE_DIAGRAM_PROMPT.md)
- 🔧 [Configuration Details](.env.example)#   I n t e l l i d o c s  
 