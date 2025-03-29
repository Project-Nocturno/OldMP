from flask import request
from json import loads, dumps
from os import path as ospath
from datetime import datetime

def register_generic_profile_handler(app, oldmp):
    @app.route('/fortnite/api/game/v2/profile/<account>/client/<operation>', methods=['POST', 'GET'])
    def generic_profile_handler(account, operation):
        # This handler will catch any profile operations that don't have specific handlers
        
        if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
            r = {
                "profileRevision": 0,
                "profileId": request.args.get("profileId"),
                "profileChangesBaseRevision": 0,
                "profileChanges": [],
                "profileCommandRevision": 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }

            resp = app.response_class(
                    response=dumps(r),
                    status=200,
                    mimetype='application/json'
                )
            return resp
        
        profile = loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[oldmp.session.get('username')].copy()

        ApplyProfileChanges = []
        BaseRevision = profile['rvn'] or 0
        QueryRevision = request.args.get('rvn') or -1
        
        if QueryRevision != BaseRevision:
            ApplyProfileChanges = [{
                "changeType": "fullProfileUpdate",
                "profile": profile
            }]
        
        r = {
            "profileRevision": profile['rvn'] or 0,
            "profileId": request.args.get("profileId") or "athena",
            "profileChangesBaseRevision": BaseRevision,
            "profileChanges": ApplyProfileChanges,
            "profileCommandRevision": profile['commandRevision'] or 0,
            "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "responseVersion": 1
        }
        
        resp = app.response_class(
            response=dumps(r),
            status=200,
            mimetype='application/json'
        )
        return resp