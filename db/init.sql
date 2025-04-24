CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    channel_name TEXT NOT NULL,
    message_id INTEGER NOT NULL,
    text TEXT,
    views INTEGER,
    timestamp TIMESTAMP NOT NULL,
    tags TEXT[],
    source TEXT,
    UNIQUE(channel_name, message_id)
);

-- Индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_timestamp ON events (timestamp);
CREATE INDEX IF NOT EXISTS idx_channel_name ON events (channel_name);
