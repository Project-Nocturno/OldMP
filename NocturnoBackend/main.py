from flask import Flask, request, Response, send_from_directory
import json
import uuid
from datetime import datetime
import os
import hashlib
import sys
import configparser
import random
import requests



config=configparser.ConfigParser()
config.read('data/Config/config.ini')
Memory_CurrentAccountID=config['Config']['displayName']

api_url='https://nocturno.games/api'
app=Flask("Nocturno Backend")


class Data():
    def __init__(self, usernm: str, api_url: str='https://nocturno.games/api', url_key: str='VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0'):
        self.usernm=usernm
        self.api_url=api_url
        self.mtx=int(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=mtx', verify=False).json())
        self.items=list(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=items', verify=False).json())
        self.level=int(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=level', verify=False).json())
        self.xp=int(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=exp', verify=False).json())
        self.top1=int(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=top1', verify=False).json())
        self._catalogconfig=dict(requests.get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=shop', verify=False).json())
        self._discover_frontend=dict(requests.get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=discoverfrontend', verify=False).json())
        self._keychain=list(requests.get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=keychain', verify=False).json())
        self._contentpages=dict(requests.get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=contentpages', verify=False).json())
        self._catalog=dict(requests.get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=catalog', verify=False).json())
        self._data={
            'athena': [], 
            'profile0': [], 
            'common_core': [], 
            'common_public': [], 
            'collections': [], 
            'seasondata': [], 
            'friendlist': [], 
            'friendlistv2': [], 
            'quests': [], 
            'privacy': [],
            'catalogconfig': [],
            'discover_frontend': [],
            'keychain': [],
            'contentpages': [],
            'catalog': []
        }
        self._data['privacy']=json.loads(self.privacy())
        self._data['athena']=json.loads(self.athena())
        self._data['common_core']=json.loads(self.commoncore())
        self._data['common_public']=json.loads(self.commonpublic())
        self._data['profile0']=json.loads(self.profile0())
        self._data['collections']=json.loads(self.collections())
        self._data['seasondata']=json.loads(self.seasondata())
        self._data['friendlist']=json.loads(self.friendlist())
        self._data['friendlistv2']=json.loads(self.friendlistv2())
        self._data['quests']=json.loads(self.quests())
        self._data['catalogconfig']=self._catalogconfig
        self._data['discover_frontend']=self._discover_frontend
        self._data['keychain']=self._keychain
        self._data['contentpages']=self._contentpages
        self._data['catalog']=self._catalog
    
    def athena(self):
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
        self._athena={
            "created": "0001-01-01T00:00:00.000Z",
            "updated": "0001-01-01T00:00:00.000Z",
            "rvn": 0,
            "wipeNumber": 1,
            "accountId": self.usernm,
            "profileId": "athena",
            "version": "no_version",
            "items": {},
            "stats": {
                "attributes": {
                    "past_seasons": [],
                    "season_match_boost": 0,
                    "loadouts": [
                        "ettrr4h-2wedfgbn-8i9jsghj-lpw9t2to-loadout1"
                    ],
                    "favorite_victorypose": "",
                    "mfa_reward_claimed": True,
                    "quest_manager": {
                        "dailyLoginInterval": "0001-01-01T00:00:00.000Z",
                        "dailyQuestRerolls": 1
                    },
                    "book_level": 0,
                    "season_num": 3,
                    "favorite_consumableemote": "",
                    "banner_color": "DefaultColor14",
                    "favorite_callingcard": "",
                    "favorite_character": "AthenaCharacter:CID_001_Athena_Commando_F_Default",
                    "favorite_spray": [],
                    "book_xp": 0,
                    "battlestars": 0,
                    "battlestars_season_total": 0,
                    "style_points": 0,
                    "alien_style_points": 0,
                    "party_assist_quest": "",
                    "pinned_quest": "",
                    "purchased_bp_offers": [],
                    "favorite_loadingscreen": "",
                    "book_purchased": False,
                    "lifetime_wins": self.top1,
                    "favorite_hat": "",
                    "level": self.level,
                    "favorite_battlebus": "",
                    "favorite_mapmarker": "",
                    "favorite_vehicledeco": "",
                    "accountLevel": self.level,
                    "favorite_backpack": "",
                    "favorite_dance": [
                        "AthenaDance:eid_dancemoves",
                        "",
                        "",
                        "",
                        "",
                        ""
                    ],
                    "inventory_limit_bonus": 0,
                    "last_applied_loadout": "",
                    "favorite_skydivecontrail": "",
                    "favorite_pickaxe": "AthenaPickaxe:DefaultPickaxe",
                    "favorite_glider": "AthenaGlider:DefaultGlider",
                    "daily_rewards": {},
                    "xp": self.xp,
                    "season_friend_match_boost": 0,
                    "active_loadout_index": 0,
                    "favorite_musicpack": "AthenaMusicPack:MusicPack_119_CH1_DefaultMusic",
                    "banner_icon": "StandardBanner1",
                    "favorite_itemwraps": [
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        ""
                    ]
                }
            },
            "commandRevision": 0
        }
        new_items={
            "ettrr4h-2wedfgbn-8i9jsghj-lpw9t2to-loadout1": {
                "templateId": "CosmeticLocker:cosmeticlocker_athena",
                "attributes": {
                    "locker_slots_data": {
                        "slots": {
                            "MusicPack": {
                                "items": [
                                    "AthenaMusicPack:MusicPack_119_CH1_DefaultMusic"
                                ]
                            },
                            "Character": {
                                "items": [
                                    "AthenaCharacter:CID_001_Athena_Commando_F_Default"
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
                      "locker_name": "NocturnoServer",
                      "item_seen": False,
                      "favorite": False
                  },
                  "quantity": 1
              }
          }
        self.items_id=[]
        for i in self.items:
            for x in self.exchange_table:
                if i==x['name']:
                    self.items_id.append(x['id'])
        
        conv_table=[
            {'name': 'skins', 'id': 'AthenaCharacter'}, 
            {'name': 'backpacks', 'id': 'AthenaBackpack'}, 
            {'name': 'gliders', 'id': 'AthenaGlider'},
            {'name': 'pickaxes', 'id': 'AthenaPickaxe'},
            {'name': 'musicspacks', 'id': 'AthenaMusicPack'},
            {'name': 'loadingscreens', 'id': 'AthenaLoadingScreen'}
        ]
        
        for i in self.items_id:
            for x in self.exchange_table:
                if i==x['id']:
                    for z in conv_table:
                        if z['name']==x['style']:
                            i=f"{z['id']}:{i}"
                            item_temp={
                                i: {
                                      "templateId": i,
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
                            new_items.update(item_temp)
        self._athena['items']=new_items
        
        return json.dumps(self._athena, indent=4)

    def commoncore(self):
        self._commoncore={
            "created": "0001-01-01T00:00:00.000Z",
            "updated": "0001-01-01T00:00:00.000Z",
            "rvn": 0,
            "wipeNumber": 1,
            "accountId": self.usernm,
            "profileId": "common_core",
            "version": "no_version",
            "items": {
                "Campaign": {
                "templateId": "",
                "attributes": {
                    "max_level_bonus": 0,
                    "level": 1,
                    "item_seen": False,
                    "xp": 0,
                    "favorite": False
                },
                "quantity": 1
                },
                "Currency": {
                "templateId": "Currency:MtxPurchased",
                "attributes": {
                    "platform": "EpicPC"
                },
                "quantity": 1000000000
                },
                "Token:FounderChatUnlock": {
                "templateId": "Token:FounderChatUnlock",
                "attributes": {
                    "max_level_bonus": 0,
                    "level": self.level,
                    "item_seen": True,
                    "xp": self.xp,
                    "favorite": False
                },
                "quantity": 1
                }
            },
            "stats": {
                "attributes": {
                    "survey_data": {},
                    "personal_offers": {},
                    "intro_game_played": True,
                    "import_friends_claimed": {},
                    "mtx_purchase_history": {
                        "refundsUsed": 0,
                        "refundCredits": 3,
                        "purchases": []
                    },
                    "undo_cooldowns": [],
                    "mtx_affiliate_set_time": "",
                    "inventory_limit_bonus": 0,
                    "current_mtx_platform": "EpicPC",
                    "mtx_affiliate": "",
                    "forced_intro_played": "Coconut",
                    "weekly_purchases": {},
                    "daily_purchases": {},
                    "ban_history": {},
                    "in_app_purchases": {},
                    "permissions": [],
                    "undo_timeout": "min",
                    "monthly_purchases": {},
                    "allowed_to_send_gifts": True,
                    "mfa_enabled": True,
                    "allowed_to_receive_gifts": True,
                    "gift_history": {}
                }
            },
            "commandRevision": 0
        }
        
        return json.dumps(self._commoncore, indent=4)

    def collections(self):
        self._collections={
            "_id": self.usernm,
            "created": "0001-01-01T00:00:00.000Z",
            "updated": "0001-01-01T00:00:00.000Z",
            "rvn": 0,
            "wipeNumber": 1,
            "accountId": self.usernm,
            "profileId": "collections",
            "version": "no_version",
            "items": {},
            "stats": {
                "attributes": {}
            },
            "commandRevision": 0
        }
        return json.dumps(self._collections, indent=4)     

    def seasondata(self):
          self._seasondata={
              "Season2": {
                  "battlePassPurchased": False,
                  "battlePassTier": 0,
                  "battlePassXPBoost": 0,
                  "battlePassXPFriendBoost": 0
              },
              "Season3": {
                  "battlePassPurchased": False,
                  "battlePassTier": 0,
                  "battlePassXPBoost": 0,
                  "battlePassXPFriendBoost": 0
              },
              "Season4": {
                  "battlePassPurchased": False,
                  "battlePassTier": 0,
                  "battlePassXPBoost": 0,
                  "battlePassXPFriendBoost": 0
              },
              "Season5": {
                  "battlePassPurchased": False,
                  "battlePassTier": 0,
                  "battlePassXPBoost": 0,
                  "battlePassXPFriendBoost": 0
              }
          }
          return json.dumps(self._seasondata, indent=4)

    def friendlist(self):
        self._friendlist=[
            {
                "accountId": self.usernm,
                "status": "ACCEPTED",
                "direction": "OUTBOUND",
                "created": "2022-09-15T19:37:28.837Z",
                "favorite": False
            }
        ]
        return json.dumps(self._friendlist, indent=4)
      
    def friendlistv2(self):
        self._friendlistv2={
            "friends": [
                {
                    "accountId": self.usernm,
                    "groups": [],
                    "mutual": 0,
                    "alias": "",
                    "note": "",
                    "favorite": False,
                    "created": "2022-09-15T19:37:28.837Z"
                }
            ],
            "incoming": [],
            "outgoing": [],
            "suggested": [],
            "blocklist": [],
            "settings": {
                "acceptInvites": "public"
            }
        }
        return json.dumps(self._friendlistv2, indent=4)

    def commonpublic(self):
          self._commonpublic={
            "created": "0001-01-01T00:00:00.000Z",
            "updated": "0001-01-01T00:00:00.000Z",
            "rvn": 0,
            "wipeNumber": 1,
            "accountId": "",
            "profileId": "common_public",
            "version": "no_version",
            "items": {},
            "stats": {
                "attributes": {
                    "banner_color": "DefaultColor14",
                    "homebase_name": "",
                    "banner_icon": "SurvivalBannerStonewoodComplete"
                }
            },
            "commandRevision": 0
          }
          return json.dumps(self._commonpublic, indent=4)

    def quests(self):
        self._quests={
          "author": "Created by PRO100KatYT, edited by 4lxprime",
          "BattleRoyale": {
              "Daily": [],
              "Season3": {},
              "Season4": {},
              "Season5": {}
          }
        }
        return json.dumps(self._quests, indent=4)
    
    def privacy(self):
        self._privacy={
            "accountId": "",
            "optOutOfPublicLeaderboards": False
        }
        return json.dumps(self._privacy, indent=4)
      
    def profile0(self):
          self._profile0={
              "_id": self.usernm,
              "created": "0001-01-01T00:00:00.000Z",
              "updated": "0001-01-01T00:00:00.000Z",
              "rvn": 0,
              "wipeNumber": 1,
              "accountId": self.usernm,
              "profileId": "profile0",
              "version": "no_version",
              "items": {},
              "stats": {
                  "templateId": "profile_v2",
                  "attributes": {
                      "mtx_purchase_history": {
                          "purchases": []
                      },
                      "mission_alert_redemption_record": {
                          "lastClaimTimesMap": {
                              "General": {
                                  "missionAlertGUIDs": [
                                      "",
                                      "",
                                      ""
                                  ],
                                  "lastClaimedTimes": []
                              },
                              "StormLow": {
                                  "missionAlertGUIDs": [],
                                  "lastClaimedTimes": []
                              },
                              "Halloween": {
                                  "missionAlertGUIDs": [],
                                  "lastClaimedTimes": []
                              },
                              "Horde": {
                                  "missionAlertGUIDs": [],
                                  "lastClaimedTimes": []
                              },
                              "Storm": {
                                  "missionAlertGUIDs": [],
                                  "lastClaimedTimes": []
                              }
                          },
                          "oldestClaimIndexForCategory": [
                                0,
                                0,
                                0,
                                0,
                                0
                          ]
                      },
                      "twitch": {},
                      "client_settings": {
                          "pinnedQuestInstances": []
                      },
                      "level": self.level,
                      "named_counters": {
                          "SubGameSelectCount_Campaign": {
                              "current_count": 0,
                              "last_incremented_time": ""
                          },
                        "SubGameSelectCount_Athena": {
                            "current_count": 0,
                            "last_incremented_time": ""
                        }
                      },
                      "default_hero_squad_id": "",
                      "collection_book": {
                          "pages": [],
                          "maxBookXpLevelAchieved": 0
                      },
                      "quest_manager": {
                          "dailyLoginInterval": "",
                          "dailyQuestRerolls": 1
                      },
                      "bans": {},
                      "gameplay_stats": [
                          {
                              "statName": "zonescompleted",
                              "statValue": 1
                          }
                      ],
                      "inventory_limit_bonus": 100000,
                      "current_mtx_platform": "Epic",
                      "weekly_purchases": {},
                      "daily_purchases": {
                          "lastInterval": "2017-08-29T00:00:00.000Z",
                          "purchaseList": {
                              "1F6B613D4B7BAD47D8A93CAEED2C4996": 1
                          }
                      },
                      "mode_loadouts": [
                          {
                              "loadoutName": "Default",
                              "selectedGadgets": [
                                  "",
                                  ""
                              ]
                          }
                      ],
                      "in_app_purchases": {
                          "receipts": [
                              "EPIC:0aba47abf15143f18370dbc70b910b14",
                              "EPIC:ee397e98af0042159fec830aea1224d5"
                          ],
                          "fulfillmentCounts": {
                              "0A6CB5B346A149F31A4C3FBDF4BBC198": 3,
                              "DEF6D31D416227E7D73F65B27288ED6F": 1,
                              "82ADCC874CFC2D47927208BAE871CF2B": 1,
                              "F0033207441AC38CD704718B91B2C8EF": 1
                          }
                      },
                      "daily_rewards": {
                        "nextDefaultReward": 0,
                        "totalDaysLoggedIn": 0,
                        "lastClaimDate": "2022-09-15T00:00:00.000Z",
                        "additionalSchedules": {
                            "founderspackdailyrewardtoken": {
                                "rewardsClaimed": 0,
                                "claimedToday": True
                            }
                        }
                      },
                      "monthly_purchases": {},
                      "xp": self.xp,
                      "homebase": {
                          "townName": "Nocturno Town",
                          "bannerIconId": "OT10Banner",
                          "bannerColorId": "DefaultColor14",
                          "flagPattern": -1,
                          "flagColor": -1
                      },
                      "packs_granted": 0
                  }
              },
              "commandRevision": 0
          }
          return json.dumps(self._profile0, indent=4)
    
    def alldata(self):
        return json.dumps(self._data, indent=4)
    

data=json.loads(Data(usernm='4lxprime').alldata())




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
                "lobby": "LobbyWinterDecor"
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



def getShop():
    catalog_config=data['catalogconfig']
    catalog=data['catalog']

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
    
    contentpage=data['contentpages']
    
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




@app.route('/clearitemsforshop', methods=['GET'])
def cleanitem():
    
    athena=data['athena']
    shop=data['catalogconfig']
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
        
        data[request.args.get("profileid") or "athena"]=athena
        
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
        response=json.dumps({}),
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
        "https://projectnocturno.ol.epicgames.com/"
    ]}

    head={"Content-Type": "application/json"}

    resp=app.response_class(
        response=json.dumps(distrib),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/launcher/api/public/assets/', methods=['GET'])
def publicsaassets():
    assets={
        "appName": "FortniteContentBuilds",
        "labelName": "NocturnoBackend",
        "buildVersion": "++Fortnite+Release-20.00-CL-19458861-Windows",
        "catalogItemId": "5cb97847cee34581afdbc445400e2f77",
        "expires": "9999-12-31T23:59:59.999Z",
        "items": {
            "MANIFEST": {
                "signature": "NocturnoBackend",
                "distribution": "https://nocturnoBackend.ol.epicgames.com/",
                "path": "Builds/Fortnite/Content/CloudDir/NocturnoBackend.manifest",
                "hash": "55bb954f5596cadbe03693e1c06ca73368d427f3",
                "additionalDistributions": []
            },
            "CHUNKS": {
                "signature": "NocturnoBackend",
                "distribution": "https://nocturnoBackend.ol.epicgames.com/",
                "path": "Builds/Fortnite/Content/CloudDir/NocturnoBackend.manifest",
                "additionalDistributions": []
            }
        },
        "assetId": "FortniteContentBuilds"
    }

    resp=app.response_class(
        response=json.dumps(assets),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/Builds/Fortnite/Content/CloudDir/*.manifest', methods=['GET'])
def fortnitebuildclouddirmanifest():

    manifest=open('data/connect/CloudDir/NocturnoBackend.manifest', 'r', encoding="utf-8").read()

    resp=app.response_class(
        response=json.dumps(manifest),
        status=200,
        mimetype='application/octet-stream'
    )
    return resp
    
@app.route('/Builds/Fortnite/Content/CloudDir/*.chunck', methods=['GET'])
def fortnitebuildclouddirchunck():

    chunck=open('data/connect/CloudDir/NocturnoBackend.chunc', 'r', encoding="utf-8").read()

    resp=app.response_class(
        response=json.dumps(chunck),
        status=200,
        mimetype='application/octet-stream'
    )
    return resp

@app.route('/Builds/Fortnite/Content/CloudDir/*.ini', methods=['GET'])
def fortnitebuildclouddirini():
        
    ini=open('data/connect/CloudDir/NocturnoBackend.ini', 'r', encoding="utf-8").read()

    resp=app.response_class(
        response=json.dumps(ini),
        status=200,
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
        response=json.dumps(socialban),
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
        "accountId": accountId
    }

    resp=app.response_class(
        response=json.dumps(account),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/api/v1/events/Fortnite/download/', methods=['GET'])
def apieventsdownload():
    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/friendcodes/<idk>/epic', methods=['GET'])
def apifriendcodesepic(idk):
    resp=app.response_class(
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/events/tournamentandhistory/<idk>EU/WindowsClient', methods=['GET'])
def apiWindowsClientEU(idk):
    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/presence/api/v1/_/<account>/last-online', methods=['GET'])
def apipresence(account):
    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/leaderboards/cohort/<account>', methods=['GET'])
def fortniteapileaderboards(account):
    resp=app.response_class(
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )
    return resp

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
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/receipts/v1/account/<account>/receipts', methods=['GET'])
def apireceipts(account):
    resp=app.response_class(
        response=json.dumps([]),
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
        response=json.dumps(regions),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/matchmaking/session/findPlayer/<account>', methods=['GET'])
def apisessionfindplayer(account):
    resp=Response()
    resp.status_code=200
    return resp

@app.route('/fortnite/api/matchmaking/session/<sessionId>', methods=['GET'])
def apimatchmakingsessionid(sessionId):

    session={
        "id": sessionId,
        "ownerId": uuid.uuid4(),
        "ownerName": "[DS]fortnite-liveeugcec1c2e30ubrcore0a-z8hj-1968",
        "serverName": "[DS]fortnite-liveeugcec1c2e30ubrcore0a-z8hj-1968",
        "serverAddress": "0.0.0.0",
        "serverPort": 3551,
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
            "SESSIONKEY_s": uuid.uuid4(),
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
        "allowJoinViaPresence": True,
        "allowJoinViaPresenceFriendsOnly": False,
        "buildUniqueId": request.cookies.get('currentbuildUniqueId') or "0",
        "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "started": False
    }

    resp=app.response_class(
        response=json.dumps(session),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/affiliate/api/public/affiliates/slug/<slugs>', methods=['GET'])
def affiliateslug(slugs):
    
    SupportedCodes=json.loads([])
    
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
                response=json.dumps(slug),
                status=200,
                mimetype='application/json'
            )
            return resp

    if not ValidCode:
        resp=app.response_class(
            response=json.dumps(slug),
            status=200,
            mimetype='application/json'
        )
        return resp

@app.route('/fortnite/api/cloudstorage/system', methods=['GET'])
def cloudstoragesystem():

    CloudFiles=[]

    for name in os.listdir("data/CloudStorage"):
        if name.endswith('.ini'):
            
            ParsedFile=open(f'data/CloudStorage/{name}', 'r', encoding="utf-8").read()
            
            length=os.path.getsize(f'data/CloudStorage/{name}')
            mtime=os.path.getmtime(f'data/CloudStorage/{name}')
            
            CloudFiles.append({
                "uniqueFilename": name,
                "filename": name,
                "hash": hashlib.sha1(ParsedFile.encode()).hexdigest(),
                "hash256": hashlib.sha256(ParsedFile.encode()).hexdigest(),
                "length": length,
                "contentType": "application/octet-stream",
                "uploaded": datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "storageType": "S3",
                "storageIds": {},
                "doNotCache": True
            })
            
    resp=app.response_class(
        response=json.dumps(CloudFiles),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route("/fortnite/api/cloudstorage/system/<file>", methods=["GET"])
def get_file(file):
    file_path=f'data/CloudStorage/{file}'
    if os.path.exists(file_path):
        return send_from_directory("data/CloudStorage", file)
    else:
        response=app.response_class(
            response="",
            status=200
        )
        return response
    
@app.route('/fortnite/api/cloudstorage/user/<account>/<files>', methods=['GET'])
def cloudstoragesystemallfile(account, files):
    
    if files!="ClientSettings.Sav":
        resp=app.response_class(
            response=json.dumps({"error": "file not found"}),
            status=404,
            mimetype='application/json'
        )
        return resp
    
    memory=getVersion(request=request)
    currentBuildID=memory['CL']
    
    if os.path.exists(f'{os.path.dirname(__file__)}/ClientSettings/ClientSettings-{currentBuildID}.Sav'):
        ParsedFile=open(f'{os.path.dirname(__file__)}/ClientSettings/ClientSettings-{currentBuildID}.Sav', 'r', encoding="Latin-1").read()
        resp=app.response_class(
            response=ParsedFile,
            status=200,
            mimetype='application/octet-stream'
        )
        return resp
    
    else:
        resp=Response()
        resp.status_code=200
        return resp
    
@app.route(f'/fortnite/api/cloudstorage/user/<accountId>', methods=['GET'])
def cloudstorageaccid(accountId):
    
    memory=getVersion(request=request)
    currentBuildID=memory['CL']
    
    file=f'{os.path.dirname(__file__)}/ClientSettings/ClientSettings-{currentBuildID}.Sav'
    
    if os.path.exists(file):
        
        ParsedFile=open(file, 'r', encoding="Latin-1").read()
        
        mtime=os.path.getmtime(file)
        result=[{
            "uniqueFilename": "ClientSettings.Sav",
            "filename": "ClientSettings.Sav",
            "hash": hashlib.sha1(ParsedFile.encode()).hexdigest(),
            "hash256": hashlib.sha256(ParsedFile.encode()).hexdigest(),
            "length": sys.getsizeof(ParsedFile),
            "contentType": "application/octet-stream",
            "uploaded": datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "storageType": "S3",
            "storageIds": {},
            "accountId": accountId,
            "doNotCache": True
        }]
        
        resp=app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
        return resp
    
    else:
        
        resp=app.response_class(
            response=json.dumps([]),
            status=200,
            mimetype='application/json'
        )
        return resp
    
@app.route('/content/api/pages/', methods=['GET'])
@app.route('/content/api/pages/fortnite-game', methods=['GET'])
def contentapipages():
    
    contentpages=getContentPages(request=request)
    
    resp=app.response_class(
            response=json.dumps(contentpages),
            status=200,
            mimetype='application/json'
        )
    return resp

@app.route('/links/api/fn/mnemonic/', methods=['GET'])
def linksmnemonic():
        
    discover=data['discover_frontend']
    
    for i in discover['Panels'][0]['Pages'][0]['results']:
        if discover['Panels'][0]['Pages'][0]['results'][i]['linkData']['mnemonic']==request.url.split("/").slice(-1)[0]:
    
            resp=app.response_class(
                response=json.dumps(discover['Panels'][0]['Pages'][0]['results'][i]['linkData']),
                status=200,
                mimetype='application/json'
            )
            return resp

@app.route('/friends/api/v1/<account>/settings', methods=['GET'])
def friendssettings(account):
    
    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/friends/api/v1/<account>/blocklist', methods=['GET'])
def friendsblocklist(account):
    
    resp=app.response_class(
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )
    return resp

def sendXmppMessageToAll(body):
    """get all flask clients and send an xmpp global message"""

@app.route(f'/friends/api/public/friends/<accountId>', methods=['GET'])
def friendsaccountID(accountId):
    
    friendslist=data['friendlist']
    friendslist2=data['friendlistv2']

    for z in friendslist:
        if z['accountId']!=accountId:
            FriendObject={
            "accountId": accountId,
            "status": "ACCEPTED",
            "direction": "OUTBOUND",
            "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "favorite": False
            }
            break
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
    
    """
    sendXmppMessageToAll({
            "payload": FriendObject,
            "type": "com.epicgames.friends.core.apiobjects.Friend",
            "timestamp": FriendObject.created
        })

    sendXmppMessageToAll({
        "type": "FRIENDSHIP_REQUEST",
        "timestamp": FriendObject.created,
        "from": FriendObject.accountId,
        "status": FriendObject.status
    })
    """
    data['friendlist']=friendslist
    data['friendlistv2']=friendslist2

    resp=app.response_class(
        response=json.dumps(friendslist),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route(f'/friends/api/v1/<accountId>/summary', methods=['GET'])
def friendsaccountIDsummary(accountId):
        
    friendslist=data['friendlist']
    friendslist2=data['friendlistv2']

    for i in friendslist2[0]['friends']['accountId']:
        if i!=accountId:
            FriendObject={
            "accountId": accountId,
            "groups": [],
            "mutual": 0,
            "alias": "",
            "note": "",
            "favorite": False,
            "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
            break
    friendslist2['friends'].append(FriendObject)
    friendslist.append({
        "accountId": FriendObject['accountId'],
        "status": "ACCEPTED",
        "direction": "OUTBOUND",
        "favorite": FriendObject['favorite'],
        "created": FriendObject['created']
    })
    
    """
    sendXmppMessageToAll({
        "payload": {
            "accountId": FriendObject.accountId,
            "status": "ACCEPTED",
            "direction": "OUTBOUND",
            "created": FriendObject.created,
            "favorite": FriendObject.favorite
        },
        "type": "com.epicgames.friends.core.apiobjects.Friend",
        "timestamp": FriendObject.created
    })

    sendXmppMessageToAll({
        "type": "FRIENDSHIP_REQUEST",
        "timestamp": FriendObject.created,
        "from": FriendObject.accountId,
        "status": "ACCEPTED"
    })
    """
    data['friendlist']=friendslist
    data['friendlistv2']=friendslist2

    resp=app.response_class(
        response=json.dumps(friendslist),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/friends/api/public/list/fortnite/<account>/recentPlayers', methods=['GET'])
def friendsrecentplayers(account):
    
    resp=app.response_class(
        response=json.dumps([]),
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
        response=json.dumps(blocked),
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
        response=json.dumps(service),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/lightswitch/api/service/bulk/status', methods=['GET'])
def lightswitchservicebulkstatus():
    
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
          "banned": False,
          "launcherInfoDTO": {
              "appName": "Fortnite",
              "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
              "namespace": "fn"
          }
      }]

    resp=app.response_class(
        response=json.dumps(service2),
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
        response=json.dumps(party),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route(f'/fortnite/api/game/v2/privacy/account/<accountId>', methods=['GET'])
def privacyaccountid(accountId):
    
    privacy=data['privacy']
    
    privacy['accountId']=accountId

    resp=app.response_class(
        response=json.dumps(privacy),
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
    
    catalog=getShop()

    resp=app.response_class(
        response=json.dumps(catalog),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/storefront/v2/keychain', methods=['GET'])
def storefrontkeychain():
    
    keychain=data['keychain']

    resp=app.response_class(
        response=json.dumps(keychain),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/catalog/api/shared/bulk/offers', methods=['GET'])
def catalogapisharedoffers():

    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/calendar/v1/timeline', methods=['GET'])
def apitimeline():

    memory=getVersion(request=request)
    
    activeEvents=[
    {
        "eventType": f'EventFlag.Season{memory["season"]}',
        "activeUntil": "9999-12-31T00:00:00.000Z",
        "activeSince": "2020-01-01T00:00:00.000Z"
    },
    {
        "eventType": f'EventFlag.{memory["lobby"]}',
        "activeUntil": "9999-12-31T00:00:00.000Z",
        "activeSince": "2020-01-01T00:00:00.000Z"
    }]
    
    if memory["season"]==3:
        activeEvents.append({
            "eventType": "EventFlag.Spring2018Phase1",
            "activeUntil": "2023-2-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })
        if memory['build']>=3.1:
            activeEvents.append({
                "eventType": "EventFlag.Spring2018Phase2",
                "activeUntil": "2023-2-14T10:05:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        if memory['build']>=3.3:
            activeEvents.append({
                "eventType": "EventFlag.Spring2018Phase3",
                "activeUntil": "9999-12-31T00:00:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        if memory['build']>=3.4:
            activeEvents.append({
                "eventType": "EventFlag.Spring2018Phase4",
                "activeUntil": "9999-12-31T00:00:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
    if memory["season"]==4:
        activeEvents.append({
            "eventType": "EventFlag.Blockbuster2018",
            "activeUntil": "9999-12-31T00:00:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.Blockbuster2018Phase1",
            "activeUntil": "9999-12-31T00:00:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })
        if memory['build']>=4.3:
            activeEvents.append({
                "eventType": "EventFlag.Blockbuster2018Phase2",
                "activeUntil": "9999-12-31T00:00:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        if memory['build']>=4.4:
            activeEvents.append({
                "eventType": "EventFlag.Blockbuster2018Phase3",
                "activeUntil": "9999-12-31T00:00:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        if memory['build']>=4.5:
            activeEvents.append({
                "eventType": "EventFlag.Blockbuster2018Phase4",
                "activeUntil": "9999-12-31T00:00:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
    if memory["season"]==5:
        activeEvents.append({
            "eventType": "EventFlag.RoadTrip2018",
            "activeUntil": "9999-12-31T00:00:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.Horde",
            "activeUntil": "9999-12-31T00:00:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.Anniversary2018_BR",
            "activeUntil": "9999-12-31T00:00:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.LTM_Heist",
            "activeUntil": "9999-12-31T00:00:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })
    if memory['build']==5.10:
        activeEvents.append({
            "eventType": "EventFlag.BirthdayBattleBus",
            "activeUntil": "9999-12-31T00:00:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })

    r={
        "channels": {
            "client-matchmaking": {
                "states": [],
                "cacheExpire": "9999-01-01T22:28:47.830Z"
            },
            "client-events": {
                "states": [{
                    "validFrom": "2020-01-01T20:28:47.830Z",
                    "activeEvents": activeEvents,
                    "state": {
                        "activeStorefronts": [],
                        "eventNamedWeights": {},
                        "seasonNumber": memory["season"],
                        "seasonTemplateId": f'AthenaSeason:athenaseason{memory["season"]}',
                        "matchXpBonusPoints": 0,
                        "seasonBegin": "2020-01-01T13:00:000Z",
                        "seasonEnd": "9999-12-31T00:00:00.000Z",
                        "seasonDisplayedEnd": "9999-12-31T00:00:00.000Z",
                        "weeklyStoreEnd": "9999-12-31T00:00:00.000Z",
                        "stwEventStoreEnd": "9999-12-31T00:00:00.000Z",
                        "stwWeeklyStoreEnd": "9999-12-31T00:00:00.000Z",
                        "dailyStoreEnd": "9999-12-31T00:00:00.000Z"
                    }
                }],
                "cacheExpire": "9999-01-01T22:28:47.830Z"
            }
        },
        "eventsTimeOffsetHrs": 0,
        "cacheIntervalMins": 10,
        "currentTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    resp=app.response_class(
        response=json.dumps(r),
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
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route(f'/account/api/public/account/<accountId>', methods=['GET'])
def accountpublicaccountid(accountId):

    r={
        "id": accountId,
        "displayName": Memory_CurrentAccountID,
        "name": "Projectnocturno",
        "email": f"{Memory_CurrentAccountID}@projectnocturno.com",
        "failedLoginAttempts": 0,
        "lastLogin": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "numberOfDisplayNameChanges": 0,
        "ageGroup": "UNKNOWN",
        "headless": False,
        "country": "US",
        "lastName": "Server",
        "preferredLanguage": "en",
        "canUpdateDisplayName": False,
        "tfaEnabled": False,
        "emailVerified": True,
        "minorVerified": False,
        "minorExpected": False,
        "minorStatus": "UNKNOWN"
    }
    
    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/account/api/public/account/<accountId>/externalAuths', methods=['GET'])
def accountpublicexternalauths(accountId):
    
    resp=app.response_class(
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/account/api/oauth/verify', methods=['GET'])
def accountoauthverify():

    r={
        "token": "projectnocturnotoken",
        "session_id": "3c3662bcb661d6de679c636744c66b62",
        "token_type": "bearer",
        "client_id": "projectnocturnotoken",
        "internal_client": True,
        "client_service": "fortnite",
        "account_id": Memory_CurrentAccountID,
        "expires_in": 28800,
        "expires_at": "9999-12-02T01:12:01.100Z",
        "auth_method": "exchange_code",
        "display_name": Memory_CurrentAccountID,
        "app": "fortnite",
        "in_app_id": Memory_CurrentAccountID,
        "device_id": "projectnocturnodeviceid"
    }

    resp=app.response_class(
        response=json.dumps(r),
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
        response=json.dumps(r),
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
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/v2/versioncheck/<version>', methods=['GET'])
def fortniteapiv2versioncheck(version):

    r={"type": "NO_UPDATE"}

    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/v2/versioncheck', methods=['GET'])
def fortniteapiv2versioncheck2():

    r={"type": "NO_UPDATE"}

    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/versioncheck', methods=['GET'])
def fortniteapiversioncheck():

    r={"type": "NO_UPDATE"}

    resp=app.response_class(
        response=json.dumps(r),
        mimetype='application/json'
    )
    return resp

#POST

@app.route('/fortnite/api/game/v2/grant_access/<accountId>', methods=['POST'])
def fortniteapiv2grantacces(accountId):

    resp=app.response_class(
        response=json.dumps({}),
        status=204,
        mimetype='application/json'
    )
    return resp

@app.route('/api/v1/user/setting', methods=['POST'])
def apiv1settings():

    resp=app.response_class(
        response=json.dumps([]),
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

    r={
        "startTime": 0,
        "endTime": 0,
        "stats": {},
        "accountId": accountId
    }

    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/statsproxy/api/statsv2/account/<accountId>', methods=['GET'])
def statproxystatsv2account(accountId):

    r={
        "startTime": 0,
        "endTime": 0,
        "stats": {},
        "accountId": accountId
    }

    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/statsv2/query', methods=['POST'])
def fortnitestatsv2query():

    resp=app.response_class(
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/statsproxy/api/statsv2/query', methods=['POST'])
def statproxystatsv2query():

    resp=app.response_class(
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/events/v2/setSubgroup/', methods=['POST'])
def fortniteapigamev2setSubgroup():

    resp=Response()
    resp.status_code=204
    return resp

@app.route('/fortnite/api/game/v2/chat/*/*/*/pc', methods=['POST'])
def fortnitechatpcgame():

    resp=app.response_class(
        response=json.dumps({ "GlobalChatRooms": [{"roomName":"NocturnoBackendglobal"}] }),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/chat/<account>/recommendGeneralChatRooms/pc', methods=['POST'])
def fortnitegamev2recommendGeneralChatRoomspc(account):

    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/datarouter/api/v1/public/data', methods=['POST'])
def datarouterapipublicdata():

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
        response=json.dumps([]),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/*/discovery/surface/', methods=['POST'])
def discoverysurfaceall(idk):

    discovery=data['discover_frontend']

    resp=app.response_class(
        response=json.dumps(discovery),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/links/api/fn/mnemonic', methods=['POST'])
def linksfnmnemonic():

    MnemonicArray=[]
        
    discovery=data['discover_frontend']
        
    for i in discovery['Panels'][0]['Pages'][0]['results']:
        MnemonicArray.append(['Panels'][0]['Pages'][0]['results'][i]['linkData'])

    resp=app.response_class(
        response=json.dumps(MnemonicArray),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/party/api/v1/Fortnite/parties', methods=['POST'])
def partyfortniteapiparties():
    
    if not json.loads(request.get_data('join_info'))['join_info']:
        resp=app.response_class(
            response=json.dumps({}),
            status=200,
            mimetype='application/json'
        )
        return resp
    if not json.loads(request.get_data('join_info'))['join_info']['connection']:
        resp=app.response_class(
            response=json.dumps({}),
            status=200,
            mimetype='application/json'
        )
        return resp

    party={
        "id": uuid.uuid4(),
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "config": {
            "type": "DEFAULT",
            f"{[i for i in json.loads(request.get_data('config'))['config']]}"
            "discoverability": "ALL",
            "sub_type": "default",
            "invite_ttl": 14400,
            "intention_ttl": 60
        },
        "members": [{
            "account_id": (json.loads(request.get_data('join_info'))['join_info']['connection']['id'] or "").split("@prod")[0],
            "meta": json.loads(request.get_data('join_info'))['join_info']['meta'] or {},
            "connections": [
                {
                    "id": json.loads(request.get_data('join_info'))['join_info']['connection']['id'] or "",
                    "connected_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "yield_leadership": False,
                    "meta": json.loads(request.get_data('join_info'))['join_info']['connection']['meta'] or {}
                }
            ],
            "revision": 0,
            "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "joined_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "role": "CAPTAIN"
        }],
        "applicants": [],
        "meta": json.loads(request.get_data('meta'))['meta'] or {},
        "invites": [],
        "revision": 0,
        "intentions": []
    }

    resp=app.response_class(
        response=json.dumps(party),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route(f'/fortnite/api/game/v2/privacy/account/<accountId>', methods=['POST'])
def fortniteapigamev2accountId(accountId):

    privacy=data['privacy']
        
    privacy['accountId']=accountId
    privacy['optOutOfPublicLeaderboards']=json.loads(request.get_data('optOutOfPublicLeaderboards'))['optOutOfPublicLeaderboards']
    
    data['privacy']=privacy

    resp=app.response_class(
        response=json.dumps(privacy),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/account/api/oauth/token', methods=['POST'])
def accountoauthtoken():

    r={
        "access_token": "projectnocturnotoken",
        "expires_in": 28800,
        "expires_at": "9999-12-31T00:00:00.000Z",
        "token_type": "bearer",
        "refresh_token": "projectnocturnotoken",
        "refresh_expires": 86400,
        "refresh_expires_at": "9999-12-31T00:00:00.000Z",
        "account_id": Memory_CurrentAccountID,
        "client_id": "projectnocturnoclientid",
        "internal_client": True,
        "client_service": "fortnite",
        "displayName": Memory_CurrentAccountID,
        "app": "fortnite",
        "in_app_id": Memory_CurrentAccountID,
        "device_id": "projectnocturnodeviceid"
    }

    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/account/api/oauth/exchange', methods=['POST'])
def accountoauthexchange():

    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
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

@app.route('/account/api/oauth/sessions/kill', methods=['DELETE'])
def accountoauthsessionskill():

    resp=Response()
    resp.status_code=204
    return resp

@app.route('/account/api/oauth/sessions/kill/<token>', methods=['DELETE'])
def accountoauthsessionskillall(token):
    
    resp=Response()
    resp.status_code=204
    return resp

@app.route('/fortnite/api/cloudstorage/user/<accountId>/<files>', methods=['PUT'])
def fortnitecloudstorageuserfile(accountId, files):
    if files!="ClientSettings.Sav":
        resp=app.response_class(
            response=json.dumps({"error": "file not found"}),
            status=404,
            mimetype='application/octet-stream'
        )
        return resp
    
    memory=getVersion(request=request)
    
    currentBuildID=memory['CL']
        
    file=f'{os.path.dirname(__file__)}/ClientSettings/ClientSettings-{currentBuildID}.Sav'

    with open(file, 'w', encoding='Latin-1') as f:
        f.write(request.stream.read().decode('Latin-1'))

    resp=Response()
    resp.status_code=204
    return resp

@app.route('/fortnite/api/game/v2/matchmakingservice/ticket/player/<accountId>', methods=['GET'])
def fortniteapigamev2mathcmakingplayerticket(accountId):

    r={
        "serviceUrl": "",
        "ticketType": "mms-player",
        "payload": "69=",
        "signature": "420="
    }

    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    resp.set_cookie("currentbuildUniqueId", request.args.get('bucketId').split(":")[0])
    return resp

@app.route('/fortnite/api/game/v2/matchmaking/account/<accountId>/session/<sessionId>', methods=['GET'])
def fortniteapigamev2mathcmakingsessionid(accountId, sessionId):

    r={
        "accountId": accountId,
        "sessionId": sessionId,
        "key": "AOJEv8uTFmUh7XM2328kq9rlAzeQ5xzWzPIiyKn2s7s="
    }

    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/enabled_features', methods=['GET'])
def apigamev2enabledfeatures():
    
    resp=app.response_class(
        response=json.dumps([]),
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
    
    resp=app.response_class(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return resp

def find(pred, iterable):
    for element in iterable:
        if pred(element):
            return element
    return None

@app.route('/fortnite/api/game/v2/profile/<account>/client/PurchaseCatalogEntry', methods=['POST'])
def PurchaseCatalogEntry(account):
    profile=data[request.args.get('profileId') or 'athena']
    itemId=json.loads(request.get_data('offerId'))['offerId']
    
    ApplyProfileChanges=[]
    BaseRevision=profile['rvn'] or 0
    QueryRevision=request.args.get('rvn') or -1
    
    conv_table=[
        {'name': 'skins', 'id': 'AthenaCharacter'}, 
        {'name': 'backpacks', 'id': 'AthenaBackpack'}, 
        {'name': 'gliders', 'id': 'AthenaGlider'},
        {'name': 'pickaxes', 'id': 'AthenaPickaxe'},
        {'name': 'musicspacks', 'id': 'AthenaMusicPack'},
        {'name': 'loadingscreens', 'id': 'AthenaLoadingScreen'}
    ]
    exchange_table=[
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
    
    exist=False
    
    for i in profile['items']:
        if itemId in i:
            exist=True
    
    if not exist:
        BaseRevision+=1
        for i in exchange_table:
            if itemId==i['id']:
                r=requests.get(f"{api_url}/post/item/item.php?urlkey=VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0&token=&passwd=&usernm=&item={i['name']}")
                for x in conv_table:
                    if i['style']==x['name']:
                        itemId=f"{x['id']}:{itemId}"
                        item={
                            itemId: {
                                "templateId": itemId,
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
                        profile['items'].update(item)
    
    data['athena']=profile
    
    if QueryRevision != BaseRevision:
            ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
    
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get('profileId') or 'athena',
        "profileCommandRevision": BaseRevision or 0,
        "profileChanges": ApplyProfileChanges,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }
    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/SetPartyAssistQuest', methods=['POSt'])
def mcpSetPartyAssistQuest(account):
    
    profile=data[request.args.get("profileid") or "athena"]

    ApplyProfileChanges=[]
    BaseRevision=profile['rvn'] or 0
    QueryRevision=request.args['rvn'] or -1
    StatChanged=False

    if "party_assist_quest" in profile['stats']['attributes']:
        profile['stats']['attributes']=json.loads(request.get_data('questToPinAsPartyAssist'))['questToPinAsPartyAssist'] or ""
        StatChanged=True
    
    if StatChanged:
        profile['rvn']+=1
        profile['commandRevision']+=1

        ApplyProfileChanges.append({
            "changeType": "statModified",
            "name": "party_assist_quest",
            "value": profile['stats']['attributes']['party_assist_quest']
        })

        data[request.args.get("profileid") or "athena"]=profile
    
    if QueryRevision!=BaseRevision:
        ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
    
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get("profileid") or "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }

    resp=app.response_class(
            response=json.dumps(r),
            status=200,
            mimetype='application/json'
        )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/AthenaPinQuest', methods=['POST'])
def mcpAthenaPinQuest(account):
    
    profile=data[request.args.get("profileid") or "athena"]

    ApplyProfileChanges=[]
    BaseRevision=profile['rvn'] or 0
    QueryRevision=request.args['rvn'] or -1
    StatChanged=False

    if "pinned_quest" in profile['stats']['attributes']:
        profile['stats']['attributes']=json.loads(request.get_data('pinned_quest'))['pinned_quest'] or ""
        StatChanged=True
    
    if StatChanged:
        profile['rvn']+=1
        profile['commandRevision']+=1

        ApplyProfileChanges.append({
            "changeType": "statModified",
            "name": "pinned_quest",
            "value": profile['stats']['attributes']['pinned_quest']
        })

        data[request.args.get("profileid") or "athena"]=profile
    
    if QueryRevision!=BaseRevision:
        ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
    
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get("profileid") or "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }

    resp=app.response_class(
            response=json.dumps(r),
            status=200,
            mimetype='application/json'
        )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/SetItemFavoriteStatus', methods=['POST'])
def SetItemFavoriteStatus(account):
    
    profile=data[request.args.get("profileid") or "athena"]

    ApplyProfileChanges=[]
    BaseRevision=profile['rvn'] or 0
    QueryRevision=request.args.get('rvn') or -1
    StatChanged=False
    
    if json.loads(request.get_data('targetItemId'))['targetItemId']:
        profile['items'][json.loads(request.get_data('targetItemId'))['targetItemId']]['attributes']['favorite']=json.loads(request.get_data('bFavorite'))['bFavorite'] or False
        StatChanged=True
        
    if StatChanged:
        profile['rvn']+=1
        profile['commandRevision']+=1
        
        ApplyProfileChanges.append({
            "changeType": "itemAttrChanged",
            "itemId": json.loads(request.get_data('targetItemId'))['targetItemId'],
            "attributeName": "favorite",
            "attributeValue": profile['items'][json.loads(request.get_data('targetItemId'))['targetItemId']]['attributes']['favorite']
        })
        
        data[request.args.get("profileid") or "athena"]=profile
    
    if QueryRevision!=BaseRevision:
        ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
    
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get("profileid") or "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }
    
    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/MarkItemSeen', methods=['POST'])
def MarkItemSeen(account):
    
    profile=data[request.args.get("profileid") or "athena"]

    ApplyProfileChanges=[]
    BaseRevision=profile['rvn'] or 0
    QueryRevision=request.args.get('rvn') or -1
    StatChanged=False
    
    if json.loads(request.get_data('itemIds'))['itemIds']:
        
        itemIdsL=json.loads(request.get_data('itemIds'))['itemIds']
        
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
        
        data[request.args.get("profileid") or "athena"]=profile
    
    if QueryRevision!=BaseRevision:
        ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
    
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get("profileid") or "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }
    
    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/EquipBattleRoyaleCustomization', methods=['POST'])
def EquipBattleRoyaleCustomization(account):
    
    profile=data[request.args.get("profileid") or "athena"]
    
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
        
        variantUpdatesL=json.loads(request.get_data('variantUpdates'))['variantUpdates']
        ReturnVariantsAsString=variantUpdatesL or []
        
        if "active" in ReturnVariantsAsString:
            itemToSlotJ=json.loads(request.get_data('itemToSlot'))['itemToSlot']
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
    
    if json.loads(request.get_data('slotName'))['slotName']:
        
        slotNameJ=json.loads(request.get_data('slotName'))['slotName']
        print(slotNameJ)
        itemToSlotJ=json.loads(request.get_data('itemToSlot'))['itemToSlot']
        print(itemToSlotJ)
        if slotNameJ=="Character":
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
            indexWithinSlot=json.loads(request.get_data('indexWithinSlot'))['indexWithinSlot']
            if indexWithinSlot>=0:
                profile['stats']['attributes']['favorite_dance'][indexWithinSlot]=itemToSlotJ or ""
            StatChanged=True
            pass

        if slotNameJ=="ItemWrap":
            indexwithinslot=json.loads(request.get_data('indexWithinSlot'))['indexWithinSlot'] or 0

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

        data[request.args.get("profileid") or "athena"]=profile

    if QueryRevision!=BaseRevision:
        ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]

    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get("profileid") or "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }
    
    resp=app.response_class(
        response=json.dumps(r),
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
@app.route('/fortnite/api/game/v2/profile/<account>/client/SetMtxPlatform', methods=['POST'])
def fortnitegameapiclientall(account):
    
    profile=data[request.args.get("profileid") or "athena"]

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
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/SetBattleRoyaleBanner', methods=['POST'])
def SetBattleRoyaleBanner(account):
    
    profile=data[request.args.get("profileid") or "athena"]

    ApplyProfileChanges=[]
    BaseRevision=profile['rvn'] or 0
    QueryRevision=request.args.get('rvn') or -1
    StatChanged=False
    
    if json.loads(request.get_data('homebaseBannerIconId'))['homebaseBannerIconId'] and json.loads(request.get_data('homebaseBannerColorId'))['homebaseBannerColorId']:
        profile['stats']['attributes']['banner_icon']=json.loads(request.get_data('homebaseBannerIconId'))['homebaseBannerIconId']
        profile['stats']['attributes']['banner_color']=json.loads(request.get_data('homebaseBannerColorId'))['homebaseBannerColorId']
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
        
        data[request.args.get("profileid") or "athena"]=profile
    
    if QueryRevision!=BaseRevision:
        ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
    
    
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get("profileid") or "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }
    
    resp=app.response_class(
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/ClientQuestLogin', methods=['POST'])
def ClientQuestLogin(account):
    
    profile=data[request.args.get('profileId') or 'athena']
    QuestIDS=data['quests']
    memory=getVersion(request=request)

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
                NewQuestID=uuid.uuid4()
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
                profile.lower().pop(key)
                
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
                
                if config["Profile"]["bCompletedSeasonalQuests"]==True and "questStages" in ChallengeBundle:
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
                
                if config["Profile"]["bCompletedSeasonalQuests"]:
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
            
            if config["Profile"]['bCompletedSeasonalQuests']:
                profile['items'][Quest['itemGuid']]['attributes']['quest_state']="Claimed"
            
            for x in range(len(Quest['objectives'])):
                if config["Profile"]['bCompletedSeasonalQuests']:
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
        
        data[request.args.get("profileid") or "athena"]=profile
    
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
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/fortnite/api/game/v2/profile/<account>/client/IncrementNamedCounterStat', methods=['POSt'])
def IncrementNamedCounterStat(account):
    
    profile=data[request.args.get("profileid") or "athena"]

    ApplyProfileChanges=[]
    BaseRevision=profile['rvn'] or 0
    QueryRevision=request.args['rvn'] or -1
    StatChanged=False

    if "named_counters" in profile['stats']['attributes'] and json.loads(request.get_data('counterName'))['counterName']:
        if json.loads(request.get_data('counterName'))['counterName'] in profile['stats']['attributes']['named_counters']:
            profile['stats']['attributes']['named_counters'][json.loads(request.get_data('counterName'))['counterName']]['current_count']+=1
            profile['stats']['attributes']['named_counters'][json.loads(request.get_data('counterName'))['counterName']]['last_incremented_time']=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            StatChanged=True
    
    if StatChanged:
        profile['rvn']+=1
        profile['commandRevision']+=1

        ApplyProfileChanges.append({
            "changeType": "statModified",
            "name": "named_counters",
            "value": profile['stats']['attributes']['named_counters']
        })

        data[request.args.get("profileid") or "athena"]=profile
    
    if QueryRevision!=BaseRevision:
        ApplyProfileChanges=[{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
    
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": request.args.get("profileid") or "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }

    resp=app.response_class(
            response=json.dumps(r),
            status=200,
            mimetype='application/json'
        )
    return resp

@app.route('/fortnite/api/game/v2/profile/', methods=['GET'])
def handle_request_profile():
    if not request.args.get('profileId') and request.path.lower().startswith('/fortnite/api/game/v2/profile/'):
        error = {'error': 'Profile not defined.'}
        return Response(json.dumps(error), status=404, mimetype='application/json')

    for file in data:
        memory = getVersion(request=request)

        profile=data[file]
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
            SeasonData=data['seasondata']
            profile['stats']['attributes']['season_num'] = memory['season']

            if f'Season{memory["season"]}' in SeasonData:
                SeasonData = SeasonData[f'Season{memory["season"]}']

                profile['stats']['attributes']['book_purchased'] = SeasonData['battlePassPurchased']
                profile['stats']['attributes']['book_level'] = SeasonData['battlePassTier']
                profile['stats']['attributes']['season_match_boost'] = SeasonData['battlePassXPBoost']
                profile['stats']['attributes']['season_friend_match_boost'] = SeasonData['battlePassXPFriendBoost']

            data[request.args.get("profileid") or "athena"]=profile

    return Response(status=200)

@app.route("/fortnite/api/game/v2/profile/<account>/client/RefundMtxPurchase", methods=["POST"])
def refund_mtx_purchase(account):
    profile=data[request.args.get('profileId') or 'common_core']
    item_profile=data['athena']

    apply_profile_changes = []
    multi_update = []
    base_revision = profile.get("rvn") or 0
    query_revision = request.args.get("rvn") or -1
    stat_changed = False

    item_guids = []

    if "purchaseId" in request.form:
        multi_update.append({
            "profileRevision": item_profile.get("rvn") or 0,
            "profileId": request.args.get("profileid") or "athena",
            "profileChangesBaseRevision": item_profile.get("rvn") or 0,
            "profileChanges": [],
            "profileCommandRevision": item_profile.get("commandRevision") or 0,
        })

        profile["stats"]["attributes"]["mtx_purchase_history"]["refundsUsed"] += 1
        profile["stats"]["attributes"]["mtx_purchase_history"]["refundCredits"] -= 1

        for purchase in profile["stats"]["attributes"]["mtx_purchase_history"]["purchases"]:
            if purchase["purchaseId"] == json.loads(request.get_data("purchaseId"))["purchaseId"]:
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
        
        data['athena']=item_profile
        data[request.args.get("profileid") or 'common_core']=profile
    
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
            response=json.dumps(r),
            status=200,
            mimetype='application/json'
        )
    return resp

@app.route("/fortnite/api/game/v2/profile/<account>/client/UpdateQuestClientObjectives", methods=["POST"])
def update_quest_client_objectives(account):
    profile=data[request.args.get('profileId') or 'campaign']

    apply_profile_changes = []
    base_revision = profile.get("rvn", 0)
    query_revision = request.args.get("rvn", -1)
    stat_changed = False

    if json.loads(request.get_data('advance'))['advance']:
        for i in json.loads(request.get_data('advance'))['advance']:
            quests_to_update = []
            for x in profile["items"]:
                if profile['items'][x]["templateId"].lower().startswith("quest:"):
                    for y in profile['items'][x]['attributes']:
                        if y.lower()==f"completion_{json.loads(request.get_data('advance'))['advance'][i]['statName']}":
                            quests_to_update.append(x)
            
            for i in len(quests_to_update):
                b_incomplete = False

                profile["items"][quests_to_update[i]]["attributes"][f"completion_{json.loads(request.get_data('advance'))['advance'][i]['statName']}"] = json.loads(request.get_data('advance'))['advance'][i]["count"]

                apply_profile_changes.append({
                    "changeType": "itemAttrChanged",
                    "itemId": quests_to_update[i],
                    "attributeName": f"completion_{json.loads(request.get_data('advance'))['advance'][i]['statName']}",
                    "attributeValue": json.loads(request.get_data('advance'))['advance'][i]["count"]
                })
                if profile["items"][quests_to_update[i]]["attributes"]["quest_state"].lower() != "claimed":
                    for x in profile["items"][quests_to_update[i]]["attributes"]:
                        if x.lower().startswith("completion_"):
                            if profile['items'][quests_to_update[i]]['attributes']==0:
                                b_incomplete = True
                                
                    if not b_incomplete:
                        profile["items"][quests_to_update[i]]["attributes"]["quest_state"] = "Claimed"

                        apply_profile_changes.append({
                            "changeType": "itemAttrChanged",
                            "itemId": quests_to_update[i],
                            "attributeName": "quest_state",
                            "attributeValue": profile["items"][quests_to_update[i]]["attributes"]["quest_state"]
                        })
                stat_changed = True

    if stat_changed:
        profile["rvn"] += 1
        profile["commandRevision"] += 1

        data[request.args.get('profileId') or 'campaign']=profile

    if query_revision != base_revision:
        apply_profile_changes = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }]
        
    r={
        "profileRevision": profile['rvn'] or 0,
        "profileId": "campaign",
        "profileChangesBaseRevision": base_revision,
        "profileChanges": apply_profile_changes,
        "profileCommandRevision": profile['commandRevision'] or 0,
        "serverTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "responseVersion": 1
    }

    resp=app.response_class(
            response=json.dumps(r),
            status=200,
            mimetype='application/json'
        )
    return resp

@app.route("/fortnite/api/game/v2/profile/<account>/client/FortRerollDailyQuest", methods=["POST"])
def FortRerollDailyQuest(aaccount):
    profile=data[request.args.get('profileId') or 'athena']
    DailyQuestIDS=data['quests']

    ApplyProfileChanges = []
    Notifications = []
    BaseRevision = profile.get("rvn", 0)
    QueryRevision = request.args.get("rvn", -1)
    StatChanged = False

    if request.args.get('profileId') == "athena":
        DailyQuestIDS = DailyQuestIDS["BattleRoyale"]["Daily"]

    NewQuestID = uuid.uuid4()
    randomNumber = random.randint(0, len(DailyQuestIDS) - 1)

    for key, item in profile["items"]:
        while DailyQuestIDS[randomNumber]["templateId"].lower() == item["templateId"].lower():
            randomNumber = random.randint(0, len(DailyQuestIDS) - 1)

    if "questId" in request.form and profile["stats"]["attributes"]["quest_manager"]["dailyQuestRerolls"] >= 1:
        profile["stats"]["attributes"]["quest_manager"]["dailyQuestRerolls"] -= 1

        del profile["items"][json.loads(request.get_data('questId'))['questId']]

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
            "itemId": json.loads(request.get_data('questId'))['questId']
        })
        
        Notifications.append({
            "type": "dailyQuestReroll",
            "primary": True,
            "newQuestId": DailyQuestIDS[randomNumber]['templateId']
        })

        data[request.args.get('profileId') or 'athena']=profile

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
        response=json.dumps(r),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/test')
def test():
    print(request.headers["user-agent"])
    
    resp=Response()
    resp.status_code=200
    return resp


app.run("0.0.0.0", 3551)