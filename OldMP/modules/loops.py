from PIL import Image
import time

class Loops():
    def __init__(self, palyerscoords: list):
        self.palyerscoords=palyerscoords
    
    def makemap(self):
        while 1:
            img=Image.open('data/content/images/MiniMapAthena.png')
            #cursorImg.resize(40, 40)
            for player in self.palyerscoords:
                cursor=Image.open('data/content/images/cursor.png').copy()
                img.paste(cursor)
            img.save('data/content/images/ActMiniMapAthena.png')
            time.sleep(30)