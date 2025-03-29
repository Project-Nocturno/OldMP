import websockets
import hashlib
import json
import asyncio
import logging
from datetime import datetime
import socket
import uuid
import signal
import sys

# Based on https://github.com/Lawin0129/FortMatchmaker by lawin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='matchmaker.log'
)
logger = logging.getLogger('MatchMaker')

class MatchMakerV1:
    """
    Legacy TCP socket-based matchmaker implementation
    """
    def __init__(self, MMP: int=3553):
        self.port = MMP
        self.running = True
        logger.info(f"MatchMakerV1 initialized on port {self.port}")
    
    def handle_signals(self):
        """Set up signal handlers for graceful shutdown"""
        def signal_handler(sig, frame):
            logger.info("Shutdown signal received, closing server...")
            self.running = False
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def main(self):
        """Main server loop for TCP socket-based matchmaker"""
        self.handle_signals()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', self.port))
                s.listen(5)  # Allow up to 5 queued connections
                s.settimeout(1.0)  # Add timeout to allow checking self.running
                
                logger.info(f"MatchMakerV1 listening on port {self.port}")
                
                while self.running:
                    try:
                        conn, addr = s.accept()
                        logger.info(f"New connection from {addr}")
                        
                        with conn:
                            while self.running:
                                try:
                                    data = conn.recv(1024)
                                    if not data:
                                        break
                                    
                                    logger.debug(f"Received data: {data}")
                                    # Process data here if needed
                                    
                                except socket.timeout:
                                    continue
                                except Exception as e:
                                    logger.error(f"Error handling connection: {e}")
                                    break
                    
                    except socket.timeout:
                        continue
                    except Exception as e:
                        logger.error(f"Error accepting connection: {e}")
                        if not self.running:
                            break
        
        except Exception as e:
            logger.error(f"Server error: {e}")
        
        logger.info("MatchMakerV1 server stopped")


class MatchMakerV2:
    """
    WebSocket-based matchmaker implementation with improved handling
    """
    def __init__(self, MMP: int=3553):
        self.port = MMP
        self.active_connections = set()
        self.server = None
        logger.info(f"MatchMakerV2 initialized on port {self.port}")
    
    async def start_server(self):
        """Start the WebSocket server"""
        # Define stop handler for graceful shutdown
        async def stop():
            if self.server:
                self.server.close()
                await self.server.wait_closed()
                logger.info("WebSocket server closed")
        
        # Set up signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            asyncio.get_event_loop().add_signal_handler(
                sig, lambda: asyncio.create_task(stop())
            )
        
        # Start server
        self.server = await websockets.serve(self.on_connection, '0.0.0.0', self.port)
        logger.info(f"MatchMakerV2 listening on port {self.port}")
        
        # Keep the server running
        await asyncio.Future()  # Run forever
    
    def run(self):
        """Run the WebSocket server"""
        try:
            asyncio.run(self.start_server())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
    
    async def on_connection(self, ws, path):
        """Handle new WebSocket connections"""
        client_id = str(uuid.uuid4())
        self.active_connections.add(client_id)
        
        try:
            # Check if it's an XMPP connection (which we don't want to handle)
            if "Sec-WebSocket-Protocol" in ws.request_headers and "xmpp" in ws.request_headers["Sec-WebSocket-Protocol"].lower():
                logger.info(f"Rejected XMPP connection from {ws.remote_address}")
                await ws.close()
                self.active_connections.remove(client_id)
                return
            
            logger.info(f"New WebSocket connection from {ws.remote_address} (ID: {client_id})")
            
            # Generate unique IDs for this session
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            ticket_id = hashlib.md5(f"1{timestamp}{client_id}".encode()).hexdigest()
            match_id = hashlib.md5(f"2{timestamp}{client_id}".encode()).hexdigest()
            session_id = hashlib.md5(f"3{timestamp}{client_id}".encode()).hexdigest()
            
            # Process the matchmaking flow
            await self.send_connecting_status(ws)
            await self.send_waiting_status(ws)
            await self.send_queued_status(ws, ticket_id)
            await self.send_session_assignment(ws, match_id)
            await asyncio.sleep(2)  # Simulate processing time
            await self.send_join(ws, match_id, session_id)
            
            # Handle incoming messages
            async for message in ws:
                try:
                    logger.info(f"Message from {client_id}: {message}")
                    # Process message here if needed
                    
                    # Example: Echo the message back
                    data = json.loads(message)
                    await ws.send(json.dumps({
                        "payload": {
                            "echo": data,
                            "status": "received"
                        },
                        "name": "Echo"
                    }))
                    
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from {client_id}")
                except Exception as e:
                    logger.error(f"Error processing message from {client_id}: {e}")
        
        except Exception as e:
            logger.error(f"Error handling connection {client_id}: {e}")
        
        finally:
            # Clean up when the connection is closed
            if client_id in self.active_connections:
                self.active_connections.remove(client_id)
            logger.info(f"Connection closed for {client_id}")
    
    async def send_connecting_status(self, ws):
        """Send connecting status update"""
        await ws.send(json.dumps({
            "payload": {
                "state": "Connecting"
            },
            "name": "StatusUpdate"
        }))
        logger.debug("Sent 'Connecting' status")
    
    async def send_waiting_status(self, ws):
        """Send waiting status update"""
        await ws.send(json.dumps({
            "payload": {
                "totalPlayers": 1,
                "connectedPlayers": 1,
                "state": "Waiting"
            },
            "name": "StatusUpdate"
        }))
        logger.debug("Sent 'Waiting' status")
    
    async def send_queued_status(self, ws, ticket_id):
        """Send queued status update"""
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
        logger.debug(f"Sent 'Queued' status with ticket ID: {ticket_id}")
    
    async def send_session_assignment(self, ws, match_id):
        """Send session assignment status update"""
        await ws.send(json.dumps({
            "payload": {
                "matchId": match_id,
                "state": "SessionAssignment"
            },
            "name": "StatusUpdate"
        }))
        logger.debug(f"Sent 'SessionAssignment' status with match ID: {match_id}")
    
    async def send_join(self, ws, match_id, session_id):
        """Send join command"""
        await ws.send(json.dumps({
            "payload": {
                "matchId": match_id,
                "sessionId": session_id,
                "joinDelaySec": 1
            },
            "name": "Play"
        }))
        logger.debug(f"Sent 'Play' command with session ID: {session_id}")


# Main execution block
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Fortnite Matchmaker Server')
    parser.add_argument('--version', type=int, choices=[1, 2], default=2,
                        help='Matchmaker version to use (1=TCP Socket, 2=WebSocket)')
    parser.add_argument('--port', type=int, default=3553,
                        help='Port to listen on')
    
    args = parser.parse_args()
    
    try:
        if args.version == 1:
            logger.info(f"Starting MatchMakerV1 on port {args.port}")
            matchmaker = MatchMakerV1(args.port)
            matchmaker.main()
        else:
            logger.info(f"Starting MatchMakerV2 on port {args.port}")
            matchmaker = MatchMakerV2(args.port)
            matchmaker.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)