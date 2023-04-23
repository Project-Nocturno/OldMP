from flask import Flask
#from flask_mysqldb import MySQL
import psycopg2
#import mysql.connector #
from cryptography.fernet import Fernet
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

#list
blacklist={}
whitelist=[]

playerscoords=[]
session={}
rps={}

# db conn
#cnxx=mysql.connector.connect( #
#    user='doadmin',
#    password='AVNS_nXyKDgrPe47nLv5q43k',
#    host='db-mysql-fra1-71731-do-user-13276156-0.b.db.ondigitalocean.com',
#    database='nocturnoDB2',
#    port='25060'
#)
cnx = psycopg2.connect(
    host="db-postgresql-fra1-29006-nocturno-do-user-13276156-0.b.db.ondigitalocean.com",
    port=25060,
    database="nocturnoDB",
    user="doadmin",
    password="AVNS_EAUVPPgoAPAk4mDd8QC"
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

# db conn
#app.config['MYSQL_HOST'] = 'db-mysql-fra1-71731-do-user-13276156-0.b.db.ondigitalocean.com'
#app.config['MYSQL_PORT'] = 25060
#app.config['MYSQL_USER'] = 'doadmin'
#app.config['MYSQL_PASSWORD'] = 'AVNS_nXyKDgrPe47nLv5q43k'
#app.config['MYSQL_DB'] = 'nocturnoDB2'

#appweb.config['MYSQL_HOST'] = 'db-mysql-fra1-71731-do-user-13276156-0.b.db.ondigitalocean.com'
#appweb.config['MYSQL_PORT'] = 25060
#appweb.config['MYSQL_USER'] = 'doadmin'
#appweb.config['MYSQL_PASSWORD'] = 'AVNS_nXyKDgrPe47nLv5q43k'
#appweb.config['MYSQL_DB'] = 'nocturnoDB2'

#applaunch.config['MYSQL_HOST'] = 'db-mysql-fra1-71731-do-user-13276156-0.b.db.ondigitalocean.com'
#applaunch.config['MYSQL_PORT'] = 25060
#applaunch.config['MYSQL_USER'] = 'doadmin'
#applaunch.config['MYSQL_PASSWORD'] = 'AVNS_nXyKDgrPe47nLv5q43k'
#applaunch.config['MYSQL_DB'] = 'nocturnoDB2'

#mysql = MySQL(app)
#mysqlweb = MySQL(appweb)
#mysqllaunch = MySQL(applaunch)

# start all the back services
tl=Thread(target=loops(playerscoords, rps).makemap)
tl.setDaemon(True)
tl.start()

tl=Thread(target=loops(playerscoords, rps).updaterps)
tl.setDaemon(True)
tl.start()

tweb=Thread( # thread for the website services
    target=oldmpweb, args=(
        #mysqlweb,
        cnx,
        logsapp,
        playerscoords,
        appweb,
        websiteP,
        rps,
        session,
        whitelist,
        blacklist
    )
)
tweb.setDaemon(True)
tweb.start()

sleep(1)
tlaunch=Thread( # thread for the launcher backend services
    target=oldmplauncher, args=(
        enc,
        dec,
        #mysqllaunch,
        cnx,
        logsapp,
        applaunch,
        launcherP,
        api_url,
        proxy,
        startWithProxy,
        session,
        rps,
        whitelist,
        blacklist
    )
)
tlaunch.setDaemon(True)
tlaunch.start()

sleep(1)
oldmp( # start the main backend service
    #mysql,
    cnx,
    dec,
    enc,
    logsapp,
    app,
    startWithProxy,
    api_url,
    proxy,
    backendP,
    session,
    rps,
    playerscoords,
    whitelist,
    blacklist
)