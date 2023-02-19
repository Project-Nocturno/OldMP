# OldMP (S1-S8)
OldMP est un ensemble de services dont un emulateur de lobby pour fortnite aussi appeler serveur backend, une interface web et un service de backend pour un launcher.
Les parametres updatable quand il est lancer sont dans [conf.json](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/conf.json), les parametres principaux des differents services sont dans [main.py](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/main.py). Les services OldMP sont situés dans les [modules](https://github.com/Project-Nocturno/OldMP/tree/main/OldMP/modules).  
Les differents services backend ont un ratelimite pour eviter des attaques bruteforce ou ddos:
```py
@app.before_request                             # s'execute avant chaque requete
def checkrps():
    exist=False
    for i in rps:                               # savoir si l'ip est deja enregistrer
        if i==request.remote_addr:
            exist=True
    if exist:                                   # si elle est enregistrer:
        if rps[request.remote_addr]>=20:        # si le nombre de requete par seconde est en dessous de 20
            respon=self.functions.createError(  # creer un message d'erreur si il y a trop de requetes
                "errors.com.epicgames.account.too_many_requests",
                "You have made more than the limited number of requests", 
                [], 18031, "too_many_requests"
            )
            resp=app.response_class(            # creer une erreur
                response=dumps(respon),
                status=400,
                mimetype='application/json'
            )
            return resp                         # envoyer l'erreur au client
        else:
            rps[request.remote_addr]+=1         # sinon ajouter 1 au nombre de requetes/s
    else:
        rps.update({request.remote_addr: 0})    # si l'ip n'existe pas la creer
```

## OldMP
Le service backend principal est par defaut sur le port 3551, il sert a faire fonctionner le jeux, il est connecter a une DB et il effectue des requetes vers une API. Le code est [ici](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmp.py)  
Pour recuperer des informations sur la partie ou le jeux, OldMP utilise la requete `/datarouter/api/v1/public/data`:
```py
@app.route('/datarouter/api/v1/public/data', methods=['POST'])
def datarouterapipublicdata():

    data=request.stream.read()
    for events in loads(data.decode())['Events']:
        for event in events:
            if event=='PlayerLocation': # recuperer les coordonnées des joueurs pour la map
                coords=str(events[event]).split(',')
                x: int=coords[0]
                y: int=coords[1]
                self.playerscoords.append((x, y))
                
            elif event=='AthenaPlayersLeft': # connaitre le nombre de joueurs restants
                sessions(sessionL, request.remote_addr).put('partyPlayerLeft', int(events[event]))
                
            elif event=='Location': # savoir si le joueur est en jeux
                if events[event]=='InGame':
                    sessions(sessionL, request.remote_addr).put('InGame', True)
                else:
                    sessions(sessionL, request.remote_addr).put('InGame', False)
            
            elif event=='AthenaMapName': # recuperer le nom de la map actuelle
                sessions(sessionL, request.remote_addr).put('mapName', events[event])
            
            elif event=='EventName':
                if events[event]=='SessionEnd': # savoir si l'utilisateur a quitter la partie en 1.8
                    sessions(sessionL, request.remote_addr).clear()

    resp=Response()
    resp.status_code=204
    return resp # retourne un code 204
```

## OldMPWeb
Le site web de OldMP est par defaut sur le port 80, il permet d'apporter une interface web pour les administarteurs et pour les utilisateurs, il y a egalement un systeme de carte (avec les emplacements de tous les joueurs de la partie) qui as été developper sur l'url `/map`.  
Il y a differentes fonctions qui permettent de recuperer les contents publiques (images et fichiers json) comme `/content/files/<file>` pour des fichiers json ou `/content/images/<file>` pour des images, pour lister tous les fichiers on utilise la commande `listall` a la place de `<file>`.
Le ratelimite pour ce service est de `5`  
Le code est [ici](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmpweb.py)

## OldMPLauncher

Le backend launcher est par defaut sur le port 4971, il propose un systeme d'authentification (la requete: `/launcher/auth` qui necessite un argument `grant_type`, `username`, `password`). 
le code retourner si il n'y a pas d'erreur est: 
```json
{
    "accountId": "<account_id>",
    "display_name": "<display_name>",
    "device_id": "<device_id>",
    "session_id": "<session_id>",
    "expire_in": 14400,
    "expire_at": "<date_dans_4h>"
}
```  
Un systeme de verification de MAJ avec la requete: `/launcher/versioncheck` qui retourne la bonne version  
Un systeme de rpc avec la requete: `/launcher/rpc/` qui vas retourner au format json:  
ce code si il est au lobby:
```json
{
    "username": "<username>",
    "character": "<skin>",
    "party": {
        "mapName": "Lobby",
        "playerLeft": 0
    }
}
```
et si il est in-game:
```json
{
    "username": "<username>",
    "character": "<skin>",
    "party": {
        "mapName": "<map_name>",
        "playerLeft": "<nombre_de_joueurs_restants>"
    }
}
```  
Un systeme de status avec l'url `/launcher/status` qui retourne (`online`, `maintenance` ou `offline`) au format text.
Un systeme de news avec l'url `/launcher/news` qui vas retourner les news au format text.  
Le ratelimite pour ce service est de `5`  
Le code est [ici](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmplauncher.py)
# Versions compatibles
## Versions:
 - 1.8
 - 1.9
 - 1.11
 - 2.4.2
 - 2.5
 - 3.5
 - 4.5
 - 6.21
 - 7.30
 - 8.40