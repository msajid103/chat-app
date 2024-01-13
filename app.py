from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'dfygyrsktk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    ph_no = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    messages_sent = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id')
    messages_received = db.relationship('Message', backref='receiver', lazy=True, foreign_keys='Message.receiver_id')

class Message(db.Model):   
    id = db.Column(db.Integer, primary_key=True) 
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.String(11), db.ForeignKey('person.ph_no'), nullable=False)
    receiver_id = db.Column(db.String(11), db.ForeignKey('person.ph_no'), nullable=False)


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
# with app.app_context():
#     db.create_all()
#     db.session.query(Message).delete()
#     db.session.commit()
    

@app.route('/')
def index():
    return render_template('login_signup.html')
users = None
phn = None
@app.route('/login', methods=['POST'])
def login():
    global users
    global phn
    phone_number = request.form.get('loginPhoneNumber')
    password = request.form.get('loginPassword')
    user = Person.query.filter_by(ph_no=phone_number, password=password).first()
    if user:
        phn = phone_number
        users = Person.query.filter(Person.ph_no != phone_number).all()  
        messages = Message.query.filter(
        ((Message.sender_id == phone_number) & (Message.receiver_id == users[0].ph_no)) |
        ((Message.sender_id == users[0].ph_no) & (Message.receiver_id == phone_number))).all()    
        return render_template('index.html',
            user_names = users, 
            receiver_name = users[0].name,  
            name= Person.query.get(phone_number),
            messages = messages)
    return render_template('login_signup.html',error = 'Invalid login credentials')


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('signupName')
    phone_number = request.form.get('signupPhoneNumber')
    password = request.form.get('signupPassword')
    confirm_password = request.form.get('confirmPassword')
    if password == confirm_password:
        existing_user = Person.query.filter_by(ph_no=phone_number).first()
        if existing_user:
            return render_template('login_signup.html', error='User with this phone number already exists.')
        new_user = Person(ph_no=phone_number, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login_signup.html')
    return render_template('login_signup.html', error='Passwords do not match.')



@app.route('/message_handling', methods=['POST'])
def message_handling():
    global users
    global phn    
    message = request.form.get('message')
    receiver_phno = request.form.get('phone_number')
    encrypted = encrypt(message) 
    if message != "" and message != " ":
        new_message = Message(content=encrypted, sender_id= str(phn) , receiver_id=receiver_phno)
        db.session.add(new_message)
        db.session.commit()
    messages = Message.query.filter(
    ((Message.sender_id == phn) & (Message.receiver_id == receiver_phno)) |
    ((Message.sender_id == receiver_phno) & (Message.receiver_id == phn)))
    return render_template('index.html', 
        user_names = users, 
        receiver_name = Person.query.get(receiver_phno).name,
        name= Person.query.get(phn),
        messages = messages)


if __name__ == '__main__':
    # db.create_all()
   
    app.run(debug=True)
