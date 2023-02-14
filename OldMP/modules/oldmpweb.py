from flask import Flask, request, send_file, render_template
from .func import OldMPFunc as func
from json import dumps, loads
from os import listdir as oslistdir
from os import path as ospath

class OldMPWeb():
    def __init__(
        self,
        cnx,
        logsapp: bool=True,
        clients: list=[], 
        palyerscoords: list=[], 
        appweb: Flask=Flask("OldMPWeb"),
        port: int=80
    ):
        
        self.clients=clients
        self.appweb=appweb
        self.functions=func(request=request, app=appweb, clients=clients, cnx=cnx)
        self.NLogs=self.functions.logs

        self.NLogs(logsapp, "OmdMPWeb started!")
        
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

        @self.appweb.route('/status')
        def getstatus():
            resp=self.appweb.response_class(
                response=dumps({'status': 'online'}),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        @self.appweb.route('/favicon.ico')
        def favicon():
            return send_file('data/content/images/logo.ico', mimetype='image/ico')

        @self.appweb.route('/help', methods=['GET', 'POST'])
        def helppage():
            pass

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
                if '.png' in file:
                    return send_file(filename, mimetype='image/png')
                elif '.jpg' in file:
                    return send_file(filename, mimetype='image/jpg')
                elif '.ico' in file:
                    return send_file(filename, mimetype='image/ico')
                else:
                    return send_file(filename)
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
                listseason=oslistdir('data/content/season')
                [listdir.append(i) for i in listseason]
                for i in listdir:
                    if not '.' in i:
                        listdir.remove(i)
                listdir.remove('season')
                        
                resp=self.appweb.response_class(
                    response=dumps(listdir),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
            if 'season' in file:
                filename=f'data/content/season/{file}'
            else:
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
            
            presence=False
            for i in self.clients:
                if i['ip']==request.remote_addr:
                    presence=True

            if ospath.exists('data/content/images/ActMiniMapAthena.png'):
                mapFile='ActMiniMapAthena.png'
            else:
                mapFile='MiniMapAthena.png'

            resp=self.appweb.response_class(
                response=render_template('map.html', presence=presence, mapFile=mapFile),
                status=200,
                mimetype='text/html'
            )
            return resp
            # if ospath.exists('data/content/images/ActMiniMapAthena.png'):
            #     return send_file('data/content/images/ActMiniMapAthena.png', mimetype='image/png')
            
            # else:
            #     return send_file('data/content/images/MiniMapAthena.png', mimetype='image/png')
            
        @self.appweb.route('/map/setcoords', methods=['POST'])
        def mapsetcoords():
            if request.args.get('acceskey')=="zEnc087zzsO3oHKmVymVIDb51wn_FqqsTM1BxKRcm7g=":
                x: int=request.args.get('x')
                z: int=request.args.get('z')
                palyerscoords.append((x/1, z/1))
                
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
        
        self.appweb.run('0.0.0.0', port, debug=False)
