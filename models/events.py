from database import sql_select_all,sql_write, sql_select_all_by_col
from datetime import datetime

class Event:
    def __init__(self,id, name, type,description, location, date, start_time, end_time, email_list, user_id ) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.location = location
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.email_list = email_list
        self.user_id = user_id


def get_all_events(user_email, user_id):
    events =  sql_select_all_by_col("SELECT id, name, type, description, location, date, start_time, end_time, email_list, user_id FROM events WHERE date>NOW() AND (type = 'Public' OR %s = ANY(email_list) OR user_id =%s) ORDER BY date ASC",[user_email, user_id])
    all_events = []
    for event in events:
        all_events.append(Event(id=event['id'],
           name=event['name'],
           type=event['type'],
           description=event['description'],
           location=event['location'],
           date=event['date'],
           start_time= (event['start_time']).strftime("%I:%M %p"),
           end_time = (event['end_time']).strftime("%I:%M %p"),
           email_list = event['email_list'],
           user_id = event['user_id']))    
    return all_events

def get_all_my_events(user_id):
    events =  sql_select_all_by_col("SELECT id, name, type, description, location, date, start_time, end_time, email_list, user_id FROM events WHERE date>NOW() AND user_id =%s ORDER BY date ASC",[user_id])
    all_events = []
    for event in events:
        all_events.append(Event(id=event['id'],
           name=event['name'],
           type=event['type'],
           description=event['description'],
           location=event['location'],
           date=event['date'],
           start_time= (event['start_time']).strftime("%I:%M %p"),
           end_time = (event['end_time']).strftime("%I:%M %p"),
           email_list = event['email_list'],
           user_id = event['user_id']))
    return all_events

    
def insert_public_event(name, type, description, location, date, start_time, end_time, user_id):
    return sql_write("INSERT INTO events (name, type, description, location, date, start_time, end_time, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [name, type, description,location, date, start_time, end_time, user_id])

def insert_private_event(name, type, description, location, date, start_time, end_time,email_list, user_id):
    return sql_write("INSERT INTO events (name, type, description, location, date, start_time, end_time,email_list, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", [name, type, description,location, date, start_time, end_time,email_list, user_id])


