from .banner_routes import register_banner_routes
from .counter_routes import register_counter_routes
from .quest_routes import register_quest_routes
from .purchase_routes import register_purchase_routes
from .profile_routes import register_profile_routes
from .generic_profile_handler import register_generic_profile_handler
import time
import logging

logger = logging.getLogger('Routes')

def register_all_routes(app, oldmp):
    """Register all route handlers with the Flask app"""
    start_time = time.time()
    
    # Register all route modules
    register_banner_routes(app, oldmp)
    register_counter_routes(app, oldmp)
    register_quest_routes(app, oldmp)
    register_purchase_routes(app, oldmp)
    register_profile_routes(app, oldmp)
    
    # Register the generic handler last so it doesn't override specific handlers
    register_generic_profile_handler(app, oldmp)
    
    elapsed_time = time.time() - start_time
    logger.info(f"All routes registered in {elapsed_time:.2f} seconds")