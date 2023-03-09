from database import sql_select_all, sql_select_all_by_col,sql_select_one, sql_delete, sql_write_with_return
from datetime import datetime
import smtplib
import os


my_email = os.environ.get('MY_EMAIL')
my_pass = os.environ.get('MY_PASS')


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

    def send_email(self, user_name):
        parsed_date = self.date.strftime("%d %B, %Y")

        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=my_email, password=my_pass)
        for email in self.email_list:
             connection.sendmail(from_addr=my_email,
                                to_addrs=email, 
                                msg=f"Subject: Invitation to {self.name}\n\nHi,\n\nYou are cordially invited to attend {self.name}, that we have planned for {parsed_date}. It will be wonderful to have you among us!\nLocation: {self.location}.\nDate and Time: {self.date}, from {self.start_time} to {self.end_time} \n\nKind Regards,\n{user_name}")
        connection.close()    


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
    events =  sql_select_all_by_col("SELECT id, name, type, description, location, date, start_time, end_time, email_list, user_id FROM events WHERE user_id =%s ORDER BY date ASC",[user_id])
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

    
# def insert_public_event(name, type, description, location, date, start_time, end_time, user_id):
#     return sql_write("INSERT INTO events (name, type, description, location, date, start_time, end_time, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [name, type, description,location, date, start_time, end_time, user_id])

def insert_event(name, type, description, location, date, start_time, end_time,email_list, user_id):
    id =  sql_write_with_return("INSERT INTO events (name, type, description, location, date, start_time, end_time,email_list, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", [name, type, description,location, date, start_time, end_time, email_list, user_id])
    return id

def update_event(name, type, description, location, date, start_time, end_time, email_list, user_id, id):
    id = sql_write_with_return('UPDATE events SET name=%s, type=%s, description=%s, location=%s, date=%s, start_time=%s, end_time=%s, email_list=%s, user_id=%s WHERE id=%s RETURNING id',[name, type, description, location, date, start_time, end_time, email_list, user_id, id])
    return id

def get_event_by_id(id):
    event = sql_select_one("SELECT id, name, type, description, location, date, start_time, end_time,email_list, user_id FROM events WHERE id=%s",[id])
    return Event(id=event['id'],
           name=event['name'],
           type=event['type'],
           description=event['description'],
           location=event['location'],
           date=event['date'],
           start_time= (event['start_time']).strftime("%I:%M %p"),
           end_time = (event['end_time']).strftime("%I:%M %p"),
           email_list = event['email_list'],
           user_id = event['user_id'])


def delete_event_by_id(id):
    return sql_delete('DELETE FROM events WHERE id=%s',[id])



