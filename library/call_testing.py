from flask import Flask, render_template, json, request, session, url_for, redirect, g
from user import login, registration, getProfile, update_profile, forgetpasswd
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login user
# user = "sri2@mail.com"
# passwd = 'sri1'
# password = hash_password(passwd)
# testing = login(user, password)
# print(testing.user_login())

# registration user
# email = "smulfa@mail.com"
# user = "smulfa"
# passwd = "smulfa"
# word = hash_password(passwd)
# tahu = registration(user, email, word)
# print(tahu.signUp())

# get Profile user
# username = 'sri2@mail.com'
# user = getProfile(username)
# print(user.profile())


# username = 'mukidi2'
# password = 'mukidi2'
# email = 'linggar@mail.com'
#
# update = update_profile(username, password, email)
# print(update.updateprofile())

# update password
# email = 'linggar@mail.com'
# passwordold = 'mukidi2'
# passwordnew = 'mukidijalan'
# getEmail = forgetpasswd(email, passwordold, passwordnew)
# print(getEmail.getOldPassword())
# print(getEmail.chPasswd())

@app.route('/')
def index():
    return "Welcome Home"

@app.route('/password')
def password():
    username = 'sri2@mail.com'
    user = getProfile(username)
    namelist = user.profile()
    nama = namelist[0][1]
    email = namelist[0][2]
    return json.dumps(namelist)

if __name__ == '__main__':
    app.run(debug=True)