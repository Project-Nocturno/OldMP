import requests
import json


class Data():
    def __init__(self, usernm: str, api_url: str='https://nocturno.games/api'):
        self.usernm=usernm
        self.api_url=api_url
        self.mtx=requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=mtx', verify=False).text
        self.items=requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=items', verify=False).text
        self.level=requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=level', verify=False).text
        self.xp=requests.get(f'{self.api_url}/get/stats/stats.php?user={self.usernm}&action=exp', verify=False).text
    
    def athena(self):
        self.items_l=list(self.items)
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
                "xp": 0,
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
        for i in self.items_l:
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

open('data/athena.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").athena())
open('data/common_core.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").commoncore())
open('data/collections.json', 'w', encoding='utf-8').write(Data(usernm="4lxprime").collections())