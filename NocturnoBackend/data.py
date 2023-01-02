from requests import get
from json import loads, load, dump, dumps

class Data():
    def __init__(self, usernm: str, api_url: str='https://nocturno.games/api', url_key: str='VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0'):
        self.usernm=usernm
        self.api_url=api_url
        self.mtx=int(get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=mtx', verify=False).json())
        self.items=list(get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=items', verify=False).json())
        self.level=int(get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=level', verify=False).json())
        self.xp=int(get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=exp', verify=False).json())
        self.top1=int(get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=top1', verify=False).json())
        self._catalogconfig=dict(get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=shop', verify=False).json())
        self._discover_frontend=dict(get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=discoverfrontend', verify=False).json())
        self._keychain=list(get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=keychain', verify=False).json())
        self._contentpages=dict(get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=contentpages', verify=False).json())
        self._catalog=dict(get(f'{self.api_url}/get/lobby/lobby.php?urlkey={url_key}&passwd=&user={self.usernm}&action=catalog', verify=False).json())
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
        self._data['privacy']=loads(self.privacy())
        self._data['athena']=loads(self.athena())
        self._data['common_core']=loads(self.commoncore())
        self._data['common_public']=loads(self.commonpublic())
        self._data['profile0']=loads(self.profile0())
        self._data['collections']=loads(self.collections())
        self._data['seasondata']=loads(self.seasondata())
        self._data['friendlist']=loads(self.friendlist())
        self._data['friendlistv2']=loads(self.friendlistv2())
        self._data['quests']=loads(self.quests())
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
        
        return dumps(self._athena, indent=4)

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
                "quantity": self.mtx
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
        
        return dumps(self._commoncore, indent=4)

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
        return dumps(self._collections, indent=4)     

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
          return dumps(self._seasondata, indent=4)

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
        return dumps(self._friendlist, indent=4)
      
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
        return dumps(self._friendlistv2, indent=4)

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
          return dumps(self._commonpublic, indent=4)

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
        return dumps(self._quests, indent=4)
    
    def privacy(self):
        self._privacy={
            "accountId": "",
            "optOutOfPublicLeaderboards": False
        }
        return dumps(self._privacy, indent=4)
      
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
          return dumps(self._profile0, indent=4)
    
    def alldata(self):
        return dumps(self._data, indent=4)