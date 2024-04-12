CREATE TABLE users(
  user_id SERIAL PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE trainer(
  trainer_id SERIAL PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  start_time TIME,
  end_time TIME
);

CREATE TABLE goals(
  user_id INT NOT NULL,
  goal_weight INT,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE userMetrics(
  user_id INT NOT NULL,
  height INT,
  weight INT,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE rooms(
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    is_private BOOLEAN NOT NULL
);

CREATE TABLE class(
  class_id SERIAL PRIMARY KEY,
  class_name VARCHAR(255) NOT NULL,
  trainer_id INT NOT NULL,
  room_id INT,
  date DATE NOT NULL,
  time TIME NOT NULL,
  is_private BOOLEAN NOT NULL DEFAULT FALSE,
  has_room_booking BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id),
  FOREIGN KEY (room_id) REFERENCES rooms(room_id)  
);

CREATE TABLE classRegistration(
  registration_id SERIAL PRIMARY KEY,
  user_id INT,
  class_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE adminStaff(
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE roomBooking(
    room_booking_id SERIAL PRIMARY KEY,
    room_id INT,
    class_id INT,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),   
    FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE equipment(
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255) NOT NULL,
    maintenance_date DATE NOT NULL
);

CREATE TABLE payment(
    payment_id SERIAL PRIMARY KEY,
    user_id INT,
    registration_id INT,
    amount DECIMAL(10, 2),
    is_payed BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (registration_id) REFERENCES classRegistration(registration_id)
);
