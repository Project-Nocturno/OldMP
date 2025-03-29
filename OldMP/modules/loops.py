from PIL import Image
import time
import threading
from io import BytesIO

class Loops():
    def __init__(self, playerscoords: list=[], rps: dict={}):
        self.playerscoords = playerscoords
        self.rps = rps
        self.map_base = None
        self.cursor = None
        self.map_lock = threading.Lock()
        
        # Load images once at initialization
        try:
            self.map_base = Image.open('data/content/images/MiniMapAthena.png').convert("RGBA")
            self.cursor = Image.open('data/content/images/cursor.png').copy()
            self.cursor.thumbnail((40, 40))
            self.cursor = self.cursor.convert("RGBA")
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def makemap(self):
        """Generate the map with player positions"""
        if not self.map_base or not self.cursor:
            print("Map or cursor image not loaded")
            return
            
        while True:
            try:
                with self.map_lock:
                    # Create a copy of the base map for this iteration
                    map_copy = self.map_base.copy()
                    
                    # Add all player cursors
                    for player in self.playerscoords:
                        x_pos = round(player[0] * 0.0079)
                        y_pos = round(player[1] * 0.0079)
                        map_copy.paste(self.cursor, (x_pos, y_pos), self.cursor)
                    
                    # Save the map efficiently
                    buffer = BytesIO()
                    map_copy.save(buffer, format="PNG")
                    
                    with open('data/content/images/ActMiniMapAthena.png', 'wb') as f:
                        f.write(buffer.getvalue())
                    
            except Exception as e:
                print(f"Error in makemap: {e}")
                
            time.sleep(30)
            
    def updaterps(self):
        """Reset request per second counters"""
        while True:
            time.sleep(1)
            # Use a more efficient approach to reset counters
            for key in list(self.rps.keys()):
                self.rps[key] = 0