import json
from datetime import datetime

def getTheater(request):
    memory=getVersion(request=request)
    
    theater=json.load(open('data/connect/worldstw.json', 'r', encoding="utf-8"))
    Season=f"Season{memory['season']}"
    
    try:
        date=str(datetime.now()).replace(" ", "T")
        
        if memory["season"]>=9:
            date=date.split("T")[0]+"T23:59:59.999Z"
        else:
            if date<(date.split("T")[0] + "T05:59:59.999Z"):
                date=date.split("T")[0] + "T05:59:59.999Z"
            elif date<(date.split("T")[0] + "T11:59:59.999Z"):
                date=date.split("T")[0] + "T11:59:59.999Z"
            elif date<(date.split("T")[0] + "T17:59:59.999Z"):
                date=date.split("T")[0] + "T17:59:59.999Z"
            elif date<(date.split("T")[0] + "T23:59:59.999Z"):
                date=date.split("T")[0] + "T23:59:59.999Z"
                
        theater=theater.replace('2022-12-14T23:59:59.999Z', date)
    except:
        pass
    
    if "Seasonal" in theater:
        if "Season" in theater['Seasonal']:
            theater['theaters']=theater['theaters']+theater['Seasonal'][Season]['theaters']
            theater['missions']=theater['theaters']+theater['Seasonal'][Season]['missions']
            theater['missionAlerts']=theater['theaters']+theater['Seasonal'][Season]['missionAlerts']
        theater.pop('Seasonal')
    
    return theater

def getShop():
    catalog_config=json.load(open('data/Config/catalog_config.json', 'r', encoding="utf-8"))
    catalog=json.load(open('data/connect/catalog.json', 'r', encoding="utf-8"))

    for value in catalog_config:
        if isinstance(catalog_config[value]['itemGrants'], list):
            if len(catalog_config[value]['itemGrants']) != 0:
                catalog_entry = {
                    "devName": "",
                    "offerId": "",
                    "fulfillmentIds": [],
                    "dailyLimit": -1,
                    "weeklyLimit": -1,
                    "monthlyLimit": -1,
                    "categories": [],
                    "prices": [{
                        "currencyType": "MtxCurrency",
                        "currencySubType": "",
                        "regularPrice": 0,
                        "finalPrice": 0,
                        "saleExpiration": "9999-12-02T01:12:00Z",
                        "basePrice": 0
                    }],
                    "matchFilter": "",
                    "filterWeight": 0,
                    "appStoreId": [],
                    "requirements": [],
                    "offerType": "StaticPrice",
                    "giftInfo": {
                        "bIsEnabled": False,
                        "forcedGiftBoxTemplateId": "",
                        "purchaseRequirements": [],
                        "giftRecordIds": []
                    },
                    "refundable": True,
                    "metaInfo": [],
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
                                
                                if len(catalog_entry['itemGrants'])!=0:
                                    catalog['storefronts'][i]['catalogEntries'].append(catalog_entry)
    return catalog

def getContentPages(request):
    memory=getVersion(request=request)
    
    contentpage=json.load(open('data/connect/contentpages.json', 'r', encoding="Latin-1"))
    
    language="en"
    
    if request.headers["accept-language"]:
        if "-" in request.headers["accept-language"] and request.headers["accept-language"]!="es-419" and request.headers["accept-language"]!="pt-BR":
            language=request.headers["accept-language"].split("-")[0]
        else:
            language=request.headers["accept-language"]
            
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
                contentpage[mode]['news']['messages'][0]['image']="https://cdn.discordapp.com/attachments/1012885147240124496/1049090228666781726/zyro-image.png"
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
    
    return contentpage

def getVersion(request):
    memory={
        "season": 0,
        "build": 0.0,
        "CL": "",
        "lobby": ""
    }
    
    if request.headers["user-agent"]:
        try:
            BuildID=str(request.headers["user-agent"]).split("-")[3].split(",")[0]
            if not isinstance(BuildID, int):
                if " " in BuildID:
                    CL=BuildID.split(' ')[0]
                else:
                    CL=BuildID
                
            else:
                BuildID=str(request.headers["user-agent"]).split("-")[3].split(" ")[0]
                if not isinstance(BuildID, int):
                    if " " in BuildID:
                        CL=BuildID.split(' ')[0]
                    else:
                        CL=BuildID
        except:
            try:
                BuildID=str(request.headers["user-agent"]).split("-")[1].split("+")[0]
                if not isinstance(BuildID, int):
                    if " " in BuildID:
                        CL=BuildID.split(' ')[0]
                    else:
                        CL=BuildID
            except:
                pass
        
        try:
            Build=str(request.headers["user-agent"]).split("Release-")[1].split("-")[0]
            if len(Build.split("."))==3:
                Value=Build.split(".")
                Build=Value[0]+"."+Value[1]+Value[2]
                
            season=int(Build.split(".")[0])
            memory={
                "season": season,
                "build": int(Build),
                "CL": CL,
                "lobby": f"LobbyWinterDecor"
            }
            if int(season):
                TypeError
        except:
            memory={
                "season": 3,
                "build": 3.5,
                "CL": CL,
                "lobby": "LobbyWinterDecor"
            }
    return memory