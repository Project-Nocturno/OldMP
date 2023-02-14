from flask import Flask
from cryptography.fernet import Fernet
import mysql.connector
from threading import Thread

from modules.oldmpweb import OldMPWeb as oldmpweb
from modules.oldmp import OldMP as oldmp
from modules.oldmplauncher import OldMPLauncher as oldmplauncher
from modules.loops import Loops as loops


backendP=3551 # backend port
websiteP=80 # base web port
launcherP=4971 # launcher port
# 20228

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
logsapp=True


urlkey="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mUDSFJsdJOFKJKJSDgjkojsdJJKOGJJKOSJGKJOjsDJKO"
enckey="1ldcQilhWsPDjlFyLFU3VJXCNJQW6gf6oI6CoLbeNSc="
enc=Fernet(enckey).encrypt
dec=Fernet(enckey).decrypt


website_url="https://www.nocturno.games"
api_url="https://nocturno.games/api"


app=Flask("OldMP")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

appweb=Flask("OldMPWeb")

applaunch=Flask("OldMPLauncher")
applaunch.config["SESSION_PERMANENT"] = False
applaunch.config["SESSION_TYPE"] = "filesystem"

tempfileclst='data/clientsettings'
clients=[]
palyerscoords=[]


tl=Thread(target=loops(palyerscoords).makemap)
tl.setDaemon(True)
tl.start()

tweb=Thread(target=oldmpweb, args=(cnx, logsapp, clients, palyerscoords, appweb, websiteP))
tweb.setDaemon(True)
tweb.start()

tlaunch=Thread(target=oldmplauncher, args=(enc, dec, cnx, logsapp, applaunch, launcherP, clients, api_url, proxy, startWithProxy))
tlaunch.setDaemon(True)
tlaunch.start()

oldmp(cnx, dec, enc, logsapp, app, clients, tempfileclst, startWithProxy, api_url, proxy, backendP)