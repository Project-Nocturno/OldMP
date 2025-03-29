from flask import request, Response
from json import loads, dumps
from os import path as ospath
from datetime import datetime

def register_profile_routes(app, oldmp):
    @app.route('/fortnite/api/game/v2/profile/<account>/client/QueryProfile', methods=['POST'])
    def fortnitegameapiclientall(account):
        if request.args.get("profileId") in ['athena', 'profile0', 'common_core', 'common_public']:
            print('pass')
            pass
        else:
            profile = {
                "_id": oldmp.session.get('username'),
                "created": "0001-01-01T00:00:00.000Z",
                "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "rvn": 0,
                "wipeNumber": 1,
                "accountId": oldmp.session.get('username'),
                "profileId": request.args.get('profileId'),
                "version": "no_version",
                "items": {},
                "stats": {
                    "attributes": {}
                },
                "commandRevision": 0
            }
            
            ApplyProfileChanges = []
            BaseRevision = 0
            QueryRevision = request.args.get('rvn') or -1
            
            if QueryRevision != BaseRevision:
                ApplyProfileChanges = [{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r = {
                "profileRevision": 0,
                "profileId": request.args.get("profileId"),
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
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
    
    @app.route('/fortnite/api/game/v2/profile/<account>/client/GetMcpTimeForLogin', methods=['POST'])
    def fortniteGetMcpTimeForLogin(account):
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
    
    @app.route('/fortnite/api/game/v2/profile/<account>/client/SetMtxPlatform', methods=['POST'])
    def fortnitegameapiclientall2(account):
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

    @app.route('/fortnite/api/game/v2/profile/', methods=['GET'])
    def handle_request_profile():
        if not request.args.get('profileId') and request.path.lower().startswith('/fortnite/api/game/v2/profile/'):
            error = {'error': 'Profile not defined.'}
            resp = app.response_class(
                response=dumps(error),
                status=200,
                mimetype='application/json'
            )
            return resp

        for file in ['data/profiles/athena.json', 'data/profiles/profile0.json', 'data/common_core.json']:
            memory = oldmp.functions.getVersion()

            profile = loads(open(file, 'r', encoding='utf-8').read())[oldmp.session.get('username')].copy()
                    
            if not profile.get('rvn'):
                profile['rvn'] = 0
            if not profile.get('items'):
                profile['items'] = {}
            if not profile.get('stats'):
                profile['stats'] = {}
            if not profile['stats'].get('attributes'):
                profile['stats']['attributes'] = {}
            if not profile.get('commandRevision'):
                profile['commandRevision'] = 0

            if file == 'athena.json':
                SeasonData = loads(open(f'data/profiles/seasondata.json', 'r', encoding='utf-8').read())
                profile['stats']['attributes']['season_num'] = memory['season']

                if f'Season{memory["season"]}' in SeasonData[oldmp.session.get('username')]:
                    SeasonDatas = SeasonData[oldmp.session.get('username')][f'Season{memory["season"]}']

                    profile['stats']['attributes']['book_purchased'] = SeasonDatas['battlePassPurchased']
                    profile['stats']['attributes']['book_level'] = SeasonDatas['battlePassTier']
                    profile['stats']['attributes']['season_match_boost'] = SeasonDatas['battlePassXPBoost']
                    profile['stats']['attributes']['season_friend_match_boost'] = SeasonDatas['battlePassXPFriendBoost']

                oldprofile = loads(open(file, 'r', encoding='utf-8').read())
                oldprofile[oldmp.session.get('username')] = profile
                open(file, 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))

        return Response(status=200)