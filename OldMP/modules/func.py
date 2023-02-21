from flask import Flask
from json import loads, dumps
from datetime import datetime, timedelta
import mysql.connector
from os import mkdir as osmkdir

class OldMPFunc():
    def __init__(
        self,
        request,
        app: Flask,
        logsapp: bool=True,
        cnx: mysql.connector=mysql.connector.connect()
    ):
        self.request=request
        self.app=app
        self.cnx=cnx
        
        self.logsapp=logsapp
        self.NLogs=self.logs
        
        self.exchange_table=[
            {'name': 'skull_trooper', 'id': 'CID_030_Athena_Commando_M_Halloween', 'price': 1500, 'style': 'skins'},
            {'name': 'ghoul_trooper', 'id': 'CID_029_Athena_Commando_F_Halloween', 'price': 0, 'style': 'skins'},
            {'name': 'recon_specialist', 'id': 'CID_024_Athena_Commando_F', 'price': 0, 'style': 'skins'},
            {'name': 'brawler', 'id': 'CID_021_Athena_Commando_F', 'price': 0, 'style': 'skins'},
            {'name': 'racon_expert', 'id': 'CID_022_Athena_Commando_F', 'price': 0, 'style': 'skins'},
            {'name': 'love_ranger', 'id': 'CID_070_Athena_Commando_M_Cupid', 'price': 0, 'style': 'skins'},
            {'name': 'cuddle_team_leader', 'id': 'CID_069_Athena_Commando_F_PinkBear', 'price': 0, 'style': 'skins'},
            {'name': 'e.l.f', 'id': 'CID_051_Athena_Commando_M_HolidayElf', 'price': 0, 'style': 'skins'},
            {'name': 'merry_marauder', 'id': 'CID_049_Athena_Commando_M_HolidayGingerbread', 'price': 0, 'style': 'skins'},
            {'name': 'nog_ops', 'id': 'CID_046_Athena_Commando_F_HolidaySweater', 'price': 0, 'style': 'skins'},
            {'name': 'funk_ops', 'id': 'CID_038_Athena_Commando_M_Disco', 'price': 0, 'style': 'skins'},
            {'name': 'rednosed_raider', 'id': 'CID_047_Athena_Commando_F_HolidayReindeer', 'price': 0, 'style': 'skins'},
            {'name': 'yuletide_ranger', 'id': 'CID_045_Athena_Commando_M_HolidaySweater', 'price': 0, 'style': 'skins'},
            {'name': 'brite_bomber', 'id': 'CID_044_Athena_Commando_F_SciPop', 'price': 0, 'style': 'skins'},
            {'name': 'crackshot', 'id': 'CID_050_Athena_Commando_M_HolidayNutcracker', 'price': 0, 'style': 'skins'},
            {'name': 'artic_assassin', 'id': 'CID_037_Athena_Commando_F_WinterCamo', 'price': 0, 'style': 'skins'},
            {'name': 'blue_team_leader', 'id': 'CID_052_Athena_Commando_F_PSBlue', 'price': 0, 'style': 'skins'},
            {'name': 'dazzle', 'id': 'CID_076_Athena_Commando_F_Sup', 'price': 0, 'style': 'skins'},
            {'name': 'jungle_scout', 'id': 'CID_074_Athena_Commando_F_Stripe', 'price': 0, 'style': 'skins'},
            {'name': 'mogul_master', 'id': 'CID_065_Athena_Commando_F_SkiGirl_FRA', 'price': 0, 'style': 'skins'},
            {'name': 'sash_sergeant', 'id': 'CID_072_Athena_Commando_M_Scout', 'price': 0, 'style': 'skins'},
            {'name': 'default_skin', 'id': 'CID_001_Athena_Commando_F_Default', 'price': 0, 'style': 'skins'},
            {'name': 'reaper', 'id': 'HalloweenScythe', 'price': 0, 'style': 'pickaxes'},
            {'name': 'close_shave', 'id': 'BoltonPickaxe', 'price': 0, 'style': 'pickaxes'},
            {'name': 'death_valley', 'id': 'Pickaxe_Deathvalley', 'price': 0, 'style': 'pickaxes'},
            {'name': 'candy_axe', 'id': 'Pickaxe_ID_015_HolidayCandyCane', 'price': 0, 'style': 'pickaxes'},
            {'name': 'disco_brawl', 'id': 'Pickaxe_ID_016_Disco', 'price': 0, 'style': 'pickaxes'},
            {'name': 'ice_breaker', 'id': 'Pickaxe_ID_014_WinterCamo', 'price': 0, 'style': 'pickaxes'},
            {'name': 'chomp_jr', 'id': 'Pickaxe_ID_017_Shark', 'price': 0, 'style': 'pickaxes'},
            {'name': 'plunja', 'id': 'Pickaxe_ID_024_Plunger', 'price': 0, 'style': 'pickaxes'},
            {'name': 'tat_axe', 'id': 'Pickaxe_ID_019_Heart', 'price': 0, 'style': 'pickaxes'},
            {'name': 'batsickle', 'id': 'SickleBatPickaxe', 'price': 0, 'style': 'pickaxes'},
            {'name': 'Default_Pickaxe', 'id': 'DefaultPickaxe', 'price': 0, 'style': 'pickaxes'},
            {'name': 'mako', 'id': 'Glider_Warthog', 'price': 0, 'style': 'gliders'},
            {'name': 'prismatic', 'id': 'Glider_Prismatic', 'price': 0, 'style': 'gliders'},
            {'name': 'gum_drop', 'id': 'Glider_ID_009_CandyCoat', 'price': 0, 'style': 'gliders'},
            {'name': 'cozy_coaster', 'id': 'Glider_ID_005_HolidaySweater', 'price': 0, 'style': 'gliders'},
            {'name': 'cloud_strike', 'id': 'Glider_ID_010_Storm', 'price': 0, 'style': 'gliders'},
            {'name': 'snowflake', 'id': 'Umbrella_Snowflake', 'price': 0, 'style': 'gliders'},
            {'name': 'umbrella', 'id': 'Solo_Umbrella', 'price': 0, 'style': 'gliders'},
            {'name': 'default_glider', 'id': 'DefaultGlider', 'price': 0, 'style': 'gliders'},
            {'name': 'royale_knight', 'id': 'CID_033_Athena_Commando_F_Medieval', 'price': 0, 'style': 'skins'},
            {'name': 'blue_squire', 'id': 'CID_032_Athena_Commando_M_Medieval', 'price': 0, 'style': 'skins'},
            {'name': 'sparkle_specialist', 'id': 'CID_039_Athena_Commando_F_Disco', 'price': 0, 'style': 'skins'},
            {'name': 'black_knight', 'id': 'CID_035_Athena_Commando_M_Medieval', 'price': 0, 'style': 'skins'},
            {'name': 'strike_specialist', 'id': 'CID_025_Athena_Commando_M', 'price': 0, 'style': 'skins'},
            {'name': 'circuit_breaker', 'id': 'CID_042_Athena_Commando_M_Cyberpunk', 'price': 0, 'style': 'skins'},
            {'name': 'renegade_raider', 'id': 'CID_028_Athena_Commando_F', 'price': 0, 'style': 'skins'},
            {'name': 'assault_trooper', 'id': 'CID_017_Athena_Commando_M', 'price': 0, 'style': 'skins'},
            {'name': 'red_knight', 'id': 'CID_034_Athena_Commando_F_Medieval', 'price': 0, 'style': 'skins'},
            {'name': 'pusle_axe', 'id': 'Pickaxe_ID_012_District', 'price': 0, 'style': 'pickaxes'},
            {'name': 'axecalibur', 'id': 'Pickaxe_ID_011_Medieval', 'price': 0, 'style': 'pickaxes'},
            {'name': 'ac_dc', 'id': 'Pickaxe_ID_013_Teslacoil', 'price': 0, 'style': 'pickaxes'},
            {'name': 'lucky', 'id': 'HappyPickaxe', 'price': 0, 'style': 'pickaxes'},
            {'name': 'shouldnt_have', 'id': 'Pickaxe_ID_022_HolidayGiftWrap', 'price': 0, 'style': 'pickaxes'},
            {'name': 'raider_revenge', 'id': 'Pickaxe_Lockjaw', 'price': 0, 'style': 'pickaxes'},
            {'name': 'the_brave', 'id': 'Glider_ID_002_Medieval', 'price': 0, 'style': 'gliders'},
            {'name': 'royale_x', 'id': 'Glider_ID_003_District', 'price': 0, 'style': 'gliders'},
            {'name': 'get_down', 'id': 'Glider_ID_004_Disco', 'price': 0, 'style': 'gliders'},
            {'name': 'voyager', 'id': 'Glider_Voyager', 'price': 0, 'style': 'gliders'},
            {'name': 'zephyr', 'id': 'Glider_ID_008_Graffiti', 'price': 0, 'style': 'gliders'},
            {'name': 'pink_flamingo', 'id': 'Pickaxe_Flamingo', 'price': 0, 'style': 'gliders'},
            {'name': 'roadtrip', 'id': 'Glider_RoadTrip', 'price': 0, 'style': 'gliders'}
        ]
        
        self.conv_table=[
            {'name': 'skins', 'id': 'AthenaCharacter'}, 
            {'name': 'backpacks', 'id': 'AthenaBackpack'}, 
            {'name': 'gliders', 'id': 'AthenaGlider'},
            {'name': 'pickaxes', 'id': 'AthenaPickaxe'},
            {'name': 'musicspacks', 'id': 'AthenaMusicPack'},
            {'name': 'loadingscreens', 'id': 'AthenaLoadingScreen'}
        ]
        
        self.new_items={
            "ettrr4h-2wedfgbn-8i9jsghj-lpw9t2to-loadout1": {
            "templateId": "CosmeticLocker:cosmeticlocker_athena",
            "attributes": {
                "locker_slots_data": {
                    "slots": {
                        "MusicPack": {
                            "items": [
                                ""
                            ]
                        },
                        "Character": {
                            "items": [
                                ""
                            ],
                            "activeVariants": [
                                None
                            ]
                        },
                        "Backpack": {
                            "items": [
                                ""
                            ],
                            "activeVariants": [
                                None
                            ]
                        },
                        "SkyDiveContrail": {
                            "items": [
                                ""
                            ],
                            "activeVariants": [
                                None
                            ]
                        },
                        "Dance": {
                            "items": [
                                "AthenaDance:eid_dancemoves",
                                "",
                                "",
                                "",
                                "",
                                ""
                            ]
                        },
                        "LoadingScreen": {
                            "items": [
                                ""
                            ]
                        },
                        "Pickaxe": {
                            "items": [
                                "AthenaPickaxe:DefaultPickaxe"
                                ],
                            "activeVariants": [
                                None
                            ]
                        },
                        "Glider": {
                            "items": [
                                "AthenaGlider:DefaultGlider"
                                ],
                            "activeVariants": [
                                None
                            ]
                        },
                        "ItemWrap": {
                            "items": [
                                "",
                                "",
                                "",
                                "",
                                "",
                                "",
                                ""
                            ],
                            "activeVariants": [
                                None,
                                None,
                                None,
                                None,
                                None,
                                None,
                                None
                            ]
                        }
                    }
                },
                "use_count": 0,
                "banner_icon_template": "StandardBanner1",
                "banner_color_template": "DefaultColor14",
                "locker_name": "OldMP",
                "item_seen": False,
                "favorite": False
            },
            "quantity": 1
            }
        }
    
    def req(self, sql: str):
        cursor=self.cnx.cursor()
        cursor.execute(sql)
        results=cursor.fetchall()
        cursor.close()
        return results
    
    def getVersion(self):
        memory={
            "season": 0,
            "build": 0.0,
            "CL": "",
            "lobby": ""
        }
        
        if self.request.headers["user-agent"]:
            try:
                BuildID=str(self.request.headers["user-agent"]).split("-")[3].split(",")[0]
                if not isinstance(BuildID, int):
                    if " " in BuildID:
                        CL=BuildID.split(' ')[0]
                    else:
                        CL=BuildID
                    
                else:
                    BuildID=str(self.request.headers["user-agent"]).split("-")[3].split(" ")[0]
                    if not isinstance(BuildID, int):
                        if " " in BuildID:
                            CL=BuildID.split(' ')[0]
                        else:
                            CL=BuildID
            except:
                try:
                    BuildID=str(self.request.headers["user-agent"]).split("-")[1].split("+")[0]
                    if not isinstance(BuildID, int):
                        if " " in BuildID:
                            CL=BuildID.split(' ')[0]
                        else:
                            CL=BuildID
                except:
                    pass
            
            try:
                Build=str(self.request.headers["user-agent"]).split("Release-")[1].split("-")[0]
                if len(Build.split("."))==3:
                    Value=Build.split(".")
                    Build=Value[0]+"."+Value[1]+Value[2]
                    
                season=float(Build.split(".")[0])

                memory['season']=int(season)
                memory['build']=float(Build)
                memory['CL']=CL
                memory['lobby']=f"LobbySeason{int(memory['season'])}"
                
                if isinstance(season, int):
                    memory['season']=2
                    memory['build']=2.0
                    memory['CL']=CL
                    memory['lobby']="LobbyWinterDecor"
                    
            except:
                memory['season']=2
                memory['build']=2.0
                memory['CL']=CL
                memory['lobby']="LobbyWinterDecor"

        return memory



    def getShop(self):
        catalog_config=loads(open(f'data/content/catalogconfig.json', 'r', encoding='utf-8').read())
        catalog=loads(open(f'data/items/catalog.json', 'r', encoding='utf-8').read())

        for value in catalog_config:
            if isinstance(catalog_config[value]['itemGrants'], list):
                if len(catalog_config[value]['itemGrants']) != 0:
                    catalog_entry={
                        "devName": "",
                        "offerId": "",
                        "fulfillmentIds": [],
                        "dailyLimit": -1,
                        "weeklyLimit": -1,
                        "monthlyLimit": -1,
                        "categories": [],
                        "prices": [
                            {
                                "currencyType": "MtxCurrency",
                                "currencySubType": "",
                                "regularPrice": 0,
                                "finalPrice": 0,
                                "saleExpiration": "9999-12-02T01:12:00Z",
                                "basePrice": 0
                            }
                        ],
                        "meta": {
                            "SectionId": "Featured",
                            "TileSize": "Small"
                        },
                        "matchFilter": "",
                        "filterWeight": 0,
                        "appStoreId": [],
                        "requirements": [],
                        "offerType": "StaticPrice",
                        "giftInfo": {
                            "bIsEnabled":False,
                            "forcedGiftBoxTemplateId": "",
                            "purchaseRequirements": [],
                            "giftRecordIds": []
                        },
                        "refundable": True,
                        "metaInfo": [
                            {
                                "key": "SectionId",
                                "value": "Featured"
                            },
                            {
                                "key": "TileSize",
                                "value": "Small"
                            }
                        ],
                        "displayAssetPath": "",
                        "itemGrants": [],
                        "sortPriority": 0,
                        "catalogGroupPriority": 0
                    }

                    if value.lower().startswith("daily"):
                        for i, storefront in enumerate(catalog['storefronts']):
                            if storefront['name'] == "BRDailyStorefront":
                                catalog_entry['requirements'] = []
                                catalog_entry['itemGrants'] = []

                                for x in catalog_config[value]['itemGrants']:
                                    if isinstance(x, str):
                                        if len(x) != 0:
                                            catalog_entry['devName'] = catalog_config[value]['itemGrants'][0]
                                            catalog_entry['offerId'] = catalog_config[value]['itemGrants'][0]

                                            catalog_entry['requirements'].append({
                                                "requirementType": "DenyOnItemOwnership",
                                                "requiredId": x,
                                                "minQuantity": 1
                                            })
                                            catalog_entry['itemGrants'].append({
                                                "templateId": x,
                                                "quantity": 1
                                            })

                                catalog_entry['prices'][0]['basePrice'] = catalog_config[value]['price']
                                catalog_entry['prices'][0]['regularPrice'] = catalog_config[value]['price']
                                catalog_entry['prices'][0]['finalPrice'] = catalog_config[value]['price']

                                if len(catalog_entry['itemGrants'])!=0:
                                    catalog['storefronts'][i]['catalogEntries'].append(catalog_entry)
                    
                    if value.lower().startswith("featured"):
                        for i, storefront in enumerate(catalog['storefronts']):
                            catalog_entry['requirements']=[]
                            catalog_entry['itemGrants']=[]
                            
                            for x in range(len(catalog_config[value]['itemGrants'])):
                                if isinstance(catalog_config[value]['itemGrants'][x], str):
                                    if len(catalog_config[value]['itemGrants'][x])!=0:
                                        catalog_entry['devName']=catalog_config[value]['itemGrants'][0]
                                        catalog_entry['offerId']=catalog_config[value]['itemGrants'][0]
                                        
                                        catalog_entry['requirements'].append({ "requirementType": "DenyOnItemOwnership", "requiredId": catalog_config[value]['itemGrants'][x], "minQuantity": 1 })
                                        catalog_entry['itemGrants'].append({ "templateId": catalog_config[value]['itemGrants'][x], "quantity": 1 })

                                    catalog_entry['prices'][0]['basePrice']=catalog_config[value]['price']
                                    catalog_entry['prices'][0]['regularPrice']=catalog_config[value]['price']
                                    catalog_entry['prices'][0]['finalPrice']=catalog_config[value]['price']
                                    
                                    catalog_entry['meta']['TileSize']="Normal"
                                    catalog_entry['metaInfo'][1]['value']="Normal"
                                    
                                    if len(catalog_entry['itemGrants'])!=0:
                                        catalog['storefronts'][i]['catalogEntries'].append(catalog_entry)
        return catalog

    def getContentPages(self):
        
        emergency=loads(open('conf.json', 'r', encoding='utf-8').read())["Content"]['loadEmergency']
        
        memory=self.getVersion()
        contentpage=loads(open(f'data/content/contentpages.json', 'r', encoding='utf-8').read())
        language="fr"
        
        if self.request.headers["accept-language"]:
            if "-" in self.request.headers["accept-language"] and self.request.headers["accept-language"]!="es-419" and self.request.headers["accept-language"]!="pt-BR":
                language=self.request.headers["accept-language"].split("-")[0]
            else:
                language=self.request.headers["accept-language"]
                
        modes=["battleRoyale", "saveTheWorld"]
        news=["battleroyalenews"]
        motdnews=["battleroyalenews"]
        
        try:
            for mode in modes:
                contentpage['subgameselectdata'][mode]['message']['title']=contentpage['subgameselectdata'][mode]['message']['title'][language]
                contentpage['subgameselectdata'][mode]['message']['body']=contentpage['subgameselectdata'][mode]['message']['body'][language]
                
        except:
            pass
        
        try:
            if memory['build']<5.30:
                for mode in news:
                    contentpage[mode]['news']['messages'][0]['image']="http://oldmp.software:3551/content/images/logo.png"
                    contentpage[mode]['news']['messages'][0]['title']=f"Bienvenue sur Fortnite saison {memory['season']}"
                    contentpage[mode]['news']['messages'][1]['image']=""
        except:
            pass
        
        try:
            for news in motdnews:
                for motd in contentpage[news]['news']['motds']:
                    motd['title']=motd['title'][language]
                    motd['body']=motd['body'][language]
        except:
            pass
        
        try:
            contentpage['dynamicbackgrounds']['backgrounds']['backgrounds'][0]['stage']=f'season{memory["season"]}'
            contentpage['dynamicbackgrounds']['backgrounds']['backgrounds'][1]['stage']=f'season{memory["season"]}'
            
        except:
            pass
        
        try:
            if emergency:
                contentpage.update(loads(open('conf.json', 'r', encoding='utf-8').read())['Content']['emergencymsg']['v1'])
                contentpage.update(loads(open('conf.json', 'r', encoding='utf-8').read())['Content']['emergencymsg']['v2'])
        
        except:
            pass
        
        try:
            contentpage.update(loads(open('conf.json', 'r', encoding='utf-8').read())['Content']['loginmess'])
        
        except:
            pass
        
        return contentpage
    
    def sendXmppMessageToAll(self, req):
        pass
    
    def find(self, pred, iterable):
        for element in iterable:
            if pred(element):
                return element
        return None
    
    def genToken(self, ip: str, clientId, enc):

        return f'NOCTURNOISBETTER_{enc(f"clientId:{clientId}|ip:{ip}".encode()).decode()}'
                
    def createError(self, errorCode, errorMessage, messageVars, numericErrorCode, error):
        response={
            'X-Epic-Error-Name': errorCode,
            'X-Epic-Error-Code': numericErrorCode,
            'errorCode': errorCode,
            'errorMessage': errorMessage,
            'messageVars': messageVars,
            'numericErrorCode': numericErrorCode,
            'originatingService': "any",
            'intent': "prod",
            'error_description': errorMessage,
            'error': error 
        }
        return response
    
    def createDate(self, hour: int=0, min: int=0, sec: int=0):
        dt=datetime.now()
        dt=dt+timedelta(hours=hour, minutes=min, seconds=sec)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def loadProfile(self, username: str):
        
        if self.checkProfile(username):
            pass
        else:
            return True
        
        stats=self.req(f"SELECT top1 FROM stat WHERE username='{username}'")
        stats2=self.req(f"SELECT mtx, item, level, exp FROM users WHERE username='{username}'")
        favorites=self.req(f"SELECT * FROM favorites WHERE username='{username}'")
        
        try:
            mtx=int(stats2[0][0])
            items=list(str(stats2[0][1]).split(', '))
            level=int(stats2[0][2])
            xp=int(stats2[0][3])
            top1=int(stats[0][0])
            
            f_char=favorites[0][0]
            f_back=favorites[0][1]
            f_pic=favorites[0][2]
            f_glid=favorites[0][3]
            f_sky=favorites[0][4]
            f_music=favorites[0][5]
            f_load=favorites[0][6]
            f_dance=favorites[0][7]
            
        except:
            self.NLogs(self.logsapp, "error")
            respon=self.createError(
                "errors.com.epicgames.account.invalid_profile",
                "Your profile does not exist. Please verify your account on our website: https://www.nocturno.games/", 
                [], 18031, "invalid_profile"
            )
            resp=self.app.response_class(
                response=dumps(respon),
                status=400,
                mimetype='application/json'
            )
            return resp
        
        for i in ['athena.json', 'profile0.json', 'common_core.json', 'common_public.json']:
            profiles=loads(open(f'data/profiles/{i}', 'r', encoding='utf-8').read())
                    
            if i.replace('.json', '')=='athena':
                
                newitems=self.new_items.copy()
                
                items_id=[]
                for p in items:
                    for x in self.exchange_table:
                        if p==x['name']:
                            items_id.append(x['id'])
                            
                for p in items_id:
                    for x in self.exchange_table:
                        if p==x['id']:
                            for z in self.conv_table:
                                if z['name']==x['style']:
                                    p=f"{z['id']}:{p}"
                                    item_temp={
                                        p: {
                                            "templateId": p,
                                            "attributes": {
                                                "max_level_bonus": 0,
                                                "level": 1,
                                                "item_seen": True,
                                                "xp": 0,
                                                "variants": [],
                                                "favorite": False
                                            },
                                            "quantity": 1
                                        }
                                    }
                                    newitems.update(item_temp)
                
                profiles[username]['items']=dict(newitems)
                profiles[username]['stats']['attributes']['accountLevel']=level
                profiles[username]['stats']['attributes']['level']=level
                profiles[username]['stats']['attributes']['xp']=xp
                profiles[username]['stats']['attributes']['book_level']=0
                profiles[username]['stats']['attributes']['lifetime_wins']=top1
                profiles[username]['stats']['attributes']['book_xp']=0
                profiles[username]['stats']['attributes']['book_purchased']=False
                
                profiles[username]['stats']['attributes']['favorite_character']=f_char
                profiles[username]['stats']['attributes']['favorite_loadingscreen']=f_load
                profiles[username]['stats']['attributes']['favorite_backpack']=f_back
                profiles[username]['stats']['attributes']['favorite_dance']=f_dance
                profiles[username]['stats']['attributes']['favorite_skydivecontrail']=f_sky
                profiles[username]['stats']['attributes']['favorite_pickaxe']=f_pic
                profiles[username]['stats']['attributes']['favorite_glider']=f_glid
                profiles[username]['stats']['attributes']['favorite_musicpack']=f_music
                profiles[username]['stats']['attributes']['fortnite_character']=f_char
            
            elif i.replace('.json', '')=='common_core':
                profiles[username]['items']['Currency']['quantity']=mtx
                profiles[username]['items']['Token:FounderChatUnlock']['attributes']['level']=level
                profiles[username]['items']['Token:FounderChatUnlock']['attributes']['xp']=xp
                
            elif i.replace('.json', '')=='profile0':
                profiles[username]['items']['c5e97bfa-d599-42d0-a07e-735507956ba9']['quantity']=mtx
                profiles[username]['stats']['attributes']['level']=level
                profiles[username]['stats']['attributes']['xp']=xp
            
            profiles[username]['rvn']=0
            profiles[username]['commandRevision']=0
            profiles[username]['_id']=username
            profiles[username]['accountId']=username
            profiles[username]['updated']=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
            open(f'data/profiles/{i}', 'w', encoding='utf-8').write(dumps(profiles, indent=4))
    
    def createProfile(self, username: str):
        
        stats=self.req(f"SELECT top1 FROM stat WHERE username='{username}'")
        stats2=self.req(f"SELECT mtx, item, level, exp FROM users WHERE username='{username}'")
        favorites=self.req(f"SELECT * FROM favorites WHERE username='{username}'")
        
        try:
            mtx=int(stats2[0][0])
            items=list(str(stats2[0][1]).split(', '))
            level=int(stats2[0][2])
            xp=int(stats2[0][3])
            top1=int(stats[0][0])
            
            f_char=favorites[0][0]
            f_back=favorites[0][1]
            f_pic=favorites[0][2]
            f_glid=favorites[0][3]
            f_sky=favorites[0][4]
            f_music=favorites[0][5]
            f_load=favorites[0][6]
            f_dance=favorites[0][7]
            
        except:
            respon=self.createError(
                "errors.com.epicgames.account.invalid_profile",
                "Your profile does not exist. Please verify your account on our website: https://www.nocturno.games/", 
                [], 18031, "invalid_profile"
            )
            resp=self.app.response_class(
                response=dumps(respon),
                status=400,
                mimetype='application/json'
            )
            return resp
        
        osmkdir(f'data/friends/{username}')
        open(f'data/friends/{username}/friendslist.json', 'w', encoding='utf-8').write(dumps(
            [
                {
                    "accountId": "defaultprofile",
                    "status": "ACCEPTED",
                    "direction": "OUTBOUND",
                    "created": "0001-01-01T00:00:00.000Z",
                    "favorite": False
                }
            ], indent=4
        ))
        
        open(f'data/friends/{username}/friendslist2.json', 'w', encoding='utf-8').write(dumps(
            {
                "friends": [
                    {
                        "accountId": "defaultprofile",
                        "groups": [],
                        "mutual": 0,
                        "alias": "",
                        "note": "",
                        "favorite": False,
                        "created": "0001-01-01T00:00:00.000Z"
                    }
                ],
                "incoming": [],
                "outgoing": [],
                "suggested": [],
                "blocklist": [],
                "settings": {
                    "acceptInvites": "public"
                }
            }, indent=4
        ))
        
        seasondata=loads(open('data/profiles/seasondata.json', 'r', encoding='utf-8').read())
        
        seasondata[username]={}
        for i in range(9):
            nb=i+2
            seasondata[username].update({
                f"Season{nb}": {
                    "battlePassPurchased": False,
                    "battlePassTier": 1,
                    "battlePassXPBoost": 0,
                    "battlePassXPFriendBoost": 0
                }
            })
        
        open('data/profiles/seasondata.json', 'w', encoding='utf-8').write(dumps(seasondata, indent=4))
        
        for i in ['athena.json', 'profile0.json', 'common_core.json', 'common_public.json']:
            file=loads(open(f'data/profiles/{i}', 'r', encoding='utf-8').read())
            
            basicprofile=file['defaultprofile'].copy()
                    
            if file[username]:
                    return False
            
            if basicprofile['profileId']=='athena':
                
                newitems=self.new_items.copy()
                
                items_id=[]
                for p in items:
                    for x in self.exchange_table:
                        if p==x['name']:
                            items_id.append(x['id'])
                            
                for p in items_id:
                    for x in self.exchange_table:
                        if p==x['id']:
                            for z in self.conv_table:
                                if z['name']==x['style']:
                                    p=f"{z['id']}:{p}"
                                    item_temp={
                                        p: {
                                            "templateId": p,
                                            "attributes": {
                                                "max_level_bonus": 0,
                                                "level": 1,
                                                "item_seen": True,
                                                "xp": 0,
                                                "variants": [],
                                                "favorite": False
                                            },
                                            "quantity": 1
                                        }
                                    }
                                    newitems.update(item_temp)
                
                basicprofile['items']=dict(newitems)
                basicprofile['stats']['attributes']['accountLevel']=level
                basicprofile['stats']['attributes']['level']=level
                basicprofile['stats']['attributes']['xp']=xp
                basicprofile['stats']['attributes']['book_level']=0
                basicprofile['stats']['attributes']['lifetime_wins']=top1
                basicprofile['stats']['attributes']['book_xp']=0
                
                basicprofile['stats']['attributes']['favorite_character']=f_char
                basicprofile['stats']['attributes']['favorite_loadingscreen']=f_load
                basicprofile['stats']['attributes']['favorite_backpack']=f_back
                basicprofile['stats']['attributes']['favorite_dance']=f_dance
                basicprofile['stats']['attributes']['favorite_skydivecontrail']=f_sky
                basicprofile['stats']['attributes']['favorite_pickaxe']=f_pic
                basicprofile['stats']['attributes']['favorite_glider']=f_glid
                basicprofile['stats']['attributes']['favorite_musicpack']=f_music
                basicprofile['stats']['attributes']['fortnite_character']=f_char
            
            elif basicprofile['profileId']=='common_core':
                basicprofile['items']['Currency']['quantity']=mtx
                basicprofile['items']['Token:FounderChatUnlock']['attributes']['level']=level
                basicprofile['items']['Token:FounderChatUnlock']['attributes']['xp']=xp
                
            elif basicprofile['profileId']=='profile0':
                basicprofile['items']['c5e97bfa-d599-42d0-a07e-735507956ba9']['quantity']=mtx
                basicprofile['stats']['attributes']['level']=level
                basicprofile['stats']['attributes']['xp']=xp
            
            basicprofile['rvn']=0
            basicprofile['commandRevision']=0
            basicprofile['_id']=username
            basicprofile['accountId']=username
            basicprofile['created']=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            basicprofile['updated']=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                
            file.update({username: basicprofile})
            
            open(f'data/profiles/{i}', 'w', encoding='utf-8').write(dumps(file, indent=4))
    
    def checkProfile(self, accountId):
        athena=loads(open('data/profiles/athena.json', 'r', encoding='utf-8').read())
        ext=False
        if athena[accountId]:
            print('ext')
            ext=True
        if not ext:
            self.createProfile(accountId)
            return False
        return True
    
    def logs(self, logst: bool, msg):
        if logst:
            print(f'\nSERVER:[{self.createDate(0, 0, 0)}] - {msg}\n')
        else:
            pass