# app.py

from flask import Flask, render_template, request

app = Flask(__name__)


def encrypt(message, key):   
    encrypted_message = ""
    for char in message:
        index = key.index(char)
        encrypted_message += key[(index + 3) % len(key)]
    return encrypted_message

def decrypt(encrypted_message, key):
    # Decrypt the message using the provided key
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
    print(f"Login request received. Phone Number: {phone_number}, Password: {password}")
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('signupName')
    phone_number = request.form.get('signupPhoneNumber')
    password = request.form.get('signupPassword')
    confirm_password = request.form.get('confirmPassword')
    if password == confirm_password:
        print(f"Signup request received. Name: {name}, Phone Number: {phone_number}, Password: {password}")    
    return render_template('login_signup.html')

@app.route('/sendMessage', methods = ['POST'])
def sendMessage():
    message = request.form.get('message')
    key = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789, ")
    encrypted_message = encrypt(message,key)
    return render_template('index.html', message = message,  encrypted_message = encrypted_message)

if __name__ == '__main__':
    app.run(debug=True)
