from flask import Flask, request, send_file
from .func import OldMPFunc as func
from json import dumps, loads
from requests import get
from uuid import uuid4

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
        rps: dict={}
    ):
        
        self.version='0.1'
        self.applaunch=applaunch
        self.functions=func(request=request, app=applaunch, cnx=cnx)
        self.NLogs=self.functions.logs
        self.api_url=api_url
        self.proxy=proxy
        self.NLogs(logsapp, "OmdMPLauncher started!")
        
        @applaunch.before_request
        def checkrps():
            exist=False
            for i in rps:
                if i==request.remote_addr:
                    exist=True
            if exist:
                if rps[request.remote_addr]>=5:
                    respon=self.functions.createError(
                        "errors.com.epicgames.account.too_many_requests",
                        "You have made more than the limited number of requests", 
                        [], 18031, "too_many_requests"
                    )
                    resp=applaunch.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
                else:
                    rps[request.remote_addr]+=1
            else:
                rps.update({request.remote_addr: 0})
        
        @self.applaunch.route("/", methods=['GET'])
        def baseroute():

            resp=self.applaunch.response_class(
                response="",
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route('/favicon.ico')
        def favicon():
            return send_file('data/content/images/logo.ico', mimetype='image/ico')
        
        @self.applaunch.route("/versioncheck", methods=['GET'])
        def versioncheck():

            resp=self.applaunch.response_class(
                response=self.version,
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/status", methods=['GET'])
        def getstatusw():

            status=loads(open('conf.json', 'r', encoding='utf-8').read())['Status']['launcher']

            resp=self.applaunch.response_class(
                response=status,
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/auth", methods=['GET'])
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
                
                if startWithProxy:
                    rg=get(f'{self.api_url}/get/check.php?user={username}&pass={password}', proxies=self.proxy)
                else:
                    rg=get(f'{self.api_url}/get/check.php?user={username}&pass={password}')
                    
                if not 'ok' in rg:
                    sessions(sessionL, request.remote_addr).put('username', username)
                    sessions(sessionL, request.remote_addr).put('password', password)
                    sessions(sessionL, request.remote_addr).put('deviceId', str(uuid4()).replace("-", ""))
                    sessions(sessionL, request.remote_addr).put('sessionId', str(uuid4()).replace("-", ""))
                    sessions(sessionL, request.remote_addr).put('launcher', True)
                
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
                
                if not username==sessions(sessionL, request.remote_addr).get('username') and password==sessions(sessionL, request.remote_addr).get('password'):
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
                'accountId': sessions(sessionL, request.remote_addr).get('username'),
                'display_name': sessions(sessionL, request.remote_addr).get('username'),
                'device_id': sessions(sessionL, request.remote_addr).get('deviceId'),
                'session_id': sessions(sessionL, request.remote_addr).get('sessionId'),
                'expire_in': 14400,
                'expire_at': self.functions.createDate(4)
            }

            resp=self.applaunch.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        @self.applaunch.route("/rpc/", methods=['GET'])
        def rpc():
            if sessions(sessionL, request.remote_addr).get('InGame')==True:
                r={
                    'username': sessions(sessionL, request.remote_addr).get('username'),
                    'character': sessions(sessionL, request.remote_addr).get('character'),
                    'party': {
                        'mapName': sessions(sessionL, request.remote_addr).get('mapName'),
                        'playerLeft': sessions(sessionL, request.remote_addr).get('partyPlayerLeft')
                    }
                }
                
            else:
                r={
                    'username': sessions(sessionL, request.remote_addr).get('username'),
                    'character': sessions(sessionL, request.remote_addr).get('character'),
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
