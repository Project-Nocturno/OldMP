from flask import Flask
from cryptography.fernet import Fernet
import mysql.connector
from threading import Thread
from time import sleep

from modules.oldmpweb import OldMPWeb as oldmpweb
from modules.oldmp import OldMP as oldmp
from modules.oldmplauncher import OldMPLauncher as oldmplauncher
from modules.loops import Loops as loops


backendP=3551 # backend port
websiteP=80 # base web port
launcherP=4971 # launcher port
# 20228

clients=[]
palyerscoords=[]
session={}
rps={}

# db conn
cnx=mysql.connector.connect(
    user='doadmin',
    password='AVNS_-j7sW3k0hYO3J6dIq_q',
    host='db-mysql-tor1-84534-do-user-12821157-0.b.db.ondigitalocean.com',
    database='nocturnoDB',
    port='25060'
)

# proxy parameters
startWithProxy=True
proxy={
   'http': 'http://127.0.0.1:9999',
   'https': 'http://127.0.0.1:9999',
}
logsapp=True

# all the website and encryption
website_url="https://www.nocturno.games"
api_url="https://nocturno.games/api"
urlkey="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mUDSFJsdJOFKJKJSDgjkojsdJJKOGJJKOSJGKJOjsDJKO"

enckey="1ldcQilhWsPDjlFyLFU3VJXCNJQW6gf6oI6CoLbeNSc="
enc=Fernet(enckey).encrypt
dec=Fernet(enckey).decrypt

# all the backend services conf
app=Flask("OldMP") # lobby emulator conf
appweb=Flask("OldMPWeb") # website conf
applaunch=Flask("OldMPLauncher") # launcher backend services conf

# start all the backend services
tl=Thread(target=loops(palyerscoords).makemap)
tl.setDaemon(True)
tl.start()

tweb=Thread( # thread for the website services
    target=oldmpweb, args=(
        cnx,
        logsapp,
        clients,
        palyerscoords,
        appweb,
        websiteP,
        rps
    )
)
tweb.setDaemon(True)
tweb.start()
sleep(1)

tlaunch=Thread( # thread for the launcher backend services
    target=oldmplauncher, args=(
        enc,
        dec,
        cnx,
        logsapp,
        applaunch,
        launcherP,
        clients,
        api_url,
        proxy,
        startWithProxy,
        session,
        rps
    )
)
tlaunch.setDaemon(True)
tlaunch.start()

sleep(1)
oldmp( # start the main backend service
    cnx,
    dec,
    enc,
    logsapp,
    app,
    clients,
    startWithProxy,
    api_url,
    proxy,
    backendP,
    session,
    rps
)