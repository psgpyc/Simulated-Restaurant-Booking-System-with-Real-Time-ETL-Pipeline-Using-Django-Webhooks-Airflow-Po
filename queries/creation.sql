DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE customers(
	customer_id INT PRIMARY KEY,
	customer_name VARCHAR(100) NOT NULL, 
	customer_phone VARCHAR(15) NOT NULL, 
	customer_email VARCHAR(50) NOT NULL,
	joined_date TIMESTAMPTZ)
	
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

--- Updated theb table to fit few new types of phone formats and length
-- ALTER TABLE customers
-- ALTER COLUMN customer_phone TYPE VARCHAR(50);


-- ALTER TABLE customers
-- ALTER COLUMN customer_phone SET NOT NULL;



DROP TABLE IF EXISTS menuitems CASCADE;
CREATE TABLE menuitems (
	menuitems_id INT primary key, 
	name VARCHAR(50) NOT NULL,
	price NUMERIC(10, 2) NOT NULL CHECK(price > 0.00),
	course VARCHAR(50),
	is_available BOOLEAN NOT NULL DEFAULT TRUE
	
)

-- Test insert
-- INSERT INTO menuitems VALUES
-- (1, 'Momo', 6.99, 'Main Course', TRUE),
-- (2, 'Newari Khaja Set', 12.99, 'Main Course', TRUE),
-- (3, 'Daal Bhat', 10.99, 'Main Course', TRUE),
-- (4, 'Jerri', 2.99, 'Dessert', TRUE),
-- (5, 'Papad', 0.99, 'Sides', TRUE),
-- (6, 'Aalu ko Aachar', 2.99, 'Starter', TRUE),
-- (7, 'Gajar ko Haluwa', 3.99, 'Dessert', TRUE),
-- (8, 'Chowmein', 9.99, 'Main Course', TRUE)


DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
	order_id INT PRIMARY KEY, 
	customer_id INT REFERENCES customers(customer_id),
	created_on TIMESTAMPTZ NOT NULL,
	updated_on TIMESTAMPTZ NOT NULL,
	total_price NUMERIC(10, 2) NOT NULL CHECK(total_price > 0.00),
	is_completed BOOLEAN DEFAULT FALSE
)

DROP TABLE IF EXISTS orderitems;
CREATE TABLE orderitems(
	order_id INT REFERENCES orders(order_id),
	customer_id INT REFERENCES customers(customer_id),
	menu_item INT REFERENCES menuitems(menuitems_id),
	quantity INT CHECK(quantity > 0),
	PRIMARY KEY (order_id, customer_id, menu_item)
)
