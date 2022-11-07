const Express = require("express");
const express = Express.Router();
const fs = require("fs");
const path = require("path");
const iniparser = require("ini");
const config = iniparser.parse(fs.readFileSync(path.join(__dirname, "..", "Config", "config.ini")).toString());
const functions = require("./functions.js");
const catalog = functions.getItemShop();

express.use((req, res, next) => {
    if (!req.query.profileId && req.originalUrl.toLowerCase().startsWith("/fortnite/api/game/v2/profile/")) {
        return res.status(404).json({
            error: "Profile not defined."
        });
    }

    fs.readdirSync("./data").forEach((file) => {
        if (file.endsWith(".json")) {
            const memory = functions.GetVersionInfo(req);

            const profile = require(`./../data/${file}`);
            if (!profile.rvn) profile.rvn = 0;
            if (!profile.items) profile.items = {}
            if (!profile.stats) profile.stats = {}
            if (!profile.stats.attributes) profile.stats.attributes = {}
            if (!profile.commandRevision) profile.commandRevision = 0;

            if (file == "athena.json") {
                var SeasonData = JSON.parse(JSON.stringify(require("./../connect/SeasonData.json")));
                profile.stats.attributes.season_num = memory.season;

                if (SeasonData[`Season${memory.season}`]) {
                    SeasonData = SeasonData[`Season${memory.season}`];

                    profile.stats.attributes.book_purchased = SeasonData.battlePassPurchased;
                    profile.stats.attributes.book_level = SeasonData.battlePassTier;
                    profile.stats.attributes.season_match_boost = SeasonData.battlePassXPBoost;
                    profile.stats.attributes.season_friend_match_boost = SeasonData.battlePassXPFriendBoost;
                }

                fs.writeFileSync("./data/athena.json", JSON.stringify(profile, null, 2));
            }
        }
    })

    return next();
});

// Set support a creator code
express.post("/fortnite/api/game/v2/profile/*/client/SetAffiliateName", async (req, res) => {
    const profile = require("./../data/common_core.json");

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    const SupportedCodes = require("./../connect/SAC.json");
    SupportedCodes.forEach(code => {
        if (req.body.affiliateName.toLowerCase() == code.toLowerCase() || req.body.affiliateName == "") {
            profile.stats.attributes.mtx_affiliate_set_time = new Date().toISOString();
            profile.stats.attributes.mtx_affiliate = req.body.affiliateName;
            
            StatChanged = true;
        }
    })

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "mtx_affiliate_set_time",
            "value": profile.stats.attributes.mtx_affiliate_set_time
        })

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "mtx_affiliate",
            "value": profile.stats.attributes.mtx_affiliate
        })

        fs.writeFileSync("./data/common_core.json", JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": "common_core",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Remove gift box
express.post("/fortnite/api/game/v2/profile/*/client/RemoveGiftBox", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    // Gift box ID on 11.31
    if (req.body.giftBoxItemId) {
        var id = req.body.giftBoxItemId;

        delete profile.items[id];

        ApplyProfileChanges.push({
            "changeType": "itemRemoved",
            "itemId": id
        })

        StatChanged = true;
    }

    // Gift box ID on 19.01
    if (req.body.giftBoxItemIds) {
        for (var i in req.body.giftBoxItemIds) {
            var id = req.body.giftBoxItemIds[i];

            delete profile.items[id];

            ApplyProfileChanges.push({
                "changeType": "itemRemoved",
                "itemId": id
            })
        }

        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Set party assist quest
express.post("/fortnite/api/game/v2/profile/*/client/SetPartyAssistQuest", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (profile.stats.attributes.hasOwnProperty("party_assist_quest")) {
        profile.stats.attributes.party_assist_quest = req.body.questToPinAsPartyAssist || "";
        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "party_assist_quest",
            "value": profile.stats.attributes.party_assist_quest
        })

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Set pinned BR quest
express.post("/fortnite/api/game/v2/profile/*/client/AthenaPinQuest", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (profile.stats.attributes.hasOwnProperty("pinned_quest")) {
        profile.stats.attributes.pinned_quest = req.body.pinnedQuest || "";
        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "pinned_quest",
            "value": profile.stats.attributes.pinned_quest
        })

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Replace Daily Quests
express.post("/fortnite/api/game/v2/profile/*/client/FortRerollDailyQuest", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);
    var DailyQuestIDS = JSON.parse(JSON.stringify(require("./../connect/quests.json")));

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var Notifications = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.query.profileId == "athena") {
        DailyQuestIDS = DailyQuestIDS.BattleRoyale.Daily
    }

    const NewQuestID = functions.MakeID();
    var randomNumber = Math.floor(Math.random() * DailyQuestIDS.length);

    for (var key in profile.items) {
        while (DailyQuestIDS[randomNumber].templateId.toLowerCase() == profile.items[key].templateId.toLowerCase()) {
            randomNumber = Math.floor(Math.random() * DailyQuestIDS.length);
        }
    }

    if (req.body.questId && profile.stats.attributes.quest_manager.dailyQuestRerolls >= 1) {
        profile.stats.attributes.quest_manager.dailyQuestRerolls -= 1;

        delete profile.items[req.body.questId];

        profile.items[NewQuestID] = {
            "templateId": DailyQuestIDS[randomNumber].templateId,
            "attributes": {
                "creation_time": new Date().toISOString(),
                "level": -1,
                "item_seen": false,
                "playlists": [],
                "sent_new_notification": false,
                "challenge_bundle_id": "",
                "xp_reward_scalar": 1,
                "challenge_linked_quest_given": "",
                "quest_pool": "",
                "quest_state": "Active",
                "bucket": "",
                "last_state_change_time": new Date().toISOString(),
                "challenge_linked_quest_parent": "",
                "max_level_bonus": 0,
                "xp": 0,
                "quest_rarity": "uncommon",
                "favorite": false
            },
            "quantity": 1
        };

        for (var i in DailyQuestIDS[randomNumber].objectives) {
            profile.items[NewQuestID].attributes[`completion_${DailyQuestIDS[randomNumber].objectives[i].toLowerCase()}`] = 0
        }

        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "quest_manager",
            "value": profile.stats.attributes.quest_manager
        })

        ApplyProfileChanges.push({
            "changeType": "itemAdded",
            "itemId": NewQuestID,
            "item": profile.items[NewQuestID]
        })

        ApplyProfileChanges.push({
            "changeType": "itemRemoved",
            "itemId": req.body.questId
        })

        Notifications.push({
            "type": "dailyQuestReroll",
            "primary": true,
            "newQuestId": DailyQuestIDS[randomNumber].templateId
        })

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "notifications": Notifications,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Mark New Quest Notification Sent
express.post("/fortnite/api/game/v2/profile/*/client/MarkNewQuestNotificationSent", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.itemIds) {
        for (var i in req.body.itemIds) {
            var id = req.body.itemIds[i];

            profile.items[id].attributes.sent_new_notification = true

            ApplyProfileChanges.push({
                "changeType": "itemAttrChanged",
                "itemId": id,
                "attributeName": "sent_new_notification",
                "attributeValue": true
            })
        }

        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Check for new quests
express.post("/fortnite/api/game/v2/profile/*/client/ClientQuestLogin", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);
    var QuestIDS = JSON.parse(JSON.stringify(require("./../connect/quests.json")));
    const memory = functions.GetVersionInfo(req);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    var QuestCount = 0;
    var ShouldGiveQuest = true;
    var DateFormat = (new Date().toISOString()).split("T")[0];
    var DailyQuestIDS;
    var SeasonQuestIDS;

    try {
        if (req.query.profileId == "athena") {
            DailyQuestIDS = QuestIDS.BattleRoyale.Daily

            if (QuestIDS.BattleRoyale.hasOwnProperty(`Season${memory.season}`)) {
                SeasonQuestIDS = QuestIDS.BattleRoyale[`Season${memory.season}`]
            }

            for (var key in profile.items) {
                if (profile.items[key].templateId.toLowerCase().startsWith("quest:athenadaily")) {
                    QuestCount += 1;
                }
            }
        }

        if (profile.stats.attributes.hasOwnProperty("quest_manager")) {
            if (profile.stats.attributes.quest_manager.hasOwnProperty("dailyLoginInterval")) {
                if (profile.stats.attributes.quest_manager.dailyLoginInterval.includes("T")) {
                    var DailyLoginDate = (profile.stats.attributes.quest_manager.dailyLoginInterval).split("T")[0];

                    if (DailyLoginDate == DateFormat) {
                        ShouldGiveQuest = false;
                    } else {
                        ShouldGiveQuest = true;
                        if (profile.stats.attributes.quest_manager.dailyQuestRerolls <= 0) {
                            profile.stats.attributes.quest_manager.dailyQuestRerolls += 1;
                        }
                    }
                }
            }
        }

        if (QuestCount < 3 && ShouldGiveQuest == true) {
            const NewQuestID = functions.MakeID();
            var randomNumber = Math.floor(Math.random() * DailyQuestIDS.length);

            for (var key in profile.items) {
                while (DailyQuestIDS[randomNumber].templateId.toLowerCase() == profile.items[key].templateId.toLowerCase()) {
                    randomNumber = Math.floor(Math.random() * DailyQuestIDS.length);
                }
            }

            profile.items[NewQuestID] = {
                "templateId": DailyQuestIDS[randomNumber].templateId,
                "attributes": {
                    "creation_time": new Date().toISOString(),
                    "level": -1,
                    "item_seen": false,
                    "playlists": [],
                    "sent_new_notification": false,
                    "challenge_bundle_id": "",
                    "xp_reward_scalar": 1,
                    "challenge_linked_quest_given": "",
                    "quest_pool": "",
                    "quest_state": "Active",
                    "bucket": "",
                    "last_state_change_time": new Date().toISOString(),
                    "challenge_linked_quest_parent": "",
                    "max_level_bonus": 0,
                    "xp": 0,
                    "quest_rarity": "uncommon",
                    "favorite": false
                },
                "quantity": 1
            };

            for (var i in DailyQuestIDS[randomNumber].objectives) {
                profile.items[NewQuestID].attributes[`completion_${DailyQuestIDS[randomNumber].objectives[i].toLowerCase()}`] = 0
            }

            profile.stats.attributes.quest_manager.dailyLoginInterval = new Date().toISOString();

            ApplyProfileChanges.push({
                "changeType": "itemAdded",
                "itemId": NewQuestID,
                "item": profile.items[NewQuestID]
            })

            ApplyProfileChanges.push({
                "changeType": "statModified",
                "name": "quest_manager",
                "value": profile.stats.attributes.quest_manager
            })

            StatChanged = true;
        }
    } catch (err) {}

    for (var key in profile.items) {
        if (key.split("")[0] == "S" && (Number.isInteger(Number(key.split("")[1]))) && (key.split("")[2] == "-" || (Number.isInteger(Number(key.split("")[2])) && key.split("")[3] == "-"))) {
            if (!key.startsWith(`S${memory.season}-`)) {
                delete profile.items[key];

                ApplyProfileChanges.push({
                    "changeType": "itemRemoved",
                    "itemId": key
                })

                StatChanged = true;
            }
        }
    }

    if (SeasonQuestIDS) {
        if (req.query.profileId == "athena") {
            for (var ChallengeBundleSchedule in SeasonQuestIDS.ChallengeBundleSchedules) {
                if (profile.items.hasOwnProperty(ChallengeBundleSchedule.itemGuid)) {
                    ApplyProfileChanges.push({
                        "changeType": "itemRemoved",
                        "itemId": ChallengeBundleSchedule.itemGuid
                    })
                }

                ChallengeBundleSchedule = SeasonQuestIDS.ChallengeBundleSchedules[ChallengeBundleSchedule];

                profile.items[ChallengeBundleSchedule.itemGuid] = {
                    "templateId": ChallengeBundleSchedule.templateId,
                    "attributes": {
                        "unlock_epoch": new Date().toISOString(),
                        "max_level_bonus": 0,
                        "level": 1,
                        "item_seen": true,
                        "xp": 0,
                        "favorite": false,
                        "granted_bundles": ChallengeBundleSchedule.granted_bundles
                    },
                    "quantity": 1
                }

                ApplyProfileChanges.push({
                    "changeType": "itemAdded",
                    "itemId": ChallengeBundleSchedule.itemGuid,
                    "item": profile.items[ChallengeBundleSchedule.itemGuid]
                })

                StatChanged = true;
            }

            for (var ChallengeBundle in SeasonQuestIDS.ChallengeBundles) {
                if (profile.items.hasOwnProperty(ChallengeBundle.itemGuid)) {
                    ApplyProfileChanges.push({
                        "changeType": "itemRemoved",
                        "itemId": ChallengeBundle.itemGuid
                    })
                }

                ChallengeBundle = SeasonQuestIDS.ChallengeBundles[ChallengeBundle];

                if (config.Profile.bCompletedSeasonalQuests == true && ChallengeBundle.hasOwnProperty("questStages")) {
                    ChallengeBundle.grantedquestinstanceids = ChallengeBundle.grantedquestinstanceids.concat(ChallengeBundle.questStages);
                }

                profile.items[ChallengeBundle.itemGuid] = {
                    "templateId": ChallengeBundle.templateId,
                    "attributes": {
                        "has_unlock_by_completion": false,
                        "num_quests_completed": 0,
                        "level": 0,
                        "grantedquestinstanceids": ChallengeBundle.grantedquestinstanceids,
                        "item_seen": true,
                        "max_allowed_bundle_level": 0,
                        "num_granted_bundle_quests": 0,
                        "max_level_bonus": 0,
                        "challenge_bundle_schedule_id": ChallengeBundle.challenge_bundle_schedule_id,
                        "num_progress_quests_completed": 0,
                        "xp": 0,
                        "favorite": false
                    },
                    "quantity": 1
                }

                profile.items[ChallengeBundle.itemGuid].attributes.num_granted_bundle_quests = ChallengeBundle.grantedquestinstanceids.length;

                if (config.Profile.bCompletedSeasonalQuests == true) {
                    profile.items[ChallengeBundle.itemGuid].attributes.num_quests_completed = ChallengeBundle.grantedquestinstanceids.length;
                    profile.items[ChallengeBundle.itemGuid].attributes.num_progress_quests_completed = ChallengeBundle.grantedquestinstanceids.length;
                }

                ApplyProfileChanges.push({
                    "changeType": "itemAdded",
                    "itemId": ChallengeBundle.itemGuid,
                    "item": profile.items[ChallengeBundle.itemGuid]
                })

                StatChanged = true;
            }
        }

        for (var Quest in SeasonQuestIDS.Quests) {
            if (profile.items.hasOwnProperty(Quest.itemGuid)) {
                ApplyProfileChanges.push({
                    "changeType": "itemRemoved",
                    "itemId": Quest.itemGuid
                })
            }

            Quest = SeasonQuestIDS.Quests[Quest];

            profile.items[Quest.itemGuid] = {
                "templateId": Quest.templateId,
                "attributes": {
                    "creation_time": new Date().toISOString(),
                    "level": -1,
                    "item_seen": true,
                    "playlists": [],
                    "sent_new_notification": true,
                    "challenge_bundle_id": Quest.challenge_bundle_id || "",
                    "xp_reward_scalar": 1,
                    "challenge_linked_quest_given": "",
                    "quest_pool": "",
                    "quest_state": "Active",
                    "bucket": "",
                    "last_state_change_time": new Date().toISOString(),
                    "challenge_linked_quest_parent": "",
                    "max_level_bonus": 0,
                    "xp": 0,
                    "quest_rarity": "uncommon",
                    "favorite": false
                },
                "quantity": 1
            }

            if (config.Profile.bCompletedSeasonalQuests == true) {
                profile.items[Quest.itemGuid].attributes.quest_state = "Claimed";
            }

            for (var i in Quest.objectives) {
                if (config.Profile.bCompletedSeasonalQuests == true) {
                    profile.items[Quest.itemGuid].attributes[`completion_${Quest.objectives[i].name.toLowerCase()}`] = Quest.objectives[i].count;
                } else {
                    profile.items[Quest.itemGuid].attributes[`completion_${Quest.objectives[i].name.toLowerCase()}`] = 0;
                }
            }

            ApplyProfileChanges.push({
                "changeType": "itemAdded",
                "itemId": Quest.itemGuid,
                "item": profile.items[Quest.itemGuid]
            })

            StatChanged = true;
        }
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Refund V-Bucks purchase
express.post("/fortnite/api/game/v2/profile/*/client/RefundMtxPurchase", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "common_core"}.json`);
    const ItemProfile = require("./../data/athena.json");

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var MultiUpdate = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    var ItemGuids = [];

    if (req.body.purchaseId) {
        MultiUpdate.push({
            "profileRevision": ItemProfile.rvn || 0,
            "profileId": "athena",
            "profileChangesBaseRevision": ItemProfile.rvn || 0,
            "profileChanges": [],
            "profileCommandRevision": ItemProfile.commandRevision || 0,
        })

        profile.stats.attributes.mtx_purchase_history.refundsUsed += 1;
        profile.stats.attributes.mtx_purchase_history.refundCredits -= 1;

        for (var i in profile.stats.attributes.mtx_purchase_history.purchases) {
            if (profile.stats.attributes.mtx_purchase_history.purchases[i].purchaseId == req.body.purchaseId) {
                for (var x in profile.stats.attributes.mtx_purchase_history.purchases[i].lootResult) {
                    ItemGuids.push(profile.stats.attributes.mtx_purchase_history.purchases[i].lootResult[x].itemGuid)
                }

                profile.stats.attributes.mtx_purchase_history.purchases[i].refundDate = new Date().toISOString();

                for (var key in profile.items) {
                    if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                        if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                            profile.items[key].quantity += profile.stats.attributes.mtx_purchase_history.purchases[i].totalMtxPaid;
        
                            ApplyProfileChanges.push({
                                "changeType": "itemQuantityChanged",
                                "itemId": key,
                                "quantity": profile.items[key].quantity
                            })
        
                            break;
                        }
                    }
                }
            }
        }

        for (var i in ItemGuids) {
			try {
				delete ItemProfile.items[ItemGuids[i]]

				MultiUpdate[0].profileChanges.push({
					"changeType": "itemRemoved",
					"itemId": ItemGuids[i]
				})
			} catch (err) {}
        }

        ItemProfile.rvn += 1;
        ItemProfile.commandRevision += 1;
        profile.rvn += 1;
        profile.commandRevision += 1;

        StatChanged = true;
    }

    if (StatChanged == true) {
        
        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "mtx_purchase_history",
            "value": profile.stats.attributes.mtx_purchase_history
        })

        MultiUpdate[0].profileRevision = ItemProfile.rvn || 0;
        MultiUpdate[0].profileCommandRevision = ItemProfile.commandRevision || 0;

        fs.writeFileSync(`./data/${req.query.profileId || "common_core"}.json`, JSON.stringify(profile, null, 2));
        fs.writeFileSync(`./data/athena.json`, JSON.stringify(ItemProfile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "common_core",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "multiUpdate": MultiUpdate,
        "responseVersion": 1
    })
    res.end();
});

// Increase a named counter value (e.g. when selecting a game mode)
express.post("/fortnite/api/game/v2/profile/*/client/IncrementNamedCounterStat", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "profile0"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.counterName && profile.stats.attributes.hasOwnProperty("named_counters")) {
        if (profile.stats.attributes.named_counters.hasOwnProperty(req.body.counterName)) {
            profile.stats.attributes.named_counters[req.body.counterName].current_count += 1;
            profile.stats.attributes.named_counters[req.body.counterName].last_incremented_time = new Date().toISOString();

            StatChanged = true;
        }
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "named_counters",
            "value": profile.stats.attributes.named_counters
        })

        fs.writeFileSync(`./data/${req.query.profileId || "profile0"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "profile0",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Update quest client objectives
express.post("/fortnite/api/game/v2/profile/*/client/UpdateQuestClientObjectives", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "campaign"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.advance) {
        for (var i in req.body.advance) {
            var QuestsToUpdate = [];

            for (var x in profile.items) {
                if (profile.items[x].templateId.toLowerCase().startsWith("quest:")) {
                    for (var y in profile.items[x].attributes) {
                        if (y.toLowerCase() == `completion_${req.body.advance[i].statName}`) {
                            QuestsToUpdate.push(x)
                        }
                    }
                }
            }

            for (var i = 0; i < QuestsToUpdate.length; i++) {
                var bIncomplete = false;
                
                profile.items[QuestsToUpdate[i]].attributes[`completion_${req.body.advance[i].statName}`] = req.body.advance[i].count;

                ApplyProfileChanges.push({
                    "changeType": "itemAttrChanged",
                    "itemId": QuestsToUpdate[i],
                    "attributeName": `completion_${req.body.advance[i].statName}`,
                    "attributeValue": req.body.advance[i].count
                })

                if (profile.items[QuestsToUpdate[i]].attributes.quest_state.toLowerCase() != "claimed") {
                    for (var x in profile.items[QuestsToUpdate[i]].attributes) {
                        if (x.toLowerCase().startsWith("completion_")) {
                            if (profile.items[QuestsToUpdate[i]].attributes[x] == 0) {
                                bIncomplete = true;
                            }
                        }
                    }
    
                    if (bIncomplete == false) {
                        profile.items[QuestsToUpdate[i]].attributes.quest_state = "Claimed";
    
                        ApplyProfileChanges.push({
                            "changeType": "itemAttrChanged",
                            "itemId": QuestsToUpdate[i],
                            "attributeName": "quest_state",
                            "attributeValue": profile.items[QuestsToUpdate[i]].attributes.quest_state
                        })
                    }
                }

                StatChanged = true;
            }
        }
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        fs.writeFileSync(`./data/${req.query.profileId || "campaign"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "campaign",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Purchase item
express.post("/fortnite/api/game/v2/profile/*/client/PurchaseCatalogEntry", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "profile0"}.json`);
    const athena = require("./../data/athena.json");
    const ItemIDS = require("./../connect/ItemIDS.json");

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var MultiUpdate = [];
    var Notifications = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var PurchasedLlama = false;
    var AthenaModified = false;
    var ItemExists = false;

    if (req.body.offerId && profile.profileId == "profile0" && PurchasedLlama == false) {
        catalog.storefronts.forEach(function(value, a) {
            if (value.name.toLowerCase().startsWith("cardpack")) {
                catalog.storefronts[a].catalogEntries.forEach(function(value, b) {
                    if (value.offerId == req.body.offerId) {
                        var Quantity = 0;
                        catalog.storefronts[a].catalogEntries[b].itemGrants.forEach(function(value, c) {
                            Quantity = req.body.purchaseQuantity || 1;

                            const Item = {
                                "templateId": value.templateId,
                                "attributes": {
                                    "is_loot_tier_overridden": false,
                                    "max_level_bonus": 0,
                                    "level": 1391,
                                    "pack_source": "Schedule",
                                    "item_seen": false,
                                    "xp": 0,
                                    "favorite": false,
                                    "override_loot_tier": 0
                                },
                                "quantity": 1
                            };

                            for (var i = 0; i < Quantity; i++) {
                                var ID = functions.MakeID();

                                profile.items[ID] = Item

                                ApplyProfileChanges.push({
                                    "changeType": "itemAdded",
                                    "itemId": ID,
                                    "item": profile.items[ID]
                                })
                            }
                        })
                        // Vbucks spending
                        if (catalog.storefronts[a].catalogEntries[b].prices[0].currencyType.toLowerCase() == "mtxcurrency") {
                            for (var key in profile.items) {
                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                        profile.items[key].quantity -= (catalog.storefronts[a].catalogEntries[b].prices[0].finalPrice) * Quantity;
                                                                        
                                        ApplyProfileChanges.push({
                                            "changeType": "itemQuantityChanged",
                                            "itemId": key,
                                            "quantity": profile.items[key].quantity
                                        })
                                                
                                        profile.rvn += 1;
                                        profile.commandRevision += 1;
                                                
                                        break;
                                    }
                                }
                            }
                        }
                    }
                })
            }

            // Battle pass
            if (value.name.startsWith("BRSeason")) {
                if (!Number.isNaN(Number(value.name.split("BRSeason")[1]))) {
                    var offer = value.catalogEntries.find(i => i.offerId == req.body.offerId);

                    if (offer) {
                        if (MultiUpdate.length == 0) {
                            MultiUpdate.push({
                                "profileRevision": athena.rvn || 0,
                                "profileId": "athena",
                                "profileChangesBaseRevision": athena.rvn || 0,
                                "profileChanges": [],
                                "profileCommandRevision": athena.commandRevision || 0,
                            })
                        }

                        var Season = value.name.split("BR")[1];
                        var BattlePass = require(`./../connect/BattlePass/${Season}.json`);

                        if (BattlePass) {
                            var SeasonData = require("./../connect/SeasonData.json");

                            if (BattlePass.battlePassOfferId == offer.offerId || BattlePass.battleBundleOfferId == offer.offerId) {
                                var lootList = [];
                                var EndingTier = SeasonData[Season].battlePassTier;
                                SeasonData[Season].battlePassPurchased = true;

                                if (BattlePass.battleBundleOfferId == offer.offerId) {
                                    SeasonData[Season].battlePassTier += 25;
                                    if (SeasonData[Season].battlePassTier > 100) SeasonData[Season].battlePassTier = 100;
                                    EndingTier = SeasonData[Season].battlePassTier;
                                }

                                for (var i = 0; i < EndingTier; i++) {
                                    var FreeTier = BattlePass.freeRewards[i] || {};
                                    var PaidTier = BattlePass.paidRewards[i] || {};

                                    for (var item in FreeTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += FreeTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":FreeTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": FreeTier[item]
                                        })
                                    }

                                    for (var item in PaidTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += PaidTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":PaidTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": PaidTier[item]
                                        })
                                    }
                                }

                                var GiftBoxID = functions.MakeID();
                                var GiftBox = {"templateId":Number(Season.split("Season")[1]) <= 4 ? "GiftBox:gb_battlepass" : "GiftBox:gb_battlepasspurchased","attributes":{"max_level_bonus":0,"fromAccountId":"","lootList":lootList}}

                                if (Number(Season.split("Season")[1]) > 2) {
                                    profile.items[GiftBoxID] = GiftBox;
                                    
                                    ApplyProfileChanges.push({
                                        "changeType": "itemAdded",
                                        "itemId": GiftBoxID,
                                        "item": GiftBox
                                    })
                                }

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "statModified",
                                    "name": "book_purchased",
                                    "value": SeasonData[Season].battlePassPurchased
                                })

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "statModified",
                                    "name": "book_level",
                                    "value": SeasonData[Season].battlePassTier
                                })

                                AthenaModified = true;
                            }

                            if (BattlePass.tierOfferId == offer.offerId) {
                                var lootList = [];
                                var StartingTier = SeasonData[Season].battlePassTier;
                                var EndingTier;
                                SeasonData[Season].battlePassTier += req.body.purchaseQuantity || 1;
                                EndingTier = SeasonData[Season].battlePassTier;

                                for (var i = StartingTier; i < EndingTier; i++) {
                                    var FreeTier = BattlePass.freeRewards[i] || {};
                                    var PaidTier = BattlePass.paidRewards[i] || {};

                                    for (var item in FreeTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += FreeTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":FreeTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": FreeTier[item]
                                        })
                                    }

                                    for (var item in PaidTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += PaidTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":PaidTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": PaidTier[item]
                                        })
                                    }
                                }

                                var GiftBoxID = functions.MakeID();
                                var GiftBox = {"templateId":"GiftBox:gb_battlepass","attributes":{"max_level_bonus":0,"fromAccountId":"","lootList":lootList}}

                                if (Number(Season.split("Season")[1]) > 2) {
                                    profile.items[GiftBoxID] = GiftBox;
                                    
                                    ApplyProfileChanges.push({
                                        "changeType": "itemAdded",
                                        "itemId": GiftBoxID,
                                        "item": GiftBox
                                    })
                                }

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "statModified",
                                    "name": "book_level",
                                    "value": SeasonData[Season].battlePassTier
                                })

                                AthenaModified = true;
                            }

                            fs.writeFileSync("./connect/SeasonData.json", JSON.stringify(SeasonData, null, 2));
                        }
                    }
                }
            }

            if (value.name.startsWith("BR")) {
                catalog.storefronts[a].catalogEntries.forEach(function(value, b) {
                    if (value.offerId == req.body.offerId) {
                        catalog.storefronts[a].catalogEntries[b].itemGrants.forEach(function(value, c) {
                            const ID = value.templateId;

                            for (var key in athena.items) {
                                if (value.templateId.toLowerCase() == athena.items[key].templateId.toLowerCase()) {
                                    ItemExists = true;
                                }
                            }

                            if (ItemExists == false) {
                                if (MultiUpdate.length == 0) {
                                    MultiUpdate.push({
                                        "profileRevision": athena.rvn || 0,
                                        "profileId": "athena",
                                        "profileChangesBaseRevision": athena.rvn || 0,
                                        "profileChanges": [],
                                        "profileCommandRevision": athena.commandRevision || 0,
                                    })
                                }

                                if (Notifications.length == 0) {
                                    Notifications.push({
                                        "type": "CatalogPurchase",
                                        "primary": true,
                                        "lootResult": {
                                            "items": []
                                        }
                                    })
                                }

                                const Item = {
                                    "templateId": value.templateId,
                                    "attributes": {
                                        "max_level_bonus": 0,
                                        "level": 1,
                                        "item_seen": false,
                                        "xp": 0,
                                        "variants": [],
                                        "favorite": false
                                    },
                                    "quantity": 1
                                };

                                athena.items[ID] = Item;

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "itemAdded",
                                    "itemId": ID,
                                    "item": athena.items[ID]
                                })

                                Notifications[0].lootResult.items.push({
                                    "itemType": value.templateId,
                                    "itemGuid": ID,
                                    "itemProfile": "athena",
                                    "quantity": value.quantity
                                })

                                AthenaModified = true;
                            }

                            ItemExists = false;
                        })
                        // Vbucks spending
                        if (catalog.storefronts[a].catalogEntries[b].prices[0].currencyType.toLowerCase() == "mtxcurrency") {
                            for (var key in profile.items) {
                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                        profile.items[key].quantity -= (catalog.storefronts[a].catalogEntries[b].prices[0].finalPrice) * req.body.purchaseQuantity || 1;
                        
                                        ApplyProfileChanges.push({
                                            "changeType": "itemQuantityChanged",
                                            "itemId": key,
                                            "quantity": profile.items[key].quantity
                                        })

                                        profile.rvn += 1;
                                        profile.commandRevision += 1;

                                        break;
                                    }
                                }
                            }
                        }
                    }
                })
            }
        })

        PurchasedLlama = true;

        if (AthenaModified == true) {
            athena.rvn += 1;
            athena.commandRevision += 1;

            if (MultiUpdate[0]) {
                MultiUpdate[0].profileRevision = athena.rvn || 0;
                MultiUpdate[0].profileCommandRevision = athena.commandRevision || 0;
            }

            fs.writeFileSync("./data/athena.json", JSON.stringify(athena, null, 2));
            fs.writeFileSync(`./data/${req.query.profileId || "profile0"}.json`, JSON.stringify(profile, null, 2));
        }

        if (AthenaModified == false) {
            profile.rvn += 1;
            profile.commandRevision += 1;

            fs.writeFileSync(`./data/${req.query.profileId || "profile0"}.json`, JSON.stringify(profile, null, 2));
        }
    }

    if (req.body.offerId && profile.profileId == "common_core") {
        catalog.storefronts.forEach(function(value, a) {
            if (value.name.toLowerCase().startsWith("cardpack")) {
                catalog.storefronts[a].catalogEntries.forEach(function(value, b) {
                    if (value.offerId == req.body.offerId) {
                        var Quantity = 0;
                        catalog.storefronts[a].catalogEntries[b].itemGrants.forEach(function(value, c) {
                            const memory = functions.GetVersionInfo(req);

                            if (4 >= memory.season && PurchasedLlama == false) {
                                if (MultiUpdate.length == 0) {
                                    MultiUpdate.push({
                                        "profileRevision": campaign.rvn || 0,
                                        "profileId": "campaign",
                                        "profileChangesBaseRevision": campaign.rvn || 0,
                                        "profileChanges": [],
                                        "profileCommandRevision": campaign.commandRevision || 0,
                                    })
                                }

                                Quantity = req.body.purchaseQuantity || 1;

                                const Item = {
                                    "templateId": value.templateId,
                                    "attributes": {
                                        "is_loot_tier_overridden": false,
                                        "max_level_bonus": 0,
                                        "level": 1391,
                                        "pack_source": "Schedule",
                                        "item_seen": false,
                                        "xp": 0,
                                        "favorite": false,
                                        "override_loot_tier": 0
                                    },
                                    "quantity": 1
                                };

                                for (var i = 0; i < Quantity; i++) {
                                    var ID = functions.MakeID();
    
                                    campaign.items[ID] = Item

                                    MultiUpdate[0].profileChanges.push({
                                        "changeType": "itemAdded",
                                        "itemId": ID,
                                        "item": campaign.items[ID]
                                    })
                                }

                                PurchasedLlama = true;
                            }

                            if (memory.build >= 5 && memory.build <= 7.20 && PurchasedLlama == false) {
                                if (MultiUpdate.length == 0) {
                                    MultiUpdate.push({
                                        "profileRevision": campaign.rvn || 0,
                                        "profileId": "campaign",
                                        "profileChangesBaseRevision": campaign.rvn || 0,
                                        "profileChanges": [],
                                        "profileCommandRevision": campaign.commandRevision || 0,
                                    })
                                }

                                Quantity = req.body.purchaseQuantity || 1;

                                const Item = {
                                    "templateId": value.templateId,
                                    "attributes": {
                                        "is_loot_tier_overridden": false,
                                        "max_level_bonus": 0,
                                        "level": 1391,
                                        "pack_source": "Schedule",
                                        "item_seen": false,
                                        "xp": 0,
                                        "favorite": false,
                                        "override_loot_tier": 0
                                    },
                                    "quantity": 1
                                };

                                for (var i = 0; i < Quantity; i++) {
                                    var ID = functions.MakeID();
    
                                    campaign.items[ID] = Item

                                    MultiUpdate[0].profileChanges.push({
                                        "changeType": "itemAdded",
                                        "itemId": ID,
                                        "item": campaign.items[ID]
                                    })
                                }

                                Notifications.push({
                                    "type": "cardPackResult",
                                    "primary": true,
                                    "lootGranted": {
                                        "tierGroupName": "",
                                        "items": []
                                    },
                                    "displayLevel": 0
                                })

                                PurchasedLlama = true;
                            }

                            if (6 < memory.season && PurchasedLlama == false) {
                                if (MultiUpdate.length == 0) {
                                    MultiUpdate.push({
                                        "profileRevision": campaign.rvn || 0,
                                        "profileId": "campaign",
                                        "profileChangesBaseRevision": campaign.rvn || 0,
                                        "profileChanges": [],
                                        "profileCommandRevision": campaign.commandRevision || 0,
                                    })
                                }

                                Quantity = req.body.purchaseQuantity || 1;
                                var LlamaItemIDS = [];

                                var Item = {
                                    "templateId": value.templateId,
                                    "attributes": {
                                        "is_loot_tier_overridden": false,
                                        "max_level_bonus": 0,
                                        "level": 1391,
                                        "pack_source": "Schedule",
                                        "item_seen": false,
                                        "xp": 0,
                                        "favorite": false,
                                        "override_loot_tier": 0
                                    },
                                    "quantity": 1
                                };

                                for (var i = 0; i < Quantity; i++) {
                                    var ID = functions.MakeID();
    
                                    campaign.items[ID] = Item

                                    MultiUpdate[0].profileChanges.push({
                                        "changeType": "itemAdded",
                                        "itemId": ID,
                                        "item": campaign.items[ID]
                                    })

                                    LlamaItemIDS.push(ID);
                                }

                                Notifications.push({
                                    "type": "CatalogPurchase",
                                    "primary": true,
                                    "lootResult": {
                                        "items": []
                                    }
                                })

                                if (req.body.currencySubType.toLowerCase() != "accountresource:voucher_basicpack") {
                                    for (var x = 0; x < Quantity; x++) {
                                        for (var key in campaign.items) {
                                            if (campaign.items[key].templateId.toLowerCase() == "prerolldata:preroll_basic") {
                                                if (campaign.items[key].attributes.offerId == req.body.offerId) {
                                                    for (var item in campaign.items[key].attributes.items) {
                                                        const id = functions.MakeID();
                                                        var Item = {"templateId":campaign.items[key].attributes.items[item].itemType,"attributes":campaign.items[key].attributes.items[item].attributes,"quantity":campaign.items[key].attributes.items[item].quantity};
                
                                                        campaign.items[id] = Item;

                                                        MultiUpdate[0].profileChanges.push({
                                                            "changeType": "itemAdded",
                                                            "itemId": id,
                                                            "item": Item
                                                        })

                                                        Notifications[0].lootResult.items.push({
                                                            "itemType": campaign.items[key].attributes.items[item].itemType,
                                                            "itemGuid": id,
                                                            "itemProfile": "campaign",
                                                            "attributes": Item.attributes,
                                                            "quantity": 1
                                                        })
                                                    }

                                                    campaign.items[key].attributes.items = [];

                                                    for (var i = 0; i < 10; i++) {
                                                        const randomNumber = Math.floor(Math.random() * ItemIDS.length);

                                                        campaign.items[key].attributes.items.push({"itemType":ItemIDS[randomNumber],"attributes":{"legacy_alterations":[],"max_level_bonus":0,"level":1,"refund_legacy_item":false,"item_seen":false,"alterations":["","","","","",""],"xp":0,"refundable":false,"alteration_base_rarities":[],"favorite":false},"quantity":1})
                                                    }

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "items",
                                                        "attributeValue": campaign.items[key].attributes.items
                                                    })
                                                }
                                            }
                                        }
                                    }
                                }

                                try {
                                    if (req.body.currencySubType.toLowerCase() != "accountresource:voucher_basicpack") {
                                        for (var i in LlamaItemIDS) {
                                            var id = LlamaItemIDS[i];

                                            delete campaign.items[id];
                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "itemRemoved",
                                                "itemId": id
                                            })
                                        }
                                    }
                                } catch (err) {}

                                PurchasedLlama = true;
                            }
                        })
                        // Vbucks spending
                        if (catalog.storefronts[a].catalogEntries[b].prices[0].currencyType.toLowerCase() == "mtxcurrency") {
                            for (var key in profile.items) {
                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                        profile.items[key].quantity -= (catalog.storefronts[a].catalogEntries[b].prices[0].finalPrice) * Quantity;
                                                
                                        ApplyProfileChanges.push({
                                            "changeType": "itemQuantityChanged",
                                            "itemId": key,
                                            "quantity": profile.items[key].quantity
                                        })
                        
                                        profile.rvn += 1;
                                        profile.commandRevision += 1;
                        
                                        break;
                                    }
                                }
                            }
                        }
                    }
                })
            }

            // Battle pass
            if (value.name.startsWith("BRSeason")) {
                if (!Number.isNaN(Number(value.name.split("BRSeason")[1]))) {
                    var offer = value.catalogEntries.find(i => i.offerId == req.body.offerId);

                    if (offer) {
                        if (MultiUpdate.length == 0) {
                            MultiUpdate.push({
                                "profileRevision": athena.rvn || 0,
                                "profileId": "athena",
                                "profileChangesBaseRevision": athena.rvn || 0,
                                "profileChanges": [],
                                "profileCommandRevision": athena.commandRevision || 0,
                            })
                        }

                        var Season = value.name.split("BR")[1];
                        var BattlePass = require(`./../connect/BattlePass/${Season}.json`);

                        if (BattlePass) {
                            var SeasonData = require("./../connect/SeasonData.json");

                            if (BattlePass.battlePassOfferId == offer.offerId || BattlePass.battleBundleOfferId == offer.offerId) {
                                var lootList = [];
                                var EndingTier = SeasonData[Season].battlePassTier;
                                SeasonData[Season].battlePassPurchased = true;

                                if (BattlePass.battleBundleOfferId == offer.offerId) {
                                    SeasonData[Season].battlePassTier += 25;
                                    if (SeasonData[Season].battlePassTier > 100) SeasonData[Season].battlePassTier = 100;
                                    EndingTier = SeasonData[Season].battlePassTier;
                                }

                                for (var i = 0; i < EndingTier; i++) {
                                    var FreeTier = BattlePass.freeRewards[i] || {};
                                    var PaidTier = BattlePass.paidRewards[i] || {};

                                    for (var item in FreeTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += FreeTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":FreeTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": FreeTier[item]
                                        })
                                    }

                                    for (var item in PaidTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += PaidTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":PaidTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": PaidTier[item]
                                        })
                                    }
                                }

                                var GiftBoxID = functions.MakeID();
                                var GiftBox = {"templateId":Number(Season.split("Season")[1]) <= 4 ? "GiftBox:gb_battlepass" : "GiftBox:gb_battlepasspurchased","attributes":{"max_level_bonus":0,"fromAccountId":"","lootList":lootList}}

                                if (Number(Season.split("Season")[1]) > 2) {
                                    profile.items[GiftBoxID] = GiftBox;
                                    
                                    ApplyProfileChanges.push({
                                        "changeType": "itemAdded",
                                        "itemId": GiftBoxID,
                                        "item": GiftBox
                                    })
                                }

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "statModified",
                                    "name": "book_purchased",
                                    "value": SeasonData[Season].battlePassPurchased
                                })

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "statModified",
                                    "name": "book_level",
                                    "value": SeasonData[Season].battlePassTier
                                })

                                AthenaModified = true;
                            }

                            if (BattlePass.tierOfferId == offer.offerId) {
                                var lootList = [];
                                var StartingTier = SeasonData[Season].battlePassTier;
                                var EndingTier;
                                SeasonData[Season].battlePassTier += req.body.purchaseQuantity || 1;
                                EndingTier = SeasonData[Season].battlePassTier;

                                for (var i = StartingTier; i < EndingTier; i++) {
                                    var FreeTier = BattlePass.freeRewards[i] || {};
                                    var PaidTier = BattlePass.paidRewards[i] || {};

                                    for (var item in FreeTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += FreeTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += FreeTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":FreeTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": FreeTier[item]
                                        })
                                    }

                                    for (var item in PaidTier) {
                                        if (item.toLowerCase() == "token:athenaseasonxpboost") {
                                            SeasonData[Season].battlePassXPBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_match_boost",
                                                "value": SeasonData[Season].battlePassXPBoost
                                            })
                                        }

                                        if (item.toLowerCase() == "token:athenaseasonfriendxpboost") {
                                            SeasonData[Season].battlePassXPFriendBoost += PaidTier[item];

                                            MultiUpdate[0].profileChanges.push({
                                                "changeType": "statModified",
                                                "name": "season_friend_match_boost",
                                                "value": SeasonData[Season].battlePassXPFriendBoost
                                            })
                                        }

                                        if (item.toLowerCase().startsWith("currency:mtx")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                                        profile.items[key].quantity += PaidTier[item];
                                                        break;
                                                    }
                                                }
                                            }
                                        }

                                        if (item.toLowerCase().startsWith("homebasebanner")) {
                                            for (var key in profile.items) {
                                                if (profile.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    profile.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    ApplyProfileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": profile.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"item_seen":false},"quantity":1};

                                                profile.items[ItemID] = Item;

                                                ApplyProfileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        if (item.toLowerCase().startsWith("athena")) {
                                            for (var key in athena.items) {
                                                if (athena.items[key].templateId.toLowerCase() == item.toLowerCase()) {
                                                    athena.items[key].attributes.item_seen = false;
                                                    ItemExists = true;

                                                    MultiUpdate[0].profileChanges.push({
                                                        "changeType": "itemAttrChanged",
                                                        "itemId": key,
                                                        "attributeName": "item_seen",
                                                        "attributeValue": athena.items[key].attributes.item_seen
                                                    })
                                                }
                                            }

                                            if (ItemExists == false) {
                                                var ItemID = functions.MakeID();
                                                var Item = {"templateId":item,"attributes":{"max_level_bonus":0,"level":1,"item_seen":false,"xp":0,"variants":[],"favorite":false},"quantity":PaidTier[item]}

                                                athena.items[ItemID] = Item;

                                                MultiUpdate[0].profileChanges.push({
                                                    "changeType": "itemAdded",
                                                    "itemId": ItemID,
                                                    "item": Item
                                                })
                                            }

                                            ItemExists = false;
                                        }

                                        lootList.push({
                                            "itemType": item,
                                            "itemGuid": item,
                                            "quantity": PaidTier[item]
                                        })
                                    }
                                }

                                var GiftBoxID = functions.MakeID();
                                var GiftBox = {"templateId":"GiftBox:gb_battlepass","attributes":{"max_level_bonus":0,"fromAccountId":"","lootList":lootList}}

                                if (Number(Season.split("Season")[1]) > 2) {
                                    profile.items[GiftBoxID] = GiftBox;
                                    
                                    ApplyProfileChanges.push({
                                        "changeType": "itemAdded",
                                        "itemId": GiftBoxID,
                                        "item": GiftBox
                                    })
                                }

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "statModified",
                                    "name": "book_level",
                                    "value": SeasonData[Season].battlePassTier
                                })

                                AthenaModified = true;
                            }

                            fs.writeFileSync("./connect/SeasonData.json", JSON.stringify(SeasonData, null, 2));
                        }
                    }
                }
            }

            if (value.name.startsWith("BR")) {
                catalog.storefronts[a].catalogEntries.forEach(function(value, b) {
                    if (value.offerId == req.body.offerId) {
                        catalog.storefronts[a].catalogEntries[b].itemGrants.forEach(function(value, c) {
                            const ID = value.templateId;

                            for (var key in athena.items) {
                                if (value.templateId.toLowerCase() == athena.items[key].templateId.toLowerCase()) {
                                    ItemExists = true;
                                }
                            }

                            if (ItemExists == false) {
                                if (MultiUpdate.length == 0) {
                                    MultiUpdate.push({
                                        "profileRevision": athena.rvn || 0,
                                        "profileId": "athena",
                                        "profileChangesBaseRevision": athena.rvn || 0,
                                        "profileChanges": [],
                                        "profileCommandRevision": athena.commandRevision || 0,
                                    })
                                }

                                if (Notifications.length == 0) {
                                    Notifications.push({
                                        "type": "CatalogPurchase",
                                        "primary": true,
                                        "lootResult": {
                                            "items": []
                                        }
                                    })
                                }

                                const Item = {
                                    "templateId": value.templateId,
                                    "attributes": {
                                        "max_level_bonus": 0,
                                        "level": 1,
                                        "item_seen": false,
                                        "xp": 0,
                                        "variants": [],
                                        "favorite": false
                                    },
                                    "quantity": 1
                                };

                                athena.items[ID] = Item;

                                MultiUpdate[0].profileChanges.push({
                                    "changeType": "itemAdded",
                                    "itemId": ID,
                                    "item": Item
                                })

                                Notifications[0].lootResult.items.push({
                                    "itemType": value.templateId,
                                    "itemGuid": ID,
                                    "itemProfile": "athena",
                                    "quantity": value.quantity
                                })

                                AthenaModified = true;
                            }

                            ItemExists = false;
                        })
                        // Vbucks spending
                        if (catalog.storefronts[a].catalogEntries[b].prices[0].currencyType.toLowerCase() == "mtxcurrency") {
                            for (var key in profile.items) {
                                if (profile.items[key].templateId.toLowerCase().startsWith("currency:mtx")) {
                                    if (profile.items[key].attributes.platform.toLowerCase() == profile.stats.attributes.current_mtx_platform.toLowerCase() || profile.items[key].attributes.platform.toLowerCase() == "shared") {
                                        profile.items[key].quantity -= (catalog.storefronts[a].catalogEntries[b].prices[0].finalPrice) * req.body.purchaseQuantity || 1;
                                                
                                        ApplyProfileChanges.push({
                                            "changeType": "itemQuantityChanged",
                                            "itemId": key,
                                            "quantity": profile.items[key].quantity
                                        })
                        
                                        break;
                                    }
                                }
                            }
                        }

                        if (catalog.storefronts[a].catalogEntries[b].itemGrants.length != 0) {
                            // Add to refunding tab
                            var purchaseId = functions.MakeID();
                            profile.stats.attributes.mtx_purchase_history.purchases.push({"purchaseId":purchaseId,"offerId":`v2:/${purchaseId}`,"purchaseDate":new Date().toISOString(),"freeRefundEligible":false,"fulfillments":[],"lootResult":Notifications[0].lootResult.items,"totalMtxPaid":catalog.storefronts[a].catalogEntries[b].prices[0].finalPrice,"metadata":{},"gameContext":""})

                            ApplyProfileChanges.push({
                                "changeType": "statModified",
                                "name": "mtx_purchase_history",
                                "value": profile.stats.attributes.mtx_purchase_history
                            })
                        }

                        profile.rvn += 1;
                        profile.commandRevision += 1;
                    }
                })
            }
        })

        if (AthenaModified == true) {
            athena.rvn += 1;
            athena.commandRevision += 1;

            if (MultiUpdate[0]) {
                MultiUpdate[0].profileRevision = athena.rvn || 0;
                MultiUpdate[0].profileCommandRevision = athena.commandRevision || 0;
            }

            fs.writeFileSync("./data/athena.json", JSON.stringify(athena, null, 2));
            fs.writeFileSync(`./data/${req.query.profileId || "common_core"}.json`, JSON.stringify(profile, null, 2));
        }

        if (AthenaModified == false) {
            campaign.rvn += 1;
            campaign.commandRevision += 1;

            if (MultiUpdate[0]) {
                MultiUpdate[0].profileRevision = campaign.rvn || 0;
                MultiUpdate[0].profileCommandRevision = campaign.commandRevision || 0;
            }
            fs.writeFileSync(`./data/${req.query.profileId || "common_core"}.json`, JSON.stringify(profile, null, 2));
        }
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "profile0",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "notifications": Notifications,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "multiUpdate": MultiUpdate,
        "responseVersion": 1
    })
    res.end();
});

// Set multiple items favorite
express.post("/fortnite/api/game/v2/profile/*/client/SetItemFavoriteStatusBatch", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.itemIds) {
        for (var i in req.body.itemIds) {
            profile.items[req.body.itemIds[i]].attributes.favorite = req.body.itemFavStatus[i] || false;

            ApplyProfileChanges.push({
                "changeType": "itemAttrChanged",
                "itemId": req.body.itemIds[i],
                "attributeName": "favorite",
                "attributeValue": profile.items[req.body.itemIds[i]].attributes.favorite
            })
        }
        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Set favorite on item
express.post("/fortnite/api/game/v2/profile/*/client/SetItemFavoriteStatus", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.targetItemId) {
        profile.items[req.body.targetItemId].attributes.favorite = req.body.bFavorite || false;
        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "itemAttrChanged",
            "itemId": req.body.targetItemId,
            "attributeName": "favorite",
            "attributeValue": profile.items[req.body.targetItemId].attributes.favorite
        })

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Mark item as seen
express.post("/fortnite/api/game/v2/profile/*/client/MarkItemSeen", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.itemIds) {
        for (var i in req.body.itemIds) {
            profile.items[req.body.itemIds[i]].attributes.item_seen = true;

            ApplyProfileChanges.push({
                "changeType": "itemAttrChanged",
                "itemId": req.body.itemIds[i],
                "attributeName": "item_seen",
                "attributeValue": profile.items[req.body.itemIds[i]].attributes.item_seen
            })
        }
        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Equip BR Locker 1
express.post("/fortnite/api/game/v2/profile/*/client/EquipBattleRoyaleCustomization", async (req, res) => {
    const profile = require("./../data/athena.json");

    try {
        if (!profile.stats.attributes.favorite_dance) {
            profile.stats.attributes.favorite_dance = ["","","","","",""];
        }
        if (!profile.stats.attributes.favorite_itemwraps) {
            profile.stats.attributes.favorite_itemwraps = ["","","","","","",""];
        }
    } catch (err) {}

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;
    var VariantChanged = false;

    try {
        const ReturnVariantsAsString = JSON.stringify(req.body.variantUpdates || [])

        if (ReturnVariantsAsString.includes("active")) {
            if (profile.items[req.body.itemToSlot].attributes.variants.length == 0) {
                profile.items[req.body.itemToSlot].attributes.variants = req.body.variantUpdates || [];
            }
			
            for (var i in profile.items[req.body.itemToSlot].attributes.variants) {
                try {
                    if (profile.items[req.body.itemToSlot].attributes.variants[i].channel.toLowerCase() == req.body.variantUpdates[i].channel.toLowerCase()) {
                        profile.items[req.body.itemToSlot].attributes.variants[i].active = req.body.variantUpdates[i].active || "";
                    }
                } catch (err) {}
            }
			
            VariantChanged = true;
        }
    } catch (err) {}

    if (req.body.slotName) {

        switch (req.body.slotName) {

            case "Character":
                profile.stats.attributes.favorite_character = req.body.itemToSlot || "";
                StatChanged = true;
                break;

            case "Backpack":
                profile.stats.attributes.favorite_backpack = req.body.itemToSlot || "";
                StatChanged = true;
                break;

            case "Pickaxe":
                profile.stats.attributes.favorite_pickaxe = req.body.itemToSlot || "";
                StatChanged = true;
                break;

            case "Glider":
                profile.stats.attributes.favorite_glider = req.body.itemToSlot || "";
                StatChanged = true;
                break;

            case "SkyDiveContrail":
                profile.stats.attributes.favorite_skydivecontrail = req.body.itemToSlot || "";
                StatChanged = true;
                break;

            case "MusicPack":
                profile.stats.attributes.favorite_musicpack = req.body.itemToSlot || "";
                StatChanged = true;
                break;

            case "LoadingScreen":
                profile.stats.attributes.favorite_loadingscreen = req.body.itemToSlot || "";
                StatChanged = true;
                break;

            case "Dance":
                var indexwithinslot = req.body.indexWithinSlot || 0;

                if (Math.sign(indexwithinslot) == 1 || Math.sign(indexwithinslot) == 0) {
                    profile.stats.attributes.favorite_dance[indexwithinslot] = req.body.itemToSlot || "";
                }

                StatChanged = true;
                break;

            case "ItemWrap":
                var indexwithinslot = req.body.indexWithinSlot || 0;

                switch (Math.sign(indexwithinslot)) {

                    case 0:
                        profile.stats.attributes.favorite_itemwraps[indexwithinslot] = req.body.itemToSlot || "";
                        break;

                    case 1:
                        profile.stats.attributes.favorite_itemwraps[indexwithinslot] = req.body.itemToSlot || "";
                        break;

                    case -1:
                        for (var i = 0; i < 7; i++) {
                            profile.stats.attributes.favorite_itemwraps[i] = req.body.itemToSlot || "";
                        }
                        break;

                }

                StatChanged = true;
                break;

        }

    }

    if (StatChanged == true) {
        var Category = (`favorite_${req.body.slotName || "character"}`).toLowerCase()

        if (Category == "favorite_itemwrap") {
            Category += "s"
        }

        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": Category,
            "value": profile.stats.attributes[Category]
        })

        if (VariantChanged == true) {
            ApplyProfileChanges.push({
                "changeType": "itemAttrChanged",
                "itemId": req.body.itemToSlot,
                "attributeName": "variants",
                "attributeValue": profile.items[req.body.itemToSlot].attributes.variants
            })
        }
        fs.writeFileSync("./data/athena.json", JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Set BR Banner 1
express.post("/fortnite/api/game/v2/profile/*/client/SetBattleRoyaleBanner", async (req, res) => {
    const profile = require("./../data/athena.json");

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.homebaseBannerIconId && req.body.homebaseBannerColorId) {
        profile.stats.attributes.banner_icon = req.body.homebaseBannerIconId;
        profile.stats.attributes.banner_color = req.body.homebaseBannerColorId;
        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "banner_icon",
            "value": profile.stats.attributes.banner_icon
        })

        ApplyProfileChanges.push({
            "changeType": "statModified",
            "name": "banner_color",
            "value": profile.stats.attributes.banner_color
        })

        fs.writeFileSync("./data/athena.json", JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Set BR Banner 2
express.post("/fortnite/api/game/v2/profile/*/client/SetCosmeticLockerBanner", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    if (req.body.bannerIconTemplateName && req.body.bannerColorTemplateName && req.body.lockerItem) {
        profile.items[req.body.lockerItem].attributes.banner_icon_template = req.body.bannerIconTemplateName;
        profile.items[req.body.lockerItem].attributes.banner_color_template = req.body.bannerColorTemplateName;
        StatChanged = true;
    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "itemAttrChanged",
            "itemId": req.body.lockerItem,
            "attributeName": "banner_icon_template",
            "attributeValue": profile.items[req.body.lockerItem].attributes.banner_icon_template
        })

        ApplyProfileChanges.push({
            "changeType": "itemAttrChanged",
            "itemId": req.body.lockerItem,
            "attributeName": "banner_color_template",
            "attributeValue": profile.items[req.body.lockerItem].attributes.banner_color_template
        })

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// Set BR Locker 2
express.post("/fortnite/api/game/v2/profile/*/client/SetCosmeticLockerSlot", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;
    var StatChanged = false;

    try {
        const ReturnVariantsAsString = JSON.stringify(req.body.variantUpdates || [])

        if (ReturnVariantsAsString.includes("active")) {
            var new_variants = [
                {
                    "variants": []
                }
            ];

            if (profile.profileId == "athena") {
                if (profile.items[req.body.itemToSlot].attributes.variants.length == 0) {
                    profile.items[req.body.itemToSlot].attributes.variants = req.body.variantUpdates || [];
                }
				
                for (var i in profile.items[req.body.itemToSlot].attributes.variants) {
                    try {
                        if (profile.items[req.body.itemToSlot].attributes.variants[i].channel.toLowerCase() == req.body.variantUpdates[i].channel.toLowerCase()) {
                            profile.items[req.body.itemToSlot].attributes.variants[i].active = req.body.variantUpdates[i].active || "";
                        }
                    } catch (err) {}
                }
            }

            for (var i in req.body.variantUpdates) {
                new_variants[0].variants.push({
                    "channel": req.body.variantUpdates[i].channel,
                    "active": req.body.variantUpdates[i].active
                })

                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots[req.body.category].activeVariants = new_variants;
            }
        }
    } catch (err) {}

    if (req.body.category && req.body.lockerItem) {

        switch (req.body.category) {

            case "Character":
                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.Character.items = [req.body.itemToSlot || ""];
                StatChanged = true;
                break;

            case "Backpack":
                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.Backpack.items = [req.body.itemToSlot || ""];
                StatChanged = true;
                break;

            case "Pickaxe":
                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.Pickaxe.items = [req.body.itemToSlot || ""];
                StatChanged = true;
                break;

            case "Glider":
                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.Glider.items = [req.body.itemToSlot || ""];
                StatChanged = true;
                break;

            case "SkyDiveContrail":
                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.SkyDiveContrail.items = [req.body.itemToSlot || ""];
                StatChanged = true;
                break;

            case "MusicPack":
                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.MusicPack.items = [req.body.itemToSlot || ""];
                StatChanged = true;
                break;

            case "LoadingScreen":
                profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.LoadingScreen.items = [req.body.itemToSlot || ""];
                StatChanged = true;
                break;

            case "Dance":
                var indexwithinslot = req.body.slotIndex || 0;

                if (Math.sign(indexwithinslot) == 1 || Math.sign(indexwithinslot) == 0) {
                    profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.Dance.items[indexwithinslot] = req.body.itemToSlot || "";
                }

                StatChanged = true;
                break;

            case "ItemWrap":
                var indexwithinslot = req.body.slotIndex || 0;

                switch (Math.sign(indexwithinslot)) {

                    case 0:
                        profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.ItemWrap.items[indexwithinslot] = req.body.itemToSlot || "";
                        break;

                    case 1:
                        profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.ItemWrap.items[indexwithinslot] = req.body.itemToSlot || "";
                        break;

                    case -1:
                        for (var i = 0; i < 7; i++) {
                            profile.items[req.body.lockerItem].attributes.locker_slots_data.slots.ItemWrap.items[i] = req.body.itemToSlot || "";
                        }
                        break;

                }

                StatChanged = true;
                break;

        }

    }

    if (StatChanged == true) {
        profile.rvn += 1;
        profile.commandRevision += 1;

        ApplyProfileChanges.push({
            "changeType": "itemAttrChanged",
            "itemId": req.body.lockerItem,
            "attributeName": "locker_slots_data",
            "attributeValue": profile.items[req.body.lockerItem].attributes.locker_slots_data
        })

        fs.writeFileSync(`./data/${req.query.profileId || "athena"}.json`, JSON.stringify(profile, null, 2));
    }

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

// any mcp request that doesn't have something assigned to it
express.post("/fortnite/api/game/v2/profile/*/client/*", async (req, res) => {
    const profile = require(`./../data/${req.query.profileId || "athena"}.json`);

    // do not change any of these or you will end up breaking it
    var ApplyProfileChanges = [];
    var BaseRevision = profile.rvn || 0;
    var QueryRevision = req.query.rvn || -1;

    // this doesn't work properly on version v12.20 and above but whatever
    if (QueryRevision != BaseRevision) {
        ApplyProfileChanges = [{
            "changeType": "fullProfileUpdate",
            "profile": profile
        }];
    }

    res.json({
        "profileRevision": profile.rvn || 0,
        "profileId": req.query.profileId || "athena",
        "profileChangesBaseRevision": BaseRevision,
        "profileChanges": ApplyProfileChanges,
        "profileCommandRevision": profile.commandRevision || 0,
        "serverTime": new Date().toISOString(),
        "responseVersion": 1
    })
    res.end();
});

module.exports = express;
