import pyglet
import config

IMAGES = {}

class Button(pyglet.sprite.Sprite):
    "A sprite that reacts when clicked."
    def __init__(self, image, x, y, text = None):
        super(Button, self).__init__(image)
        #The following text part needs work.
##        if text:
##            self.text = pyglet.text.label(text)
        self.x = x
        self.y = y
        self.command = lambda : None
    def click(self, x, y):
        if self.x < x < self.x + self.width:
            if self.y < y < self.y + self.height:
                self.command()
    
    
