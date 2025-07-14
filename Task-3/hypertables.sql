-- Main table
CREATE TABLE IF NOT EXISTS raw_data (
    user_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    value DOUBLE PRECISION,
    PRIMARY KEY (user_id, metric, timestamp)
);

-- Convert to hypertable
SELECT create_hypertable('raw_data', 'timestamp', if_not_exists => TRUE);

-- Aggregated hypertables

-- 1-minute
CREATE TABLE IF NOT EXISTS data_1m (
    user_id TEXT,
    metric TEXT,
    timestamp TIMESTAMPTZ,
    avg_value DOUBLE PRECISION,
    PRIMARY KEY (user_id, metric, timestamp)
);
SELECT create_hypertable('data_1m', 'timestamp', if_not_exists => TRUE);

-- 1-hour
CREATE TABLE IF NOT EXISTS data_1h (
    user_id TEXT,
    metric TEXT,
    timestamp TIMESTAMPTZ,
    avg_value DOUBLE PRECISION,
    PRIMARY KEY (user_id, metric, timestamp)
);
SELECT create_hypertable('data_1h', 'timestamp', if_not_exists => TRUE);

-- 1-day
CREATE TABLE IF NOT EXISTS data_1d (
    user_id TEXT,
    metric TEXT,
    timestamp TIMESTAMPTZ,
    avg_value DOUBLE PRECISION,
    PRIMARY KEY (user_id, metric, timestamp)
);
SELECT create_hypertable('data_1d', 'timestamp', if_not_exists => TRUE);