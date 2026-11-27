-- Создание тестовой базы данных при первой инициализации контейнера PostgreSQL.
-- Скрипты из /docker-entrypoint-initdb.d выполняются только при пустом томе pgdata.
CREATE DATABASE wallet_test;