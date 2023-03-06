import psycopg2
from psycopg2.extras import RealDictCursor

def sql_select_all(query):
    db_connection = psycopg2.connect('dbname=event_planner')
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    return result

def sql_select_all_by_id(query, params):
    db_connection = psycopg2.connect('dbname=event_planner')
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    db_cursor.execute(query, params)
    result = db_cursor.fetchall()
    db_cursor.close()
    db_connection.close()
    return result


def sql_select_one(query, params):
    db_connection = psycopg2.connect('dbname=event_planner')
    db_cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    db_cursor.execute(query, params)
    result = db_cursor.fetchone()
    db_cursor.close()
    db_connection.close()
    return result


def sql_write(query, params):
    db_connection = psycopg2.connect('dbname=event_planner')
    db_cursor = db_connection.cursor()
    db_cursor.execute(query, params)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


def sql_delete(query, params):
    db_connection = psycopg2.connect('dbname=event_planner')
    db_cursor = db_connection.cursor()
    db_cursor.execute(query, params)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()