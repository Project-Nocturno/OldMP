from flask import Flask, request, send_file, send_from_directory, abort
from .func import OldMPFunc as func
from json import dumps, loads
from uuid import uuid4
from hashlib import sha256, sha512
import urllib.parse

from modules.session import Session as sessions

class OldMPLauncher():
    def __init__(
        self,
        enc,
        dec,
        cnx,
        logsapp: bool=True,
        applaunch: Flask=Flask("OldMPLauncher"),
        port: int=4971,
        api_url: str='https://nocturno.games/api', 
        proxy: dict={
            'http': 'http://127.0.0.1:9999', 
            'https': 'http://127.0.0.1:9999',
        },
        startWithProxy: bool=False,
        sessionL: dict={},
        rps: dict={},
        whitelist: list=[],
        blacklist: dict={}
    ):
        
        self.applaunch=applaunch
        self.functions=func(request=request, app=applaunch, cnx=cnx, whitelist=whitelist, blacklist=blacklist)
        self.NLogs=self.functions.logs
        self.proxy=proxy
        self.NLogs(logsapp, "OmdMPLauncher started!")
        self.session=sessions(session=sessionL, req=request)
        
        @applaunch.before_request
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
                if rps[request.remote_addr]>=loads(open('conf.json', 'r', encoding='utf-8').read())['rps']['launcher']:
                    abort(403)
                else:
                    rps[request.remote_addr]+=1
            else:
                rps.update({request.remote_addr: 0})
        
        @applaunch.errorhandler(404)
        def error404(e):
            self.functions.addLog(request, 404, "oldmplaunch")
            resp=applaunch.response_class(
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

        @applaunch.errorhandler(401)
        def error401(e):
            self.functions.addLog(request, 401, "oldmplaunch")
            resp=applaunch.response_class(
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

        @applaunch.errorhandler(403)
        def error403(e):
            self.functions.addLog(request, 403, "oldmplaunch")
            resp=applaunch.response_class(
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
                
        @applaunch.errorhandler(405)
        def error405(e):
            resp=applaunch.response_class(
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

        @applaunch.errorhandler(500)
        def error500(e):
            self.functions.addLog(request, 500, "oldmplaunch")
            resp=applaunch.response_class(
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

        @self.applaunch.route('/favicon.ico')
        def favicon():
            return send_file('data/content/images/logo.ico', mimetype='image/ico')
        


        @self.applaunch.route("/", methods=['GET'])
        def baseroute():

            resp=self.applaunch.response_class(
                response="",
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/launcher/versioncheck", methods=['GET'])
        def versioncheck():

            version=loads(open('conf.json', 'r', encoding='utf-8').read())['Content']['LauncherMsg']['version']

            resp=self.applaunch.response_class(
                response=version,
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/launcher/status", methods=['GET'])
        def getstatusw():

            status=loads(open('conf.json', 'r', encoding='utf-8').read())['Status']['launcher']

            resp=self.applaunch.response_class(
                response=status,
                status=200,
                mimetype='text/plain'
            )
            return resp

        @self.applaunch.route("/launcher/<user>/grade", methods=['GET'])
        def getgradeuser(user):

            grade=self.functions.req(f"SELECT grade FROM users WHERE username='{user}'")[0][0]
            print(grade)

            resp=self.applaunch.response_class(
                response=grade,
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/launcher/content/news", methods=['GET'])
        def getnews():

            news=loads(open('conf.json', 'r', encoding='utf-8').read())['Content']['LauncherMsg']['news']

            resp=self.applaunch.response_class(
                response=news,
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/launcher/content/patchnotes", methods=['GET'])
        def getpatch():

            patch=loads(open('conf.json', 'r', encoding='utf-8').read())['Content']['LauncherMsg']['patchnotes']

            resp=self.applaunch.response_class(
                response=patch,
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/launcher/content/fnsolo", methods=['GET'])
        def getfnsolo():

            solo=loads(open('conf.json', 'r', encoding='utf-8').read())['Content']['LauncherMsg']['fnsolo']

            resp=self.applaunch.response_class(
                response=solo,
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/launcher/dll/client/download", methods=['GET'])
        def sendclient():

            return send_from_directory('data/files/', 'client.dll')
        
        @self.applaunch.route("/launcher/patchunk/stats/download/pak", methods=['GET'])
        def packstatsdownloadpak():

            return send_from_directory('data/files/pack/stats/', 'patchunkStats-WindowsClient.pak')
        
        @self.applaunch.route("/launcher/patchunk/stats/download/sig", methods=['GET'])
        def packstatsdownloadsig():

            return send_from_directory('data/files/pack/stats/', 'patchunkStats-WindowsClient.sig')
        
        @self.applaunch.route("/launcher/auth", methods=['GET'])
        def authsys():

            grant_type=request.args.get('grant_type')
            username=request.args.get('username')
            password=request.args.get('password')
            
            if grant_type=='password':
                
                if not username or not password:
                    respon=self.functions.createError(
                        "errors.com.epicgames.common.oauth.invalid_request",
                        "Username/password is required.", 
                        [], 1013, "invalid_request"
                    )
                    resp=applaunch.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
                
                passwd=self.functions.req(f"SELECT password FROM users WHERE username='{username}'")
                passw=sha256(urllib.parse.unquote(password).encode()).hexdigest().encode()
                
                if passwd[0][0]==passw:
                    self.session.put('username', username)
                    self.session.put('password', password)
                    self.session.put('deviceId', str(uuid4()).replace("-", ""))
                    self.session.put('sessionId', str(uuid4()).replace("-", ""))
                    self.session.put('launcher', True)
                
                else:
                    respon=self.functions.createError(
                        "errors.com.epicgames.account.invalid_account_credentials",
                        "Your username and/or password are incorrect. Please verify your account on our website: https://www.nocturno.games/", 
                        [], 18031, "invalid_grant"
                    )
                    resp=applaunch.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
            
            elif grant_type=='refresh':
                username=request.args.get('username')
                password=request.args.get('password')
                password=sha256(urllib.parse.unquote(password).encode()).hexdigest().encode()
                
                if not username or not password:
                    respon=self.functions.createError(
                        "errors.com.epicgames.common.oauth.invalid_request",
                        "Username/password is required.", 
                        [], 1013, "invalid_request"
                    )
                    resp=applaunch.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
                
                if not username==self.session.get('username') and password==self.session.get('password'):
                    respon=self.functions.createError(
                        "errors.com.epicgames.account.invalid_account_credentials",
                        "Your username and/or password are incorrect. Please verify your account on our website: https://www.nocturno.games/", 
                        [], 18031, "invalid_grant"
                    )
                    resp=applaunch.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
            
            r={
                'accountId': self.session.get('username'),
                'display_name': self.session.get('username'),
                'device_id': self.session.get('deviceId'),
                'session_id': self.session.get('sessionId'),
                'expire_in': 14400,
                'expire_at': self.functions.createDate(4)
            }

            resp=self.applaunch.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        @self.applaunch.route("/launcher/rpc/", methods=['GET'])
        def rpc():
            if self.session.get('InGame')==True:
                r={
                    'username': self.session.get('username'),
                    'character': self.session.get('character'),
                    'party': {
                        'mapName': self.session.get('mapName'),
                        'playerLeft': self.session.get('partyPlayerLeft')
                    }
                }
                
            else:
                r={
                    'username': self.session.get('username'),
                    'character': self.session.get('character'),
                    'party': {
                        'mapName': 'Lobby',
                        'playerLeft': 0
                    }
                }
            
            resp=self.applaunch.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        
        self.applaunch.run('0.0.0.0', port, debug=False)
