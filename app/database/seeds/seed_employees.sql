INSERT INTO employees (id, name, position) VALUES
(101, 'Иванов Алексей Петрович', 'Инженер'),
(102, 'Смирнова Мария Сергеевна', 'Менеджер');

INSERT INTO detections (timestamp, employee_id, camera_id) VALUES
('2024-05-20 14:00:00', 101, 'cam_1'),
('2024-05-20 14:15:00', 101, 'cam_5');