# Educanta sandbox

## How to config local database

We use a local database for tests and development. You only need to create the local database the first time you're running the code. Then, you'll have the local database configured and ready to develop the product.

To create a local database:

1. Install postgresql in your computer.
   - If Mac, use `brew install postgresql`.
1. Do `pg_ctl -D /usr/local/var/postgres start && brew services start postgresql` to start the database.
1. Do `psql postgres` to enter in the database.
   - If it gives you an error like "database files are incompatible with server", try this: https://gist.github.com/joho/3735740
1. Do `CREATE ROLE postgres WITH LOGIN SUPERUSER;`.
1. Do `CREATE ROLE rdsadmin;`.
1. Do `CREATE DATABASE dev;`.

# Database operations

## Create database
`CREATE TABLE students (id SERIAL PRIMARY KEY, name VARCHAR, email VARCHAR, school VARCHAR, start_date DATE, end_date DATE, signup_at TIMESTAMP);`
`CREATE TABLE companies (id SERIAL PRIMARY KEY, name VARCHAR, signup_at TIMESTAMP);`
`CREATE TABLE projects (id SERIAL PRIMARY KEY, name VARCHAR, company INTEGER REFERENCES companies (id), start_date DATE, end_date DATE, hours_per_week INTEGER, skills VARCHAR, signup_at TIMESTAMP);`

# Access database in psql
`psql -U postgres -d dev`

## Insert data into tables
`insert into students(name,email,school,start_date,end_date) values ('João AAA', 'email@email.com', 'IST', '2022-06-01', '2022-09-30')`