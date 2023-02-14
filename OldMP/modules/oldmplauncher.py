from flask import Flask, request, render_template, session
from flask_session import Session
from .func import OldMPFunc as func
from json import dumps
from uuid import uuid4
from requests import get

class OldMPLauncher():
    def __init__(
        self,
        enc,
        dec,
        cnx,
        logsapp: bool=True,
        applaunch: Flask=Flask("OldMPLauncher"),
        port: int=4971,
        clients: list=[],
        api_url: str='https://nocturno.games/api', 
        proxy: dict={
            'http': 'http://127.0.0.1:9999', 
            'https': 'http://127.0.0.1:9999',
        },
        startWithProxy: bool=False
    ):
        
        self.applaunch=applaunch
        Session(applaunch)
        self.functions=func(request=request, app=applaunch, clients=clients, cnx=cnx)
        self.NLogs=self.functions.logs
        self.api_url=api_url
        self.proxy=proxy

        self.NLogs(logsapp, "OmdMPLauncher started!")
        
        @self.applaunch.route("/", methods=['GET'])
        def baseroute():

            resp=self.applaunch.response_class(
                response="",
                status=200,
                mimetype='text/plain'
            )
            return resp
        
        @self.applaunch.route("/auth", methods=['GET'])
        def authsys():

            grant_type=request.args.get('grant_type')
            
            if grant_type=='password':
                
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
                
                if startWithProxy:
                    rg=get(f'{self.api_url}/get/check.php?user={username}&pass={password}', proxies=self.proxy)
                else:
                    rg=get(f'{self.api_url}/get/check.php?user={username}&pass={password}')
                    
                if not 'ok' in rg:
                    session['username']=username
                    session['password']=password
                    session['deviceId']=request.args.get('device_id')
                
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
                pass
            
            sessionId=uuid4().replace('-', '')
            
            r={
                'accountId': session['username'],
                'access_token': enc(f"sessionId:{sessionId}|deviceId:{session['deviceId']}|ip:{request.remote_addr}".encode()).decode(),
                'session_id': sessionId,
                'expire_in': 14400,
                'expire_at': self.functions.createDate(4),
                'display_name': session['username'],
                'device_id': session['deviceId']
            }

            resp=self.applaunch.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        
        
        self.applaunch.run('0.0.0.0', port, debug=False)
