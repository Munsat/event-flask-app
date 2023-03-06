from database import sql_write, sql_select_all_by_id, sql_delete

class Attendance:
    def __init__(self,id, user_id, event_id) -> None:
        self.id = id
        self.user_id = user_id
        self.event_id = event_id

def insert_event_attendance(user_id, event_id):
    return sql_write('INSERT INTO attendances (user_id, event_id) SELECT %s,%s WHERE NOT EXISTS (SELECT * FROM attendances WHERE user_id = %s AND event_id = %s )',[user_id, event_id,user_id, event_id])

def get_all_attendance_by_userid(user_id):
    attendances = sql_select_all_by_id('SELECT attendances.id, attendances.user_id, attendances.event_id FROM attendances JOIN users ON users.id = attendances.user_id JOIN events ON events.id = attendances.event_id WHERE users.id = %s',[user_id])
    all_attendances = []
    for attendance in attendances:
        all_attendances.append(Attendance(attendance['id'], 
                                          attendance['user_id'], 
                                          attendance['event_id']))
    return all_attendances    

def delete_attendance_by_eventid(event_id):
    return sql_delete('DELETE FROM attendances WHERE event_id = %s', [event_id])