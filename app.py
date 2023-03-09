from flask import Flask, render_template, request,redirect, session, flash
from models.events import get_all_events, delete_event_by_id, insert_event, get_all_my_events, get_event_by_id, update_event
from models.users import insert_user, select_user_by_email, get_all_user_emails, delete_user
from models.attendances import insert_event_attendance, get_all_attendance_by_userid, delete_attendance_by_eventid
from werkzeug.security import generate_password_hash
import requests
from geopy.geocoders import Nominatim
import random
import os
from weather_code import get_weather_info
from datetime import datetime, date



# #  Import
# from cloudinary import CloudinaryImage
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url

# # Config
# cloudinary.config(
#   cloud_name = "dfqp346je",
#   api_key = "657155384573282",
#   api_secret = "o6anqoQUN2M_cVJ7_q5Ulunuws4",
#   secure = True
# )

# # Upload
# upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", public_id="olympic_flag")

# # Transform
# url, options = cloudinary_url("olympic_flag", width=100, height=150, crop="fill")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')



@app.route('/')
def index():
    all_events=get_all_events(session.get('email'), session.get('id'))
    return render_template('index.html', 
                           all_events= random.sample(all_events, 3),
                           user_name =session.get('name', 'UNKNOWN'))



@app.route('/upcoming_events')
def upcoming_events():
    all_events = get_all_events(session.get('email'), session.get('id'))
    if session.get('name', 'UNKNOWN') != 'UNKNOWN':
        all_attendances = get_all_attendance_by_userid(session.get('id'))
        return render_template('upcoming_events.html',  
                           all_events=all_events,
                           user_name =session.get('name', 'UNKNOWN'),
                           all_attendances = all_attendances,
                           user_id = session.get('id'))
    return render_template('upcoming_events.html',  
                           all_events=all_events,
                           user_name =session.get('name', 'UNKNOWN'),
                           user_id = session.get('id'))



@app.route ('/attending_events')
def attending_events():
    all_events = get_all_events(session.get('email'), session.get('id'))
    if session.get('name', 'UNKNOWN') != 'UNKNOWN':
        all_attendances = get_all_attendance_by_userid(session.get('id'))
    return render_template('upcoming_events.html',
                           show_attendance = True,
                           all_events=all_events,
                           user_name =session.get('name', 'UNKNOWN'),
                           all_attendances=all_attendances,
                           user_id = session.get('id')
                          )



@app.route('/attend_event_action')
def attend_event_action():
    event_id = request.args.get('id')
    user_id = session.get('id')
    insert_event_attendance(user_id, event_id)
    return redirect('/upcoming_events')



@app.route('/cancel_attendance')
def cancel_attendance():
    event_id = request.args.get('id')
    delete_attendance_by_eventid(event_id)
    return redirect('/upcoming_events')
    


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    is_duplicate = False
    if request.method == 'POST':
        name = request.form.get('name').strip().capitalize()
        email = request.form.get('email').lower().strip()
        if request.form.get('password1') == request.form.get('password2'):
            hashed_password = generate_password_hash(request.form.get('password1')) 
            all_emails = get_all_user_emails()
            for each_email in all_emails:
                if email == each_email['email']:
                    is_duplicate =True
            if not is_duplicate:
                user_id = insert_user(name, email, hashed_password)
                session['email'] = email
                session['id'] = user_id
                session['name'] = name
                flash('You were successfully logged in')
                return redirect('/')
            else:
                flash('Sorry, this email is already registered with us. Try logging in.')
                return redirect('/login')   
        else:
            flash('Sorry your passwords do not match. Please try again.')
            return redirect('/signup') 
    return render_template('signup.html', 
                           user_name =session.get('name', 'UNKNOWN'))




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        user = select_user_by_email(email)
        if ((user.validate_password(password) and user.email == email) if user != None else None):
            session['email'] = user.email
            session['id'] = user.id
            session['name'] = user.name
            flash('You have successfully logged in.')
            return redirect('/')
        else:
            flash('Your email or password was incorrect. Please try again.')
            return redirect('/login')
        
    return render_template ('login.html', 
                            user_name =session.get('name', 'UNKNOWN'))



@app.route('/logout')
def logout():
    session.pop('name')
    session.pop('email')
    session.pop('id')
    flash('You have successfully logged out.')
    return redirect('/')


@app.route('/delete_acc')
def delete_acc():
    id = session.get('id')
    delete_user(id)
    session.pop('name')
    session.pop('email')
    session.pop('id')
    return redirect('/')



@app.route('/add_or_edit_event', methods=['GET', 'POST'])
def add_or_edit_event():
    id = request.args.get('id')
    if request.method == 'POST':
        event_name = request.form.get('name')
        type = request.form.get('type')
        description = request.form.get('description')
        location = request.form.get('location').capitalize()
        date = request.form.get('date')
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        user_id = session.get('id')
        type = request.form.get('type')
        email_list = request.form.get('emails').lower().split(',')
        parsed_email_list = [email.strip() for email in email_list]

        if id == None:
            id = insert_event(event_name, type, description, location,date,start_time,end_time,parsed_email_list,user_id )
            flash(f'A new {type.lower()} event has been created.')
        else:
            id = update_event(event_name, type, description, location,date,start_time,end_time,parsed_email_list,user_id,id )
            flash(f'{event_name} event has been updated.')
        if email_list != ['']:    
            event = get_event_by_id(id)
            event.send_email(session.get('name'))
            flash('Emails have been sent to the invitees.')
        return redirect ('/')


    else:
        if id == None:
            return render_template('create_event.html', event =[])
        else:
            event = get_event_by_id(id)
            start_time = datetime.strptime(event.start_time, '%I:%M %p').strftime('%H:%M') 
            end_time = datetime.strptime(event.end_time, '%I:%M %p').strftime('%H:%M')
            return render_template('create_event.html', event=event, start_time=start_time, end_time=end_time)



@app.route('/my_events')
def my_events():
    if session.get('name', 'UNKNOWN') != 'UNKNOWN':
        all_events = get_all_my_events(session.get('id',))
        return render_template('my_events.html',  
                           all_events=all_events,
                           user_name =session.get('name', 'UNKNOWN')
                           )
    return redirect('/')



@app.route('/event_details')
def event_details():
    is_soon = False
    id = request.args.get('id')
    event = get_event_by_id(id)
    date_diff = (event.date - date.today()).days
    if date_diff < 15:
        is_soon = True
        geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
        location = geolocator.geocode(event.location)
        params = {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'daily': 'weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max',
            'timezone':'Australia/Sydney',
            'forecast_days':16,
        }
        response = requests.get(url=f'https://api.open-meteo.com/v1/forecast', params=params).json()
        index = None
        index =[num for num,each in enumerate(response['daily']['time']) if each == datetime.strftime(event.date, '%Y-%m-%d')][0]
        weather_code = get_weather_info(response['daily']['weathercode'][index]) 
        temperature_max = response['daily']['temperature_2m_max'][index]
        temperature_min = response['daily']['temperature_2m_min'][index]
        print(weather_code, temperature_max, temperature_min)
        return render_template('event_details.html', 
            event=event,
            user_id = session.get('id'),
            weather_code = weather_code,
            temperature_max=temperature_max,
            temperature_min=temperature_min,
            is_soon=is_soon
            )
    return render_template('event_details.html', 
            event=event,
            user_id = session.get('id'))
    


@app.route('/delete_event')
def delete_event():
    id = request.args.get('id')
    delete_event_by_id(id)
    return redirect('/upcoming_events')




if __name__ == '__main__':
    app.run(debug = True) 


