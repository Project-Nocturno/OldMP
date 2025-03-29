from flask import request
from json import loads, dumps
from os import path as ospath
from datetime import datetime

def register_purchase_routes(app, oldmp):
    @app.route("/fortnite/api/game/v2/profile/<account>/client/RefundMtxPurchase", methods=["POST"])
    def refund_mtx_purchase(account):
        profile = loads(open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'r', encoding='utf-8').read())[oldmp.session.get('username')].copy()
        item_profile = loads(open(f'data/profiles/athena.json', 'r', encoding='utf-8').read())[oldmp.session.get('username')].copy()

        apply_profile_changes = []
        multi_update = []
        base_revision = profile.get("rvn") or 0
        query_revision = request.args.get("rvn") or -1
        stat_changed = False

        item_guids = []

        if "purchaseId" in request.form:
            multi_update.append({
                "profileRevision": item_profile.get("rvn") or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": item_profile.get("rvn") or 0,
                "profileChanges": [],
                "profileCommandRevision": item_profile.get("commandRevision") or 0,
            })

            profile["stats"]["attributes"]["mtx_purchase_history"]["refundsUsed"] += 1
            profile["stats"]["attributes"]["mtx_purchase_history"]["refundCredits"] -= 1

            for purchase in profile["stats"]["attributes"]["mtx_purchase_history"]["purchases"]:
                if purchase["purchaseId"] == loads(request.get_data("purchaseId"))["purchaseId"]:
                    for loot_result in purchase["lootResult"]:
                        item_guids.append(loot_result["itemGuid"])

                    purchase["refundDate"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

                    for key, item in profile["items"].items():
                        if item["templateId"].lower().startswith("currency:mtx"):
                            if item["attributes"]["platform"].lower() == profile["stats"]["attributes"]["current_mtx_platform"].lower() or item["attributes"]["platform"].lower() == "shared":
                                item["quantity"] += purchase["totalMtxPaid"]

                                apply_profile_changes.append({
                                    "changeType": "itemQuantityChanged",
                                    "itemId": key,
                                    "quantity": item["quantity"]
                                })

                                break

            for item_guid in item_guids:
                try:
                    del item_profile["items"][item_guid]

                    multi_update[0]["profileChanges"].append({
                        "changeType": "itemRemoved",
                        "itemId": item_guid
                    })
                except KeyError:
                    pass

            item_profile['rvn'] += 1
            item_profile['commandRevision'] += 1
            profile['rvn'] += 1
            profile['commandRevision'] += 1
            
            stat_changed = True
        
        if stat_changed:
            apply_profile_changes.append({
                "changeType": "statModified",
                "name": "mtx_purchase_history",
                "value": profile['stats']['attributes']['mtx_purchase_history']
            })
            
            multi_update[0]['profileRevision'] = item_profile['rvn'] or 0
            multi_update[0]['profileCommandRevision'] = item_profile['commandRevision'] or 0
            
            oldprofile = loads(open(f'data/profiles/athena.json', 'r', encoding='utf-8').read())
            oldprofile[oldmp.session.get('username')] = item_profile
            open(f'data/profiles/athena.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            oldprofile = loads(open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'r', encoding='utf-8').read())
            oldprofile[oldmp.session.get('username')] = profile
            open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
        
        if query_revision != base_revision:
            apply_profile_changes = [{
                "changeType": "fullProfileUpdate",
                "profile": profile
            }]
        
        r = {
            "profileRevision": profile['rvn'] or 0,
            "profileId": request.args.get('profileId') or 'common_core',
            "profileChangesBaseRevision": base_revision,
            "profileChanges": apply_profile_changes,
            "profileCommandRevision": profile['commandRevision'] or 0,
            "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "multiUpdate": multi_update,
            "responseVersion": 1
        }

        resp = app.response_class(
            response=dumps(r),
            status=200,
            mimetype='application/json'
        )
        return resp