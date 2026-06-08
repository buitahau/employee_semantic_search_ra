-- Create the vector DB (runs while connected to owt_employee, the POSTGRES_DB default)
CREATE DATABASE owt_vector;

-- Switch to owt_vector and install the pgvector extension
\c owt_vector
CREATE EXTENSION IF NOT EXISTS vector;

-- Switch back to owt_employee and install the pgvector extension
\c owt_employee
CREATE EXTENSION IF NOT EXISTS vector;
