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
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='oldmpweb.log'
        )
        self.logger = logging.getLogger('OldMPWeb')
        
        # Initialize class properties
        self.appweb = appweb
        self.functions = func(request=request, app=appweb, cnx=cnx, whitelist=whitelist, blacklist=blacklist)
        self.NLogs = self.functions.logs
        self.session = sessions(session=sessionL, req=request)
        self.playerscoords = playerscoords
        
        # Cache for config and content
        self.config_cache = {}
        self.content_cache = {}
        
        self.NLogs(logsapp, "OldMPWeb started!")
        
        # Register routes and start server
        self._register_error_handlers(appweb)
        self._register_routes()
        
        # Start the Flask app with threading for better performance
        self.appweb.run('0.0.0.0', port, debug=False, threaded=True)
    
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
                if self.functions.rps[request.remote_addr] >= config['rps']['website']:
                    abort(403)
                self.functions.rps[request.remote_addr] += 1
            else:
                self.functions.rps[request.remote_addr] = 0
        
        @app.errorhandler(404)
        def error404(e):
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
            return {"rps": {"website": 10}, "Status": {}}
    
    def _register_routes(self):
        """Register all routes for the web interface"""
        
        @self.appweb.route('/favicon.ico')
        def favicon():
            return send_file('data/content/images/logo.ico', mimetype='image/ico')
        
        @self.appweb.route("/", methods=['GET', 'POST'])
        def baseroute():
            presence = self.session.exist()
            return self.appweb.response_class(
                response=render_template('index.html', presence=presence),
                status=200,
                mimetype='text/html'
            )

        @self.appweb.route('/players')
        def getplayers():
            return self.appweb.response_class(
                response=dumps({'players': self.session.len()}),
                status=200,
                mimetype='application/json'
            )
        
        @self.appweb.route('/status')
        def getstatus():
            config = self._get_config()
            status = config['Status'].get('website', '')
            return self.appweb.response_class(
                response=dumps({'status': status}),
                status=200,
                mimetype='application/json'
            )

        @self.appweb.route('/logs')
        def getlogs():
            urlkey = request.args.get('urlkey')
            
            if not urlkey or urlkey != 'DE1NOCTURNOBZCOSMOSETDE2NOCTURNOISBETTER':
                error = self.functions.createError(
                    "errors.com.epicgames.account.invalid_key",
                    "Your admin urlkey is incorrect",
                    [], 18031, "invalid_grant"
                )
                return self.appweb.response_class(
                    response=dumps(error),
                    status=400,
                    mimetype='application/json'
                )
            
            try:
                logs = loads(open('logs.json', 'r', encoding='utf-8').read())
                return self.appweb.response_class(
                    response=dumps({'logs': logs}, indent=4),
                    status=200,
                    mimetype='application/json'
                )
            except Exception as e:
                self.logger.error(f"Error loading logs: {e}")
                return self.appweb.response_class(
                    response=dumps({'error': 'Failed to load logs'}),
                    status=500,
                    mimetype='application/json'
                )
            
        @self.appweb.route('/blacklist')
        def getbl():
            urlkey = request.args.get('urlkey')
            
            if not urlkey or urlkey != 'DE1NOCTURNOBZCOSMOSETDE2NOCTURNOISBETTERETDE3ONBZCOSMOS':
                error = self.functions.createError(
                    "errors.com.epicgames.account.invalid_key",
                    "Your admin urlkey is incorrect",
                    [], 18031, "invalid_grant"
                )
                return self.appweb.response_class(
                    response=dumps(error),
                    status=400,
                    mimetype='application/json'
                )
            
            return self.appweb.response_class(
                response=dumps({'blacklist': self.functions.blacklist}, indent=4),
                status=200,
                mimetype='application/json'
            )
        
        @self.appweb.route('/help', methods=['GET', 'POST'])
        def helppage():
            return '', 200

        @self.appweb.route('/content/images/<file>', methods=['GET', 'POST'])
        def getcontentimage(file):
            if file == 'listall':
                try:
                    listdir = oslistdir('data/content/images/')
                    return self.appweb.response_class(
                        response=dumps(listdir),
                        status=200,
                        mimetype='application/json'
                    )
                except Exception as e:
                    self.logger.error(f"Error listing images: {e}")
                    return self.appweb.response_class(
                        response=dumps({'error': 'Failed to list images'}),
                        status=500,
                        mimetype='application/json'
                    )
            
            filename = f'data/content/images/{file}'
            
            if ospath.exists(filename):
                # Determine mimetype based on file extension
                if file.endswith('.png'):
                    mimetype = 'image/png'
                elif file.endswith('.jpg') or file.endswith('.jpeg'):
                    mimetype = 'image/jpeg'
                elif file.endswith('.ico'):
                    mimetype = 'image/x-icon'
                else:
                    mimetype = None
                
                return send_file(filename, mimetype=mimetype)
            else:
                return self.appweb.response_class(
                    response=dumps({'error': "file doesn't exist"}),
                    status=404,
                    mimetype='application/json'
                )
            
        @self.appweb.route('/content/files/<file>', methods=['GET', 'POST'])
        def getcontentfile(file):
            if file == 'listall':
                try:
                    # Get all files from content directory
                    content_files = [f for f in oslistdir('data/content/') if '.' in f and f != 'season']
                    
                    # Get all files from season directory
                    try:
                        season_files = oslistdir('data/content/season')
                    except:
                        season_files = []
                    
                    # Combine the lists
                    all_files = content_files + season_files
                    
                    return self.appweb.response_class(
                        response=dumps(all_files),
                        status=200,
                        mimetype='application/json'
                    )
                except Exception as e:
                    self.logger.error(f"Error listing content files: {e}")
                    return self.appweb.response_class(
                        response=dumps({'error': 'Failed to list content files'}),
                        status=500,
                        mimetype='application/json'
                    )
            
            # Determine the file path
            if 'season' in file:
                filename = f'data/content/season/{file}'
            else:
                filename = f'data/content/{file}'
            
            if ospath.exists(filename):
                return send_file(filename, mimetype='application/json')
            else:
                return self.appweb.response_class(
                    response=dumps({'error': "file doesn't exist"}),
                    status=404,
                    mimetype='application/json'
                )

        @self.appweb.route('/friends/<accountId>', methods=['GET', 'POST'])
        def sendfriends(accountId):
            try:
                friendlist = loads(open(f'data/friends/{accountId}/friendslist.json', 'r', encoding='utf-8').read())
                friends = [i['accountId'] for i in friendlist]
                
                return self.appweb.response_class(
                    response=dumps(friends),
                    status=200,
                    mimetype='application/json'
                )
            except Exception as e:
                self.logger.error(f"Error getting friends for {accountId}: {e}")
                return self.appweb.response_class(
                    response=dumps({'error': 'Failed to get friends list'}),
                    status=500,
                    mimetype='application/json'
                )

        @self.appweb.route('/adminacc', methods=['GET'])
        def adminacc():
            user = request.args.get('user')
            passw = request.args.get('passw')
            
            if not user or not passw:
                error = self.functions.createError(
                    "errors.com.epicgames.account.invalid_admin_account_credentials",
                    "Your admin username and/or password are incorrect",
                    [], 18031, "invalid_grant"
                )
                return self.appweb.response_class(
                    response=dumps(error),
                    status=400,
                    mimetype='application/json'
                )
            
            if user != 'rootuser' or passw != 'TheSecureR00tUserPassITh1Nk':
                error = self.functions.createError(
                    "errors.com.epicgames.account.invalid_admin_account_credentials",
                    "Your admin username and/or password are incorrect",
                    [], 18031, "invalid_grant"
                )
                return self.appweb.response_class(
                    response=dumps(error),
                    status=400,
                    mimetype='application/json'
                )
            
            # Return session information for admin
            return self.appweb.response_class(
                response=dumps({
                    'players': self.session.len(),
                    'clients': self.session.session
                }, indent=4),
                status=200,
                mimetype='application/json'
            )
