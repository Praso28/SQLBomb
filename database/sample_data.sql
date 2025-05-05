-- Insert bomb data
INSERT INTO bombs (location, voltage_readings, last_maintained, signal_strength, battery_level, frequency_pattern, device_signature)
VALUES
    ('Warehouse', '210,215,208', '2025-03-01 09:00', 85, 72, '1.2,1.3,1.2', 'A7X92'),
    ('Airport', '220,219,221', '2025-03-08 11:00', 98, 95, '3.7,3.7,3.7', 'B9Z31'),
    ('Train Station', '218,217,215', '2025-03-02 14:00', 82, 68, '2.1,2.0,2.2', 'C3Y45'),
    ('Shopping Mall', '212,214,213', '2025-03-05 16:30', 88, 75, '1.8,1.9,1.8', 'A7X29'),
    ('City Hall', '216,215,217', '2025-03-03 13:15', 90, 82, '2.5,2.4,2.5', 'D5F18'),
    ('Bus Terminal', '217,218,216', '2025-03-04 10:45', 92, 88, '3.2,3.1,3.2', 'B9Z35'),
    ('Stadium', '219,220,218', '2025-03-07 15:20', 95, 90, '3.5,3.6,3.5', 'B9Z38'),
    ('Hospital', '211,213,212', '2025-03-06 08:30', 80, 65, '1.5,1.6,1.5', 'E2K77');

-- Insert suspect data
INSERT INTO suspects (name, access_level, last_login)
VALUES
    ('John Doe', 3, '2025-03-07 08:00'),
    ('Sarah Connor', 5, '2025-03-08 10:30'),
    ('Mike Johnson', 4, '2025-03-08 09:45'),
    ('Emily Chen', 4, '2025-03-07 14:20'),
    ('David Miller', 5, '2025-03-08 08:15'),
    ('Lisa Wong', 3, '2025-03-06 16:45');

-- Insert bomb components
INSERT INTO bomb_components (bomb_id, component_name, material, activation_code)
VALUES
    (1, 'Timer', 'Plastic', '123'),
    (1, 'Wiring', 'Copper', '456'),
    (1, 'Detonator', 'Aluminum', '789'),
    (2, 'Timer', 'Metal', '512'),
    (2, 'Wiring', 'Silver', '789'),
    (2, 'Detonator', 'Titanium', '221'),
    (2, 'Circuit', 'Gold', '221'),
    (3, 'Timer', 'Plastic', '321'),
    (3, 'Wiring', 'Aluminum', '654'),
    (3, 'Detonator', 'Steel', '987'),
    (4, 'Timer', 'Plastic', '111'),
    (4, 'Wiring', 'Copper', '222'),
    (4, 'Detonator', 'Iron', '333'),
    (5, 'Timer', 'Plastic', '222'),
    (5, 'Wiring', 'Copper', '333'),
    (5, 'Detonator', 'Steel', '444'),
    (6, 'Timer', 'Metal', '555'),
    (6, 'Wiring', 'Silver', '666'),
    (6, 'Detonator', 'Titanium', '221'),
    (7, 'Timer', 'Metal', '777'),
    (7, 'Wiring', 'Silver', '888'),
    (7, 'Detonator', 'Titanium', '999'),
    (7, 'Circuit', 'Gold', '221'),
    (8, 'Timer', 'Plastic', '135'),
    (8, 'Wiring', 'Copper', '246'),
    (8, 'Detonator', 'Aluminum', '357');

-- Insert access logs
INSERT INTO access_logs (suspect_id, bomb_id, access_time, action_performed)
VALUES
    (1, 1, '2025-03-06 14:30', 'Maintenance'),
    (2, 2, '2025-03-08 09:45', 'Installation'),
    (3, 3, '2025-03-07 11:20', 'Inspection'),
    (2, 4, '2025-03-07 16:15', 'Maintenance'),
    (1, 5, '2025-03-05 10:00', 'Inspection'),
    (3, 6, '2025-03-04 13:45', 'Maintenance'),
    (1, 7, '2025-03-07 09:30', 'Inspection'),
    (2, 7, '2025-03-07 14:15', 'Maintenance'),
    (2, 8, '2025-03-06 11:20', 'Inspection'),
    (3, 2, '2025-03-08 08:30', 'Testing'),
    (1, 2, '2025-03-07 15:45', 'Inspection'),
    (2, 5, '2025-03-03 16:00', 'Testing'),
    (3, 1, '2025-03-01 10:30', 'Installation'),
    (1, 3, '2025-03-02 13:15', 'Testing'),
    (2, 6, '2025-03-04 15:30', 'Installation');
