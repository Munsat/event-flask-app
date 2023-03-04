DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS events;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(255)
);

INSERT INTO users (name, email)VALUES
('Sam', 'sam_1@yahoo.com'),
('Maria', 'maria121@yahoo.com'),
('Irene', 'ariel1@gmail.com');


CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    type VARCHAR(15),
    location TEXT,
    date DATE,
    user_id INT,
    CONSTRAINT fk_events_users
    FOREIGN KEY (user_id)
    REFERENCES users(id)
);

INSERT INTO events (name,type,location,date,user_id) VALUES 
('Sam & Pete''s Wedding', 'Private', '36 Marshall Road, NSW, 2560', '2023-11-04', 1),
('Maria''s Sweet 16', 'Private', '51 O''Connell St, Gladstone, Queensland, 4680', '2023-09-12', 2);