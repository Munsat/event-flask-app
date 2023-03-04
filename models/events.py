from database import sql_select_all

class Event:
    def __init__(self,id, name, type,description, location, date ) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.location = location
        self.date = date


def get_all_events():
    events =  sql_select_all("SELECT id, name, type, description, location, date FROM events WHERE date>NOW() AND type = 'Public' ")
    all_events = []
    for event in events:
        all_events.append(Event(id=event['id'],
           name=event['name'],
           type=event['type'],
           description=event['description'],
           location=event['location'],
           date=event['date']))
    return all_events

    
    
