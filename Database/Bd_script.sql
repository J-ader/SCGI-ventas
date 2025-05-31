CREATE DATABASE IF NOT EXISTS gestion_med;
 
 
USE gestion_med;
 
 -- tabla de usuarios --
CREATE TABLE IF NOT EXISTS usuarios (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(255) UNIQUE NOT NULL,
    fecha_nacimiento DATE,
    password VARCHAR(255) NOT NULL
 
);

-- sistema de roles --
ALTER TABLE usuarios ADD rol ENUM('admin', 'cliente') DEFAULT 'cliente';


-- agrgando administrador de forma manual en la BD--
UPDATE usuarios SET rol = 'admin' WHERE email = 'admin_admin@gmail.com';





-- tabla productos---
CREATE TABLE IF NOT EXISTS productos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

USE gestion_med;


select * from usuarios;

