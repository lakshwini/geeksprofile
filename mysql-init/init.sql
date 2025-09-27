CREATE DATABASE IF NOT EXISTS geekprofile;
USE geekprofile;

CREATE TABLE IF NOT EXISTS accounts (
    id int(11) NOT NULL AUTO_INCREMENT,
    username varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    organisation varchar(100) NOT NULL,
    address varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    state varchar(100) DEFAULT NULL,
    country varchar(100) NOT NULL,
    postalcode varchar(10) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO accounts (username, password, email, organisation, address, city, country, postalcode) VALUES
('testuser', 'testpass', 'test@example.com', 'Test Org', '123 Test St', 'Test City', 'Test Country', '12345');