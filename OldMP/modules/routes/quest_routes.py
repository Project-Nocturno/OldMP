from flask import request
from json import loads, dumps
from os import path as ospath
from datetime import datetime
from uuid import uuid4
import random

def register_quest_routes(app, oldmp):
    @app.route('/fortnite/api/game/v2/profile/<account>/client/ClientQuestLogin', methods=['POST'])
    def ClientQuestLogin(account):
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
        
        QuestIDS = loads(open(f'data/items/quests.json', 'r', encoding='utf-8').read())
        memory = oldmp.functions.getVersion()

        ApplyProfileChanges = []
        BaseRevision = profile['rvn'] or 0
        QueryRevision = request.args.get('rvn') or -1
        StatChanged = False
        
        QuestCount = 0
        ShouldGiveQuest = True
        DateFormat = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ").split("T")[0]
        SeasonQuestIDS = {}
        
        try:
            if request.args.get('profileId') == "athena":
                DailyQuestIDS = QuestIDS['BattleRoyale']['Daily']
                if f"Season{memory['season']}" in QuestIDS['BattleRoyale']:
                    SeasonQuestIDS = QuestIDS['BattleRoyale'][f"Season{memory['season']}"]
                for key in profile['items']:
                    if profile['items'][key]['templateId'].lower().startswith("quest:athenadaily"):
                        QuestCount += 1
                
                if "quest_manager" in profile['stats']['attributes']:
                    if "dailyLoginInterval" in profile['stats']['attributes']['quest_manager']:
                        if "T" in profile['stats']['attributes']['quest_manager']['dailyLoginInterval']:
                            DailyLoginDate = str(profile['stats']['attributes']['quest_manager']['dailyLoginInterval']).split("t")
                            
                            if DailyLoginDate == DateFormat:
                                ShouldGiveQuest = False
                            else:
                                ShouldGiveQuest = True
                                if profile['stats']['attributes']['quest_manager']['dailyQuestRerolls'] <= 0:
                                    profile['stats']['attributes']['quest_manager']['dailyQuestRerolls'] = +1
                if QuestCount < 3 and ShouldGiveQuest == True:
                    NewQuestID = str(uuid4()).replace("-", "")
                    randomNumber = round(random.randint() * len(DailyQuestIDS))
                    
                    for key in profile['items']:
                        while DailyQuestIDS[randomNumber]['templateId'].lower() == profile['items'][key]['templateId'].lower():
                            randomNumber = round(random.randint() * len(DailyQuestIDS))
                
                profile['items'][NewQuestID] = {
                    "templateId": DailyQuestIDS[randomNumber]['templateId'],
                    "attributes": {
                        "creation_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "level": -1,
                        "item_seen": False,
                        "playlists": [],
                        "sent_new_notification": False,
                        "challenge_bundle_id": "",
                        "xp_reward_scalar": 1,
                        "challenge_linked_quest_given": "",
                        "quest_pool": "",
                        "quest_state": "Active",
                        "bucket": "",
                        "last_state_change_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "challenge_linked_quest_parent": "",
                        "max_level_bonus": 0,
                        "xp": 0,
                        "quest_rarity": "uncommon",
                        "favorite": False
                    },
                    "quantity": 1
                }
                
                for i in DailyQuestIDS[randomNumber]['objectives']:
                    profile['items'][NewQuestID]['attributes'][f"completion_{DailyQuestIDS[randomNumber]['objectives'][i].lower()}"]

                profile['stats']['attributes']['quest_manager']['dailyLoginInterval'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                
                ApplyProfileChanges.append({
                    "changeType": "itemAdded",
                    "itemId": NewQuestID,
                    "item": profile['items'][NewQuestID]
                })
                
                ApplyProfileChanges.append({
                    "changeType": "statModified",
                    "name": "quest_manager",
                    "value": profile['stats']['attributes']['quest_manager']
                })
                
                StatChanged = True
        except:
            pass
        
        for key in profile['items']:
            if str(key)[0] == "S" and isinstance(str(key)[1], int) and (str(key)[2] == "-" or isinstance(str(key)[2], int) and str(key)[3] == "-"):
                if not str(key).startswith(f"S{memory['season']}-"):
                    profile['items'].pop(key)
                    
                    ApplyProfileChanges.append({
                        "changeType": "itemRemoved",
                        "itemId": key
                    })
                    
                    StatChanged = True
        
        if SeasonQuestIDS:
            if request.args.get('profileId') == "athena":
                for i, ChallengeBundleSchedule in enumerate(SeasonQuestIDS['ChallengeBundleSchedules']):
                    if ChallengeBundleSchedule['itemGuid'] in profile['items']:
                        ApplyProfileChanges.append({
                            "changeType": "itemRemoved",
                            "itemId": ChallengeBundleSchedule['itemGuid']
                        })
                    
                    ChallengeBundleSchedule = SeasonQuestIDS['ChallengeBundleSchedules'][i]
                    
                    profile['items'][ChallengeBundleSchedule['itemGuid']] = {
                        "templateId": ChallengeBundleSchedule['templateId'],
                        "attributes": {
                            "unlock_epoch": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "max_level_bonus": 0,
                            "level": 1,
                            "item_seen": True,
                            "xp": 0,
                            "favorite": False,
                            "granted_bundles": ChallengeBundleSchedule['granted_bundles']
                        },
                        "quantity": 1
                    }
                    
                    ApplyProfileChanges.append({
                        "changeType": "itemAdded",
                        "itemId": ChallengeBundleSchedule['itemGuid'],
                        "item": profile['items'][ChallengeBundleSchedule['itemGuid']]
                    })
                    
                    StatChanged = True
                
                for i, ChallengeBundle in enumerate(SeasonQuestIDS['ChallengeBundles']):
                    if ChallengeBundle['itemGuid'] in profile['items']:
                        ApplyProfileChanges.append({
                            "changeType": "itemRemoved",
                            "itemId": ChallengeBundle['itemGuid']
                        })
                    
                    ChallengeBundle = SeasonQuestIDS['ChallengeBundles'][i]
                    
                    if loads(open('conf.json', 'r', encoding='utf-8').read())["Profile"]["bCompletedSeasonalQuests"] == True and "questStages" in ChallengeBundle:
                        ChallengeBundle['grantedquestinstanceids'] = ChallengeBundle['grantedquestinstanceids'] + ChallengeBundle['questStages']
                    
                    profile['items'][ChallengeBundle['itemGuid']] = {
                        "templateId": ChallengeBundle['templateId'],
                        "attributes": {
                            "has_unlock_by_completion": False,
                            "num_quests_completed": 0,
                            "level": 0,
                            "grantedquestinstanceids": ChallengeBundle['grantedquestinstanceids'],
                            "item_seen": True,
                            "max_allowed_bundle_level": 0,
                            "num_granted_bundle_quests": 0,
                            "max_level_bonus": 0,
                            "challenge_bundle_schedule_id": ChallengeBundle['challenge_bundle_schedule_id'],
                            "num_progress_quests_completed": 0,
                            "xp": 0,
                            "favorite": False
                        },
                        "quantity": 1
                    }
                    
                    profile['items'][ChallengeBundle['itemGuid']]['attributes']['num_granted_bundle_quests'] = len(ChallengeBundle['grantedquestinstanceids'])
                    
                    if loads(open('conf.json', 'r', encoding='utf-8').read())["Profile"]["bCompletedSeasonalQuests"]:
                        profile['items'][ChallengeBundle['itemGuid']]['attributes']['num_quests_completed'] = len(ChallengeBundle['grantedquestinstanceids'])
                        profile['items'][ChallengeBundle['itemGuid']]['attributes']['num_progress_quests_completed'] = len(ChallengeBundle['grantedquestinstanceids'])
                    
                    ApplyProfileChanges.append({
                        "changeType": "itemAdded",
                        "itemId": ChallengeBundle['itemGuid'],
                        "item": profile['items'][ChallengeBundle['itemGuid']]
                    })
                    
                    StatChanged = True
            
            for i, Quest in enumerate(SeasonQuestIDS['Quests']):
                if Quest['itemGuid'] in profile['items']:
                    ApplyProfileChanges.append({
                        "changeType": "itemRemoved",
                        "itemId": Quest['itemGuid']
                    })
                
                Quest = SeasonQuestIDS['Quests'][i]
                
                profile['items'][Quest['itemGuid']] = {
                    "templateId": Quest['templateId'],
                    "attributes": {
                        "creation_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "level": -1,
                        "item_seen": True,
                        "playlists": [],
                        "sent_new_notification": True,
                        "challenge_bundle_id": Quest['challenge_bundle_id'] or "",
                        "xp_reward_scalar": 1,
                        "challenge_linked_quest_given": "",
                        "quest_pool": "",
                        "quest_state": "Active",
                        "bucket": "",
                        "last_state_change_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "challenge_linked_quest_parent": "",
                        "max_level_bonus": 0,
                        "xp": 0,
                        "quest_rarity": "uncommon",
                        "favorite": False
                    },
                    "quantity": 1
                }
                
                if loads(open('conf.json', 'r', encoding='utf-8').read())["Profile"]['bCompletedSeasonalQuests']:
                    profile['items'][Quest['itemGuid']]['attributes']['quest_state'] = "Claimed"
                
                for x in range(len(Quest['objectives'])):
                    if loads(open('conf.json', 'r', encoding='utf-8').read())["Profile"]['bCompletedSeasonalQuests']:
                        profile['items'][Quest['itemGuid']]['attributes'][f"completion_{Quest['objectives'][x]['name'][0]}"] = Quest['objectives'][x]['count']
                    else:
                        profile['items'][Quest['itemGuid']]['attributes'][f"completion_{Quest['objectives'][x]['name'][0]}"] = 0
                
                ApplyProfileChanges.append({
                    "changeType": "itemAdded",
                    "itemId": Quest['itemGuid'],
                    "item": profile['items'][Quest['itemGuid']]
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
            "profileId": "athena",
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

    @app.route("/fortnite/api/game/v2/profile/<account>/client/FortRerollDailyQuest", methods=["POST"])
    def FortRerollDailyQuest(account):
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
        DailyQuestIDS = loads(open(f'data/items/quests.json', 'r', encoding='utf-8').read())

        ApplyProfileChanges = []
        Notifications = []
        BaseRevision = profile.get("rvn", 0)
        QueryRevision = request.args.get("rvn", -1)
        StatChanged = False

        if request.args.get('profileId') == "athena":
            DailyQuestIDS = DailyQuestIDS["BattleRoyale"]["Daily"]

        NewQuestID = str(uuid4()).replace("-", "")
        randomNumber = random.randint(0, len(DailyQuestIDS) - 1)

        for key, item in profile["items"]:
            while DailyQuestIDS[randomNumber]["templateId"].lower() == item["templateId"].lower():
                randomNumber = random.randint(0, len(DailyQuestIDS) - 1)

        if "questId" in request.form and profile["stats"]["attributes"]["quest_manager"]["dailyQuestRerolls"] >= 1:
            profile["stats"]["attributes"]["quest_manager"]["dailyQuestRerolls"] -= 1

            del profile["items"][loads(request.get_data())['questId']]

            profile["items"][NewQuestID] = {
                "templateId": DailyQuestIDS[randomNumber]["templateId"],
                "attributes": {
                    "creation_time": datetime.now().isoformat(),
                    "level": -1,
                    "item_seen": False,
                    "playlists": [],
                    "sent_new_notification": False,
                    "challenge_bundle_id": "",
                    "xp_reward_scalar": 1,
                    "challenge_linked_quest_given": "",
                    "quest_pool": "",
                    "quest_state": "Active",
                    "bucket": "",
                    "last_state_change_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "challenge_linked_quest_parent": "",
                    "max_level_bonus": 0,
                    "xp": 0,
                    "quest_rarity": "uncommon",
                    "favorite": False
                },
                "quantity": 1
            }

            for i in DailyQuestIDS[randomNumber]["objectives"]:
                profile["items"][NewQuestID]["attributes"][f"completion_{i.lower()}"] = 0

            StatChanged = True
            
        if StatChanged:
            profile['rvn'] += 1
            profile['commandRevision'] += 1
            
            ApplyProfileChanges.append({
                "changeType": "statModified",
                "name": "quest_manager",
                "value": profile['stats']['attributes']['quest_manager']
            })
            
            ApplyProfileChanges.append({
                "changeType": "itemAdded",
                "itemId": NewQuestID,
                "item": profile['items'][NewQuestID]
            })
            
            ApplyProfileChanges.append({
                "changeType": "itemRemoved",
                "itemId": loads(request.get_data())['questId']
            })
            
            Notifications.append({
                "type": "dailyQuestReroll",
                "primary": True,
                "newQuestId": DailyQuestIDS[randomNumber]['templateId']
            })

            oldprofile = loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
            oldprofile[oldmp.session.get('username')] = profile
            open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))

        if QueryRevision != BaseRevision:
            apply_profile_changes = [{
                "changeType": "fullProfileUpdate",
                "profile": profile
            }]
            
        r = {
            "profileRevision": profile['rvn'] or 0,
            "profileId": request.args.get('profileId') or 'athena',
            "profileChangesBaseRevision": BaseRevision,
            "profileChanges": apply_profile_changes,
            "notifications": Notifications,
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