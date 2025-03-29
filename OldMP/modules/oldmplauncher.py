from flask import Flask, request, send_file, send_from_directory, abort
from .func import OldMPFunc as func
from json import dumps, loads
from uuid import uuid4
from hashlib import sha256
import urllib.parse
import logging
from functools import lru_cache
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
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='oldmplauncher.log'
        )
        self.logger = logging.getLogger('OldMPLauncher')
        
        # Initialize class properties
        self.applaunch = applaunch
        self.functions = func(request=request, app=applaunch, cnx=cnx, whitelist=whitelist, blacklist=blacklist)
        self.NLogs = self.functions.logs
        self.proxy = proxy
        self.session = sessions(session=sessionL, req=request)
        
        # Cache for config data
        self.config_cache = {}
        
        self.NLogs(logsapp, "OldMPLauncher started!")
        
        # Register routes and start server
        self._register_error_handlers(applaunch)
        self._register_routes()
        
        # Start the Flask app with threading for better performance
        self.applaunch.run('0.0.0.0', port, debug=False, threaded=True)
    
    def _register_error_handlers(self, app):
        """Register error handlers for the Flask app"""
        
        @app.before_request
        def checkrps():
            # Initialize blacklist entry if not exists
            if request.remote_addr not in self.functions.blacklist:
                self.functions.blacklist[request.remote_addr] = 0
            elif self.functions.blacklist[request.remote_addr] >= 8:
                abort(403)
                
            # Check and update request rate limiting
            if request.remote_addr in self.functions.rps:
                config = self._get_config()
                if self.functions.rps[request.remote_addr] >= config['rps']['launcher']:
                    abort(403)
                self.functions.rps[request.remote_addr] += 1
            else:
                self.functions.rps[request.remote_addr] = 0
        
        @app.errorhandler(404)
        def error404(e):
            self.functions.addLog(request, 404, "oldmplaunch")
            return app.response_class(
                response=dumps({
                    'error': {
                        'code': 404, 
                        'content': f'Bad request: {request.url}'
                    }
                }),
                status=404,
                mimetype='application/json'
            )

        @app.errorhandler(401)
        def error401(e):
            self.functions.addLog(request, 401, "oldmplaunch")
            return app.response_class(
                response=dumps({
                    'error': {
                        'code': 401, 
                        'content': "Nope sorry this isn't for you..."
                    }
                }),
                status=401,
                mimetype='application/json'
            )

        @app.errorhandler(403)
        def error403(e):
            self.functions.addLog(request, 403, "oldmplaunch")
            return app.response_class(
                response=dumps({
                    'error': {
                        'code': 403, 
                        'content': "You are permanently or temporarily banned"
                    }
                }),
                status=403,
                mimetype='application/json'
            )
                
        @app.errorhandler(405)
        def error405(e):
            return app.response_class(
                response=dumps({
                    'error': {
                        'code': 405, 
                        'content': f'Method {request.method} does not work'
                    }
                }),
                status=405,
                mimetype='application/json'
            )

        @app.errorhandler(500)
        def error500(e):
            self.functions.addLog(request, 500, "oldmplaunch")
            return app.response_class(
                response=dumps({
                    'error': {
                        'code': 500, 
                        'content': 'The server encountered an error'
                    }
                }),
                status=500,
                mimetype='application/json'
            )
    
    @lru_cache(maxsize=1)
    def _get_config(self):
        """Get configuration with caching to improve performance"""
        try:
            if not self.config_cache:
                self.config_cache = loads(open('conf.json', 'r', encoding='utf-8').read())
            return self.config_cache
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {"rps": {"launcher": 10}, "Content": {"LauncherMsg": {}}, "Status": {}}
    
    def _register_routes(self):
        """Register all routes for the launcher"""
        
        @self.applaunch.route('/favicon.ico')
        def favicon():
            return send_file('data/content/images/logo.ico', mimetype='image/ico')
        
        @self.applaunch.route("/", methods=['GET'])
        def baseroute():
            return self.applaunch.response_class(
                response="",
                status=200,
                mimetype='text/plain'
            )
        
        @self.applaunch.route("/launcher/versioncheck", methods=['GET'])
        def versioncheck():
            config = self._get_config()
            version = config['Content']['LauncherMsg'].get('version', '')
            return self.applaunch.response_class(
                response=version,
                status=200,
                mimetype='text/plain'
            )
        
        @self.applaunch.route("/launcher/status", methods=['GET'])
        def getstatusw():
            config = self._get_config()
            status = config['Status'].get('launcher', '')
            return self.applaunch.response_class(
                response=status,
                status=200,
                mimetype='text/plain'
            )

        @self.applaunch.route("/launcher/<user>/grade", methods=['GET'])
        def getgradeuser(user):
            try:
                grade = self.functions.req(f"SELECT grade FROM users WHERE username='{user}'")[0][0]
                return self.applaunch.response_class(
                    response=grade,
                    status=200,
                    mimetype='text/plain'
                )
            except Exception as e:
                self.logger.error(f"Error getting user grade: {e}")
                return self.applaunch.response_class(
                    response="Error",
                    status=500,
                    mimetype='text/plain'
                )
        
        @self.applaunch.route("/launcher/content/news", methods=['GET'])
        def getnews():
            config = self._get_config()
            news = config['Content']['LauncherMsg'].get('news', '')
            return self.applaunch.response_class(
                response=news,
                status=200,
                mimetype='text/plain'
            )
        
        @self.applaunch.route("/launcher/content/patchnotes", methods=['GET'])
        def getpatch():
            config = self._get_config()
            patch = config['Content']['LauncherMsg'].get('patchnotes', '')
            return self.applaunch.response_class(
                response=patch,
                status=200,
                mimetype='text/plain'
            )
        
        @self.applaunch.route("/launcher/content/fnsolo", methods=['GET'])
        def getfnsolo():
            config = self._get_config()
            solo = config['Content']['LauncherMsg'].get('fnsolo', '')
            return self.applaunch.response_class(
                response=solo,
                status=200,
                mimetype='text/plain'
            )
        
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
            grant_type = request.args.get('grant_type')
            username = request.args.get('username')
            password = request.args.get('password')
            
            # Handle password grant type
            if grant_type == 'password':
                if not username or not password:
                    error = self.functions.createError(
                        "errors.com.epicgames.common.oauth.invalid_request",
                        "Username/password is required.", 
                        [], 1013, "invalid_request"
                    )
                    return self.applaunch.response_class(
                        response=dumps(error),
                        status=400,
                        mimetype='application/json'
                    )
                
                try:
                    passwd = self.functions.req(f"SELECT password FROM users WHERE username='{username}'")
                    passw = sha256(urllib.parse.unquote(password).encode()).hexdigest().encode()
                    
                    if passwd and passwd[0][0] == passw:
                        self.session.put('username', username)
                        self.session.put('password', password)
                        self.session.put('deviceId', str(uuid4()).replace("-", ""))
                        self.session.put('sessionId', str(uuid4()).replace("-", ""))
                        self.session.put('launcher', True)
                    else:
                        error = self.functions.createError(
                            "errors.com.epicgames.account.invalid_account_credentials",
                            "Your username and/or password are incorrect. Please verify your account on our website: https://www.nocturno.games/", 
                            [], 18031, "invalid_grant"
                        )
                        return self.applaunch.response_class(
                            response=dumps(error),
                            status=400,
                            mimetype='application/json'
                        )
                except Exception as e:
                    self.logger.error(f"Authentication error: {e}")
                    error = self.functions.createError(
                        "errors.com.epicgames.common.server_error",
                        "An error occurred during authentication", 
                        [], 1000, "server_error"
                    )
                    return self.applaunch.response_class(
                        response=dumps(error),
                        status=500,
                        mimetype='application/json'
                    )
            
            # Handle refresh grant type
            elif grant_type == 'refresh':
                username = request.args.get('username')
                password = request.args.get('password')
                
                if not username or not password:
                    error = self.functions.createError(
                        "errors.com.epicgames.common.oauth.invalid_request",
                        "Username/password is required.", 
                        [], 1013, "invalid_request"
                    )
                    return self.applaunch.response_class(
                        response=dumps(error),
                        status=400,
                        mimetype='application/json'
                    )
                
                password_hash = sha256(urllib.parse.unquote(password).encode()).hexdigest().encode()
                
                if username != self.session.get('username') or password_hash != self.session.get('password'):
                    error = self.functions.createError(
                        "errors.com.epicgames.account.invalid_account_credentials",
                        "Your username and/or password are incorrect. Please verify your account on our website: https://www.nocturno.games/", 
                        [], 18031, "invalid_grant"
                    )
                    return self.applaunch.response_class(
                        response=dumps(error),
                        status=400,
                        mimetype='application/json'
                    )
            
            # Return successful authentication response
            response = {
                'accountId': self.session.get('username'),
                'display_name': self.session.get('username'),
                'device_id': self.session.get('deviceId'),
                'session_id': self.session.get('sessionId'),
                'expire_in': 14400,
                'expire_at': self.functions.createDate(4)
            }

            return self.applaunch.response_class(
                response=dumps(response),
                status=200,
                mimetype='application/json'
            )
        
        @self.applaunch.route("/launcher/rpc/", methods=['GET'])
        def rpc():
            response = {
                'username': self.session.get('username'),
                'character': self.session.get('character'),
                'party': {
                    'mapName': self.session.get('mapName') if self.session.get('InGame') else 'Lobby',
                    'playerLeft': self.session.get('partyPlayerLeft') if self.session.get('InGame') else 0
                }
            }
            
            return self.applaunch.response_class(
                response=dumps(response),
                status=200,
                mimetype='application/json'
            )
        
        
        self.applaunch.run('0.0.0.0', port, debug=False)
