import flask, os, subprocess, re, json

class Client(flask.Flask):
  from .client import setClientID, setClientSecret, setRedirectURI, setScope, createLogonSession, getLogin, saveLogin, getSavedLogin
  def __init__(self, flaskApp):
    from .data import data
    data["flaskSession"] = flaskApp

from .database import NewDatabase
