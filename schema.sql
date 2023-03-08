DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS attendances CASCADE;



CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(255),
    hashed_password TEXT
);


CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    type VARCHAR(15),
    description TEXT,
    location TEXT,
    date DATE,
    start_time TIME,
    end_time TIME,
    email_list TEXT ARRAY,
    user_id INT,
    CONSTRAINT fk_events_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);


CREATE TABLE attendances (
    id SERIAL PRIMARY KEY,
    user_id INT,
    CONSTRAINT fk_attendance_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,
    event_id INT,
    CONSTRAINT fk_attendance_events
    FOREIGN KEY (event_id)
    REFERENCES events(id)
    ON DELETE CASCADE
);
