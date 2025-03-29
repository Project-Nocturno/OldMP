from flask import request
from json import dumps

def register_error_handlers(app):
    @app.errorhandler(404)
    def error404(e):
        resp = app.response_class(
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

    @app.errorhandler(401)
    def error401(e):
        resp = app.response_class(
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

    @app.errorhandler(403)
    def error403(e):
        resp = app.response_class(
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
            
    @app.errorhandler(405)
    def error405(e):
        resp = app.response_class(
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

    @app.errorhandler(500)
    def error500(e):
        resp = app.response_class(
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