import websockets
import hashlib
import json
import asyncio
from datetime import datetime
import socket

#based on https://github.com/Lawin0129/FortMatchmaker by lawin

class MatchMakerV1():
    def __init__(self, MMP: int=3553):
        self.port=MMP
    
    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(addr)
                while 1:
                    data=conn.recv(1024)
                    if not data:
                        break
                    
                    print(data)

MatchMakerV1().main()

class MatchMakerV2():
    def __init__(self, MMP: int=3553):
        self.server=websockets.serve(self.on_connection, '0.0.0.0', MMP)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def on_connection(self, ws, path):
        if "xmpp" in ws.request_headers["Sec-WebSocket-Protocol"].lower():
            return ws.close()

        ticket_id = hashlib.md5(f"1{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}".encode()).hexdigest()
        match_id = hashlib.md5(f"2{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}".encode()).hexdigest()
        session_id = hashlib.md5(f"3{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}".encode()).hexdigest()

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