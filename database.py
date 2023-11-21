import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
import os

# from urllib.parse import urlparse


# Function to execute a SELECT query and return all results as a list of dictionaries
def sql_select_all(query):
    db_connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    return result


# Function to execute a SELECT query with parameters and return all results as a list of dictionaries
def sql_select_all_by_col(query, params):
    db_connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    db_cursor.execute(query, params)
    result = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    return result


# Function to execute a SELECT query with parameters and return the first result as a dictionary
def sql_select_one(query, params):
    db_connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    db_cursor.execute(query, params)
    result = db_cursor.fetchone()
    db_cursor.close()
    db_connection.close()
    return result


# Function to execute a write query with parameters
def sql_write(query, params):
    db_connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")
    db_cursor = db_connection.cursor()
    db_cursor.execute(query, params)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


# Function to execute a write query and return the value of the first column of the first row
def sql_write_with_return(query, params):
    db_connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")
    db_cursor = db_connection.cursor()
    db_cursor.execute(query, params)
    db_connection.commit()
    result = db_cursor.fetchone()[0]
    db_cursor.close()
    db_connection.close()
    return result


# Function to execute a DELETE query with parameters
def sql_delete(query, params):
    db_connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")
    db_cursor = db_connection.cursor()
    db_cursor.execute(query, params)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


# Function to execute multiple write queries using execute_values
def sql_multiple_write(query, params):
    db_connection = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    execute_values(db_cursor, query, params)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
