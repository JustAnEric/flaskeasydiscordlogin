import os, re, json, flask, subprocess, requests

from .data import data

class User:
  def __init__(self, user):
    return user

def setClientID(flask2, client_id):
  """
  Sets the `clientId` for Discord OAuth2. **(required)**
  """
  data["clientId"] = client_id

def setClientSecret(flask2, client_secret):
  """
  Sets the `clientSecret` for Discord OAuth2. **(required)**
  """
  data["clientSecret"] = client_secret

def setRedirectURI(flask2, redirect_uri):
  """
  Sets the `redirectURI` for Discord OAuth2. **(required)**
  """
  data["redirectURI"] = redirect_uri

def setScope(flask2, scope_list):
  """
  Sets the `scope` for Discord OAuth2. **(required)**
  scope_list = [str(x)] **- `scope_list is a list() object with strings of scopes.`**
  """
  string = ""
  for i in scope_list:
    string += f"{i}%20"
  data["scope"] = string

def createLogonSession(flask2):
  """
  Creates the logon session for Discord OAuth2.
  This function is called when you need to do OAuth with Discord.
  ```py
  ...
  @app.route('/')
  def login():
    return flaskeasydiscordlogin.Client().createLogonSession()
  ...
  ```
  """
  #create logon session using data
  f = data["flaskSession"]
  data["flaskStoreLogonSession"] = 1
  return flask.redirect(f"https://discord.com/api/oauth2/authorize?client_id={data['clientId']}&redirect_uri={data['redirectURI']}&response_type=code&scope={data['scope']}")

def getLogin(flask2, request, type="raw"):
  """
  Gets the login JSON for Discord OAuth2 after the `flaskeasydiscordlogin.Client().createLogonSession()` has been fired. 
  ```py
  ...
  @app.route('/login/done')
  def logindone():
    loginJSON = flaskeasydiscord.Client().getLogin()
    return f'Your logged in as {loginJSON.get("username")}#{loginJSON.get("discriminator")}'
  ...
  ```
  """
  flask = data["flaskSession"]
  code = request.args.get('code')
  if type == "raw":
    payload = {
      "client_id": data["clientId"],
      "client_secret": data["clientSecret"],
      "grant_type": "authorization_code",
      "code": code,
      "redirect_uri": data["redirectURI"],
      "scope": data["scope"]
    }
    try:
      r = requests.post(url="https://discord.com/api/oauth2/token", data=payload).json()
    except: return "You are unauthorized to view this page."
    at = r.get("access_token")
    r2 = requests.get('https://discord.com/api/users/@me', headers = {"Authorization": f"Bearer {at}"})
    user = r2.json()
    return {"user": user, "at": at}
  else: return "Error in flaskeasydiscordlogin: Unknown type."

def saveLogin(flask2, session, at):
  session["login_at"] = at

def getSavedLogin(flask2, session):
  if 'login_at' in session:
    r = requests.get('https://discord.com/api/users/@me', headers = {"Authorization": f"Bearer {session['login_at']}"})
    user = r.json()
    return user
  else: return False
