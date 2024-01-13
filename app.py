from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'dfygyrsktk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    ph_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    messages_sent = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id')
    messages_received = db.relationship('Message', backref='receiver', lazy=True, foreign_keys='Message.receiver_id')

class Message(db.Model):   
    id = db.Column(db.Integer, primary_key=True) 
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('person.ph_no'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('person.ph_no'), nullable=False)


def encrypt(message):
    key = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789, ")
    encrypted_message = ""
    for char in message:
        index = key.index(char)
        encrypted_message += key[(index + 3) % len(key)]
    return encrypted_message

def decrypt(encrypted_message):
    key = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789, ")
    decrypted_message = ""
    for char in encrypted_message:
        index = key.index(char)
        decrypted_message += key[(index - 3) % len(key)]
    return decrypted_message
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return render_template('login_signup.html')

@app.route('/login', methods=['POST'])
def login():
    phone_number = request.form.get('loginPhoneNumber')
    password = request.form.get('loginPassword')
    user = Person.query.filter_by(ph_no=phone_number, password=password).first()
    

    if user:
        session['user_id'] = phone_number
        users = Person.query.filter(Person.ph_no != phone_number).all()
        # user_names = [person.name for person in users]
        return render_template('index.html', user_names = users, name= Person.query.get(phone_number).name)
    return render_template('login_signup.html',error = 'Invalid login credentials')


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('signupName')
    phone_number = request.form.get('signupPhoneNumber')
    password = request.form.get('signupPassword')
    confirm_password = request.form.get('confirmPassword')

    if password == confirm_password:
        # Check if the user with the given phone_number already exists
        existing_user = Person.query.filter_by(ph_no=phone_number).first()

        if existing_user:
            # Handle the case where the user already exists
            return render_template('login_signup.html', error='User with this phone number already exists.')

        # Create a new Person instance and add it to the database
        new_user = Person(ph_no=phone_number, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login/signup page or any other appropriate page
        return render_template('login_signup.html')

    # Handle the case where passwords do not match
    return render_template('login_signup.html', error='Passwords do not match.')



@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    encrypted = encrypt(message)
    return render_template('index.html', sended_message = message, received_message = encrypted)




if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
