from flask import Flask, render_template, request, redirect, session, flash
from models.events import (
    get_all_events,
    delete_event_by_id,
    insert_event,
    get_all_my_events,
    get_event_by_id,
    update_event,
)
from models.users import (
    insert_user,
    select_user_by_email,
    get_all_user_emails,
    delete_user,
)
from models.attendances import (
    insert_event_attendance,
    get_all_attendance_by_userid,
    delete_attendance_by_eventid,
)
from models.images import insert_image, show_images
from werkzeug.security import generate_password_hash
import requests
from geopy.geocoders import Nominatim
import random
import os
from weather_code import get_weather_info
from datetime import datetime, date
from cloudinary import CloudinaryImage
import cloudinary.uploader
import asyncio


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


# Homepage
@app.route("/")
def index():
    all_events = get_all_events(session.get("email"), session.get("id"))
    return render_template(
        "index.html",
        all_events=random.sample(all_events, 3),
        user_name=session.get("name", "UNKNOWN"),
    )


# Upcoming events page
@app.route("/upcoming_events")
def upcoming_events():
    show_past = request.args.get("past_events")
    events = get_all_events(session.get("email"), session.get("id"))

    # Filtering events based on the show_past query parameter
    if show_past == "show-past":
        all_events = [event for event in events if event.date < date.today()]
    else:
        all_events = [event for event in events if event.date >= date.today()]

    # Checking if the user is logged in
    if session.get("name", "UNKNOWN") != "UNKNOWN":
        all_attendances = get_all_attendance_by_userid(session.get("id"))
        return render_template(
            "upcoming_events.html",
            all_events=all_events,
            user_name=session.get("name", "UNKNOWN"),
            all_attendances=all_attendances,
            user_id=session.get("id"),
        )
    return render_template(
        "upcoming_events.html",
        all_events=all_events,
        user_name=session.get("name", "UNKNOWN"),
        user_id=session.get("id"),
    )


# Attending events page
@app.route("/attending_events")
def attending_events():
    show_past = request.args.get("past_events")
    events = get_all_events(session.get("email"), session.get("id"))

    # Filtering events based on the show_past query parameter
    if show_past == "show-past":
        all_events = [event for event in events if event.date < date.today()]
    else:
        all_events = [event for event in events if event.date >= date.today()]
    # Checking if the user is logged in
    if session.get("name", "UNKNOWN") != "UNKNOWN":
        all_attendances = get_all_attendance_by_userid(session.get("id"))
    return render_template(
        "upcoming_events.html",
        show_attendance=True,
        all_events=all_events,
        user_name=session.get("name", "UNKNOWN"),
        all_attendances=all_attendances,
        user_id=session.get("id"),
    )


# Attendance actions
@app.route("/attend_event_action")
def attend_event_action():
    event_id = request.args.get("id")
    user_id = session.get("id")
    insert_event_attendance(user_id, event_id)
    return redirect("/upcoming_events")


@app.route("/cancel_attendance")
def cancel_attendance():
    event_id = request.args.get("id")
    delete_attendance_by_eventid(event_id)
    return redirect("/upcoming_events")


@app.get("/signup")
def signup():
    return render_template("signup.html", user_name=session.get("name", "UNKNOWN"))


# Signup page
@app.post("/signup")
def signup_action():
    is_duplicate = False
    name = request.form.get("name").strip().title()
    email = request.form.get("email").lower().strip()

    # Checking if the passwords match
    if request.form.get("password1") == request.form.get("password2"):
        hashed_password = generate_password_hash(request.form.get("password1"))
        all_emails = get_all_user_emails()
        # Checking if the email is already registered
        for each_email in all_emails:
            if email == each_email["email"]:
                is_duplicate = True
        if not is_duplicate:
            user_id = insert_user(name, email, hashed_password)
            session["email"] = email
            session["id"] = user_id
            session["name"] = name
            flash("You were successfully logged in")
            return redirect("/")
        else:
            flash("Sorry, this email is already registered with us. Try logging in.")
            return redirect("/login")
    else:
        flash("Sorry your passwords do not match. Please try again.")
        return redirect("/signup")


# Login page
@app.get("/login")
def login():
    return render_template("login.html", user_name=session.get("name", "UNKNOWN"))


# Login action
@app.post("/login")
def login_action():
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        user = select_user_by_email(email)
        # Validating user credentials
        if (
            (user.validate_password(password) and user.email == email)
            if user != None
            else None
        ):
            session["email"] = user.email
            session["id"] = user.id
            session["name"] = user.name
            flash("You have successfully logged in.")
            return redirect("/")
        else:
            flash("Your email or password was incorrect. Please try again.")
            return redirect("/login")


# Logout
@app.route("/logout")
def logout():
    session.pop("name")
    session.pop("email")
    session.pop("id")
    flash("You have successfully logged out.")
    return redirect("/")


# Delete account
@app.route("/delete_acc")
def delete_acc():
    id = session.get("id")
    delete_user(id)
    session.pop("name")
    session.pop("email")
    session.pop("id")
    return redirect("/")


# Add or edit event page
@app.get("/add_or_edit_event")
def add_or_edit_event():
    id = request.args.get("id")
    if id == None:
        return render_template("create_event.html", event=[])
    else:
        event = get_event_by_id(id)
        start_time = datetime.strptime(event.start_time, "%I:%M %p").strftime("%H:%M")
        end_time = datetime.strptime(event.end_time, "%I:%M %p").strftime("%H:%M")
        return render_template(
            "create_event.html", event=event, start_time=start_time, end_time=end_time
        )


# Add or edit event action
@app.post("/add_or_edit_event")
def add_or_edit_event_action():
    id = request.args.get("id")
    event_name = request.form.get("name")
    type = request.form.get("type")
    description = request.form.get("description")
    location = request.form.get("location").capitalize()
    date = request.form.get("date")
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")
    user_id = session.get("id")
    type = request.form.get("type")
    email_list = request.form.get("emails").lower().split(",")
    parsed_email_list = [email.strip() for email in email_list]

    # Inserting or updating the event
    if id == None:
        id = insert_event(
            event_name,
            type,
            description,
            location,
            date,
            start_time,
            end_time,
            parsed_email_list,
            user_id,
        )
        flash(f"A new {type.lower()} event has been created.")
    else:
        id = update_event(
            event_name,
            type,
            description,
            location,
            date,
            start_time,
            end_time,
            parsed_email_list,
            user_id,
            id,
        )
        flash(f"{event_name} event has been updated.")

    # Sending emails to invitees
    if email_list != [""]:
        event = get_event_by_id(id)
        asyncio.run(event.send_email(session.get("name")))
        # event.send_email(session.get('name'))
        flash("Emails have been sent to the invitees.")
    return redirect("/")


# My events page
@app.route("/my_events")
def my_events():
    show_past = request.args.get("past_events")
    # Checking if the user is logged in
    if session.get("name", "UNKNOWN") != "UNKNOWN":
        events = get_all_my_events(
            session.get(
                "id",
            )
        )
        # Filtering events based on the show_past query parameter
        if show_past == "show-past":
            all_events = [event for event in events if event.date < date.today()]
        elif show_past == "show-present":
            all_events = [event for event in events if event.date >= date.today()]
        else:
            all_events = events

        return render_template(
            "my_events.html",
            all_events=all_events,
            user_name=session.get("name", "UNKNOWN"),
        )
    return redirect("/")


# Event details page
@app.route("/event_details")
def event_details():
    is_soon = False
    id = request.args.get("id")
    event = get_event_by_id(id)
    date_diff = (event.date - date.today()).days
    if date_diff < 15 and event.date > date.today():
        is_soon = True
        # Use geolocator to get location details for weather information
        geolocator = Nominatim(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        )
        location = geolocator.geocode(event.location)

        # Check if the event is within 15 days and is in the future
        if location != None:
            params = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "timezone": "Australia/Sydney",
                "forecast_days": 16,
            }
            # Make a request to the weather API
            response = requests.get(
                url=f"https://api.open-meteo.com/v1/forecast", params=params
            ).json()
            index = None
            index = [
                num
                for num, each in enumerate(response["daily"]["time"])
                if each == datetime.strftime(event.date, "%Y-%m-%d")
            ][0]
            weather_code = get_weather_info(response["daily"]["weathercode"][index])
            temperature_max = response["daily"]["temperature_2m_max"][index]
            temperature_min = response["daily"]["temperature_2m_min"][index]
            return render_template(
                "event_details.html",
                event=event,
                user_id=session.get("id"),
                weather_code=weather_code,
                temperature_max=temperature_max,
                temperature_min=temperature_min,
                is_soon=is_soon,
                user_name=session.get("name", "UNKNOWN"),
            )
    return render_template(
        "event_details.html",
        event=event,
        user_id=session.get("id"),
        user_name=session.get("name", "UNKNOWN"),
    )


@app.route("/delete_event")
def delete_event():
    id = request.args.get("id")
    delete_event_by_id(id)
    return redirect("/upcoming_events")


@app.route("/gallery")
def gallery():
    event_id = request.args.get("id")
    # Get images associated with the event from the database
    images = show_images(event_id=event_id)
    # Transform image URLs for display using Cloudinary
    for image in images:
        transformed_url = CloudinaryImage(image.public_id).build_url(
            width=500, aspect_ratio=1.0, crop="fill", gravity="faces"
        )
        image.image_url = transformed_url
    return render_template(
        "gallery.html",
        event_id=event_id,
        images=images,
        user_name=session.get("name", "UNKNOWN"),
    )


@app.get("/upload_photo")
def upload_photo():
    return redirect("/gallery")


@app.post("/upload_photo")
def upload_photo_action():
    # Retrieve uploaded images and event ID from the request
    images = request.files.getlist("images")
    event_id = request.form.get("event_id")

    # Process each uploaded image and insert into the database
    for image in images:
        image_rows = []
        uploaded_image = cloudinary.uploader.upload(image)
        image_rows.append(
            [uploaded_image["public_id"], uploaded_image["secure_url"], event_id]
        )
        insert_image(image_rows)
    return redirect("/upcoming_events")


if __name__ == "__main__":
    # Run the Flask application
    app.run(host="localhost", port="8080", debug=True)
