from database import sql_select_all,sql_write

class Event:
    def __init__(self,id, name, type,description, location, date ) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.location = location
        self.date = date


def get_all_events():
    events =  sql_select_all("SELECT id, name, type, description, location, date FROM events WHERE date>NOW() AND type = 'Public' ORDER BY date ASC")
    all_events = []
    for event in events:
        all_events.append(Event(id=event['id'],
           name=event['name'],
           type=event['type'],
           description=event['description'],
           location=event['location'],
           date=event['date']))
    return all_events

    
def insert_event(name, type, description, location, date, start_time, end_time, user_id):
    return sql_write("INSERT INTO events (name, type, description, location, date, start_time, end_time, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [name, type, description,location, date, start_time, end_time, user_id])
