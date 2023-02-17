from PIL import Image
import time

class Loops():
    def __init__(self, playerscoords: list=[], rps: dict={}):
        self.playerscoords=playerscoords
        self.rps=rps
    
    def makemap(self):
        while 1:
            map=Image.open('data/content/images/MiniMapAthena.png')
            
            for player in self.playerscoords:
                cursor=Image.open('data/content/images/cursor.png').copy()
                cursor.thumbnail((40, 40))
                map=map.convert("RGBA")
                cursor=cursor.convert("RGBA")
                map.paste(cursor, (player[0]/2, player[1]/2), cursor)
            
            map.save('data/content/images/ActMiniMapAthena.png', format="png")
            time.sleep(30)
            
    def updaterps(self):
        while 1:
            time.sleep(1)
            for key in self.rps:
                self.rps[key]=0