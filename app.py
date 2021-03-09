from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import  SQLAlchemy
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Database initialization

db= SQLAlchemy(app)

# DATABASE MODEL

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Create a funtion to return a string when we add something
def __repr__(self):
    return '<Name %r>' % self.id


# Views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/friends', methods= ['POST','GET'])
def friends():
    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name= friend_name)
        # push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "there was a problem with adding you friend :( "
    else:
        friends_list = Friends.query.all()
        return render_template('friends.html', friends_list=friends_list)

@app.route('/friend-update/<int:id>', methods= ['POST','GET'])
def friends_update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "there was a problem with adding you friend :( "
    else:
        return render_template('friend-update.html', friend_to_update=friend_to_update)

@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')

@app.route('/sign-up', methods=["POST"])
def sign_up():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get("email")
    message = MIMEText(f"Hi {first_name} {last_name} This is an automated email from https://flaskexamplesite.herokuapp.com")
    message_to_admin = MIMEText(
        f"Hi  This is an automated email from https://flaskexamplesite.herokuapp.com {email}")
    server = smtplib.SMTP('smtp.zoho.eu','587')
    #Debug tool
    # server.set_debuglevel(1)
    server.starttls()
    server.login('michal.ogorzalek@zohomail.eu', os.environ.get('ZOHO_EMAIL_HOST_PASSWORD') )
    #print('to email: '+ email +  ' \n messege:' + message.as_string())
    server.sendmail('michal.ogorzalek@zohomail.eu', email, message.as_string())
    server.sendmail('michal.ogorzalek@zohomail.eu', 'michal.ogorzalek@gmail.com', message_to_admin.as_string())
    if not first_name or not last_name or not email:
        error_statement = "All fields are required "
        return render_template('subscribe.html', error_statement=error_statement)
    return render_template('sign-up.html', first_name= first_name,last_name=last_name,email=email)

@app.route('/friend-delete/<int:id>')
def friend_delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "there was a problem deleting from db"
