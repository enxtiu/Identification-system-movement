-- Создание таблицы сотрудников
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    embedding FLOAT[]  -- Вектор признаков лица
);

-- Создание таблицы обнаружений
CREATE TABLE IF NOT EXISTS detections (
    timestamp TIMESTAMP NOT NULL,
    employee_id INTEGER REFERENCES employees(id),
    camera_id VARCHAR(20) NOT NULL,
    photo_path VARCHAR(255)
);

-- Создание индекса для ускорения поиска по времени
CREATE INDEX idx_detections_timestamp ON detections(timestamp);

-- Создание пользователя для приложения
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT ON employees, detections TO app_user;