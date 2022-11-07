const Express = require("express");
const express = Express.Router();
const functions = require("./functions.js");

express.get("/fortnite/api/calendar/v1/timeline", async (req, res) => {
    const memory = functions.GetVersionInfo(req);

    var activeEvents = [
    {
        "eventType": `EventFlag.Season${memory.season}`,
        "activeUntil": "2022-12-14T10:05:00.000Z",
        "activeSince": "2020-01-01T00:00:00.000Z"
    },
    {
        "eventType": `EventFlag.${memory.lobby}`,
        "activeUntil": "2022-12-14T10:05:00.000Z",
        "activeSince": "2020-01-01T00:00:00.000Z"
    }];

    if (memory.season == 3) {
        activeEvents.push(
        {
            "eventType": "EventFlag.Spring2018Phase1",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })
        if (memory.build >= 3.1) {
            activeEvents.push(
            {
                "eventType": "EventFlag.Spring2018Phase2",
                "activeUntil": "2022-12-14T10:05:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        }
        if (memory.build >= 3.3) {
            activeEvents.push(
            {
                "eventType": "EventFlag.Spring2018Phase3",
                "activeUntil": "2022-12-14T10:05:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        }
        if (memory.build >= 3.4) {
            activeEvents.push(
            {
                "eventType": "EventFlag.Spring2018Phase4",
                "activeUntil": "2022-12-14T10:05:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        }
    }

    if (memory.season == 4) {
        activeEvents.push(
        {
            "eventType": "EventFlag.Blockbuster2018",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.Blockbuster2018Phase1",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })
        if (memory.build >= 4.3) {
            activeEvents.push(
            {
                "eventType": "EventFlag.Blockbuster2018Phase2",
                "activeUntil": "2022-12-14T10:05:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        }
        if (memory.build >= 4.4) {
            activeEvents.push(
            {
                "eventType": "EventFlag.Blockbuster2018Phase3",
                "activeUntil": "2022-12-14T10:05:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        }
        if (memory.build >= 4.5) {
            activeEvents.push(
            {
                "eventType": "EventFlag.Blockbuster2018Phase4",
                "activeUntil": "2022-12-14T10:05:00.000Z",
                "activeSince": "2020-01-01T00:00:00.000Z"
            })
        }
    }

    if (memory.season == 5) {
        activeEvents.push(
        {
            "eventType": "EventFlag.RoadTrip2018",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.Horde",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.Anniversary2018_BR",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        },
        {
            "eventType": "EventFlag.LTM_Heist",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })
    }
    
    if (memory.build == 5.10) {
        activeEvents.push(
        {
            "eventType": "EventFlag.BirthdayBattleBus",
            "activeUntil": "2022-12-14T10:05:00.000Z",
            "activeSince": "2020-01-01T00:00:00.000Z"
        })
    }

    res.json({
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
                        "seasonNumber": memory.season,
                        "seasonTemplateId": `AthenaSeason:athenaseason${memory.season}`,
                        "matchXpBonusPoints": 0,
                        "seasonBegin": "2020-01-01T13:00:00Z",
                        "seasonEnd": "2022-12-14T10:05:00.000Z",
                        "seasonDisplayedEnd": "2022-12-14T10:05:00.000Z",
                        "weeklyStoreEnd": "2022-12-14T10:05:00.000Z",
                        "stwEventStoreEnd": "2022-12-14T10:05:00.000Z",
                        "stwWeeklyStoreEnd": "2022-12-14T10:05:00.000Z",
                        "dailyStoreEnd": "2022-12-14T10:05:00.000Z"
                    }
                }],
                "cacheExpire": "9999-01-01T22:28:47.830Z"
            }
        },
        "eventsTimeOffsetHrs": 0,
        "cacheIntervalMins": 10,
        "currentTime": new Date().toISOString()
    });
    res.end();
})

module.exports = express;