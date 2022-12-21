import websockets
import hashlib
import json
import asyncio
from datetime import datetime

async def on_connection(ws, path):
    if "xmpp" in ws.request_headers["Sec-WebSocket-Protocol"].lower():
        return ws.close()

    # create hashes
    ticket_id = hashlib.md5(f"1{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}".encode()).hexdigest()
    match_id = hashlib.md5(f"2{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}".encode()).hexdigest()
    session_id = hashlib.md5(f"3{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}".encode()).hexdigest()

    # you can use asyncio.sleep to send the websocket messages at certain times
    await connecting()
    await waiting()
    await queued()
    await session_assignment()
    await asyncio.sleep(2)
    await join()

    async def connecting():
        await ws.send(json.dumps({
            "payload": {
                "state": "Connecting"
            },
            "name": "StatusUpdate"
        }))

    async def waiting():
        await ws.send(json.dumps({
            "payload": {
                "totalPlayers": 1,
                "connectedPlayers": 1,
                "state": "Waiting"
            },
            "name": "StatusUpdate"
        }))

    async def queued():
        await ws.send(json.dumps({
            "payload": {
                "ticketId": ticket_id,
                "queuedPlayers": 0,
                "estimatedWaitSec": 0,
                "status": {},
                "state": "Queued"
            },
            "name": "StatusUpdate"
        }))

    async def session_assignment():
        await ws.send(json.dumps({
            "payload": {
                "matchId": match_id,
                "state": "SessionAssignment"
            },
            "name": "StatusUpdate"
        }))

    async def join():
        await ws.send(json.dumps({
            "payload": {
                "matchId": match_id,
                "sessionId": session_id,
                "joinDelaySec": 1
            },
            "name": "Play"
        }))

    async for message in ws:
        print(f"A client sent a message: {message}")

# Start listening websocket on port
port = 80
server = websockets.serve(on_connection, "localhost", port)
print(f"Matchmaker started listening on port {port}")

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()