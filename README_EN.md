# OldMP (S1-S8)

## Introduction
OldMP est un ensemble de services comprenant un émulateur de lobby pour Fortnite (serveur backend), une interface web et un service de backend pour un launcher. Ce projet prend en charge les versions de Fortnite de la Saison 1 à la Saison 8.

## Configuration
Les paramètres modifiables pendant l'exécution se trouvent dans le fichier [conf.json](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/conf.json). Les paramètres principaux des différents services sont définis dans [main.py](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/main.py). Les services OldMP sont situés dans le dossier [modules](https://github.com/Project-Nocturno/OldMP/tree/main/OldMP/modules).

## Sécurité
Les différents services backend disposent d'un système de limitation de requêtes (rate limiting) pour prévenir les attaques par force brute ou DDoS. Voici un exemple de l'implémentation optimisée:

```python
@app.before_request
def checkrps():
    # Vérifier si l'IP est déjà enregistrée
    if request.remote_addr not in self.functions.rps:
        self.functions.rps[request.remote_addr] = 0
    
    # Vérifier si le nombre de requêtes par seconde dépasse la limite
    if self.functions.rps[request.remote_addr] >= config['rps']['service']:
        # Créer un message d'erreur si trop de requêtes
        error = self.functions.createError(
            "errors.com.epicgames.account.too_many_requests",
            "You have made more than the limited number of requests", 
            [], 18031, "too_many_requests"
        )
        
        # Retourner l'erreur au client
        return app.response_class(
            response=dumps(error),
            status=429,  # Code HTTP approprié pour trop de requêtes
            mimetype='application/json'
        )
    
    # Incrémenter le compteur de requêtes
    self.functions.rps[request.remote_addr] += 1
```

## Services

### OldMP (Backend Principal)
Le service backend principal fonctionne par défaut sur le port 3551. Il est responsable du fonctionnement du jeu, se connecte à une base de données et effectue des requêtes vers une API. Le code source est disponible [ici](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmp.py).

Pour récupérer des informations sur la partie ou le jeu, OldMP utilise la requête `/datarouter/api/v1/public/data`:

```python
@app.route('/datarouter/api/v1/public/data', methods=['POST'])
def datarouterapipublicdata():
    data = request.stream.read()
    events_data = loads(data.decode())['Events']
    
    for events in events_data:
        for event, value in events.items():
            if event == 'PlayerLocation':
                # Récupérer les coordonnées des joueurs pour la carte
                coords = str(value).split(',')
                x, y = int(coords[0]), int(coords[1])
                self.playerscoords.append((x, y))
                
            elif event == 'AthenaPlayersLeft':
                # Connaître le nombre de joueurs restants
                self.session.put('partyPlayerLeft', int(value))
                
            elif event == 'Location':
                # Savoir si le joueur est en jeu
                self.session.put('InGame', value == 'InGame')
            
            elif event == 'AthenaMapName':
                # Récupérer le nom de la carte actuelle
                self.session.put('mapName', value)
            
            elif event == 'EventName' and value == 'SessionEnd':
                # Savoir si l'utilisateur a quitté la partie en 1.8
                self.session.clear()

    return Response(status=204)
```

Le rate limit pour ce service est de `20` requêtes par seconde.

### OldMPWeb (Interface Web)
Le site web d'OldMP fonctionne par défaut sur le port 80. Il fournit une interface web pour les administrateurs et les utilisateurs, ainsi qu'un système de carte affichant les emplacements de tous les joueurs dans la partie, accessible via l'URL `/map`.

Différentes fonctions permettent de récupérer les contenus publics:
- `/content/files/<file>` pour les fichiers JSON
- `/content/images/<file>` pour les images
- Utiliser `listall` à la place de `<file>` pour lister tous les fichiers disponibles

Le rate limit pour ce service est de `5` requêtes par seconde.

Le code source est disponible [ici](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmpweb.py).

### OldMPLauncher (Backend Launcher)
Le backend du launcher fonctionne par défaut sur le port 4971. Il propose:

1. **Système d'authentification** via la requête `/launcher/auth` (nécessite les paramètres `grant_type`, `username`, `password`). Exemple de réponse:
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

2. **Vérification de mise à jour** via `/launcher/versioncheck`

3. **Système RPC** via `/launcher/rpc/` qui retourne des informations sur le joueur:
   - Au lobby:
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
   - En jeu:
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

4. **Système de statut** via `/launcher/status` (retourne `online`, `maintenance` ou `offline`)

5. **Système d'informations** via:
   - `/launcher/content/news` (actualités)
   - `/launcher/content/patchnotes` (notes de mise à jour)
   - `/launcher/content/fnsolo` (informations sur le mode solo)

Le rate limit pour ce service est de `5` requêtes par seconde.

Le code source est disponible [ici](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmplauncher.py).

## Versions compatibles
OldMP prend en charge les versions suivantes de Fortnite:
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

## Optimisations récentes
Les services ont été optimisés pour améliorer les performances:
- Mise en place d'un système de logging avancé
- Implémentation de caching pour les données fréquemment utilisées
- Optimisation du traitement des images dans le module loops
- Amélioration de la gestion des sessions
- Utilisation de structures de données plus efficaces
- Activation du mode threaded dans Flask pour une meilleure concurrence