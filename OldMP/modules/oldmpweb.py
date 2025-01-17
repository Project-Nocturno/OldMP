from flask import Flask, request, send_file, render_template, abort
from .func import OldMPFunc as func
from json import dumps, loads
from os import listdir as oslistdir
from os import path as ospath

from modules.session import Session as sessions

class OldMPWeb():
    def __init__(
        self,
        cnx,
        logsapp: bool=True,
        playerscoords: list=[], 
        appweb: Flask=Flask("OldMPWeb"),
        port: int=80,
        rps: dict={},
        sessionL: dict={},
        whitelist: list=[],
        blacklist: dict={}
    ):
        
        self.appweb=appweb
        self.functions=func(request=request, app=appweb, cnx=cnx, whitelist=whitelist, blacklist=blacklist)
        self.NLogs=self.functions.logs
        self.session=sessions(session=sessionL, req=request)

        self.NLogs(logsapp, "OmdMPWeb started!")
        
        @self.appweb.before_request
        def checkrps():
            if not self.functions.find(blacklist, request.remote_addr):
                blacklist.update({request.remote_addr: 0})
            else:
                if blacklist[request.remote_addr]>=8:
                    abort(403)
            exist=False
            for i in rps:
                if i==request.remote_addr:
                    exist=True
            if exist:
                if rps[request.remote_addr]>=loads(open('conf.json', 'r', encoding='utf-8').read())['rps']['website']:
                    abort(403)
                else:
                    rps[request.remote_addr]+=1
            else:
                rps.update({request.remote_addr: 0})
        
        @self.appweb.errorhandler(404)
        def error404(e):
            resp=self.appweb.response_class(
                response=dumps({
                    'error': {
                        'code': 404, 
                        'content': f'Bad request: {request.url}'
                    }
                }),
                status=404,
                mimetype='application/json'
            )
            return resp

        @self.appweb.errorhandler(401)
        def error401(e):
            resp=self.appweb.response_class(
                response=dumps({
                    'error': {
                        'code': 401, 
                        'content': "Nope sorry this isn't for you..."
                    }
                }),
                status=401,
                mimetype='application/json'
            )
            return resp

        @self.appweb.errorhandler(403)
        def error403(e):
            resp=self.appweb.response_class(
                response=dumps({
                    'error': {
                        'code': 403, 
                        'content': "You are permanently or temporarily banned"
                    }
                }),
                status=403,
                mimetype='application/json'
            )
            return resp
                
        @self.appweb.errorhandler(405)
        def error405(e):
            resp=self.appweb.response_class(
                response=dumps({
                    'error': {
                        'code': 405, 
                        'content': f'Method {request.method} does not work'
                    }
                }),
                status=405,
                mimetype='application/json'
            )
            return resp

        @self.appweb.errorhandler(500)
        def error500(e):
            resp=self.appweb.response_class(
                response=dumps({
                    'error': {
                        'code': 500, 
                        'content': 'The server encountered an error'
                    }
                }),
                status=500,
                mimetype='application/json'
            )
            return resp

        @self.appweb.route('/favicon.ico')
        def favicon():
            return send_file('data/content/images/logo.ico', mimetype='image/ico')



        @self.appweb.route("/", methods=['GET', 'POST'])
        def baseroute():
            
            presence=self.session.exist()

            resp=self.appweb.response_class(
                response=render_template('index.html', presence=presence),
                status=200,
                mimetype='text/html'
            )
            return resp

        @self.appweb.route('/players')
        def getplayers():
            resp=self.appweb.response_class(
                response=dumps({'players': self.session.len()}),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        @self.appweb.route('/status')
        def getstatus():
            
            status=loads(open('conf.json', 'r', encoding='utf-8').read())['Status']['website']
            
            resp=self.appweb.response_class(
                response=dumps({'status': status}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @self.appweb.route('/logs')
        def getlogs():
            
            if not request.args.get('urlkey'):
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_key",
                    "Your admin urlkey is incorrect",
                    [], 18031, "invalid_grant"
                )
                resp=self.appweb.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
            if request.args.get('urlkey')!='DE1NOCTURNOBZCOSMOSETDE2NOCTURNOISBETTER':
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_key",
                    "Your admin urlkey is incorrect",
                    [], 18031, "invalid_grant"
                )
                resp=self.appweb.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                
            else:
                logs=loads(open('logs.json', 'r', encoding='utf-8').read())
                
                resp=self.appweb.response_class(
                    response=dumps({'logs': logs}, indent=4),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
        @self.appweb.route('/blacklist')
        def getbl():
            
            if not request.args.get('urlkey'):
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_key",
                    "Your admin urlkey is incorrect",
                    [], 18031, "invalid_grant"
                )
                resp=self.appweb.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
            if request.args.get('urlkey')!='DE1NOCTURNOBZCOSMOSETDE2NOCTURNOISBETTERETDE3ONBZCOSMOS':
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_key",
                    "Your admin urlkey is incorrect",
                    [], 18031, "invalid_grant"
                )
                resp=self.appweb.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
            else:

                logs=loads(open('logs.json', 'r', encoding='utf-8').read())
                
                resp=self.appweb.response_class(
                    response=dumps({'blacklist': blacklist}, indent=4),
                    status=200,
                    mimetype='application/json'
                )
                return resp
        
        @self.appweb.route('/help', methods=['GET', 'POST'])
        def helppage():
            return '', 200

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

        #@self.appweb.route('/map', methods=['GET', 'POST'])
        def spawnmap():
            
            presence=self.session.exist()

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
                response=dumps({
                    'players': self.session.len(),
                    'clients': sessionL
                }, indent=4),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        self.appweb.run('0.0.0.0', port, debug=False)
