from os import path as ospath
from os import mkdir as osmkdir
from os import stat as osstat
from json import loads, dumps
import random
from requests import get
from flask import Flask, request, Response, send_from_directory
from uuid import uuid4
from datetime import datetime
from hashlib import sha256, sha1
import base64

from modules.func import OldMPFunc as func
from modules.session import Session as sessions


class OldMP():
    def __init__(
        self, 
        cnx,
        dec, 
        enc, 
        logsapp: bool=True,
        app: Flask=Flask('OldMP'), 
        startWithProxy: bool=False, 
        api_url: str='https://nocturno.games/api', 
        proxy: dict={
            'http': 'http://127.0.0.1:9999', 
            'https': 'http://127.0.0.1:9999',
        },
        port: int=3551,
        sessionL: dict={},
        rps: dict={}, 
        playerscoords: list=[]
    ):

        self.playerscoords=playerscoords
        self.functions=func(request=request, app=app, cnx=cnx)
        self.NLogs=self.functions.logs
        self.NLogs(logsapp, "OmdMP started!")
        self.session=sessions(session=sessionL, req=request)

        @app.before_request
        def checkrps():
            exist=False
            for i in rps:
                if i==request.remote_addr:
                    exist=True
            if exist:
                if rps[request.remote_addr]>=20:
                    respon=self.functions.createError(
                        "errors.com.epicgames.account.too_many_requests",
                        "You have made more than the limited number of requests", 
                        [], 18031, "too_many_requests"
                    )
                    resp=app.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
                else:
                    rps[request.remote_addr]+=1
            else:
                rps.update({request.remote_addr: 0})
            
            

        @app.route('/clearitemsforshop', methods=['GET'])
        def cleanitemforshop():
            
            athena=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()
            shop=loads(open(f'data/content/catalogconfig.json', 'r', encoding='utf-8').read())
            StatChanged=False
            
            for value in shop:
                if isinstance(shop[value]['itemGrants'], list):
                    for key in athena['items']:
                        if isinstance(shop[value]['itemGrants'][0], str):
                            if len(shop[value]['itemGrants'][0])!=0:
                                if str(shop[value]['itemGrants'][0]).lower()==str(athena['items'][key]['templateId']).lower():
                                    list(athena['items']).remove(key)
                                    StatChanged=True
            if StatChanged:
                athena['rvn']+=1
                athena['commandRevision']+=1
                
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(athena, indent=4))
                
                resp=app.response_class(
                    response='Success',
                    status=200,
                    mimetype='text/plain'
                )
                return resp
            
            else:
                resp=app.response_class(
                    response='Failed, there are no items to remove',
                    status=500,
                    mimetype='text/plain'
                )
                return resp

        @app.route('/eulatracking/api/shared/agreements/fn', methods=['GET'])
        def eulatrackingapi():
            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/launcher/api/public/distributionpoints/', methods=['GET'])
        def publicdistrib():

            distrib={"distributions": [
                "https://epicgames-download1.akamaized.net/",
                "https://download.epicgames.com/",
                "https://download2.epicgames.com/",
                "https://download3.epicgames.com/",
                "https://download4.epicgames.com/",
                "https://oldmp.ol.epicgames.com/"
            ]}

            resp=app.response_class(
                response=dumps(distrib),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/launcher/api/public/assets/', methods=['GET'])
        def publicsaassets():
            assets={
                "appName": "FortniteContentBuilds",
                "labelName": "OldMP",
                "buildVersion": "++Fortnite+Release-20.00-CL-19458861-Windows",
                "catalogItemId": "5cb97847cee34581afdbc445400e2f77",
                "expires": self.functions.createDate(48),
                "items": {
                    "MANIFEST": {
                        "signature": "OldMP",
                        "distribution": "https://oldmp.ol.epicgames.com/",
                        "path": "",
                        "hash": "",
                        "additionalDistributions": []
                    },
                    "CHUNKS": {
                        "signature": "OldMP",
                        "distribution": "https://oldmp.ol.epicgames.com/",
                        "path": "",
                        "additionalDistributions": []
                    }
                },
                "assetId": "FortniteContentBuilds"
            }

            resp=app.response_class(
                response=dumps(assets),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/Builds/Fortnite/Content/CloudDir/*.manifest', methods=['GET'])
        def fortnitebuildclouddirmanifest():

            resp=app.response_class(
                response="",
                status=204,
                mimetype='application/octet-stream'
            )
            return resp
            
        @app.route('/Builds/Fortnite/Content/CloudDir/*.chunck', methods=['GET'])
        def fortnitebuildclouddirchunck():

            resp=app.response_class(
                response="",
                status=200,
                mimetype='application/octet-stream'
            )
            return resp

        @app.route('/Builds/Fortnite/Content/CloudDir/*.ini', methods=['GET'])
        def fortnitebuildclouddirini():

            resp=app.response_class(
                response=dumps({}),
                status=204,
                mimetype='application/json'
            )
            return resp

        @app.route('/waitingroom/api/waitingroom', methods=['GET'])
        def waitingroom():

            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/socialban/api/public/v1/', methods=['GET'])
        def socialbanapi():

            socialban={
                "bans": [],
                "warnings": []
            }

            resp=app.response_class(
                response=dumps(socialban),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route(f'/fortnite/api/stats/accountId/<accountId>/bulk/window/alltime', methods=['GET'])
        def statsapi(accountId):

            account={
                "startTime": 0,
                "endTime": 0,
                "stats": {},
                "accountId": self.session.get('username')
            }

            resp=app.response_class(
                response=dumps(account),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/api/v1/events/Fortnite/download/<accountId>', methods=['GET'])
        def apieventsdownload(accountId):
            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/friendcodes/<idk>/epic', methods=['GET'])
        def apifriendcodesepic(idk):
            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/events/tournamentandhistory/<idk>/EU/WindowsClient', methods=['GET'])
        def apiWindowsClientEU(idk):
            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/presence/api/v1/_/<account>/last-online', methods=['GET'])
        def apipresence(account):
            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/leaderboards/cohort/<account>', methods=['GET'])
        def fortniteapileaderboards(account):
            
            playlist=request.args.get('playlist')
            
            if playlist=='pc_m0_p2': # solo
                pass
            
            elif playlist=='pc_m0_p10': # duo
                pass
            
            elif playlist=='pc_m0_p9': # section
                pass
            
            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/leaderboards/type/group/stat/br_placetop<place>_pc_m0_p2/window/weekly', methods=['POST'])
        def leaderbordssolo(place):
            pass

        @app.route('/fortnite/api/leaderboards/type/group/stat/br_placetop<place>_pc_m0_p10/window/weekly', methods=['POST'])
        def leaderbordsduos(place):
            pass
        
        @app.route('/fortnite/api/leaderboards/type/group/stat/br_placetop<place>_pc_m0_p9/window/weekly', methods=['POST'])
        def leaderbordssquad(place):
            pass

        @app.route('/fortnite/api/game/v2/homebase/allowed-name-chars', methods=['GET'])
        def fortniteapihomebaseallowed():
            
            r={
                "ranges": [
                    48,
                    57,
                    65,
                    90,
                    97,
                    122,
                    192,
                    255,
                    260,
                    265,
                    280,
                    281,
                    286,
                    287,
                    304,
                    305,
                    321,
                    324,
                    346,
                    347,
                    350,
                    351,
                    377,
                    380,
                    1024,
                    1279,
                    1536,
                    1791,
                    4352,
                    4607,
                    11904,
                    12031,
                    12288,
                    12351,
                    12352,
                    12543,
                    12592,
                    12687,
                    12800,
                    13055,
                    13056,
                    13311,
                    13312,
                    19903,
                    19968,
                    40959,
                    43360,
                    43391,
                    44032,
                    55215,
                    55216,
                    55295,
                    63744,
                    64255,
                    65072,
                    65103,
                    65281,
                    65470,
                    131072,
                    173791,
                    194560,
                    195103
                ],
                "singlePoints": [
                    32,
                    39,
                    45,
                    46,
                    95,
                    126
                ],
                "excludedPoints": [
                    208,
                    215,
                    222,
                    247
                ]
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/receipts/v1/account/<account>/receipts', methods=['GET'])
        def apireceipts(account):
            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/region', methods=['GET'])
        def region():

            regions={
                "continent": {
                    "code": "EU",
                    "geoname_id": 6255148,
                    "names": {
                        "de": "Europa",
                        "en": "Europe",
                        "es": "Europa",
                        "fr": "Europe",
                        "ja": "ヨーロッパ",
                        "pt-BR": "Europa",
                        "ru": "Европа",
                        "zh-CN": "欧洲"
                    }
                },
                "country": {
                    "geoname_id": 2635167,
                    "is_in_european_union": False,
                    "iso_code": "GB",
                    "names": {
                        "de": "UK",
                        "en": "United Kingdom",
                        "es": "RU",
                        "fr": "Royaume Uni",
                        "ja": "英国",
                        "pt-BR": "Reino Unido",
                        "ru": "Британия",
                        "zh-CN": "英国"
                    }
                },
                "subdivisions": [
                    {
                        "geoname_id": 6269131,
                        "iso_code": "ENG",
                        "names": {
                            "de": "England",
                            "en": "England",
                            "es": "Inglaterra",
                            "fr": "Angleterre",
                            "ja": "イングランド",
                            "pt-BR": "Inglaterra",
                            "ru": "Англия",
                            "zh-CN": "英格兰"
                        }
                    },
                    {
                        "geoname_id": 3333157,
                        "iso_code": "KEC",
                        "names": {
                            "en": "Royal Kensington and Chelsea"
                        }
                    }
                ]
            }

            resp=app.response_class(
                response=dumps(regions),
                status=200,
                mimetype='application/json'
            )
            return resp

        # MatchMaking

        @app.route('/fortnite/api/matchmaking/session/findPlayer/<account>', methods=['GET'])
        def apisessionfindplayer(account):
            
            resp=Response()
            resp.status_code=200
            return resp

        @app.route('/fortnite/api/game/v2/matchmakingservice/ticket/player/<accountId>', methods=['GET'])
        def fortniteapigamev2mathcmakingplayerticket(accountId):
            
            ip=loads(open('conf.json', 'r', encoding='utf-8').read())['MatchMaking']['ip']
            port=loads(open('conf.json', 'r', encoding='utf-8').read())['MatchMaking']['port']

            r={
                "serviceUrl": f"ws://{ip}:{port}",
                "ticketType": "mms-player",
                "payload": "69=",
                "signature": "420="
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            resp.set_cookie("currentbuildUniqueId", request.args.get('bucketId').split(":")[0])
            return resp

        @app.route('/fortnite/api/game/v2/matchmaking/account/<accountId>/session/<sessionId>', methods=['GET'])
        def fortniteapigamev2mathcmakingsessionid(accountId, sessionId):

            r={
                "accountId": self.session.get('username'),
                "sessionId": self.session.get('sessionId'),
                "key": "KvOWLwXTUO6XyXsZGpK0_GvEKZatDxwb34-rJNUW8Fs="
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/matchmaking/session/<sessionId>', methods=['GET'])
        def apimatchmakingsessionid(sessionId):

            ip=loads(open('conf.json', 'r', encoding='utf-8').read())['GameServer']['ip']
            port=loads(open('conf.json', 'r', encoding='utf-8').read())['GameServer']['port']

            sessionCode={
                "id": self.session.get('sessionId'),
                "ownerId": str(uuid4()).replace("-", "").upper(),
                "ownerName": "[DS]fortnite-liveeugcec1c2e30ubrcore0a-z8hj-1968",
                "serverName": "[DS]fortnite-liveeugcec1c2e30ubrcore0a-z8hj-1968",
                "serverAddress": ip,
                "serverPort": int(port),
                "maxPublicPlayers": 220,
                "openPublicPlayers": 175,
                "maxPrivatePlayers": 0,
                "openPrivatePlayers": 0,
                "attributes": {
                    "REGION_s": "EU",
                    "GAMEMODE_s": "FORTATHENA",
                    "ALLOWBROADCASTING_b": True,
                    "SUBREGION_s": "GB",
                    "DCID_s": "FORTNITE-LIVEEUGCEC1C2E30UBRCORE0A-14840880",
                    "tenant_s": "Fortnite",
                    "MATCHMAKINGPOOL_s": "Any",
                    "STORMSHIELDDEFENSETYPE_i": 0,
                    "HOTFIXVERSION_i": 0,
                    "PLAYLISTNAME_s": "Playlist_DefaultSolo",
                    "SESSIONKEY_s": str(uuid4()).replace("-", "").upper(),
                    "TENANT_s": "Fortnite",
                    "BEACONPORT_i": 15009
                },
                "publicPlayers": [],
                "privatePlayers": [],
                "totalPlayers": 45,
                "allowJoinInProgress": False,
                "shouldAdvertise": False,
                "isDedicated": False,
                "usesStats": False,
                "allowInvites": False,
                "usesPresence": False,
                "allowJoinViaPresence": False,
                "allowJoinViaPresenceFriendsOnly": False,
                "buildUniqueId": request.cookies.get('currentbuildUniqueId') or "0",
                "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "started": False
            }

            resp=app.response_class(
                response=dumps(sessionCode),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/affiliate/api/public/affiliates/slug/<slugs>', methods=['GET'])
        def affiliateslug(slugs):
            
            SupportedCodes=loads([])
            
            ValidCode=False

            for code in SupportedCodes:
                if slugs==code:
                    ValidCode=True

                    slug={
                        "id": code,
                        "slug": code,
                        "displayName": code,
                        "status": "ACTIVE",
                        "verified": False
                    }

                    resp=app.response_class(
                        response=dumps(slug),
                        status=200,
                        mimetype='application/json'
                    )
                    return resp

            if not ValidCode:
                resp=app.response_class(
                    response=dumps(slug),
                    status=200,
                    mimetype='application/json'
                )
                return resp

        # CloudStorage

        @app.route('/fortnite/api/cloudstorage/user/<accountId>/<files>', methods=['PUT'])
        def fortnitecloudstorageuserfile(accountId, files):
            
            if files!="ClientSettings.Sav":
                resp=app.response_class(
                    response=dumps({"error": "file not found"}),
                    status=404,
                    mimetype='application/json'
                )
                return resp
            
            memory=self.functions.getVersion()
            currentBuildID=memory['CL']
            
            file=f'data/clientsettings/{self.session.get("username")}/ClientSettings-{currentBuildID}.Sav'
            data=request.stream.read().decode('latin1')
            open(file, 'w', encoding='latin1').write(data)

            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/fortnite/api/cloudstorage/system', methods=['GET'])
        def cloudstoragesystem():

            CloudFiles=[]

            for name in ['DefaultEngine.ini', 'DefaultGame.ini', 'DefaultRuntimeOptions.ini', 'DefaultInput.ini']:
                
                ParsedFile=open(f'data/cloudstorage/{name}', 'r', encoding="utf-8").read()
                mtime=ospath.getmtime(f'data/cloudstorage/{name}')
                
                if name=='DefaultEngine.ini':
                    ParsedFile.replace('ws://', 'tcp://')
                
                CloudFiles.append({
                    "uniqueFilename": name,
                    "filename": name,
                    "hash": sha1(ParsedFile.encode()).hexdigest(),
                    "hash256": sha256(ParsedFile.encode()).hexdigest(),
                    "length": len(ParsedFile),
                    "contentType": "application/octet-stream",
                    "uploaded": datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "storageType": "S3",
                    "storageIds": {},
                    "doNotCache": True
                })
                    
            resp=app.response_class(
                response=dumps(CloudFiles),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route("/fortnite/api/cloudstorage/system/<file>", methods=["GET"])
        def get_file(file):
            
            file_path=f'data/cloudstorage/{file}'
            if ospath.exists(file_path):
                return send_from_directory('data/cloudstorage', file)
            
            else:
                resp=Response()
                resp.status_code=200
                return resp
            
        @app.route('/fortnite/api/cloudstorage/user/<account>/<files>', methods=['GET'])
        def cloudstoragesystemallfile(account, files):
            
            if not ospath.exists(f'data/clientsettings/{self.session.get("username")}/'):
                osmkdir(f'data/clientsettings/{self.session.get("username")}/')
            
            if files!="ClientSettings.Sav":
                resp=app.response_class(
                    response=dumps({"error": "file not found"}),
                    status=404,
                    mimetype='application/json'
                )
                return resp
            
            memory=self.functions.getVersion()
            currentBuildID=memory['CL']
            season=memory['season']
            
            if int(season)<3:
                resp=Response()
                resp.status_code=204
                return resp
            else:
                if ospath.exists(f'data/clientsettings/{self.session.get("username")}/ClientSettings-{currentBuildID}.Sav'):
                    return send_from_directory(f'data/clientsettings/{self.session.get("username")}/', f'ClientSettings-{currentBuildID}.Sav')
                
                else:
                    resp=Response()
                    resp.status_code=204
                    return resp

        @app.route(f'/fortnite/api/cloudstorage/user/<accountId>', methods=['GET'])
        def cloudstorageaccid(accountId):
            
            
            if not ospath.exists(f'data/clientsettings/{self.session.get("username")}/'):
                osmkdir(f'data/clientsettings/{self.session.get("username")}/')
            
            memory=self.functions.getVersion()
            currentBuildID=memory['CL']
            
            file=f'data/clientsettings/{self.session.get("username")}/ClientSettings-{currentBuildID}.Sav'
            
            if ospath.exists(file):
                
                ParsedFile=open(file, 'r', encoding="Latin-1").read()
                
                result=[{
                    "uniqueFilename": "ClientSettings.Sav",
                    "filename": "ClientSettings.Sav",
                    "hash": sha1(ParsedFile.encode()).hexdigest(),
                    "hash256": sha256(ParsedFile.encode()).hexdigest(),
                    "length": len(ParsedFile),
                    "contentType": "application/octet-stream",
                    "uploaded": osstat(file).st_mtime,
                    "storageType": "S3",
                    "storageIds": {},
                    "accountId": self.session.get('username'),
                    "doNotCache": True
                }]
                
                resp=app.response_class(
                    response=dumps(result),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
            else:
                
                resp=app.response_class(
                    response=dumps([]),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
        @app.route('/content/api/pages/', methods=['GET'])
        @app.route('/content/api/pages/fortnite-game', methods=['GET'])
        def contentapipages():
            
            contentpages=self.functions.getContentPages()
            
            resp=app.response_class(
                response=dumps(contentpages),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/links/api/fn/mnemonic/', methods=['GET'])
        def linksmnemonic():
                
            discover=loads(open(f'data/content/discover_frontend.json.json', 'r', encoding='utf-8').read())
            
            for i in discover['Panels'][0]['Pages'][0]['results']:
                if discover['Panels'][0]['Pages'][0]['results'][i]['linkData']['mnemonic']==request.url.split("/").slice(-1)[0]:
            
                    resp=app.response_class(
                        response=dumps(discover['Panels'][0]['Pages'][0]['results'][i]['linkData']),
                        status=200,
                        mimetype='application/json'
                    )
                    return resp

        @app.route('/friends/api/v1/<account>/settings', methods=['GET'])
        def friendssettings(account):
            
            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/friends/api/v1/<account>/blocklist', methods=['GET'])
        def friendsblocklist(account):
            
            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route(f'/friends/api/public/friends/<accountId>', methods=['GET'])
        def friendsaccountID(accountId):
            
            
            memory=self.functions.getVersion()
            friendslist=loads(open(f'data/friends/{self.session.get("username")}/friendslist.json', 'r', encoding='utf-8').read())
            friendslist2=loads(open(f'data/friends/{self.session.get("username")}/friendslist2.json', 'r', encoding='utf-8').read())

            if not any(i['accountId']==request.args.get('accountId') for i in friendslist):
                FriendObject={
                    "accountId": self.session.get("username"),
                    "status": "ACCEPTED",
                    "direction": "OUTBOUND",
                    "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "favorite": False
                }
                friendslist.append(FriendObject)
                friendslist2['friends'].append({
                    "accountId": FriendObject['accountId'],
                    "groups": [],
                    "mutual": 0,
                    "alias": "",
                    "note": "",
                    "favorite": FriendObject['favorite'],
                    "created": FriendObject['created']
                })
                
                self.functions.sendXmppMessageToAll({
                    "payload": FriendObject,
                    "type": "com.epicgames.friends.core.apiobjects.Friend",
                    "timestamp": FriendObject['created']
                })

                self.functions.sendXmppMessageToAll({
                    "type": "FRIENDSHIP_REQUEST",
                    "timestamp": FriendObject['created'],
                    "from": FriendObject['accountId'],
                    "status": FriendObject['status']
                })
            
            open(f'data/friends/{self.session.get("username")}/friendslist.json', 'w', encoding='utf-8').write(dumps(friendslist, indent=4))
            open(f'data/friends/{self.session.get("username")}/friendslist2.json', 'w', encoding='utf-8').write(dumps(friendslist2, indent=4))

            if memory['season']>=7:
                friends=friendslist.copy()
                print(friends + "dsfiughiuhjd<qfbvhuhijdsfguhhdsfiuhjgh")
                for i in friends:
                    if i['accountId']==request.args.get('accountId'):
                        friends.remove(i)
                resp=app.response_class(
                    response=dumps(friends),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
            resp=app.response_class(
                response=dumps(friendslist),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route(f'/friends/api/v1/<accountId>/summary', methods=['GET'])
        def friendsaccountIDsummary(accountId):
            
                
            friendslist=loads(open(f'data/friends/{self.session.get("username")}/friendslist.json', 'r', encoding='utf-8').read())
            friendslist2=loads(open(f'data/friends/{self.session.get("username")}/friendslist2.json', 'r', encoding='utf-8').read())

            if not any(i['accountId']==request.args.get('accountId') for i in friendslist2['friends']):
                FriendObject={
                    "accountId": self.session.get("username"),
                    "groups": [],
                    "mutual": 0,
                    "alias": "",
                    "note": "",
                    "favorite": False,
                    "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                friendslist2['friends'].append(FriendObject)
                friendslist.append({
                    "accountId": FriendObject['accountId'],
                    "status": "ACCEPTED",
                    "direction": "OUTBOUND",
                    "favorite": FriendObject['favorite'],
                    "created": FriendObject['created']
                })
                
                self.functions.sendXmppMessageToAll({
                    "payload": {
                        "accountId": FriendObject['accountId'],
                        "status": "ACCEPTED",
                        "direction": "OUTBOUND",
                        "created": FriendObject['created'],
                        "favorite": FriendObject['favorite']
                    },
                    "type": "com.epicgames.friends.core.apiobjects.Friend",
                    "timestamp": FriendObject['created']
                })

                self.functions.sendXmppMessageToAll({
                    "type": "FRIENDSHIP_REQUEST",
                    "timestamp": FriendObject['created'],
                    "from": FriendObject['accountId'],
                    "status": "ACCEPTED"
                })
            
            open(f'data/friends/{self.session.get("username")}/friendslist.json', 'w', encoding='utf-8').write(dumps(friendslist, indent=4))
            open(f'data/friends/{self.session.get("username")}/friendslist2.json', 'w', encoding='utf-8').write(dumps(friendslist2, indent=4))

            resp=app.response_class(
                response=dumps(friendslist),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/friends/api/public/list/fortnite/<account>/recentPlayers', methods=['GET'])
        def friendsrecentplayers(account):
            
            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/friends/api/public/blocklist/<account>', methods=['GET'])
        def friendsblocklistall(account):
            
            blocked={
                "blockedUsers": []
            }

            resp=app.response_class(
                response=dumps(blocked),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/lightswitch/api/service/Fortnite/status', methods=['GET'])
        def lightswitchservicestatus():
            
            service={
                "serviceInstanceId": "fortnite",
                "status": "UP",
                "message": "Fortnite is online",
                "maintenanceUri": None,
                "overrideCatalogIds": [
                "a7f138b2e51945ffbfdacc1af0541053"
                ],
                "allowedActions": [],
                "banned": False,
                "launcherInfoDTO": {
                "appName": "Fortnite",
                "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
                "namespace": "fn"
                }
            }

            resp=app.response_class(
                response=dumps(service),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/lightswitch/api/service/bulk/status', methods=['GET'])
        def lightswitchservicebulkstatus():
            
            stat=self.functions.req(f"SELECT status FROM users WHERE `ip`='{request.remote_addr}'")
            status=False
            if stat==[]:
                pass
            else:
                if 'ban' in stat[0]:
                    status=True
            
            service2=[{
                "serviceInstanceId": "fortnite",
                "status": "UP",
                "message": "fortnite is up.",
                "maintenanceUri": None,
                "overrideCatalogIds": [
                    "a7f138b2e51945ffbfdacc1af0541053"
                ],
                "allowedActions": [
                    "PLAY",
                    "DOWNLOAD"
                ],
                "banned": status,
                "launcherInfoDTO": {
                    "appName": "Fortnite",
                    "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
                    "namespace": "fn"
                }
            }]

            resp=app.response_class(
                response=dumps(service2),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/party/api/v1/Fortnite/user/', methods=['GET'])
        def partyapiuser():
            
            party={
                "current": [],
                "pending": [],
                "invites": [],
                "pings": []
            }

            resp=app.response_class(
                response=dumps(party),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route(f'/fortnite/api/game/v2/privacy/account/<accountId>', methods=['GET'])
        def privacyaccountid(accountId):
            
            
            privacy=loads(open(f'data/account/privacy.json', 'r', encoding='utf-8').read())
            
            privacy['accountId']=self.session.get('username')

            resp=app.response_class(
                response=dumps(privacy),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/storefront/v2/catalog', methods=['GET'])
        def fortnitestorefrontcatalogv2():
            if "2870186" in request.headers.get('user-agent'):

                resp=Response()
                resp.status_code=404
                return resp
            
            catalog=self.functions.getShop()

            resp=app.response_class(
                response=dumps(catalog),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/storefront/v2/keychain', methods=['GET'])
        def storefrontkeychain():
            
            keychain=loads(open(f'data/items/keychain.json', 'r', encoding='utf-8').read())

            resp=app.response_class(
                response=dumps(keychain),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/catalog/api/shared/bulk/offers', methods=['GET'])
        def catalogapisharedoffers():

            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/calendar/v1/timeline', methods=['GET'])
        def apitimeline():

            memory=self.functions.getVersion()
            
            activeEvents=[
            {
                "eventType": f'EventFlag.Season{memory["season"]}',
                "activeUntil": "9999-12-31T00:00:00.000Z",
                "activeSince": "0001-01-01T00:00:00.000Z"
            },
            {
                "eventType": f'EventFlag.{memory["lobby"]}',
                "activeUntil": "9999-12-31T00:00:00.000Z",
                "activeSince": "0001-01-01T00:00:00.000Z"
            }]
            
            if memory["season"]==3:
                activeEvents.append({
                    "eventType": "EventFlag.Spring2018Phase1",
                    "activeUntil": self.functions.createDate(9999),
                    "activeSince": "0001-01-01T00:00:00.000Z"
                })
                if memory['build']>=3.1:
                    activeEvents.append({
                        "eventType": "EventFlag.Spring2018Phase2",
                        "activeUntil": self.functions.createDate(9999),
                        "activeSince": "0001-01-01T00:00:00.000Z"
                    })
                if memory['build']>=3.3:
                    activeEvents.append({
                        "eventType": "EventFlag.Spring2018Phase3",
                        "activeUntil": "9999-12-31T00:00:00.000Z",
                        "activeSince": "0001-01-01T00:00:00.000Z"
                    })
                if memory['build']>=3.4:
                    activeEvents.append({
                        "eventType": "EventFlag.Spring2018Phase4",
                        "activeUntil": "9999-12-31T00:00:00.000Z",
                        "activeSince": "0001-01-01T00:00:00.000Z"
                    })
            if memory["season"]==4:
                activeEvents.append({
                    "eventType": "EventFlag.Blockbuster2018",
                    "activeUntil": "9999-12-31T00:00:00.000Z",
                    "activeSince": "0001-01-01T00:00:00.000Z"
                },
                {
                    "eventType": "EventFlag.Blockbuster2018Phase1",
                    "activeUntil": "9999-12-31T00:00:00.000Z",
                    "activeSince": "0001-01-01T00:00:00.000Z"
                })
                if memory['build']>=4.3:
                    activeEvents.append({
                        "eventType": "EventFlag.Blockbuster2018Phase2",
                        "activeUntil": "9999-12-31T00:00:00.000Z",
                        "activeSince": "0001-01-01T00:00:00.000Z"
                    })
                if memory['build']>=4.4:
                    activeEvents.append({
                        "eventType": "EventFlag.Blockbuster2018Phase3",
                        "activeUntil": "9999-12-31T00:00:00.000Z",
                        "activeSince": "0001-01-01T00:00:00.000Z"
                    })
                if memory['build']>=4.5:
                    activeEvents.append({
                        "eventType": "EventFlag.Blockbuster2018Phase4",
                        "activeUntil": "9999-12-31T00:00:00.000Z",
                        "activeSince": "0001-01-01T00:00:00.000Z"
                    })
            if memory["season"]==5:
                activeEvents.append({
                    "eventType": "EventFlag.RoadTrip2018",
                    "activeUntil": "9999-12-31T00:00:00.000Z",
                    "activeSince": "0001-01-01T00:00:00.000Z"
                },
                {
                    "eventType": "EventFlag.Horde",
                    "activeUntil": "9999-12-31T00:00:00.000Z",
                    "activeSince": "0001-01-01T00:00:00.000Z"
                },
                {
                    "eventType": "EventFlag.Anniversary2018_BR",
                    "activeUntil": "9999-12-31T00:00:00.000Z",
                    "activeSince": "0001-01-01T00:00:00.000Z"
                },
                {
                    "eventType": "EventFlag.LTM_Heist",
                    "activeUntil": "9999-12-31T00:00:00.000Z",
                    "activeSince": "0001-01-01T00:00:00.000Z"
                })
            if memory['build']==5.10:
                activeEvents.append({
                    "eventType": "EventFlag.BirthdayBattleBus",
                    "activeUntil": "9999-12-31T00:00:00.000Z",
                    "activeSince": "0001-01-01T00:00:00.000Z"
                })

            r={
                "channels": {
                    "client-matchmaking": {
                        "states": [],
                        "cacheExpire": self.functions.createDate(48)
                    },
                    "client-events": {
                        "states": [{
                            "validFrom": "2022-01-01T13:00:000Z",
                            "activeEvents": activeEvents,
                            "state": {
                                "activeStorefronts": [],
                                "eventNamedWeights": {},
                                "seasonNumber": memory["season"],
                                "seasonTemplateId": f'AthenaSeason:athenaseason{memory["season"]}',
                                "matchXpBonusPoints": 0,
                                "seasonBegin": "2022-01-01T13:00:000Z",
                                "seasonEnd": "9999-12-31T00:00:00.000Z",
                                "seasonDisplayedEnd": "9999-12-31T00:00:00.000Z",
                                "weeklyStoreEnd": self.functions.createDate(168),
                                "stwEventStoreEnd": "9999-12-31T00:00:00.000Z",
                                "stwWeeklyStoreEnd": "9999-12-31T00:00:00.000Z",
                                "dailyStoreEnd": self.functions.createDate(24)
                            }
                        }],
                        "cacheExpire": self.functions.createDate(48)
                    }
                },
                "eventsTimeOffsetHrs": 0,
                "cacheIntervalMins": 10,
                "currentTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/account/api/public/account', methods=['GET'])
        def accountpublicaccount():
            
            response=[]
            accountIds=request.args.getlist('accountId')
            for accountId in accountIds:
                if isinstance(accountId, str):
                    accountId=accountId
                    if "@" in accountId:
                        accountId=accountId.split("@")[0]
                        
                    response.append({
                        "id": accountId,
                        "displayName": accountId,
                        "externalAuths": {}
                    })
                
                if isinstance(accountId, list):
                    for x in accountId:
                        accountId=accountId[x]
                        if "@" in accountId:
                            accountId=accountId.split("@")[0]
                        
                        response.append({
                            "id": accountId,
                            "displayName": accountId,
                            "externalAuths": {}
                        })

            resp=app.response_class(
                response=dumps(response),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route(f'/account/api/public/account/<account>', methods=['GET'])
        def accountpublicaccountid(account):
            
            
            r={
                "id": self.session.get('username'),
                "displayName": self.session.get('username'),
                "name": self.session.get('username'),
                "email": f"{self.session.get('username')}@oldmp.softawre",
                "failedLoginAttempts": 0,
                "lastLogin": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "numberOfDisplayNameChanges": 0,
                "ageGroup": "UNKNOWN",
                "headless": False,
                "country": "FR",
                "lastName": "MP",
                "preferredLanguage": "fr",
                "canUpdateDisplayName": True,
                "tfaEnabled": False,
                "emailVerified": True,
                "minorVerified": False,
                "minorExpected": False,
                "minorStatus": "UNKNOWN"
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/account/api/public/account/<accountId>/externalAuths', methods=['GET'])
        def accountpublicexternalauths(accountId):
            
            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/account/api/oauth/verify', methods=['GET'])
        def accountoauthverify():
            
            btoken=request.headers.get('authorization').split("bearer ")[1]
            tkn=btoken.split('NOCTURNOISBETTER_')[1].encode()
            token=dec(tkn).decode()

            username=self.session.get('username')
            password=self.session.get('password')
            
            if username and password:
                pass
            else:
                respon=self.functions.createError(
                    "errors.com.epicgames.account.invalid_account_credentials",
                    "Your username and/or password are incorrect. Please verify your account on our website: https://www.nocturno.games/", 
                    [], 18031, "invalid_grant"
                )
                resp=app.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                return resp
            
            r={
                "token": btoken,
                "session_id": self.session.get('sessionId'),
                "token_type": "bearer",
                "client_id": self.session.get('clientId'),
                "internal_client": True,
                "client_service": "fortnite",
                "account_id": self.session.get('username'),
                "expires_in": 86400,
                "expires_at": self.functions.createDate(24),
                "auth_method": "exchange_code",
                "display_name": self.session.get('username'),
                "app": "fortnite",
                "in_app_id": self.session.get('username'),
                "device_id": self.session.get('deviceId')
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/account/api/epicdomains/ssodomains', methods=['GET'])
        def accountssodomains():

            r=[
                "unrealengine.com",
                "unrealtournament.com",
                "fortnite.com",
                "epicgames.com"
            ]

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            
            return resp

        @app.route('/fortnite/api/version', methods=['GET'])
        def fortniteapiversions():

            r={
                "app": "fortnite",
                "serverDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "overridePropertiesVersion": "unknown",
                "cln": "17951730",
                "build": "444",
                "moduleName": "Fortnite-Core",
                "buildDate": "2021-10-27T21:00:51.697Z",
                "version": "18.30",
                "branch": "Release-18.30",
                "modules": {
                "Epic-LightSwitch-AccessControlCore": {
                    "cln": "17237679",
                    "build": "b2130",
                    "buildDate": "2021-08-19T18:56:08.144Z",
                    "version": "1.0.0",
                    "branch": "trunk"
                },
                "epic-xmpp-api-v1-base": {
                    "cln": "5131a23c1470acbd9c94fae695ef7d899c1a41d6",
                    "build": "b3595",
                    "buildDate": "2019-07-30T09:11:06.587Z",
                    "version": "0.0.1",
                    "branch": "master"
                },
                "epic-common-core": {
                    "cln": "17909521",
                    "build": "3217",
                    "buildDate": "2021-10-25T18:41:12.486Z",
                    "version": "3.0",
                    "branch": "TRUNK"
                }
                }
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/v2/versioncheck/<version>', methods=['GET'])
        def fortniteapiv2versioncheck(version):

            r={"type": "NO_UPDATE"}

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/v2/versioncheck', methods=['GET'])
        def fortniteapiv2versioncheck2():

            r={"type": "NO_UPDATE"}

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/versioncheck', methods=['GET'])
        def fortniteapiversioncheck():

            r={"type": "NO_UPDATE"}

            resp=app.response_class(
                response=dumps(r),
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/grant_access/<accountId>', methods=['POST'])
        def fortniteapiv2grantacces(accountId):

            resp=app.response_class(
                response=dumps({}),
                status=204,
                mimetype='application/json'
            )
            return resp

        @app.route('/api/v1/user/setting', methods=['POST'])
        def apiv1settings():

            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/feedback/', methods=['POST'])
        def apiv1feedback():

            resp=Response()
            resp.status_code=200
            return resp

        @app.route('/fortnite/api/statsv2/account/<accountId>', methods=['GET'])
        def fortnitestatsv2account(accountId):

            # set account

            r={
                "startTime": 0,
                "endTime": 0,
                "stats": {},
                "accountId": self.session.get('username')
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/statsproxy/api/statsv2/account/<accountId>', methods=['GET'])
        def statproxystatsv2account(accountId):

            # set account

            r={
                "startTime": 0,
                "endTime": 0,
                "stats": {},
                "accountId": self.session.get('username')
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/statsv2/query', methods=['POST'])
        def fortnitestatsv2query():

            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/statsproxy/api/statsv2/query', methods=['POST'])
        def statproxystatsv2query():

            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/events/v2/setSubgroup/', methods=['POST'])
        def fortniteapigamev2setSubgroup():

            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/fortnite/api/game/v2/chat/<idk1>/<idk2>/<idk3>/pc', methods=['POST'])
        def fortnitechatpcgame(idk1, idk2, idk3):

            resp=app.response_class(
                response=dumps({ "GlobalChatRooms": [{"roomName":"OldMPglobal"}] }),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/chat/<account>/recommendGeneralChatRooms/pc', methods=['POST'])
        def fortnitegamev2recommendGeneralChatRoomspc(account):

            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/datarouter/api/v1/public/data', methods=['POST'])
        def datarouterapipublicdata():

            data=request.stream.read()
            print(data)
            for events in loads(data.decode())['Events']:
                for event in events:
                    if event=='PlayerLocation':
                        if events[event]=='':
                            pass
                        else:
                            print(events[event])
                            coords=str(events[event]).split(',')
                            print(coords)
                            x=int(round(coords[0]))
                            y=int(round(coords[1]))
                            self.playerscoords.append((x, y))
                        
                    elif event=='AthenaPlayersLeft':
                        print(events[event])
                        self.session.put('partyPlayerLeft', int(events[event]))
                        
                    elif event=='Location':
                        if events[event]=='InGame':
                            self.session.put('InGame', True)
                        else:
                            self.session.put('InGame', False)
                    
                    elif event=='AthenaMapName':
                        print(events[event])
                        self.session.put('mapName', events[event])
                    
                    elif event=='EventName':
                        if events[event]=='SessionEnd':
                            print('session clear')
                            self.session.clear()

            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/fortnite/api/matchmaking/session/<sessionId>/join', methods=['POST'])
        def fortnitematchmakingjoin(sessionId):

            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/fortnite/api/matchmaking/session/matchMakingRequest', methods=['POST'])
        def fortnitematchmakingsessionmatchMakingRequest():

            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/<idk>/discovery/surface/', methods=['POST'])
        def discoverysurfaceall(idk):

            discovery=loads(open(f'data/content/discover_frontend.json.json', 'r', encoding='utf-8').read())

            resp=app.response_class(
                response=dumps(discovery),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/links/api/fn/mnemonic', methods=['POST'])
        def linksfnmnemonic():

            MnemonicArray=[]
                
            discovery=loads(open(f'data/content/discover_frontend.json.json', 'r', encoding='utf-8').read())
                
            for i in discovery['Panels'][0]['Pages'][0]['results']:
                MnemonicArray.append(['Panels'][0]['Pages'][0]['results'][i]['linkData'])

            resp=app.response_class(
                response=dumps(MnemonicArray),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/party/api/v1/Fortnite/parties', methods=['POST'])
        def partyfortniteapiparties():
            
            if not loads(request.get_data())['join_info']:
                resp=app.response_class(
                    response=dumps({}),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            if not loads(request.get_data())['join_info']['connection']:
                resp=app.response_class(
                    response=dumps({}),
                    status=200,
                    mimetype='application/json'
                )
                return resp

            party={
                "id": str(uuid4()).replace("-", ""),
                "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "config": {
                    "type": "DEFAULT",
                    f"{[i for i in loads(request.get_data())['config']]}"
                    "discoverability": "ALL",
                    "sub_type": "default",
                    "invite_ttl": 14400,
                    "intention_ttl": 60
                },
                "members": [{
                    "account_id": (loads(request.get_data())['join_info']['connection']['id'] or "").split("@prod")[0],
                    "meta": loads(request.get_data())['join_info']['meta'] or {},
                    "connections": [
                        {
                            "id": loads(request.get_data())['join_info']['connection']['id'] or "",
                            "connected_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "yield_leadership": False,
                            "meta": loads(request.get_data())['join_info']['connection']['meta'] or {}
                        }
                    ],
                    "revision": 0,
                    "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "joined_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "role": "CAPTAIN"
                }],
                "applicants": [],
                "meta": loads(request.get_data())['meta'] or {},
                "invites": [],
                "revision": 0,
                "intentions": []
            }

            resp=app.response_class(
                response=dumps(party),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route(f'/fortnite/api/game/v2/privacy/account/<accountId>', methods=['POST'])
        def fortniteapigamev2accountId(accountId):

            # set account

            privacy=loads(open(f'data/account/privacy.json', 'r', encoding='utf-8').read())
                
            privacy['accountId']=self.session.get('username')
            privacy['optOutOfPublicLeaderboards']=loads(request.get_data())['optOutOfPublicLeaderboards']
            
            open(f'data/account/privacy.json', 'w', encoding='utf-8').write(dumps(privacy, indent=4))

            resp=app.response_class(
                response=dumps(privacy),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/account/api/oauth/token', methods=['POST'])
        def accountoauthtoken():

            ip=request.remote_addr

            try:
                clientId=base64.b64decode(request.headers["authorization"].split(" ")[1]).decode().split(":")[0]
            
            except:
                respon=self.functions.createError(
                    "errors.com.epicgames.common.oauth.invalid_client",
                    "It appears that your Authorization header may be invalid or not present.", 
                    [], 1011, "invalid_client"
                )
                resp=app.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                return resp
            
            granttype=request.get_data().decode().split('&')[0].split('=')[1]
            
            self.NLogs(logsapp, f"Grant type: {granttype}")
            
            if granttype=="client_credentials":
                token=self.functions.genToken(ip, clientId, enc)
                self.session.put('token', token)
                r={
                    "access_token": token,
                    "expires_in": 14400,
                    "expires_at": self.functions.createDate(4),
                    "token_type": "bearer",
                    "client_id": clientId,
                    "internal_client": True,
                    "client_service": "fortnite"
                }
                
                resp=app.response_class(
                    response=dumps(r),
                    status=200,
                    mimetype='application/json'
                )
                return resp
                
            elif granttype=="password":
                username=str(request.get_data().decode()).split("&")[1].split('=')[1]
                password=str(request.get_data().decode()).split("&")[2].split('=')[1]
                
                if startWithProxy:
                    r=get(f'{api_url}/get/check.php?user={username}&pass={password}', verify=False, proxies=proxy).text
                else:
                    r=get(f'{api_url}/get/check.php?user={username}&pass={password}', verify=False).text
                    
                if not 'ok' in r:
                    self.NLogs(logsapp, "Clients bad logins")
                    respon=self.functions.createError(
                        "errors.com.epicgames.account.invalid_account_credentials",
                        "Your username and/or password are incorrect. Please verify your account on our website: https://www.nocturno.games/", 
                        [], 18031, "invalid_grant"
                    )
                    resp=app.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
                
                if not username or not password:
                    respon=self.functions.createError(
                        "errors.com.epicgames.common.oauth.invalid_request",
                        "Username/password is required.", 
                        [], 1013, "invalid_request"
                    )
                    resp=app.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp

                self.functions.loadProfile(username)

                self.session.put('username', username)
                self.session.put('password', password)
                self.session.put('clientId', clientId)
                
            elif granttype=="refresh_token":
                
                refreshtoken=request.get_data().decode().split('&')[1].split('=')[1]
                self.NLogs(logsapp, f"Refresh token: {refreshtoken}")
                if not refreshtoken:
                    respon=self.functions.createError(
                        "errors.com.epicgames.common.oauth.invalid_request",
                        "Refresh token is required.", 
                        [], 1013, "invalid_request"
                    )
                    resp=app.response_class(
                        response=dumps(respon),
                        status=400,
                        mimetype='application/json'
                    )
                    return resp
                
                try:
                    refresh_token=dec(str(refreshtoken).replace('NOCTURNOISBETTER_', '').encode()).decode()
                    if not token.split('|')[1].split(':')[1]==request.remote_addr:
                        respon=self.functions.createError(
                            "errors.com.epicgames.account.auth_token.invalid_refresh_token",
                            f"Sorry the refresh token '{refresh_token}' is invalid", 
                            [refresh_token], 18036, "invalid_grant"
                        )
                        resp=app.response_class(
                            response=dumps(respon),
                            status=400,
                            mimetype='application/json'
                        )
                        return resp
                except:
                    self.NLogs(logsapp, "refreshtoken Error")
            
            elif granttype=="exchange_code":
                pass
        
            else:
                respon=self.functions.createError(
                    "errors.com.epicgames.common.oauth.unsupported_grant_type",
                    f"Unsupported grant type: {granttype}", 
                    [], 1016, "unsupported_grant_type"
                )
                resp=app.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                return resp

            r={
                "access_token": self.session.get('token'),
                "expires_in": 28800,
                "expires_at": self.functions.createDate(8),
                "token_type": "bearer",
                "refresh_token": self.session.get('token'),
                "refresh_expires": 86400,
                "refresh_expires_at": self.functions.createDate(24),
                "account_id": self.session.get('username'),
                "client_id": self.session.get('clientId'),
                "internal_client": True,
                "client_service": "fortnite",
                "displayName": self.session.get('username'),
                "app": "fortnite",
                "in_app_id": self.session.get('username'),
                "device_id": self.session.get('deviceId')
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/account/api/oauth/exchange', methods=['POST'])
        def accountoauthexchange():

            resp=app.response_class(
                response=dumps({}),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/account/api/oauth/sessions/kill', methods=['DELETE'])
        def accountoauthsessionskill():
            token=request.headers.get('authorization').split("bearer ")[1]
            token=dec(token.split('NOCTURNOISBETTER_')[1].encode()).decode()

            killType=request.args.get('killType')
            
            self.NLogs(logsapp, f"Kill type: {killType}")
            
            if killType=='ALL':
                self.session.clear()
            
            elif killType=='OTHERS':
                pass
            
            elif killType=='ALL_ACCOUNT_CLIENT':
                self.session.clear()
            
            elif killType=='OTHERS_ACCOUNT_CLIENT':
                pass
            
            elif killType=='OTHERS_ACCOUNT_CLIENT_SERVICE':
                pass
            
            else:
                respon=self.functions.createError(
                    "errors.com.epicgames.common.oauth.invalid_request",
                    "A valid killType is required.",
                    [], 1013, "invalid_request"
                )
                self.session.clear()
                resp=app.response_class(
                    response=dumps(respon),
                    status=400,
                    mimetype='application/json'
                )
                return resp

            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/account/api/oauth/sessions/kill/<token>', methods=['DELETE'])
        def accountoauthsessionskillall(token):
            
            self.session.clear()
            
            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/fortnite/api/game/v2/tryPlayOnPlatform/account/<accountId>', methods=['POST'])
        def fortniteapigamev2tryPlayOnPlatform(accountId):

            resp=app.response_class(
                response="True",
                status=200,
                mimetype='text/plain'
            )
            return resp

        @app.route('/party/api/v1/Fortnite/parties/', methods=['ALL'])
        def partyapiv1parties():

            resp=Response()
            resp.status_code=204
            return resp

        @app.route('/fortnite/api/game/v2/enabled_features', methods=['GET'])
        def apigamev2enabledfeatures():
            
            resp=app.response_class(
                response=dumps([]),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/twitch/<accountId>', methods=['GET'])
        def fortniteapigametwitch(accountId):
            
            resp=Response()
            resp.status_code=200
            return resp

        @app.route('/fortnite/api/game/v2/world/info', methods=['GET'])
        def apigamev2wotldinfo():
            
            return send_from_directory('data/content/', 'worldstw.json')

        @app.route('/fortnite/api/game/v2/profile/<account>/client/PurchaseCatalogEntry', methods=['POST'])
        def PurchaseCatalogEntry(account):
            
            
            itemId=loads(request.get_data())['offerId']
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "profile0"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()   
            athena=loads(open(f'data/profiles/athena.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()
                    
            catalog=self.functions.getShop()
            
            ApplyProfileChanges=[]
            MultiUpdate=[]
            Notifications=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            PurchasedLlama=False
            AthenaModified=False
            ItemExists=False            
            
            # for i in exchange_table:
            #     if itemId==i['id']:
            #         r=get(f"{api_url}/post/item/item.php?urlkey={urlkey}&token&passwd=&usernm={account}&item={i['name']}&action=buy_item", verify=False, proxies=proxy).text
            #         if r!="error":
            #             if r!="already_exist":
            #                 pass
            #         else:
            #             pass
            
            if loads(request.get_data())['offerId'] and request.args.get('profileId')=="profile0" and PurchasedLlama==False:
                for a, value in enumerate(catalog['storefronts']):
                    if value['name'].startswith("BRSeason"):
                        if not isinstance(value['name'].split("BRSeason")[1], int):
                            for i in value['catalogEntries']:
                                if i['offerId'] == loads(request.get_data())['offerId']:
                                    offer=i
                            if offer:
                                if len(MultiUpdate) == 0:
                                    MultiUpdate.append({
                                        "profileRevision": athena['rvn'] or 0,
                                        "profileId": request.args.get("profileId") or "athena",
                                        "profileChangesBaseRevision": athena['rvn'] or 0,
                                        "profileChanges": [],
                                        "profileCommandRevision": athena['commandRevision'] or 0,
                                    })

                                Season=value['name'].split("BR")[1]
                                BattlePass=loads(open(f'data/items/season/{Season}.json', 'r', encoding='utf-8').read())
                                
                                if BattlePass:
                                    SeasonData=loads(open(f'data/profiles/seasondata.json', 'r', encoding='utf-8').read())

                                    if BattlePass['battlePassOfferId'] == offer['offerId'] or BattlePass['battleBundleOfferId'] == offer['offerId']:
                                        lootList=[]
                                        EndingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']
                                        SeasonData[self.session.get('username')][Season]['battlePassPurchased']=True

                                        if BattlePass['battleBundleOfferId'] == offer['offerId']:
                                            SeasonData[self.session.get('username')][Season]['battlePassTier'] += 25
                                            if SeasonData[self.session.get('username')][Season]['battlePassTier'] > 100:
                                                SeasonData[self.session.get('username')][Season]['battlePassTier']=100
                                            EndingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']
                                        
                                        for i in range(EndingTier):
                                            FreeTier=BattlePass['freeRewards'][i] or {}
                                            PaidTier=BattlePass['paidRewards'][i] or {}

                                            for item in FreeTier:
                                                if item.lower() == "token:athenaseasonxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                    })

                                                if item.lower() == "token:athenaseasonfriendxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_friend_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                    })
                                                    
                                                if item.lower().startswith("currency:mtx"):
                                                    for key in profile['items']:
                                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                profile['items'][key]['quantity'] += FreeTier[item]
                                                                break

                                                if item.lower().startswith("athena"):
                                                    for key in athena['items']:
                                                        if athena['items'][key]['templateId'].lower() == item.lower():
                                                            athena['items'][key]['attributes']['item_seen']=False
                                                            ItemExists=True

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAttrChanged",
                                                                "itemId": key,
                                                                "attributeName": "item_seen",
                                                                "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                            })

                                                    if ItemExists == False:
                                                        ItemID=str(uuid4()).replace("-", "")
                                                        Item={
                                                            "templateId":item,
                                                            "attributes":
                                                                {
                                                                    "max_level_bonus":0,
                                                                    "level":1,
                                                                    "item_seen":False,
                                                                    "xp":0,
                                                                    "variants":[],
                                                                    "favorite":False
                                                                },
                                                                "quantity":FreeTier[item]
                                                        }

                                                        athena['items'][ItemID]=Item

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "itemAdded",
                                                            "itemId": ItemID,
                                                            "item": Item
                                                        })

                                                    ItemExists=False

                                                lootList.append({
                                                    "itemType": item,
                                                    "itemGuid": item,
                                                    "quantity": FreeTier[item]
                                                })

                                            for item in FreeTier:
                                                if item.lower() == "token:athenaseasonxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                    })

                                                if item.lower() == "token:athenaseasonfriendxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_friend_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                    })

                                                if item.lower().startswith("currency:mtx"):
                                                    for key in profile['items']:
                                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                profile['items'][key]['quantity'] += FreeTier[item]
                                                                break

                                                if item.lower().startswith("athena"):
                                                    for key in athena['items']:
                                                        if athena['items'][key]['templateId'].lower() == item.lower():
                                                            athena['items'][key]['attributes']['item_seen']=False
                                                            ItemExists=True

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAttrChanged",
                                                                "itemId": key,
                                                                "attributeName": "item_seen",
                                                                "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                            })

                                                    if ItemExists == False:
                                                        ItemID=str(uuid4()).replace("-", "")
                                                        Item={
                                                            "templateId":item,
                                                            "attributes":
                                                                {
                                                                    "max_level_bonus":0,
                                                                    "level":1,
                                                                    "item_seen":False,
                                                                    "xp":0,
                                                                    "variants":[],
                                                                    "favorite":False
                                                                },
                                                                "quantity":FreeTier[item]
                                                        }

                                                        athena['items'][ItemID]=Item

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "itemAdded",
                                                            "itemId": ItemID,
                                                            "item": Item
                                                        })

                                                    ItemExists=False

                                                lootList.append({
                                                    "itemType": item,
                                                    "itemGuid": item,
                                                    "quantity": FreeTier[item]
                                                })

                                                for item in PaidTier:
                                                    if item.lower()=="token:athenaseasonxpboost":
                                                        SeasonData[self.session.get('username')][Season]['battlePassXPBoost']+=PaidTier[item]
                                                        
                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "statModified",
                                                            "name": "season_match_boost",
                                                            "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                        })

                                            for item in PaidTier:
                                                if item.lower() == "token:athenaseasonxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += PaidTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                    })

                                                if item.lower() == "token:athenaseasonfriendxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += PaidTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_friend_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                    })

                                                if item.lower().startswith("currency:mtx"):
                                                    for key in profile['items']:
                                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                profile['items'][key]['quantity'] += PaidTier[item]
                                                                break

                                                if item.lower().startswith("athena"):
                                                    for key in athena['items']:
                                                        if athena['items'][key]['templateId'].lower() == item.lower():
                                                            athena['items'][key]['attributes']['item_seen']=False
                                                            ItemExists=True

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAttrChanged",
                                                                "itemId": key,
                                                                "attributeName": "item_seen",
                                                                "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                            })

                                                    if ItemExists == False:
                                                        ItemID=str(uuid4()).replace("-", "")
                                                        Item={
                                                            "templateId": item,
                                                            "attributes":
                                                                {
                                                                    "max_level_bonus": 0,
                                                                    "level": 1,
                                                                    "item_seen":False,
                                                                    "xp": 0,
                                                                    "variants": [],
                                                                    "favorite": False
                                                                },
                                                                "quantity": 
                                                                    PaidTier[item]
                                                        }

                                                        athena['items'][ItemID]=Item

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "itemAdded",
                                                            "itemId": ItemID,
                                                            "item": Item
                                                        })

                                                    ItemExists=False

                                                lootList.append({
                                                    "itemType": item,
                                                    "itemGuid": item,
                                                    "quantity": PaidTier[item]
                                                })

                                                for item in PaidTier:
                                                    if item.lower()=="token:athenaseasonxpboost":
                                                        SeasonData[self.session.get('username')][Season]['battlePassXPBoost']+=PaidTier[item]
                                                        
                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "statModified",
                                                            "name": "season_match_boost",
                                                            "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                        })
                                                        
                                            GiftBoxID=str(uuid4()).replace("-", "")
                                            GiftBox={
                                                "templateId":int(Season.split("Season")[1]), 
                                                "GiftBox:gb_battlepass" : "GiftBox:gb_battlepasspurchased",
                                                "attributes":
                                                    {
                                                        "max_level_bonus":0,
                                                        "fromAccountId":"",
                                                        "lootList":lootList
                                                    }
                                            }
                                            
                                            if int(Season.split("Season")[1]) > 2:
                                                profile['items'][GiftBoxID]=GiftBox
                                            
                                                ApplyProfileChanges.append({
                                                    "changeType": "itemAdded",
                                                    "itemId": GiftBoxID,
                                                    "item": GiftBox
                                                })

                                            MultiUpdate[0]['profileChanges'].append({
                                                "changeType": "statModified",
                                                "name": "book_purchased",
                                                "value": SeasonData[self.session.get('username')][Season]['battlePassPurchased']
                                            })

                                            MultiUpdate[0]['profileChanges'].append({
                                                "changeType": "statModified",
                                                "name": "book_level",
                                                "value": SeasonData[self.session.get('username')][Season]['battlePassTier']
                                            })

                                            AthenaModified=True
                                            
                                        if BattlePass['tierOfferId'] == offer['offerId']:
                                            lootList=[]
                                            StartingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']
                                            EndingTier
                                            SeasonData[self.session.get('username')][Season]['battlePassTier'] += loads(request.get_data())['purchaseQuantity'] or 1
                                            EndingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']

                                            for i in range(StartingTier, EndingTier):
                                                FreeTier=BattlePass['freeRewards'][i] or {}
                                                PaidTier=BattlePass['paidRewards'][i] or {}

                                                for item in FreeTier:
                                                    if item.lower() == "token:athenaseasonxpboost":
                                                        SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += FreeTier[item]

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "statModified",
                                                            "name": "season_match_boost",
                                                            "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                        })
                                                        
                                                    if item.lower() == "token:athenaseasonfriendxpboost":
                                                        SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += FreeTier[item]

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "statModified",
                                                            "name": "season_friend_match_boost",
                                                            "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                        })
                                                    
                                                    if item.lower().startswith("currency:mtx"):
                                                        for key in profile['items']:
                                                            if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                                if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                    profile['items'][key]['quantity'] += FreeTier[item]
                                                                    break
                                                                
                                                    if item.lower().startswith("athena"):
                                                        for key in athena['items']:
                                                            if athena['items'][key]['templateId'].lower() == item.lower():
                                                                athena['items'][key]['attributes']['item_seen']=False
                                                                ItemExists=True

                                                                MultiUpdate[0]['profileChanges'].append({
                                                                    "changeType": "itemAttrChanged",
                                                                    "itemId": key,
                                                                    "attributeName": "item_seen",
                                                                    "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                                })

                                                        if ItemExists == False:
                                                            ItemID=str(uuid4()).replace("-", "")
                                                            Item={
                                                                "templateId":item,
                                                                "attributes":
                                                                    {
                                                                        "max_level_bonus":0,
                                                                        "level":1,
                                                                        "item_seen":False,
                                                                        "xp":0,
                                                                        "variants":[],
                                                                        "favorite":False
                                                                    },
                                                                    "quantity":FreeTier[item]
                                                            }

                                                            athena['items'][ItemID]=Item

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAdded",
                                                                "itemId": ItemID,
                                                                "item": Item
                                                            })

                                                        ItemExists=False
                                                    
                                                    lootList.append({
                                                        "itemType": item,
                                                        "itemGuid": item,
                                                        "quantity": FreeTier[item]
                                                    })
                                                
                                                for item in PaidTier:
                                                    if item.lower() == "token:athenaseasonxpboost":
                                                        SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += PaidTier[item]

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "statModified",
                                                            "name": "season_match_boost",
                                                            "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                        })

                                                    if item.lower() == "token:athenaseasonfriendxpboost":
                                                        SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += PaidTier[item]

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "statModified",
                                                            "name": "season_friend_match_boost",
                                                            "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                        })

                                                    if item.lower().startswith("currency:mtx"):
                                                        for key in profile['items']:
                                                            if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                                if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                    profile['items'][key]['quantity'] += PaidTier[item]
                                                                    break
                                                    
                                                    if item.lower().startswith("athena"):
                                                        for key in athena['items']:
                                                            if athena['items'][key]['templateId'].lower() == item.lower():
                                                                athena['items'][key]['attributes']['item_seen']=False
                                                                ItemExists=True

                                                                MultiUpdate[0]['profileChanges'].append({
                                                                    "changeType": "itemAttrChanged",
                                                                    "itemId": key,
                                                                    "attributeName": "item_seen",
                                                                    "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                                })

                                                        if ItemExists == False:
                                                            ItemID=str(uuid4()).replace("-", "")
                                                            Item={
                                                                "templateId":item,
                                                                "attributes":
                                                                    {
                                                                        "max_level_bonus":0,
                                                                        "level":1,
                                                                        "item_seen":False,
                                                                        "xp":0,
                                                                        "variants":[],
                                                                        "favorite":False
                                                                    },"quantity":PaidTier[item]
                                                            }

                                                            athena['items'][ItemID]=Item

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAdded",
                                                                "itemId": ItemID,
                                                                "item": Item
                                                            })

                                                        ItemExists=False

                                                    lootList.append({
                                                        "itemType": item,
                                                        "itemGuid": item,
                                                        "quantity": PaidTier[item]
                                                    })
                                                    
                                            GiftBoxID=str(uuid4()).replace("-", "")
                                            GiftBox={
                                                "templateId":"GiftBox:gb_battlepass",
                                                "attributes":
                                                    {
                                                        "max_level_bonus":0,
                                                        "fromAccountId":"",
                                                        "lootList":lootList
                                                    }
                                            }
                                            
                                            if int(Season.split("Season")[1]) > 2:
                                                profile['items'][GiftBoxID]=GiftBox
                                            
                                                ApplyProfileChanges.append({
                                                    "changeType": "itemAdded",
                                                    "itemId": GiftBoxID,
                                                    "item": GiftBox
                                                })

                                            MultiUpdate[0]['profileChanges'].append({
                                                "changeType": "statModified",
                                                "name": "book_level",
                                                "value": SeasonData[self.session.get('username')][Season]['battlePassTier']
                                            })

                                            AthenaModified=True

                                        open(f'data/profiles/seasondata.json', 'w', encoding='utf-8').write(dumps(SeasonData, indent=4))
                        
                        if value['name'].startswith("BR"):
                            for b, value in enumerate(catalog['storefronts'][a]['catalogEntries']):
                                if value['offerId'] == loads(request.get_data())['offerId']:
                                    for c, value in enumerate(catalog['storefronts'][a]['catalogEntries'][b]['itemGrants']):
                                        ID=value['templateId']

                                        for key in athena['items']:
                                            if value['templateId'].lower() == athena['items'][key]['templateId'].lower():
                                                ItemExists=True


                                        if ItemExists == False:
                                            if len(MultiUpdate) == 0:
                                                MultiUpdate.append({
                                                    "profileRevision": athena['rvn'] or 0,
                                                    "profileId": request.args.get("profileId") or "athena",
                                                    "profileChangesBaseRevision": athena['rvn'] or 0,
                                                    "profileChanges": [],
                                                    "profileCommandRevision": athena['commandRevision'] or 0,
                                                })
                                            
                                            if len(Notifications) == 0:
                                                Notifications.append({
                                                    "type": "CatalogPurchase",
                                                    "primary": True,
                                                    "lootResult": {
                                                        "items": []
                                                    }
                                                })

                                            Item={
                                                "templateId": value['templateId'],
                                                "attributes": {
                                                    "max_level_bonus": 0,
                                                    "level": 1,
                                                    "item_seen": False,
                                                    "xp": 0,
                                                    "variants": [],
                                                    "favorite": False
                                                },
                                                "quantity": 1
                                            }

                                            athena['items'][ID]=Item

                                            MultiUpdate[0]['profileChanges'].append({
                                                "changeType": "itemAdded",
                                                "itemId": ID,
                                                "item": athena['items'][ID]
                                            })
                                            
                                            Notifications[0]['lootResult']['items'].append({
                                                "itemType": value['templateId'],
                                                "itemGuid": ID,
                                                "itemProfile": "athena",
                                                "quantity": value['quantity']
                                            })

                                            AthenaModified=True

                                        ItemExists=False
                                        
                                    if catalog['storefronts'][a]['catalogEntries'][b]['prices'][0]['currencyType'].lower() == "mtxcurrency":
                                        for key in profile['items']:
                                            if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                    profile['items'][key]['quantity'] -= (catalog['storefronts'][a]['catalogEntries'][b]['prices'][0]['finalPrice']) * loads(request.get_data())['purchaseQuantity'] or 1
                                    
                                                    ApplyProfileChanges.append({
                                                        "changeType": "itemQuantityChanged",
                                                        "itemId": key,
                                                        "quantity": profile['items'][key]['quantity']
                                                    })

                                                    profile['rvn'] += 1
                                                    profile['commandRevision'] += 1

                                                    break
                    
                    PurchasedLlama=True
                    
                    if AthenaModified == True:
                        athena['rvn'] += 1
                        athena['commandRevision'] += 1

                        if MultiUpdate[0]:
                            MultiUpdate[0]['profileRevision']=athena['rvn'] or 0
                            MultiUpdate[0]['profileCommandRevision']=athena['commandRevision'] or 0

                        oldprofile=loads(open(f'data/profiles/athena.json', 'r', encoding='utf-8').read())
                        oldprofile[self.session.get('username')]=athena
                        open(f'data/profiles/athena.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
                        
                        oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "profile0"}.json', 'r', encoding='utf-8').read())
                        oldprofile[self.session.get('username')]=profile
                        open(f'data/profiles/{request.args.get("profileId") or "profile0"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))

                    if AthenaModified == False:
                        profile['rvn'] += 1
                        profile['commandRevision'] += 1

                        oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "profile0"}.json', 'r', encoding='utf-8').read())
                        oldprofile[self.session.get('username')]=profile
                        open(f'data/profiles/{request.args.get("profileId") or "profile0"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
                    
                if loads(request.get_data())['offerId'] and profile['profileId'] == "common_core":
                    if value['name'].startswith("BRSeason"):
                        if not isinstance(value['name'].split("BRSeason")[1], int):
                            for i in value['catalogEntries']:
                                if i['offerId'] == loads(request.get_data())['offerId']:
                                    offer=i
                                    
                            if offer:
                                if len(MultiUpdate) == 0:
                                    MultiUpdate.append({
                                        "profileRevision": athena['rvn'] or 0,
                                        "profileId": "athena",
                                        "profileChangesBaseRevision": athena['rvn'] or 0,
                                        "profileChanges": [],
                                        "profileCommandRevision": athena['commandRevision'] or 0,
                                    })
                                    
                                Season=value['name'].split("BR")[1]
                                BattlePass=loads(open(f'data/items/season/{Season}.json', 'r', encoding='utf-8').read())
                                
                                if BattlePass:
                                    SeasonData=loads(open(f'data/profiles/seasondata.json', 'r', encoding='utf-8').read())

                                    if BattlePass['battlePassOfferId'] == offer['offerId'] or BattlePass['battleBundleOfferId'] == offer['offerId']:
                                        lootList=[]
                                        EndingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']
                                        SeasonData[self.session.get('username')][Season]['battlePassPurchased']=True

                                        if BattlePass['battleBundleOfferId'] == offer['offerId']:
                                            SeasonData[self.session.get('username')][Season]['battlePassTier'] += 25
                                            if SeasonData[self.session.get('username')][Season]['battlePassTier'] > 100:
                                                SeasonData[self.session.get('username')][Season]['battlePassTier']=100
                                            EndingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']

                                        for i in range(EndingTier):
                                            FreeTier=BattlePass['freeRewards'][i] or {}
                                            PaidTier=BattlePass['paidRewards'][i] or {}
                                            
                                            for item in FreeTier:
                                                if item.lower() == "token:athenaseasonxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                    })

                                                if item.lower() == "token:athenaseasonfriendxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_friend_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                    })
                                                    
                                                if item.lower().startswith("currency:mtx"):
                                                    for key in profile['items']:
                                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                profile['items'][key]['quantity'] += FreeTier[item]
                                                                break
                                                            
                                                if item.lower().startswith("athena"):
                                                    for key in athena['items']:
                                                        if athena['items'][key]['templateId'].lower() == item.lower():
                                                            athena['items'][key]['attributes']['item_seen']=False
                                                            ItemExists=True

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAttrChanged",
                                                                "itemId": key,
                                                                "attributeName": "item_seen",
                                                                "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                            })

                                                    if ItemExists == False:
                                                        ItemID=str(uuid4()).replace("-", "")
                                                        Item={
                                                            "templateId":item,
                                                            "attributes":
                                                                {
                                                                    "max_level_bonus":0,
                                                                    "level":1,
                                                                    "item_seen":False,
                                                                    "xp":0,
                                                                    "variants":[],
                                                                    "favorite":False
                                                                },
                                                                "quantity":FreeTier[item]
                                                        }

                                                        athena['items'][ItemID]=Item

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "itemAdded",
                                                            "itemId": ItemID,
                                                            "item": Item
                                                        })

                                                    ItemExists=False

                                                lootList.append({
                                                    "itemType": item,
                                                    "itemGuid": item,
                                                    "quantity": FreeTier[item]
                                                })
                                                
                                            for item in PaidTier:
                                                if item.lower() == "token:athenaseasonxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += PaidTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                    })

                                                if item.lower() == "token:athenaseasonfriendxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += PaidTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_friend_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                    })

                                                if item.lower().startswith("currency:mtx"):
                                                    for key in profile['items']:
                                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                profile['items'][key]['quantity'] += PaidTier[item]
                                                                break
                                                            
                                                if item.lower().startswith("athena"):
                                                    for key in athena['items']:
                                                        if athena['items'][key]['templateId'].lower() == item.lower():
                                                            athena['items'][key]['attributes']['item_seen']=False
                                                            ItemExists=True

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAttrChanged",
                                                                "itemId": key,
                                                                "attributeName": "item_seen",
                                                                "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                            })

                                                    if ItemExists == False:
                                                        ItemID=str(uuid4()).replace("-", "")
                                                        Item={
                                                            "templateId": item,
                                                            "attributes":
                                                                {
                                                                    "max_level_bonus":0,
                                                                    "level":1,
                                                                    "item_seen":False,
                                                                    "xp":0,
                                                                    "variants":[],
                                                                    "favorite":False
                                                                },
                                                                "quantity": PaidTier[item]
                                                        }

                                                        athena['items'][ItemID]=Item

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "itemAdded",
                                                            "itemId": ItemID,
                                                            "item": Item
                                                        })

                                                    ItemExists=False

                                                lootList.append({
                                                    "itemType": item,
                                                    "itemGuid": item,
                                                    "quantity": PaidTier[item]
                                                })
                                        
                                        GiftBoxID=str(uuid4()).replace("-", "")
                                        GiftBox={
                                            "templateId":int(Season.split("Season")[1]), 
                                            "GiftBox:gb_battlepass" : "GiftBox:gb_battlepasspurchased",
                                            "attributes":
                                                {
                                                    "max_level_bonus":0,
                                                    "fromAccountId":"",
                                                    "lootList":lootList
                                                }
                                        }
                                        
                                        if int(Season.split("Season")[1]) > 2:
                                            profile['items'][GiftBoxID]=GiftBox
                                            
                                            ApplyProfileChanges.append({
                                                "changeType": "itemAdded",
                                                "itemId": GiftBoxID,
                                                "item": GiftBox
                                            })

                                        MultiUpdate[0]['profileChanges'].append({
                                            "changeType": "statModified",
                                            "name": "book_purchased",
                                            "value": SeasonData[self.session.get('username')][Season]['battlePassPurchased']
                                        })

                                        MultiUpdate[0]['profileChanges'].append({
                                            "changeType": "statModified",
                                            "name": "book_level",
                                            "value": SeasonData[self.session.get('username')][Season]['battlePassTier']
                                        })

                                        AthenaModified=True
                                        
                                    if BattlePass['tierOfferId'] == offer['offerId']:
                                        lootList=[]
                                        StartingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']
                                        EndingTier
                                        SeasonData[self.session.get('username')][Season]['battlePassTier'] += loads(request.get_data())['purchaseQuantity'] or 1
                                        EndingTier=SeasonData[self.session.get('username')][Season]['battlePassTier']

                                        for StartingTier in range(EndingTier):
                                            FreeTier=BattlePass['freeRewards'][i] or {}
                                            PaidTier=BattlePass['paidRewards'][i] or {}

                                            for item in FreeTier:
                                                if item.lower() == "token:athenaseasonxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                    })

                                                if item.lower() == "token:athenaseasonfriendxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += FreeTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_friend_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                    })
                                                    
                                                if item.lower().startswith("currency:mtx"):
                                                    for key in profile['items']:
                                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                profile['items'][key]['quantity'] += FreeTier[item]
                                                                break
                                                            
                                                if item.lower().startswith("athena"):
                                                    for key in athena['items']:
                                                        if athena['items'][key]['templateId'].lower() == item.lower():
                                                            athena['items'][key]['attributes']['item_seen']=False
                                                            ItemExists=True

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAttrChanged",
                                                                "itemId": key,
                                                                "attributeName": "item_seen",
                                                                "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                            })

                                                    if ItemExists == False:
                                                        ItemID=str(uuid4()).replace("-", "")
                                                        Item={
                                                            "templateId":item,
                                                            "attributes":
                                                                {
                                                                    "max_level_bonus":0,
                                                                    "level":1,
                                                                    "item_seen":False,
                                                                    "xp":0,
                                                                    "variants":[],
                                                                    "favorite":False
                                                                },
                                                                "quantity":FreeTier[item]}

                                                        athena['items'][ItemID]=Item

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "itemAdded",
                                                            "itemId": ItemID,
                                                            "item": Item
                                                        })

                                                    ItemExists=False

                                                lootList.append({
                                                    "itemType": item,
                                                    "itemGuid": item,
                                                    "quantity": FreeTier[item]
                                                })
                                                
                                            for item in PaidTier:
                                                if item.lower() == "token:athenaseasonxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPBoost'] += PaidTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPBoost']
                                                    })

                                                if item.lower() == "token:athenaseasonfriendxpboost":
                                                    SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost'] += PaidTier[item]

                                                    MultiUpdate[0]['profileChanges'].append({
                                                        "changeType": "statModified",
                                                        "name": "season_friend_match_boost",
                                                        "value": SeasonData[self.session.get('username')][Season]['battlePassXPFriendBoost']
                                                    })

                                                if item.lower().startswith("currency:mtx"):
                                                    for key in profile['items']:
                                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                                profile['items'][key]['quantity'] += PaidTier[item]
                                                                break
                                                
                                                if item.lower().startswith("athena"):
                                                    for key in athena['items']:
                                                        if athena['items'][key]['templateId'].lower() == item.lower():
                                                            athena['items'][key]['attributes']['item_seen']=False
                                                            ItemExists=True

                                                            MultiUpdate[0]['profileChanges'].append({
                                                                "changeType": "itemAttrChanged",
                                                                "itemId": key,
                                                                "attributeName": "item_seen",
                                                                "attributeValue": athena['items'][key]['attributes']['item_seen']
                                                            })

                                                    if ItemExists == False:
                                                        ItemID=str(uuid4()).replace("-", "")
                                                        Item={
                                                            "templateId":item,
                                                            "attributes":
                                                                {
                                                                    "max_level_bonus":0,
                                                                    "level":1,
                                                                    "item_seen":False,
                                                                    "xp":0,
                                                                    "variants":[],
                                                                    "favorite":False
                                                                },
                                                                "quantity":PaidTier[item]
                                                        }

                                                        athena['items'][ItemID]=Item

                                                        MultiUpdate[0]['profileChanges'].append({
                                                            "changeType": "itemAdded",
                                                            "itemId": ItemID,
                                                            "item": Item
                                                        })

                                                    ItemExists=False

                                                lootList.append({
                                                    "itemType": item,
                                                    "itemGuid": item,
                                                    "quantity": PaidTier[item]
                                                })
                                        
                                        GiftBoxID=str(uuid4()).replace("-", "")
                                        GiftBox={
                                            "templateId":"GiftBox:gb_battlepass",
                                            "attributes":
                                                {
                                                    "max_level_bonus":0,
                                                    "fromAccountId":"",
                                                    "lootList":lootList
                                                }
                                        }
                                        
                                        if int(Season.split("Season")[1]) > 2:
                                            profile['items'][GiftBoxID]=GiftBox
                                            
                                            ApplyProfileChanges.append({
                                                "changeType": "itemAdded",
                                                "itemId": GiftBoxID,
                                                "item": GiftBox
                                            })

                                        MultiUpdate[0]['profileChanges'].append({
                                            "changeType": "statModified",
                                            "name": "book_level",
                                            "value": SeasonData[self.session.get('username')][Season]['battlePassTier']
                                        })

                                        AthenaModified=True

                                    open(f'data/profiles/seasondata.json', 'w', encoding='utf-8').write(dumps(SeasonData, indent=4))
                    
                    if value['name'].startswith("BR"):
                        for b, value in enumerate(catalog['storefronts'][a]['catalogEntries']):
                            if value['offerId'] == loads(request.get_data())['offerId']:
                                for c, value in enumerate(catalog['storefronts'][a]['catalogEntries'][b]['itemGrants']):
                                    ID=value['templateId']
                                    
                                    for key in athena['items']:
                                        if value['templateId'].lower() == athena['items'][key]['templateId'].lower():
                                            ItemExists=True
                                    
                                    if ItemExists == False:
                                        if len(MultiUpdate) == 0:
                                            MultiUpdate.append({
                                                "profileRevision": athena['rvn'] or 0,
                                                "profileId": request.args.get("profileId") or "athena",
                                                "profileChangesBaseRevision": athena['rvn'] or 0,
                                                "profileChanges": [],
                                                "profileCommandRevision": athena['commandRevision'] or 0,
                                            })

                                        if len(Notifications) == 0:
                                            Notifications.append({
                                                "type": "CatalogPurchase",
                                                "primary": True,
                                                "lootResult": {
                                                    "items": []
                                                }
                                            })

                                        Item={
                                            "templateId": value['templateId'],
                                            "attributes": {
                                                "max_level_bonus": 0,
                                                "level": 1,
                                                "item_seen": False,
                                                "xp": 0,
                                                "variants": [],
                                                "favorite": False
                                            },
                                            "quantity": 1
                                        }

                                        athena['items'][ID]=Item
                                        
                                        MultiUpdate[0]['profileChanges'].append({
                                            "changeType": "itemAdded",
                                            "itemId": ID,
                                            "item": Item
                                        })

                                        Notifications[0]['lootResult']['items'].append({
                                            "itemType": value['templateId'],
                                            "itemGuid": ID,
                                            "itemProfile": "athena",
                                            "quantity": value['quantity']
                                        })

                                        AthenaModified=True
                                        
                                    ItemExists=False
                                
                                if catalog['storefronts'][a]['catalogEntries'][b]['prices'][0]['currencyType'].lower() == "mtxcurrency":
                                    for key in profile['items']:
                                        if profile['items'][key]['templateId'].lower().startswith("currency:mtx"):
                                            if profile['items'][key]['attributes']['platform'].lower() == profile['stats']['attributes']['current_mtx_platform'].lower() or profile['items'][key]['attributes']['platform'].lower() == "shared":
                                                profile['items'][key]['quantity'] -= (catalog['storefronts'][a]['catalogEntries'][b]['prices'][0]['finalPrice']) * loads(request.get_data())['purchaseQuantity'] or 1
                                                        
                                                ApplyProfileChanges.append({
                                                    "changeType": "itemQuantityChanged",
                                                    "itemId": key,
                                                    "quantity": profile['items'][key]['quantity']
                                                })
                                
                                                break
                                
                                if len(catalog['storefronts'][a]['catalogEntries'][b]['itemGrants']) != 0:
    
                                    purchaseId=str(uuid4()).replace("-", "")
                                    profile['stats']['attributes']['mtx_purchase_history']['purchases'].append({
                                        "purchaseId":purchaseId,
                                        "offerId":f'v2:/{purchaseId}',
                                        "purchaseDate":datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                        "freeRefundEligible":False,
                                        "fulfillments":[],
                                        "lootResult":Notifications[0]['lootResult']['items'],
                                        "totalMtxPaid":catalog['storefronts'][a]['catalogEntries'][b]['prices'][0]['finalPrice'],
                                        "metadata":{},
                                        "gameContext":""
                                    })

                                    ApplyProfileChanges.append({
                                        "changeType": "statModified",
                                        "name": "mtx_purchase_history",
                                        "value": profile['stats']['attributes']['mtx_purchase_history']
                                    })

                                profile['rvn'] += 1
                                profile['commandRevision'] += 1
                                            
                if AthenaModified == True:
                    athena['rvn'] += 1
                    athena['commandRevision'] += 1

                    if len(MultiUpdate)!=0:
                        MultiUpdate[0]['profileRevision']=athena['rvn'] or 0
                        MultiUpdate[0]['profileCommandRevision']=athena['commandRevision'] or 0

                    oldprofile=loads(open('data/profiles/athena.json', 'r', encoding='utf-8').read())
                    oldprofile[self.session.get('username')]=athena
                    open('data/profiles/athena.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
                    
                    oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'r', encoding='utf-8').read())
                    oldprofile[self.session.get('username')]=profile
                    open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
        

                if AthenaModified == False:
                    profile['rvn'] += 1
                    profile['commandRevision'] += 1

                    if len(MultiUpdate)!=0:
                        MultiUpdate[0]['profileRevision']=profile['rvn'] or 0
                        MultiUpdate[0]['profileCommandRevision']=profile['commandRevision'] or 0
                        
                    oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'r', encoding='utf-8').read())
                    oldprofile[self.session.get('username')]=profile
                    open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))

            if QueryRevision != BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]

            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get('profileId') or "profile0",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "notifications": Notifications,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "multiUpdate": MultiUpdate,
                "responseVersion": 1
            }
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/SetPartyAssistQuest', methods=['POSt'])
        def mcpSetPartyAssistQuest(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()
            
            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args['rvn'] or -1
            StatChanged=False

            if "party_assist_quest" in profile['stats']['attributes']:
                profile['stats']['attributes']=loads(request.get_data())['questToPinAsPartyAssist'] or ""
                StatChanged=True
            
            if StatChanged:
                profile['rvn']+=1
                profile['commandRevision']+=1

                ApplyProfileChanges.append({
                    "changeType": "statModified",
                    "name": "party_assist_quest",
                    "value": profile['stats']['attributes']['party_assist_quest']
                })

                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }

            resp=app.response_class(
                    response=dumps(r),
                    status=200,
                    mimetype='application/json'
                )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/AthenaPinQuest', methods=['POST'])
        def mcpAthenaPinQuest(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args['rvn'] or -1
            StatChanged=False

            if "pinned_quest" in profile['stats']['attributes']:
                profile['stats']['attributes']=loads(request.get_data())['pinned_quest'] or ""
                StatChanged=True
            
            if StatChanged:
                profile['rvn']+=1
                profile['commandRevision']+=1

                ApplyProfileChanges.append({
                    "changeType": "statModified",
                    "name": "pinned_quest",
                    "value": profile['stats']['attributes']['pinned_quest']
                })

                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }

            resp=app.response_class(
                    response=dumps(r),
                    status=200,
                    mimetype='application/json'
                )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/SetItemFavoriteStatus', methods=['POST'])
        def SetItemFavoriteStatus(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp

            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            StatChanged=False
            
            if loads(request.get_data())['targetItemId']:
                profile['items'][loads(request.get_data())['targetItemId']]['attributes']['favorite']=loads(request.get_data())['bFavorite'] or False
                StatChanged=True
                
            if StatChanged:
                profile['rvn']+=1
                profile['commandRevision']+=1
                
                ApplyProfileChanges.append({
                    "changeType": "itemAttrChanged",
                    "itemId": loads(request.get_data())['targetItemId'],
                    "attributeName": "favorite",
                    "attributeValue": profile['items'][loads(request.get_data())['targetItemId']]['attributes']['favorite']
                })
                
                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/MarkItemSeen', methods=['POST'])
        def MarkItemSeen(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            StatChanged=False
            
            if loads(request.get_data())['itemIds']:
                
                itemIdsL=loads(request.get_data())['itemIds']
                
                for i in range(len(itemIdsL)):
                    profile['items'][itemIdsL[i]]['attributes']['item_seen']=True
                
                    ApplyProfileChanges.append({
                        "changeType": "itemAttrChanged",
                        "itemId": itemIdsL[i],
                        "attributeName": "item_seen",
                        "attributeValue": profile['items'][itemIdsL[i]]['attributes']['item_seen']
                    })
                
                StatChanged=True
                
            if StatChanged:
                profile['rvn']+=1
                profile['commandRevision']+=1
                
                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/EquipBattleRoyaleCustomization', methods=['POST'])
        def EquipBattleRoyaleCustomization(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()
            
            try:
                if not profile['stats']['attributes']['favorite_dance']:
                    profile['stats']['attributes']['favorite_dance']=["","","","","",""]
                    
                if not profile['stats']['attributes']['favorite_itemwraps']:
                    profile['stats']['attributes']['favorite_itemwraps']=["","","","","","",""]
            
            except:
                pass

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            StatChanged=False
            VariantChanged=False
            
            try:
                
                variantUpdatesL=loads(request.get_data())['variantUpdates']
                ReturnVariantsAsString=variantUpdatesL or []
                
                if "active" in ReturnVariantsAsString:
                    itemToSlotJ=loads(request.get_data())['itemToSlot']
                    if len(profile['items'][itemToSlotJ]['attributes']['variants'])==0:
                        profile['items'][itemToSlotJ]['attributes']['variants']=variantUpdatesL or []
                    
                    for i in profile['items'][itemToSlotJ]['attributes']['variants']:
                        try:
                            if profile['items'][itemToSlotJ]['attributes']['variants']['channel']==variantUpdatesL[i]['channel'].lower():
                                profile['items'][itemToSlotJ]['attributes']['variants'][i]['active']=variantUpdatesL[i]['active'] or ""
                        except:
                            pass
                        
                    VariantChanged=True
            except Exception as e:
                pass
            
            if loads(request.get_data())['slotName']:
                
                slotNameJ=loads(request.get_data())['slotName']
                itemToSlotJ=loads(request.get_data())['itemToSlot']
                self.functions.req(f"UPDATE favorites SET `{slotNameJ.lower()}`='{itemToSlotJ}' WHERE `username`='{self.session.get('username')}'")
                
                if slotNameJ=="Character":
                    self.session.put('character', itemToSlotJ)
                    profile['stats']['attributes']['favorite_character']=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="Backpack":
                    profile['stats']['attributes']['favorite_backpack']=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="Pickaxe":
                    profile['stats']['attributes']['favorite_pickaxe']=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="Glider":
                    profile['stats']['attributes']['favorite_glider']=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="SkyDiveContrail":
                    profile['stats']['attributes']['favorite_skydivecontrail']=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="MusicPack":
                    profile['stats']['attributes']['favorite_musicpack']=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="LoadingScreen":
                    profile['stats']['attributes']['favorite_loadingscreen']=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="Dance":
                    indexWithinSlot=loads(request.get_data())['indexWithinSlot']
                    if indexWithinSlot>=0:
                        profile['stats']['attributes']['favorite_dance'][indexWithinSlot]=itemToSlotJ or ""
                    StatChanged=True
                    pass

                if slotNameJ=="ItemWrap":
                    indexwithinslot=loads(request.get_data())['indexWithinSlot'] or 0

                    if indexwithinslot>=0 or indexwithinslot<=0:
                        if indexwithinslot==0:
                            profile['stats']['attributes']['favorite_itemwraps'][indexwithinslot]=itemToSlotJ or ""
                            pass

                        if indexwithinslot==1:
                            profile['stats']['attributes']['favorite_itemwraps'][indexwithinslot]=itemToSlotJ or ""
                            pass

                        if indexwithinslot==-1:
                            for i in range(7):
                                profile['stats']['attributes']['favorite_itemwraps'][i]=itemToSlotJ or ""
                            pass
                
            if StatChanged:
                Category=f"favorite_{slotNameJ.lower() or 'character'}"

                if Category=="favorite_itemwrap":
                    Category+="s"
                
                profile['rvn']+=1
                profile['commandRevision']+=1

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
                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))

            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]

            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/RefreshExpeditions', methods=['POST'])
        def fortniteRefreshExpeditions(account):
            
            resp=Response()
            resp.status_code=200
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/QueryProfile', methods=['POST'])
        def fortnitegameapiclientall(account):
            
            
            if request.args.get("profileId") in ['athena', 'profile0', 'common_core', 'common_public']:
                print('pass')
                pass
            else:
                profile=loads(open(f'data/unusedprofiles/{request.args.get("profileId")}.json', 'r', encoding='utf-8').read())
                profile['_id']=self.session.get('username')
                profile['accountId']=self.session.get('username')
                
                ApplyProfileChanges=[]
                BaseRevision=profile['rvn'] or 0
                QueryRevision=request.args.get('rvn') or -1
                
                if QueryRevision!=BaseRevision:
                    ApplyProfileChanges=[{
                        "changeType": "fullProfileUpdate",
                        "profile": profile
                    }]
                
                r={
                    "profileRevision": profile['rvn'] or 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": BaseRevision,
                    "profileChanges": ApplyProfileChanges,
                    "profileCommandRevision": profile['commandRevision'] or 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }
                
                resp=app.response_class(
                    response=dumps(r),
                    status=200,
                    mimetype='application/json'
                )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        @app.route('/fortnite/api/game/v2/profile/<account>/client/GetMcpTimeForLogin', methods=['POST'])
        def fortniteGetMcpTimeForLogin(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp
        
        
        @app.route('/fortnite/api/game/v2/profile/<account>/client/SetMtxPlatform', methods=['POST'])
        def fortnitegameapiclientall2(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/SetBattleRoyaleBanner', methods=['POST', 'GET'])
        def SetBattleRoyaleBanner(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            StatChanged=False
            
            if loads(request.get_data())['homebaseBannerIconId'] and loads(request.get_data())['homebaseBannerColorId']:
                profile['stats']['attributes']['banner_icon']=loads(request.get_data())['homebaseBannerIconId']
                profile['stats']['attributes']['banner_color']=loads(request.get_data())['homebaseBannerColorId']
                StatChanged=True
                
            if StatChanged:
                profile['rvn']+=1
                profile['commandRevision']+=1
                
                ApplyProfileChanges.append({
                    "changeType": "statModified",
                    "name": "banner_icon",
                    "value": profile['stats']['attributes']['banner_icon']
                })
                
                ApplyProfileChanges.append({
                    "changeType": "statModified",
                    "name": "banner_color",
                    "value": profile['stats']['attributes']['banner_color']
                })
                
                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/ClientQuestLogin', methods=['POST'])
        def ClientQuestLogin(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()
            
            QuestIDS=loads(open(f'data/items/quests.json', 'r', encoding='utf-8').read())
            memory=self.functions.getVersion()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args.get('rvn') or -1
            StatChanged=False
            
            QuestCount=0
            ShouldGiveQuest=True
            DateFormat=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ").split("T")[0]
            SeasonQuestIDS={}
            
            try:
                if request.args.get('profileId')=="athena":
                    DailyQuestIDS=QuestIDS['BattleRoyale']['Daily']
                    if f"Season{memory['season']}" in QuestIDS['BattleRoyale']:
                        SeasonQuestIDS=QuestIDS['BattleRoyale'][f"Season{memory['season']}"]
                    for key in profile['items']:
                        if profile['items'][key]['templateId'].lower().startswith("quest:athenadaily"):
                            QuestCount+=1
                    
                    if "quest_manager" in profile['stats']['attributes']:
                        if "dailyLoginInterval" in profile['stats']['attributes']['quest_manager']:
                            if "T" in profile['stats']['attributes']['quest_manager']['dailyLoginInterval']:
                                DailyLoginDate=str(profile['stats']['attributes']['quest_manager']['dailyLoginInterval']).split("t")
                                
                                if DailyLoginDate==DateFormat:
                                    ShouldGiveQuest=False
                                else:
                                    ShouldGiveQuest=True
                                    if profile['stats']['attributes']['quest_manager']['dailyQuestRerolls']<=0:
                                        profile['stats']['attributes']['quest_manager']['dailyQuestRerolls']=+1
                    if QuestCount < 3 and ShouldGiveQuest==True:
                        NewQuestID=str(uuid4()).replace("-", "")
                        randomNumber=round(random.randint()*len(DailyQuestIDS))
                        
                        for key in profile['items']:
                            while DailyQuestIDS[randomNumber]['templateId'].lower()==profile['items'][key]['templateId'].lower():
                                randomNumber=round(random.randint()*len(DailyQuestIDS))
                    
                    profile['items'][NewQuestID]={
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

                    profile['stats']['attributes']['quest_manager']['dailyLoginInterval']=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                    
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
                    
                    StatChanged=True
            except:
                pass
            
            for key in profile['items']:
                if str(key)[0]=="S" and isinstance(str(key)[1], int) and (str(key)[2]=="-" or isinstance(str(key)[2], int) and str(key)[3]=="-"):
                    if not str(key).startswith(f"S{memory['season']}-"):
                        profile['items'].pop(key)
                        
                        ApplyProfileChanges.append({
                            "changeType": "itemRemoved",
                            "itemId": key
                        })
                        
                        StatChanged=True
            
            if SeasonQuestIDS:
                if request.args.get('profileId')=="athena":
                    for i, ChallengeBundleSchedule in enumerate(SeasonQuestIDS['ChallengeBundleSchedules']):
                        if ChallengeBundleSchedule['itemGuid'] in profile['items']:
                            ApplyProfileChanges.append({
                                "changeType": "itemRemoved",
                                "itemId": ChallengeBundleSchedule['itemGuid']
                            })
                        
                        ChallengeBundleSchedule=SeasonQuestIDS['ChallengeBundleSchedules'][i]
                        
                        profile['items'][ChallengeBundleSchedule['itemGuid']]={
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
                        
                        StatChanged=True
                    
                    for i, ChallengeBundle in enumerate(SeasonQuestIDS['ChallengeBundles']):
                        if ChallengeBundle['itemGuid'] in profile['items']:
                            ApplyProfileChanges.append({
                                "changeType": "itemRemoved",
                                "itemId": ChallengeBundle['itemGuid']
                            })
                        
                        ChallengeBundle=SeasonQuestIDS['ChallengeBundles'][i]
                        
                        if loads(open('conf.json', 'r', encoding='utf-8').read())["Profile"]["bCompletedSeasonalQuests"]==True and "questStages" in ChallengeBundle:
                            ChallengeBundle['grantedquestinstanceids']=ChallengeBundle['grantedquestinstanceids']+ChallengeBundle['questStages']
                        
                        profile['items'][ChallengeBundle['itemGuid']]={
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
                        
                        profile['items'][ChallengeBundle['itemGuid']]['attributes']['num_granted_bundle_quests']=len(ChallengeBundle['grantedquestinstanceids'])
                        
                        if loads(open('conf.json', 'r', encoding='utf-8').read())["Profile"]["bCompletedSeasonalQuests"]:
                            profile['items'][ChallengeBundle['itemGuid']]['attributes']['num_quests_completed']=len(ChallengeBundle['grantedquestinstanceids'])
                            profile['items'][ChallengeBundle['itemGuid']]['attributes']['num_progress_quests_completed']=len(ChallengeBundle['grantedquestinstanceids'])
                        
                        ApplyProfileChanges.append({
                            "changeType": "itemAdded",
                            "itemId": ChallengeBundle['itemGuid'],
                            "item": profile['items'][ChallengeBundle['itemGuid']]
                        })
                        
                        StatChanged=True
                
                for i, Quest in enumerate(SeasonQuestIDS['Quests']):
                    if Quest['itemGuid'] in profile['items']:
                        ApplyProfileChanges.append({
                            "changeType": "itemRemoved",
                            "itemId": Quest['itemGuid']
                        })
                    
                    Quest=SeasonQuestIDS['Quests'][i]
                    
                    profile['items'][Quest['itemGuid']]={
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
                        profile['items'][Quest['itemGuid']]['attributes']['quest_state']="Claimed"
                    
                    for x in range(len(Quest['objectives'])):
                        if loads(open('conf.json', 'r', encoding='utf-8').read())["Profile"]['bCompletedSeasonalQuests']:
                            profile['items'][Quest['itemGuid']]['attributes'][f"completion_{Quest['objectives'][x]['name'][0]}"]=Quest['objectives'][x]['count']
                        else:
                            profile['items'][Quest['itemGuid']]['attributes'][f"completion_{Quest['objectives'][x]['name'][0]}"]=0
                    
                    ApplyProfileChanges.append({
                        "changeType": "itemAdded",
                        "itemId": Quest['itemGuid'],
                        "item": profile['items'][Quest['itemGuid']]
                    })
                    
                    StatChanged=True
                
            if StatChanged:
                profile['rvn']+=1
                profile['commandRevision']+=1
                
                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }
            
            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route('/fortnite/api/game/v2/profile/<account>/client/IncrementNamedCounterStat', methods=['POSt'])
        def IncrementNamedCounterStat(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

            ApplyProfileChanges=[]
            BaseRevision=profile['rvn'] or 0
            QueryRevision=request.args['rvn'] or -1
            StatChanged=False

            if "named_counters" in profile['stats']['attributes'] and loads(request.get_data())['counterName']:
                if loads(request.get_data())['counterName'] in profile['stats']['attributes']['named_counters']:
                    profile['stats']['attributes']['named_counters'][loads(request.get_data())['counterName']]['current_count']+=1
                    profile['stats']['attributes']['named_counters'][loads(request.get_data())['counterName']]['last_incremented_time']=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                    
                    StatChanged=True
            
            if StatChanged:
                profile['rvn']+=1
                profile['commandRevision']+=1

                ApplyProfileChanges.append({
                    "changeType": "statModified",
                    "name": "named_counters",
                    "value": profile['stats']['attributes']['named_counters']
                })

                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if QueryRevision!=BaseRevision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get("profileId") or "athena",
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }

            resp=app.response_class(
                    response=dumps(r),
                    status=200,
                    mimetype='application/json'
                )
            return resp

        @app.route('/fortnite/api/game/v2/profile/', methods=['GET'])
        def handle_request_profile():
            if not request.args.get('profileId') and request.path.lower().startswith('/fortnite/api/game/v2/profile/'):
                error={'error': 'Profile not defined.'}
                resp=app.response_class(
                    response=dumps(error),
                    status=200,
                    mimetype='application/json'
                )
                return resp

            for file in ['data/profiles/athena.json', 'data/profiles/profile0.json', 'data/common_core.json']:
                memory = self.functions.getVersion()

                profile=loads(open(file, 'r', encoding='utf-8').read())[self.session.get('username')].copy()
                        
                if not profile.get('rvn'):
                    profile['rvn'] = 0
                if not profile.get('items'):
                    profile['items']={}
                if not profile.get('stats'):
                    profile['stats'] = {}
                if not profile['stats'].get('attributes'):
                    profile['stats']['attributes'] = {}
                if not profile.get('commandRevision'):
                    profile['commandRevision'] = 0

                if file == 'athena.json':
                    SeasonData=loads(open(f'data/profiles/seasondata.json', 'r', encoding='utf-8').read())
                    profile['stats']['attributes']['season_num'] = memory['season']

                    if f'Season{memory["season"]}' in SeasonData[self.session.get('username')]:
                        SeasonDatas = SeasonData[self.session.get('username')][f'Season{memory["season"]}']

                        profile['stats']['attributes']['book_purchased'] = SeasonDatas['battlePassPurchased']
                        profile['stats']['attributes']['book_level'] = SeasonDatas['battlePassTier']
                        profile['stats']['attributes']['season_match_boost'] = SeasonDatas['battlePassXPBoost']
                        profile['stats']['attributes']['season_friend_match_boost'] = SeasonDatas['battlePassXPFriendBoost']

                    oldprofile=loads(open(file, 'r', encoding='utf-8').read())
                    oldprofile[self.session.get('username')]=profile
                    open(file, 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))

            return Response(status=200)

        @app.route("/fortnite/api/game/v2/profile/<account>/client/RefundMtxPurchase", methods=["POST"])
        def refund_mtx_purchase(account):
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()
            item_profile=loads(open(f'data/profiles/athena.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()

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

                        for key, item in profile["items"]:
                            if item["templateId"].lower().startswith("currency:mtx"):
                                if item["attributes"]["platform"].lower() == profile["stats"]["attributes"]["current_mtx_platform"].lower() or item["attributes"]["platform"].lower() == "shared":
                                    item["quantity"] += profile["stats"]["attributes"]["mtx_purchase_history"]["purchases"][purchase]["totalMtxPaid"]

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

                item_profile['rvn']+=1
                item_profile['commandRevision']+=1
                profile['rvn']+=1
                profile['commandRevision']+=1
                
                stat_changed=True
            
            if stat_changed:
                apply_profile_changes.append({
                    "changeType": "statModified",
                    "name": "mtx_purchase_history",
                    "value": profile['stats']['attributes']['mtx_purchase_history']
                })
                
                multi_update[0]['profileRevision']=item_profile['rvn'] or 0
                multi_update[0]['profileCommandRevision']=item_profile['commandRevision'] or 0
                
                oldprofile=loads(open(f'data/profiles/athena.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=item_profile
                open(f'data/profiles/athena.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
                
                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "common_core"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))
            
            if query_revision!=base_revision:
                ApplyProfileChanges=[{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
            
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get('profileId') or 'common_core',
                "profileChangesBaseRevision": base_revision,
                "profileChanges": ApplyProfileChanges,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "multiUpdate": multi_update,
                "responseVersion": 1
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp

        @app.route("/fortnite/api/game/v2/profile/<account>/client/FortRerollDailyQuest", methods=["POST"])
        def FortRerollDailyQuest(account):
            
            
            if not ospath.exists(f'data/profiles/{request.args.get("profileId")}.json'):
                r={
                    "profileRevision": 0,
                    "profileId": request.args.get("profileId"),
                    "profileChangesBaseRevision": 0,
                    "profileChanges": [],
                    "profileCommandRevision": 0,
                    "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "responseVersion": 1
                }

                resp=app.response_class(
                        response=dumps(r),
                        status=200,
                        mimetype='application/json'
                    )
                return resp
            
            profile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[self.session.get('username')].copy()
            DailyQuestIDS=loads(open(f'data/items/quests.json', 'r', encoding='utf-8').read())

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
                profile['rvn']+=1
                profile['commandRevision']+=1
                
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

                oldprofile=loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())
                oldprofile[self.session.get('username')]=profile
                open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(oldprofile, indent=4))

            if QueryRevision != BaseRevision:
                apply_profile_changes = [{
                    "changeType": "fullProfileUpdate",
                    "profile": profile
                }]
                
            r={
                "profileRevision": profile['rvn'] or 0,
                "profileId": request.args.get('profileId') or 'athena',
                "profileChangesBaseRevision": BaseRevision,
                "profileChanges": apply_profile_changes,
                "notifications": Notifications,
                "profileCommandRevision": profile['commandRevision'] or 0,
                "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "responseVersion": 1
            }

            resp=app.response_class(
                response=dumps(r),
                status=200,
                mimetype='application/json'
            )
            return resp


        app.run('0.0.0.0', port, debug=False)