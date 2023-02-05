from flask import Flask, session
from flask_session import Session
from cryptography.fernet import Fernet
import mysql.connector
from threading import Thread

from modules.oldmpweb import OldMPWeb as oldmpweb
from modules.oldmp import OldMP as oldmp
from modules.loops import Loops as loops


cnx=mysql.connector.connect(
    user='doadmin',
    password='AVNS_-j7sW3k0hYO3J6dIq_q',
    host='db-mysql-tor1-84534-do-user-12821157-0.b.db.ondigitalocean.com',
    database='nocturnoDB',
    port='25060'
)

startWithProxy=True
proxy={
   'http': 'http://127.0.0.1:9999',
   'https': 'http://127.0.0.1:9999',
}

urlkey="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mUDSFJsdJOFKJKJSDgjkojsdJJKOGJJKOSJGKJOjsDJKO"
enckey="1ldcQilhWsPDjlFyLFU3VJXCNJQW6gf6oI6CoLbeNSc="
enc=Fernet(enckey).encrypt
dec=Fernet(enckey).decrypt

website_url="https://www.nocturno.games"
api_url="https://nocturno.games/api"

app=Flask("OldMP")
appweb=Flask("OldMPWeb")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

tempfileclst='data/clientsettings'
clients=[]
palyerscoords=[]


tl=Thread(target=loops(palyerscoords).makemap)
tl.setDaemon(True)
tl.start()

tweb=Thread(target=oldmpweb, args=(clients, palyerscoords, appweb))
tweb.setDaemon(True)
tweb.start()

oldmp(dec, enc, session, app, clients, tempfileclst, startWithProxy, api_url, proxy)