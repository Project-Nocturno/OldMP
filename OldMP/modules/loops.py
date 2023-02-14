from PIL import Image
import time

class Loops():
    def __init__(self, palyerscoords: list):
        self.palyerscoords=palyerscoords
    
    def makemap(self):
        while 1:
            map=Image.open('data/content/images/MiniMapAthena.png')
            
            for player in [(200, 500), (1532, 862)]:
                cursor=Image.open('data/content/images/cursor.png').copy()
                cursor.thumbnail((40, 40))
                map=map.convert("RGBA")
                cursor=cursor.convert("RGBA")
                map.paste(cursor, player, cursor)
            
            map.save('data/content/images/ActMiniMapAthena.png', format="png")
            time.sleep(30)