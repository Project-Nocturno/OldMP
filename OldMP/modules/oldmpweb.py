from flask import Flask, request, send_file, render_template
from .func import OldMPFunc as func
from json import dumps, loads
from os import listdir as oslistdir
from os import path as ospath

class OldMPWeb():
    def __init__(self, 
            clients: list=[], 
            palyerscoords: list=[], 
            appweb: Flask=Flask("OldMPWeb")
        ):
        
        self.functions=func(request=request, app=self.appweb, clients=self.clients)
        self.clients=clients
        self.appweb=appweb
        
        @self.appweb.route("/", methods=['GET', 'POST'])
        def baseroute():
            
            presence=False
            for i in self.clients:
                if i['ip']==request.remote_addr:
                    presence=True

            resp=self.appweb.response_class(
                response=render_template('index.html', presence=presence),
                status=200,
                mimetype='text/html'
            )
            return resp

        @self.appweb.route('/content/images/<file>', methods=['GET', 'POST'])
        def getcontentimage(file):
            
            if file=='listall':
                listdir=oslistdir('data/content/images/')
                resp=self.appweb.response_class(
                    response=dumps(listdir),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
            filename=f'data/content/images/{file}'
            
            if ospath.exists(filename):
                return send_file(filename, mimetype='image/png')
            else:
                resp=self.appweb.response_class(
                    response=dumps({'error': "file doesn't exist"}),
                    status=400,
                    mimetype='application/json'
                )
                return resp
            
        @self.appweb.route('/content/files/<file>', methods=['GET', 'POST'])
        def getcontentfile(file):
            
            if file=='listall':
                listdir=oslistdir('data/content/')
                resp=self.appweb.response_class(
                    response=dumps(listdir),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
            filename=f'data/content/{file}'
            
            if ospath.exists(filename):
                return send_file(filename, mimetype='application/json')
            else:
                resp=self.appweb.response_class(
                    response=dumps({'error': "file doesn't exist"}),
                    status=400,
                    mimetype='application/json'
                )
                return resp

        @self.appweb.route('/friends/<accountId>', methods=['GET', 'POST'])
        def sendfriends(accountId):
            friendlist=loads(open(f'data/friends/{accountId}/friendslist.json', 'r', encoding='utf-8').read())
            friends=[]
            for i in friendlist:
                friends.append(i['accountId'])

            resp=self.appweb.response_class(
                response=dumps(friends),
                status=200,
                mimetype='application/json'
            )
            return resp

        @self.appweb.route('/map', methods=['GET', 'POST'])
        def spawnmap():
            if ospath.exists('data/content/images/ActMiniMapAthena.png'):
                return send_file('data/content/images/ActMiniMapAthena.png', mimetype='image/png')
            
            else:
                return send_file('data/content/images/MiniMapAthena.png', mimetype='image/png')
            
        @self.appweb.route('/map/setcoords', methods=['POST'])
        def mapsetcoords():
            if request.args.get('acceskey')=="zEnc087zzsO3oHKmVymVIDb51wn_FqqsTM1BxKRcm7g=":
                coords: str=request.stream.read()
                x: int=coords.split('|')[0]
                y: int=coords.split('|')[1]
                palyerscoords.append((x/1, y/1))
                
            else:
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_grants",
                    "Your acces key is incorrect",
                    [], 18031, "invalid_grant"
                )
                resp=self.appweb.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                return resp

        @self.appweb.route('/adminacc', methods=['GET'])
        def adminacc():
            if not request.args.get('passw') and request.args.get('user'):
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_admin_account_credentials",
                    "Your admin username and/or password are incorrect 1",
                    [], 18031, "invalid_grant"
                )
                resp=self.appweb.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                return resp
            if request.args.get('user')=='rootuser':
                if request.args.get('passw')=='TheSecureR00tUserPassITh1Nk':
                    pass
                
                else:
                    respon=self.functions.createError(
                        "errors.com.epicgames.account.invalid_admin_account_credentials",
                        "Your admin username and/or password are incorrect",
                        [], 18031, "invalid_grant"
                    )
                    resp=self.appweb.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
            else:
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_admin_account_credentials",
                    "Your admin username and/or password are incorrect 2",
                    [], 18031, "invalid_grant"
                )
                resp=self.appweb.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                return resp
            
            resp=self.appweb.response_class(
                response=dumps(self.clients),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        self.appweb.run('0.0.0.0', 80, debug=False)
