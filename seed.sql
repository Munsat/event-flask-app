TRUNCATE TABLE events CASCADE;
TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE attendances CASCADE;

ALTER SEQUENCE events_id_seq RESTART WITH 1;
ALTER SEQUENCE users_id_seq RESTART WITH 1;
ALTER SEQUENCE attendances_id_seq RESTART WITH 1;


INSERT INTO users (name, email, hashed_password)VALUES
('Sam', 'sam_1@yahoo.com','pbkdf2:sha256:260000$RWT8V70tlFP3Ivfh$4f39c4c374b8582b9cb928f36a80bc2e4a49cd7f35cad873a4c171aac52f3ff0'),
('Maria', 'maria121@yahoo.com','pbkdf2:sha256:260000$UdU3ecBXZ2TrRHbg$6e0e295a4656173740cb0e8a7fac4e8fed43bc628ef347fea612e790dd330b75'),
('Irene', 'ariel1@gmail.com','pbkdf2:sha256:260000$8LHHuiXO61DjIOZf$cbc6543c4b4d3065287e1bdc29bda2dab6313b7669e2c05c9c750a4457c9c2e6');


INSERT INTO events (name, type, description, location, date, start_time, end_time, email_list, user_id) VALUES 
('Samantha & Pete''s Wedding', 'Private','Samantha and Pete are getting married after 6 years of being together. We would love your attendance on this special day', '36 Marshall Road, Blacktown, NSW, 2560', '2023-11-04','20:00','24:00',ARRAY['a@exmaple.com', 'b@example.com'], 1),
('Cherry Harvest Festival', 'Public', 'An epic event that comes only once a year. Come visit us to get your pick of the best cherries. There will be lots of food stalls and music for you!','25 Cherry St, Coogee, NSW, 2656','2023-08-10','09:00','17:00',NULL, 3),
('Antique Auction', 'Public', 'We will be auctioning items to be sold by the official trustee in bankruptcy, jewellery and more!','25 Riverview Rd , Bondi, NSW, 2210','2023-09-16','19:00','00:00',NULL, 2),
('Karla Dickens: Embracing Shadows', 'Public', 'Wiradjuri artist Karla Dickens has assembled a range of her works to form the new exhibition Embracing Shadows, showcasing her 30 year career at the Campbelltown Arts Centre.  This free exhibition shines a spotlight on female identity and racial discrimination, two themes that Dickens'' work engages with in a profound and honest way. She explores and melds mediums to create pieces that are pastiches of what it means to be a woman and a First Nations person in a post-colonial Australia.','12 Marsh Rd , Campbelltown, NSW, 2310','2023-04-11','19:00','00:00',NULL, 3);
