INSERT INTO trainer (first_name, last_name, email, password, start_time, end_time) VALUES
('Jane', 'Smith', 'jane.smith@example.com', 'pass123', '12:00:00', '19:00:00'), ('Bob', 'Brown', 'bobbrown@example.com', 'bobby123', '8:00:00', '14:00:00'),
  ('Joey', 'Jones', 'itzjoey@example.com', 'jonesj321', '16:00:00', '22:00:00');

INSERT INTO rooms (room_name, is_private)
VALUES ('Public 200', False), ('Public 201', False), ('Public 202', False), ('Public 203', False), ('Private 100', True), ('Private 101', True), ('Private 102', True);

INSERT INTO adminStaff (first_name, last_name, email, password)
VALUES ('Ray', 'Fan', 'RayF@example.com', '1'),
       ('Dulika', 'Gamage', 'DulikaG@example.com', '2'),
       ('Hai', 'Bai', 'HaiB@example.com', '3');

INSERT INTO equipment (equipment_name, maintenance_date) VALUES 
('Treadmills', '2024-01-01'), ('Eliptical', '2024-02-05'), ('Squat Rack', '2023-10-13'), ('Dumbbell', '2023-10-5'), ('Bench Press', '2023=12-23');

