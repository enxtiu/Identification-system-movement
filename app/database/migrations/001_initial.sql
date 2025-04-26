-- migrations/002_add_email.sql
ALTER TABLE employees
ADD COLUMN email VARCHAR(100);

-- Обновление существующих данных (опционально)
UPDATE employees
SET email = CONCAT(LOWER(REPLACE(name, ' ', '_')), '@company.com');