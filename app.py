from flask import Flask, render_template, request,redirect, session
from models.events import get_all_events
from models.users import insert_user, select_user_by_email
from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route('/event_details')
def event_details():
    pass

if __name__ == '__main__':
    app.run(debug = True) 


