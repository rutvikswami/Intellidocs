-- ======================================================================
-- IntelliDocs Supabase Database Setup (FINAL CORRECTED VERSION)
-- Paste directly into Supabase SQL Editor
-- ======================================================================

-- 1. Create chat_logs table (stores user chat interactions)
CREATE TABLE IF NOT EXISTS chat_logs (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    sources TEXT[] DEFAULT '{}',
    user_id TEXT DEFAULT 'demo_user',
    session_id TEXT DEFAULT 'default_session',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    response_time_ms INTEGER DEFAULT NULL,
    document_count INTEGER DEFAULT 0
);

-- Create chat_sessions table if it doesn't exist (to prevent session_id constraint errors)
CREATE TABLE IF NOT EXISTS chat_sessions (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE DEFAULT 'default_session',
    user_id TEXT DEFAULT 'demo_user',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create document_uploads table (tracks uploaded files)
CREATE TABLE IF NOT EXISTS document_uploads (
    id BIGSERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER DEFAULT NULL,
    chunk_count INTEGER DEFAULT 0,
    upload_status TEXT DEFAULT 'success',
    user_id TEXT DEFAULT 'demo_user',
    processing_time_ms INTEGER DEFAULT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Create usage_analytics table (dashboard metrics)
CREATE TABLE IF NOT EXISTS usage_analytics (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,       -- e.g: 'document_upload', 'chat_query'
    event_data JSONB DEFAULT '{}',
    user_id TEXT DEFAULT 'demo_user',
    session_id TEXT DEFAULT 'default_session',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ======================================================================
-- INDEXES FOR PERFORMANCE
-- ======================================================================
CREATE INDEX IF NOT EXISTS idx_chat_logs_created_at ON chat_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_logs_user_id ON chat_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_document_uploads_user_id ON document_uploads(user_id);
CREATE INDEX IF NOT EXISTS idx_document_uploads_created_at ON document_uploads(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_usage_analytics_event_type ON usage_analytics(event_type);
CREATE INDEX IF NOT EXISTS idx_usage_analytics_created_at ON usage_analytics(created_at DESC);

-- Indexes for chat_sessions table
CREATE INDEX IF NOT EXISTS idx_chat_sessions_session_id ON chat_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at ON chat_sessions(created_at DESC);

-- ======================================================================
-- ROW LEVEL SECURITY (RLS)
-- ======================================================================
ALTER TABLE chat_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;

-- ======================================================================
-- RLS POLICIES (ALLOW ALL — SAFE FOR DEMO)
-- Avoid "IF NOT EXISTS" (PostgreSQL does not support it for policies)
-- Use dynamic SQL instead
-- ======================================================================
DO $$
BEGIN
    -- chat_logs
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE policyname = 'allow_all_chat_logs'
          AND tablename = 'chat_logs'
    ) THEN
        EXECUTE 'CREATE POLICY allow_all_chat_logs ON chat_logs FOR ALL USING (true) WITH CHECK (true)';
    END IF;

    -- document_uploads
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE policyname = 'allow_all_document_uploads'
          AND tablename = 'document_uploads'
    ) THEN
        EXECUTE 'CREATE POLICY allow_all_document_uploads ON document_uploads FOR ALL USING (true) WITH CHECK (true)';
    END IF;

    -- usage_analytics
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE policyname = 'allow_all_usage_analytics'
          AND tablename = 'usage_analytics'
    ) THEN
        EXECUTE 'CREATE POLICY allow_all_usage_analytics ON usage_analytics FOR ALL USING (true) WITH CHECK (true)';
    END IF;

    -- chat_sessions
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE policyname = 'allow_all_chat_sessions'
          AND tablename = 'chat_sessions'
    ) THEN
        EXECUTE 'CREATE POLICY allow_all_chat_sessions ON chat_sessions FOR ALL USING (true) WITH CHECK (true)';
    END IF;
END $$;

-- ======================================================================
-- SAMPLE DATA (OPTIONAL)
-- ======================================================================
INSERT INTO chat_logs (query, response, sources, user_id)
VALUES 
('What is the company vacation policy?',
 'Employees get 15–25 vacation days depending on tenure.',
 ARRAY['employee_handbook.pdf'],
 'demo_user');

INSERT INTO document_uploads (file_name, file_type, chunk_count, user_id)
VALUES
('employee_handbook.pdf', 'pdf', 12, 'demo_user'),
('remote_work_policy.docx', 'docx', 8, 'demo_user');

-- Insert sample chat session
INSERT INTO chat_sessions (session_id, user_id)
VALUES 
('default_session', 'demo_user');

-- ======================================================================
-- ANALYTICS VIEW
-- ======================================================================
CREATE OR REPLACE VIEW analytics_dashboard AS
SELECT 
    DATE(created_at) AS date,
    COUNT(*) AS total_queries,
    COUNT(DISTINCT user_id) AS unique_users,
    AVG(response_time_ms) AS avg_response_time,
    COUNT(DISTINCT sources[1]) AS documents_queried
FROM chat_logs
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
