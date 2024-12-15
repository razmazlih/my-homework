CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    upload_time TIMESTAMP,
    status VARCHAR(50) DEFAULT 'uploaded'
);

CREATE TABLE processed_data (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL,
    column1 TEXT NOT NULL,
    column2 VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);