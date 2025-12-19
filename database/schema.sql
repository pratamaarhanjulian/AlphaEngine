-- ============================================
-- AUREA PRIME ELITE - Database Schema
-- SQLite Database
-- ============================================

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    tier VARCHAR(20) DEFAULT 'FREE',
    package VARCHAR(20) DEFAULT NULL,
    mt5_id VARCHAR(50),
    token VARCHAR(8),
    expired_at DATETIME,
    
    -- Trading Settings (SUPER/SUPREME only)
    risk_percent DECIMAL(3,2) DEFAULT 1.0,
    lot_mode VARCHAR(10) DEFAULT 'AUTO',
    fixed_lot DECIMAL(5,2) DEFAULT 0.01,
    rr_mode VARCHAR(10) DEFAULT 'AUTO',
    fixed_rr DECIMAL(3,1) DEFAULT 2.0,
    
    -- News Settings (SUPER/SUPREME only)
    avoid_news BOOLEAN DEFAULT 1,
    trade_on_news BOOLEAN DEFAULT 0,
    
    -- Limits
    daily_signals_used INT DEFAULT 0,
    last_signal_reset DATETIME,
    
    -- Timestamps
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_active DATETIME
);

-- Table: tokens (SUPER & SUPREME only)
CREATE TABLE IF NOT EXISTS tokens (
    token VARCHAR(8) PRIMARY KEY,
    mt5_id VARCHAR(50) UNIQUE,
    user_id BIGINT,
    tier VARCHAR(20),
    expired_at DATETIME,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table: payments
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id BIGINT,
    username VARCHAR(255),
    first_name VARCHAR(255),
    package VARCHAR(50),
    duration VARCHAR(20),
    tier VARCHAR(20),
    amount INTEGER,
    proof_url TEXT,
    status VARCHAR(20) DEFAULT 'PENDING',
    verified_by BIGINT,
    verified_at DATETIME,
    rejection_reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table: signals
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id BIGINT,
    pair VARCHAR(20),
    action VARCHAR(10),
    entry DECIMAL(10,5),
    sl DECIMAL(10,5),
    tp DECIMAL(10,5),
    lot DECIMAL(5,2),
    confidence DECIMAL(5,2),
    reason TEXT,
    predictions TEXT,
    tier VARCHAR(20),
    is_news_trade BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table: executions (SUPER/SUPREME only)
CREATE TABLE IF NOT EXISTS executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id BIGINT,
    mt5_id VARCHAR(50),
    signal_id INTEGER,
    pair VARCHAR(20),
    action VARCHAR(10),
    entry_price DECIMAL(10,5),
    exit_price DECIMAL(10,5),
    lot DECIMAL(5,2),
    profit DECIMAL(10,2),
    result VARCHAR(10),
    tier VARCHAR(20),
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (signal_id) REFERENCES signals(id)
);

-- Table: news_events
CREATE TABLE IF NOT EXISTS news_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name VARCHAR(255),
    country VARCHAR(10),
    event_time DATETIME,
    impact VARCHAR(20),
    forecast VARCHAR(50),
    previous VARCHAR(50),
    actual VARCHAR(50),
    prediction VARCHAR(10),
    sentiment VARCHAR(20),
    notified BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: financial_reports (Admin analytics)
CREATE TABLE IF NOT EXISTS financial_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    total_users INT DEFAULT 0,
    free_users INT DEFAULT 0,
    premium_users INT DEFAULT 0,
    super_users INT DEFAULT 0,
    supreme_users INT DEFAULT 0,
    daily_revenue INTEGER DEFAULT 0,
    monthly_revenue INTEGER DEFAULT 0,
    total_signals INT DEFAULT 0,
    total_executions INT DEFAULT 0,
    avg_win_rate DECIMAL(5,2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: system_logs (Maintenance & errors)
CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type VARCHAR(20),
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_tier ON users(tier);
CREATE INDEX IF NOT EXISTS idx_users_token ON users(token);
CREATE INDEX IF NOT EXISTS idx_tokens_mt5_id ON tokens(mt5_id);
CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_signals_user_id ON signals(user_id);
CREATE INDEX IF NOT EXISTS idx_executions_user_id ON executions(user_id);
CREATE INDEX IF NOT EXISTS idx_news_events_time ON news_events(event_time);