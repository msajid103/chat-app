# Import necessary modules
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session security
socketio = SocketIO(app)

users = [
    {'phone_no': '1', 'password': '1', 'name': 'Sajid'},
    {'phone_no': '2', 'password': '2', 'name': 'Sadaqat'},
    {'phone_no': '3', 'password': '3', 'name': 'Ali Raza'},
    {'phone_no': '4', 'password': '4', 'name': 'Bali'},
    # Add more user entries as needed
]

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

@app.route('/')
def index():
    return render_template('login_signup.html')

@app.route('/login', methods=['POST'])
def login():
    phone_number = request.form.get('loginPhoneNumber')
    password = request.form.get('loginPassword')
    for user in users:
        if user['phone_no'] == phone_number and user['password'] == password:
            # Set user identifier in the session
            session['user_id'] = phone_number
            return render_template('index.html', name=user['name'])
    return render_template('login_signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('signupName')
    phone_number = request.form.get('signupPhoneNumber')
    password = request.form.get('signupPassword')
    confirm_password = request.form.get('confirmPassword')
    if password == confirm_password:
        users.append({'phone_no': phone_number, 'password': password, 'name': name})
    return render_template('login_signup.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    encrypted = encrypt(message)
    return render_template('index.html', sended_message = message, received_message = encrypted)




if __name__ == '__main__':
    socketio.run(app, debug=True)
