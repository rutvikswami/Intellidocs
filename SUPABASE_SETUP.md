# 🗄️ Supabase Setup Guide for IntelliDocs

## 📋 Quick Setup Steps

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Choose organization and name: `intellidocs`
4. Choose region closest to you
5. Generate strong password
6. Wait 2-3 minutes for setup

### 2. Run Database Setup
1. Go to **SQL Editor** in Supabase dashboard
2. Copy the entire contents of `database/supabase_setup.sql`
3. Paste into SQL Editor
4. Click **Run** to create all tables

### 3. Get API Credentials
1. Go to **Settings** → **API**
2. Copy these values:
   - **Project URL**: `https://your-project.supabase.co`
   - **Anon public key**: `eyJ0...` (long key)

### 4. Update Environment Variables
Add to your `.env` file:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
GEMINI_API_KEY=your_gemini_key_here
```

---

## 📊 What Supabase Will Track

### 🗨️ Chat Logs Table
**Stores every user interaction:**
- User questions and AI responses
- Source documents used
- Response times
- User IDs and timestamps

### 📄 Document Uploads Table  
**Tracks all uploaded documents:**
- File names and types
- Processing times
- Chunk counts
- Upload status

### 📈 Usage Analytics Table
**Records user behavior:**
- Feature usage (chat, summaries, comparisons)
- User sessions
- Performance metrics
- Error tracking

---

## 🔧 Tables Created

```sql
chat_logs           # User Q&A interactions
document_uploads    # File upload tracking  
usage_analytics     # Feature usage stats
analytics_dashboard # Summary view (virtual)
```

### Sample Data Structure

**chat_logs:**
| id | query | response | sources | user_id | timestamp |
|----|-------|----------|---------|---------|-----------|
| 1 | "What's the vacation policy?" | "15-25 days based on tenure" | ["handbook.pdf"] | demo_user | 2024-01-15 |

**document_uploads:**
| id | file_name | file_type | chunk_count | user_id | created_at |
|----|-----------|-----------|-------------|---------|------------|
| 1 | "policy.pdf" | "pdf" | 12 | demo_user | 2024-01-15 |

---

## ✨ Features Enabled

### 1. **Analytics Dashboard** (Future Enhancement)
- Daily usage metrics
- Popular questions
- Document engagement
- User activity patterns

### 2. **Chat History**
- Persistent conversations
- Previous Q&A sessions
- User-specific history

### 3. **Performance Monitoring**
- Response times
- Error tracking
- System health metrics

### 4. **Usage Insights**
- Most queried documents
- Popular features
- User engagement trends

---

## 🔒 Security Setup

### Row Level Security (RLS)
- **Enabled** on all tables
- **Demo policy**: Allow all operations
- **Production**: Restrict by user authentication

### Privacy Controls
- User data isolation
- Configurable data retention
- GDPR compliance ready

---

## 🧪 Testing Your Setup

### 1. Verify Connection
Run the app and check for:
- ✅ No Supabase error messages
- ✅ Chat interactions logged
- ✅ Document uploads tracked

### 2. Check Database
In Supabase dashboard:
1. Go to **Table Editor**
2. Click on `chat_logs`
3. Should see entries after using the app

### 3. View Analytics
```sql
-- Run in SQL Editor to see logged data
SELECT * FROM chat_logs ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM document_uploads ORDER BY created_at DESC;
```

---

## ⚡ Optional: Enhanced Features

### Install Supabase Package
```bash
pip install supabase
```

### Enable Advanced Logging
Uncomment logging code in:
- `services/rag_service.py`
- `components/sidebar.py` 
- `components/chat_tab.py`

---

## 🚀 Production Deployment

### Environment Variables for Streamlit Cloud
In Streamlit Cloud secrets:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_anon_key_here"
GEMINI_API_KEY = "your_gemini_key"
```

### Monitoring Setup
- Database backups enabled
- Performance insights active
- Error tracking configured

---

## ❓ Troubleshooting

### Common Issues

**"Supabase not installed" warning**
- Run: `pip install supabase`

**Connection failed**
- Check URL and key in `.env`
- Verify project is not paused

**Permission denied**
- Check RLS policies are created
- Verify API key has correct permissions

**No data showing**
- Check table names match exactly
- Verify SQL setup ran successfully

---

**🎉 Once setup, your IntelliDocs will have enterprise-grade logging and analytics!**

**Need help?** Check the Supabase documentation or contact support.

---

## 📈 Next Steps After Setup

1. **Test logging** - Upload docs and chat to see data
2. **Build dashboard** - Create analytics views  
3. **Add authentication** - User management system
4. **Scale up** - Production deployment configuration