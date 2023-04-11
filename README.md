# flaskeasydiscordlogin.py
A simple API to create an access token and share it with Flask including user data. It also has a wonderful and easy-to-use database which can be used for storing user data. It can save logins after they have been done and it can evaluate logins easy. Read the README.md file for more info!

## Getting Started
In order to use this API, you will **need to CD into your project's directory and type in Terminal**: `git clone https://github.com/JustAnEric/flaskeasydiscordlogin.py.git`
This will install **our API onto your computer or hard drive.**
To get the package working, put this in your main file:
```py
from flask import Flask, render_template, abort, flash, session, url_for, request
from flaskeasydiscordlogin import OAuth2

app = Flask('testing-123')
client = OAuth2.Client(app)

client.setClientID("your_app_client_id_here")
client.setClientSecret("your_app_client_secret_here")
client.setRedirectURI("https://your_redirect_uri_here")
client.setScope(['identity', 'email', 'guilds', 'connections']) # add or remove any scopes you (want/don't want)

@app.route('/')
def login():
  return client.createLogonSession()

@app.route('/done')
def loginDone():
  login2 = client.getLogin(request) # gets the login information and returns it as {"user": [...], "at": "..."}
  client.saveLogin(session, login2["at"]) # saves the login access token in session
  try:
    return f'{login2["user"].get("username")}#{login2["user"].get("discriminator")}' # return the username and discriminator (tag) of the user that signed in
  except: return login2 # if there is an error, we just return unauthorised.
  
app.run()
```

## Databases and Storing Information about Users
Got any premium feature or anything other? We have a Database class to store that information for you.
```py
from flask import Flask, render_template, abort, flash, session, url_for, request
from flaskeasydiscordlogin import OAuth2

app = Flask('testing-123')
client = OAuth2.Client(app)
db = OAuth2.NewDatabase("userData")

@app.route('/done')
def loginDone():
  login2 = client.getLogin(request) # gets the login information and returns it as {"user": [...], "at": "..."}
  client.saveLogin(session, login2["at"]) # saves the login access token in session
  if not db.getKey(login2["user"].get("id")):
    db.setKey(login2["user"]["id"], {
      "premium": False,
      "username": login2["user"]["tag"]
    }); # set the user information key to a dict (dictionary)
  try:
    return f'{login2["user"].get("username")}#{login2["user"].get("discriminator")}' # return the username and discriminator (tag) of the user that signed in
  except: return login2 # if there is an error, we just return unauthorised.
  
app.run()
```
