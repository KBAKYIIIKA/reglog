-- Запрос для создания таблицы внутри схемы
CREATE SCHEMA service;
CREATE TABLE service.users (
	id SERIAL PRIMARY KEY,
	full_name VARCHAR(50) NOT NULL,
	login VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL
)