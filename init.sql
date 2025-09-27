-- Création de la base de données
CREATE DATABASE IF NOT EXISTS geekprofile;

-- Utilisation de la base
USE geekprofile;

-- Création de la table accounts
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    organisation VARCHAR(100),
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    postalcode VARCHAR(20)
);

-- Insertion de données de test (optionnel)
INSERT IGNORE INTO accounts (username, password, email, organisation, address, city, state, country, postalcode) VALUES
('admin', 'admin123', 'admin@example.com', 'Test Org', '123 Test St', 'Paris', 'Île-de-France', 'France', '75001'),
('user1', 'password', 'user1@example.com', 'Company ABC', '456 Main St', 'Lyon', 'Auvergne-Rhône-Alpes', 'France', '69000');