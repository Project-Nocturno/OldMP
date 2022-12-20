import requests
import json
import os


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

class Data():
    def __init__(self, usernm: str, api_url: str='https://nocturno.games/api'):
        self.usernm=usernm
        self.api_url=api_url
        self.mtx=int(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=mtx', verify=False).json())
        self.items=list(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=items', verify=False).json())
        self.level=int(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=level', verify=False).json())
        self.xp=int(requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=exp', verify=False).json())
    
    def athena(self):
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
                  "dailyLoginInterval": "2022-09-19T11:24:34.156Z",
                  "dailyQuestRerolls": 1
                },
                "book_level": 0,
                "season_num": 3,
                "favorite_consumableemote": "",
                "banner_color": "DefaultColor15",
                "favorite_callingcard": "",
                "favorite_character": "",
                "favorite_spray": [],
                "book_xp": 0,
                "battlestars": 1,
                "battlestars_season_total": 1,
                "style_points": 1,
                "alien_style_points": 1,
                "party_assist_quest": "",
                "pinned_quest": "",
                "purchased_bp_offers": [],
                "favorite_loadingscreen": "",
                "book_purchased": True,
                "lifetime_wins": 0,
                "favorite_hat": "",
                "level": 1,
                "favorite_battlebus": "",
                "favorite_mapmarker": "",
                "favorite_vehicledeco": "",
                "accountLevel": self.level,
                "favorite_backpack": "",
                "favorite_dance": [
                  ""
                ],
                "inventory_limit_bonus": 0,
                "last_applied_loadout": "",
                "favorite_skydivecontrail": "",
                "favorite_pickaxe": "",
                "favorite_glider": "",
                "daily_rewards": {},
                "xp": self.xp,
                "season_friend_match_boost": 25,
                "active_loadout_index": 0,
                "favorite_musicpack": "",
                "banner_icon": "StandardBanner27",
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
                        ""
                      ],
                      "activeVariants": [
                        ""
                      ]
                    },
                    "Backpack": {
                      "items": [
                        ""
                      ],
                      "activeVariants": [
                        ""
                      ]
                    },
                    "SkyDiveContrail": {
                      "items": [
                        ""
                      ],
                      "activeVariants": [
                        ""
                      ]
                    },
                    "Dance": {
                      "items": [
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
                        ""
                      ],
                      "activeVariants": [
                        ""
                      ]
                    },
                    "Glider": {
                      "items": [
                        ""
                      ],
                      "activeVariants": [
                        ""
                      ]
                    },
                    "ItemWrap": {
                      "items": [
                        ""
                      ],
                      "activeVariants": [
                        ""
                      ]
                    }
                  }
                },
                "use_count": 0,
                "banner_icon_template": "StandardBanner1",
                "banner_color_template": "DefaultColor1",
                "locker_name": "Nocturno",
                "item_seen": False,
                "favorite": False
              },
              "quantity": 1
            }
          }
        self.items_id=[]
        for i in self.items:
            for x in exchange_table:
                if i==x['name']:
                    self.items_id.append(x['id'])
                  
        for i in self.items_id:
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
            "_id": self.usernm,
            "created": "0001-01-01T00:00:00.000Z",
            "updated": "0001-01-01T00:00:00.000Z",
            "rvn": 0,
            "wipeNumber": 1,
            "accountId": self.usernm,
            "profileId": "profile0",
            "version": "no_version",
            "items": {
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
            "stats": {},
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
                "banner_color": "DefaultColor15",
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

open(f'{os.path.dirname(os.path.realpath(__file__))}/data/athena.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").athena())
open(f'{os.path.dirname(os.path.realpath(__file__))}/data/common_core.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").commoncore())
open(f'{os.path.dirname(os.path.realpath(__file__))}/data/common_public.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").commoncore())
open(f'{os.path.dirname(os.path.realpath(__file__))}/data/collections.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").collections())
open(f'{os.path.dirname(os.path.realpath(__file__))}/data/connect/SeasonData.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").seasondata())
open(f'{os.path.dirname(os.path.realpath(__file__))}/data/connect/friendlist.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").friendlist())
open(f'{os.path.dirname(os.path.realpath(__file__))}/data/connect/friendlistv2.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").friendlistv2())