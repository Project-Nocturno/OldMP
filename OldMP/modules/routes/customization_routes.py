from flask import request
from json import loads, dumps
from os import path as ospath
from datetime import datetime

def register_customization_routes(app, oldmp):
    @app.route('/fortnite/api/game/v2/profile/<account>/client/SetItemFavoriteStatus', methods=['POST'])
    def SetItemFavoriteStatus(account):
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
        StatChanged = False
        
        if loads(request.get_data())['targetItemId']:
            profile['items'][loads(request.get_data())['targetItemId']]['attributes']['favorite'] = loads(request.get_data())['bFavorite'] or False
            StatChanged = True
            
        if StatChanged:
            profile['rvn'] += 1
            profile['commandRevision'] += 1
            
            ApplyProfileChanges.append({
                "changeType": "itemAttrChanged",
                "itemId": loads(request.get_data())['targetItemId'],
                "attributeName": "favorite",
                "attributeValue": profile['items'][loads(request.get_data())['targetItemId']]['attributes']['favorite']
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

    @app.route('/fortnite/api/game/v2/profile/<account>/client/MarkItemSeen', methods=['POST'])
    def MarkItemSeen(account):
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
        StatChanged = False
        
        if loads(request.get_data())['itemIds']:
            
            itemIdsL = loads(request.get_data())['itemIds']
            
            for i in range(len(itemIdsL)):
                profile['items'][itemIdsL[i]]['attributes']['item_seen'] = True
            
                ApplyProfileChanges.append({
                    "changeType": "itemAttrChanged",
                    "itemId": itemIdsL[i],
                    "attributeName": "item_seen",
                    "attributeValue": profile['items'][itemIdsL[i]]['attributes']['item_seen']
                })
            
            StatChanged = True
            
        if StatChanged:
            profile['rvn'] += 1
            profile['commandRevision'] += 1
            
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

    @app.route('/fortnite/api/game/v2/profile/<account>/client/EquipBattleRoyaleCustomization', methods=['POST'])
    def EquipBattleRoyaleCustomization(account):
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
        
        try:
            if not profile['stats']['attributes']['favorite_dance']:
                profile['stats']['attributes']['favorite_dance'] = ["","","","","",""]
                
            if not profile['stats']['attributes']['favorite_itemwraps']:
                profile['stats']['attributes']['favorite_itemwraps'] = ["","","","","","",""]
        
        except:
            pass

        ApplyProfileChanges = []
        BaseRevision = profile['rvn'] or 0
        QueryRevision = request.args.get('rvn') or -1
        StatChanged = False
        VariantChanged = False
        
        try:
            variantUpdatesL = loads(request.get_data())['variantUpdates']
            ReturnVariantsAsString = variantUpdatesL or []
            
            if "active" in ReturnVariantsAsString:
                itemToSlotJ = loads(request.get_data())['itemToSlot']
                if len(profile['items'][itemToSlotJ]['attributes']['variants']) == 0:
                    profile['items'][itemToSlotJ]['attributes']['variants'] = variantUpdatesL or []
                
                for i in profile['items'][itemToSlotJ]['attributes']['variants']:
                    try:
                        if profile['items'][itemToSlotJ]['attributes']['variants']['channel'] == variantUpdatesL[i]['channel'].lower():
                            profile['items'][itemToSlotJ]['attributes']['variants'][i]['active'] = variantUpdatesL[i]['active'] or ""
                    except:
                        pass
                    
                VariantChanged = True
        except Exception as e:
            pass
        
        if loads(request.get_data())['slotName']:
            
            slotNameJ = loads(request.get_data())['slotName']
            itemToSlotJ = loads(request.get_data())['itemToSlot']
            oldmp.functions.req2(f"UPDATE favorites SET {slotNameJ.lower()}='{itemToSlotJ}' WHERE username='{oldmp.session.get('username')}'")
            
            if slotNameJ == "Character":
                oldmp.session.put('character', itemToSlotJ)
                profile['stats']['attributes']['favorite_character'] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "Backpack":
                profile['stats']['attributes']['favorite_backpack'] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "Pickaxe":
                profile['stats']['attributes']['favorite_pickaxe'] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "Glider":
                profile['stats']['attributes']['favorite_glider'] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "SkyDiveContrail":
                profile['stats']['attributes']['favorite_skydivecontrail'] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "MusicPack":
                profile['stats']['attributes']['favorite_musicpack'] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "LoadingScreen":
                profile['stats']['attributes']['favorite_loadingscreen'] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "Dance":
                indexWithinSlot = loads(request.get_data())['indexWithinSlot']
                if indexWithinSlot >= 0:
                    profile['stats']['attributes']['favorite_dance'][indexWithinSlot] = itemToSlotJ or ""
                StatChanged = True
                pass

            if slotNameJ == "ItemWrap":
                indexwithinslot = loads(request.get_data())['indexWithinSlot'] or 0

                if indexwithinslot >= 0 or indexwithinslot <= 0:
                    if indexwithinslot == 0:
                        profile['stats']['attributes']['favorite_itemwraps'][indexwithinslot] = itemToSlotJ or ""
                        pass

                    if indexwithinslot == 1:
                        profile['stats']['attributes']['favorite_itemwraps'][indexwithinslot] = itemToSlotJ or ""
                        pass

                    if indexwithinslot == -1:
                        for i in range(7):
                            profile['stats']['attributes']['favorite_itemwraps'][i] = itemToSlotJ or ""
                        pass
            
        if StatChanged:
            Category = f"favorite_{slotNameJ.lower() or 'character'}"

            if Category == "favorite_itemwrap":
                Category += "s"
            
            profile['rvn'] += 1
            profile['commandRevision'] += 1

            ApplyProfileChanges.append({
                "changeType": "statModified",
                "name": Category,
                "value": profile['stats']['attributes'][Category]
            })

            if VariantChanged:
                ApplyProfileChanges.append({
                    "changeType": "itemAttrChanged",
                    "itemId": itemToSlotJ,
                    "attributeName": "variants",
                    "attributeValue": profile['items'][itemToSlotJ]['attributes']['variants']
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