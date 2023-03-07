from flask import Flask, render_template, request,redirect, session
from models.events import get_all_events
from models.users import insert_user, select_user_by_email
from models.attendances import insert_event_attendance, get_all_attendance_by_userid, delete_attendance_by_eventid
from werkzeug.security import generate_password_hash
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
app.config['SECRET_KEY'] = 'aspdkjpq343te5y5'


@app.route('/')
def index():
    all_events = get_all_events()
    return render_template('index.html', 
                           all_events=all_events, 
                           user_name =session.get('name', 'UNKNOWN'))

@app.route('/upcoming_events')
def upcoming_events():
    all_events = get_all_events()
    if session.get('name', 'UNKNOWN') != 'UNKNOWN':
        all_attendances = get_all_attendance_by_userid(session.get('id'))
        return render_template('upcoming_events.html',  
                           all_events=all_events,
                           user_name =session.get('name', 'UNKNOWN'),
                           all_attendances = all_attendances)
    return render_template('upcoming_events.html',  
                           all_events=all_events,
                           user_name =session.get('name', 'UNKNOWN'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email').lower()
        if request.form.get('password1') == request.form.get('password2'):
            hashed_password = generate_password_hash(request.form.get('password1')) 
            insert_user(name, email, hashed_password)
            user = select_user_by_email(email)
            session['email'] = user.email
            session['id'] = user.id
            session['name'] = user.name
            return redirect('/')
        else:
            return redirect('/')    
    return render_template('signup.html', 
                           user_name =session.get('name', 'UNKNOWN'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        user = select_user_by_email(email)
        if user.validate_password(password):
            session['email'] = user.email
            session['id'] = user.id
            session['name'] = user.name
            return redirect('/')

        
    return render_template ('login.html', 
                            user_name =session.get('name', 'UNKNOWN'))


@app.route('/logout')
def logout():
    session.pop('name')
    session.pop('email')
    session.pop('id')
    return redirect('/')

@app.route('/attend_event_action')
def attend_event_action():
    event_id = request.args.get('id')
    user_id = session.get('id')
    insert_event_attendance(user_id, event_id)
    return redirect('/upcoming_events')


@app.route ('/attending_events')
def attending_events():
    all_events = get_all_events()
    if session.get('name', 'UNKNOWN') != 'UNKNOWN':
        all_attendances = get_all_attendance_by_userid(session.get('id'))
    return render_template('upcoming_events.html',show_attendance = True,
                           all_events=all_events,
                           user_name =session.get('name', 'UNKNOWN'),
                           all_attendances=all_attendances
                          )


@app.route('/cancel_attendance')
def cancel_attendance():
    event_id = request.args.get('id')
    delete_attendance_by_eventid(event_id)
    return redirect('/upcoming_events')
    

@app.route('/create_public_event')
def create_public_event():
    return render_template('create_event.html')


@app.route('/create_private_event')
def create_private_event():
    pass


@app.route('/event_details')
def event_details():
    pass


if __name__ == '__main__':
    app.run(debug = True) 


