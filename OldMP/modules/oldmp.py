from flask import Flask, request, Response, send_from_directory
from json import loads, dumps
from os import path as ospath, makedirs
from datetime import datetime
import random
from uuid import uuid4
from .routes import register_all_routes
import logging

class OldMP:
    def __init__(self, functions):
        self.functions = functions
        self.session = {}
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='oldmp.log'
        )
        self.logger = logging.getLogger('OldMP')
        
        # Create necessary directories if they don't exist
        if not ospath.exists('data/profiles'):
            makedirs('data/profiles')
            self.logger.info("Created profiles directory")
        if not ospath.exists('data/items'):
            makedirs('data/items')
            self.logger.info("Created items directory")
    
    def set_session(self, session_data):
        """Set the current session data"""
        self.session = session_data
        self.logger.debug(f"Session updated for user: {session_data.get('username', 'unknown')}")
    
    def get_session(self):
        """Get the current session data"""
        return self.session
    
    def run(self, port):
        """Run the Flask application with all routes registered"""
        app = Flask(__name__)
        
        # Disable Flask's default logging
        app.logger.disabled = True
        log = logging.getLogger('werkzeug')
        log.disabled = True
        
        # Register all route handlers from the routes module
        register_all_routes(app, self)
        
        self.logger.info(f"Starting OldMP server on port {port}")
        
        # Start the Flask app
        app.run('0.0.0.0', port, debug=False, threaded=True)