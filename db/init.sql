CREATE USER admin WITH SUPERUSER PASSWORD 'admin';

CREATE DATABASE IF NOT EXISTS prod;

CREATE TABLE IF NOT EXISTS users (
    user_id INT GENERATED ALWAYS AS IDENTITY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
    balance INT DEFAULT 0,
	created_on TIMESTAMP NOT NULL,
    PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS items (
    item_id INT GENERATED ALWAYS AS IDENTITY,
    user_id INT NOT NULL,
    about VARCHAR ( 50 ) NOT NULL,
    pic VARCHAR ( 50 ) NOT NULL DEFAULT '0.png',
    price INT NOT NULL,
    is_in_stock BOOLEAN NOT NULL,
    created_on TIMESTAMP NOT NULL,
    PRIMARY KEY(item_id),
    CONSTRAINT user_id
      FOREIGN KEY(user_id)
	  REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT GENERATED ALWAYS AS IDENTITY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
	price INT NOT NULL,
	created_on TIMESTAMP NOT NULL,
	is_ret BOOLEAN NOT NULL,
	returned_on TIMESTAMP,
	PRIMARY KEY(order_id),
	CONSTRAINT user_id
      FOREIGN KEY(user_id)
	  REFERENCES users(user_id),
	CONSTRAINT item_id
      FOREIGN KEY(item_id)
	  REFERENCES items(item_id)
);

INSERT INTO users(username, password, email, balance, created_on) VALUES('dana', '123455', 'dana@gm.com', 10000, CURRENT_TIMESTAMP);
INSERT INTO users(username, password, email, balance, created_on) VALUES('john', 'qwerty', 'john@gm.com', 600, CURRENT_TIMESTAMP);
INSERT INTO users(username, password, email, balance, created_on) VALUES('kara', 'kara', 'kara@gm.com', 0, CURRENT_TIMESTAMP);

INSERT INTO items(user_id, price, about, pic, is_in_stock, created_on) VALUES(1, 100, 'Earrings', '1.png', TRUE, CURRENT_TIMESTAMP);
INSERT INTO items(user_id, price, about, pic, is_in_stock, created_on) VALUES(1, 1000, 'Dress', '2.png', TRUE, CURRENT_TIMESTAMP);
INSERT INTO items(user_id, price, about, pic, is_in_stock, created_on) VALUES(1, 50, 'Lipstick', '3.png', FALSE, CURRENT_TIMESTAMP);
INSERT INTO items(user_id, price, about, pic, is_in_stock, created_on) VALUES(2, 500, 'Bag', '4.png', TRUE, CURRENT_TIMESTAMP);
INSERT INTO items(user_id, price, about, pic, is_in_stock, created_on) VALUES(2, 100, 'Hat', '5.png', FALSE, CURRENT_TIMESTAMP);
INSERT INTO items(user_id, price, about, is_in_stock, created_on) VALUES(3, 700, 'iPhone 13', TRUE, CURRENT_TIMESTAMP);

INSERT INTO orders(user_id, item_id, price, created_on, is_ret) VALUES (2, 3, 50, CURRENT_TIMESTAMP, FALSE);
INSERT INTO orders(user_id, item_id, price, created_on, is_ret) VALUES (1, 5, 100, CURRENT_TIMESTAMP, FALSE);



