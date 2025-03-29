# OldMP (S1-S8)

[French Version](#README_FR.md)

## Introduction
OldMP is a set of services including a lobby emulator for Fortnite (backend server), a web interface, and a backend service for a launcher. This project supports Fortnite versions from Season 1 to Season 8.

## Configuration
The parameters that can be modified during runtime are found in the [conf.json](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/conf.json) file. The main parameters for the different services are defined in [main.py](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/main.py). The OldMP services are located in the [modules](https://github.com/Project-Nocturno/OldMP/tree/main/OldMP/modules) folder.

## Security
The different backend services have a rate limiting system to prevent brute force or DDoS attacks. Here's an example of the optimized implementation:

```python
@app.before_request
def checkrps():
    # Check if the IP is already registered
    if request.remote_addr not in self.functions.rps:
        self.functions.rps[request.remote_addr] = 0
    
    # Check if the number of requests per second exceeds the limit
    if self.functions.rps[request.remote_addr] >= config['rps']['service']:
        # Create an error message if too many requests
        error = self.functions.createError(
            "errors.com.epicgames.account.too_many_requests",
            "You have made more than the limited number of requests", 
            [], 18031, "too_many_requests"
        )
        
        # Return the error to the client
        return app.response_class(
            response=dumps(error),
            status=429,  # Appropriate HTTP code for too many requests
            mimetype='application/json'
        )
    
    # Increment the request counter
    self.functions.rps[request.remote_addr] += 1
```

## Services

### OldMP (Main Backend)
The main backend service runs by default on port 3551. It is responsible for the game's operation, connects to a database, and makes requests to an API. The source code is available [here](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmp.py).

To retrieve information about the game or match, OldMP uses the `/datarouter/api/v1/public/data` request:

```python
@app.route('/datarouter/api/v1/public/data', methods=['POST'])
def datarouterapipublicdata():
    data = request.stream.read()
    events_data = loads(data.decode())['Events']
    
    for events in events_data:
        for event, value in events.items():
            if event == 'PlayerLocation':
                # Get player coordinates for the map
                coords = str(value).split(',')
                x, y = int(coords[0]), int(coords[1])
                self.playerscoords.append((x, y))
                
            elif event == 'AthenaPlayersLeft':
                # Get the number of remaining players
                self.session.put('partyPlayerLeft', int(value))
                
            elif event == 'Location':
                # Check if the player is in-game
                self.session.put('InGame', value == 'InGame')
            
            elif event == 'AthenaMapName':
                # Get the current map name
                self.session.put('mapName', value)
            
            elif event == 'EventName' and value == 'SessionEnd':
                # Check if the user left the game in 1.8
                self.session.clear()

    return Response(status=204)
```

The rate limit for this service is `20` requests per second.

### OldMPWeb (Web Interface)
The OldMP website runs by default on port 80. It provides a web interface for administrators and users, as well as a map system displaying the locations of all players in the game, accessible via the `/map` URL.

Different functions allow retrieving public content:
- `/content/files/<file>` for JSON files
- `/content/images/<file>` for images
- Use `listall` instead of `<file>` to list all available files

The rate limit for this service is `5` requests per second.

The source code is available [here](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmpweb.py).

### OldMPLauncher (Launcher Backend)
The launcher backend runs by default on port 4971. It offers:

1. **Authentication system** via the `/launcher/auth` request (requires the parameters `grant_type`, `username`, `password`). Example response:
```json
{
    "accountId": "<account_id>",
    "display_name": "<display_name>",
    "device_id": "<device_id>",
    "session_id": "<session_id>",
    "expire_in": 14400,
    "expire_at": "<expiration_date_in_4h>"
}
```

2. **Update verification** via `/launcher/versioncheck`

3. **RPC system** via `/launcher/rpc/` which returns information about the player:
   - In the lobby:
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
   - In-game:
   ```json
   {
       "username": "<username>",
       "character": "<skin>",
       "party": {
           "mapName": "<map_name>",
           "playerLeft": "<number_of_remaining_players>"
       }
   }
   ```

4. **Status system** via `/launcher/status` (returns `online`, `maintenance`, or `offline`)

5. **Information system** via:
   - `/launcher/content/news` (news)
   - `/launcher/content/patchnotes` (update notes)
   - `/launcher/content/fnsolo` (information about solo mode)

The rate limit for this service is `5` requests per second.

The source code is available [here](https://github.com/Project-Nocturno/OldMP/blob/main/OldMP/modules/oldmplauncher.py).

## Compatible Versions
OldMP supports the following Fortnite versions:
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

## Recent Optimizations
The services have been optimized to improve performance:
- Implementation of an advanced logging system
- Caching for frequently used data
- Optimization of image processing in the loops module
- Improved session management
- Use of more efficient data structures
- Enabling threaded mode in Flask for better concurrency