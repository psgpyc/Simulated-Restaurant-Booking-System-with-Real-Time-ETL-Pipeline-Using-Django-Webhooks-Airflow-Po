DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE customers(
	customer_id INT PRIMARY KEY,
	customer_name VARCHAR(100) NOT NULL, 
	customer_phone VARCHAR(15) NOT NULL, 
	customer_email VARCHAR(50) NOT NULL,
	joined_at TIMESTAMP )
	
DROP TABLE IF EXISTS reservations;
CREATE TABLE reservations (
	reservation_id INT PRIMARY KEY, 
	customer_id INT REFERENCES customers(customer_id),
	reservation_time TIMESTAMP, 
	experience VARCHAR(255),
	size INT,
	status VARCHAR(20),
	payment_mode VARCHAR(20),
	visit_notes VARCHAR(255),
	created_at TIMESTAMP,
	source VARCHAR(100)
)



