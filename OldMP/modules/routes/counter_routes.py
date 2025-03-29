from flask import request
from json import loads, dumps
from os import path as ospath
from datetime import datetime

def register_counter_routes(app, oldmp):
    @app.route('/fortnite/api/game/v2/profile/<account>/client/IncrementNamedCounterStat', methods=['POST'])
    def IncrementNamedCounterStat(account):
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
        QueryRevision = request.args['rvn'] or -1
        StatChanged = False

        if "named_counters" in profile['stats']['attributes'] and loads(request.get_data())['counterName']:
            if loads(request.get_data())['counterName'] in profile['stats']['attributes']['named_counters']:
                profile['stats']['attributes']['named_counters'][loads(request.get_data())['counterName']]['current_count'] += 1
                profile['stats']['attributes']['named_counters'][loads(request.get_data())['counterName']]['last_incremented_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                
                StatChanged = True
        
        if StatChanged:
            profile['rvn'] += 1
            profile['commandRevision'] += 1

            ApplyProfileChanges.append({
                "changeType": "statModified",
                "name": "named_counters",
                "value": profile['stats']['attributes']['named_counters']
            })

            oldprofile = loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
            oldprofile[oldmp.session.get('username')] = profile
            open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
        
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