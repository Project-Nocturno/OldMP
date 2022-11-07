const Express = require("express");
const express = Express();
const fs = require("fs");
const path = require("path");
const cookieParser = require("cookie-parser");

express.use(Express.json());
express.use(Express.urlencoded({ extended: true }));
express.use(Express.static('public'));
express.use(cookieParser());

express.use(require("./main/party.js"));
express.use(require("./main/discovery.js"))
express.use(require("./main/privacy.js"));
express.use(require("./main/timeline.js"));
express.use(require("./main/user.js"));
express.use(require("./main/contentpages.js"));
express.use(require("./main/friends.js"));
express.use(require("./main/main.js"));
express.use(require("./main/storefront.js"));
express.use(require("./main/version.js"));
express.use(require("./main/lightswitch.js"));
express.use(require("./main/affiliate.js"));
express.use(require("./main/matchmaking.js"));
express.use(require("./main/cloudstorage.js"));
express.use(require("./main/mcp.js"));

const port = process.env.PORT || 3551;
express.listen(port, () => {
    console.log("\nProject Nocturno\n\n\x1b[32m[SUCCES] \x1b[33m- \x1b[0mLe port:", port,"a bien été connecter à NocturnoServer.");

    require("./main/xmpp.js");
}).on("error", (err) => {
    if (err.code == "EADDRINUSE") console.log(`\x1b[31m[ERROR] \x1b[33m- \x1b[0mLe port: ${port} est déjà utiliser !`);
    else throw err;

    process.exit(0);
});

try {
    if (!fs.existsSync(path.join(process.env.LOCALAPPDATA, "LawinServer"))) fs.mkdirSync(path.join(process.env.LOCALAPPDATA, "LawinServer"));
} catch (err) {
    // fallback
    if (!fs.existsSync(path.join(__dirname, "ClientSettings"))) fs.mkdirSync(path.join(__dirname, "ClientSettings"));
}

// if endpoint not found, return this error
express.use((req, res, next) => {
    var XEpicErrorName = "errors.com.lawinserver.common.not_found";
    var XEpicErrorCode = 1004;

    res.set({
        'X-Epic-Error-Name': XEpicErrorName,
        'X-Epic-Error-Code': XEpicErrorCode
    });

    res.status(404);
    res.json({
        "errorCode": XEpicErrorName,
        "errorMessage": "Sorry the resource you were trying to find could not be found",
        "numericErrorCode": XEpicErrorCode,
        "originatingService": "any",
        "intent": "prod"
    });
});