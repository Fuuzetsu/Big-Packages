import pyglet
import screen
import messenger
import button
import config
import text
from utility import load_join_i

# Non-divided sprite_sheet
SPRITE_SHEET_MERGED = load_join_i(["resources", "art", "sprite_sheet.png"]) 

# Divided sprite_sheet
SPRITE_SHEET_DIVIDED = pyglet.image.ImageGrid(SPRITE_SHEET_MERGED, 8, 8) 

IMAGES = {}
IMAGES["background"] = load_join_i(["resources", "art", "background1.png"])
IMAGES["menu_button"] = load_join_i(["resources", "art", "menu_button.png"])
IMAGES["tiber"] = SPRITE_SHEET_DIVIDED[63]
IMAGES["gwen"] = SPRITE_SHEET_DIVIDED[62]

class CharScreen(screen.AbstractScreen):
    def __init__(self):
        messenger.Messenger.charScreen = self
        self.background = IMAGES["background"]
        self.font_size = 30
        self.make_descriptions()
        self.menu_button = button.Button(image = IMAGES["menu_button"],
                                        x = 40,
                                        y = 40)
        self.menu_button.command = lambda : messenger.Messenger.change_mode("MenuScreen")
    def on_draw(self):
        self.background.blit(0,0)
        self.menu_button.draw()
        self.tiber.draw()
        self.tiber_descript.draw()
        self.gwen.draw()
        self.gwen_descript.draw()
    def on_mouse_press(self, x, y, button, modifiers):
        self.menu_button.click(x, y)
    def make_descriptions(self):
        self.tiber = button.Button(image = IMAGES["tiber"],
                                   x = 25,
                                   y = 450)
        self.tiber.scale = 4.0
        self.tiber_descript = text.TextBox(x = 100,
                                           y = 550,
                                           font_name = config.FONT_TYPE,
                                           font_size = self.font_size,
                                           color = (0, 0, 0, 255),
                                           text = """
A greedy elf warrior, in spite
of Tiberius's Christmas spirit
he was doomed to a life of
no presents. Now he returns
for his rightful tribute.""")

        self.gwen = button.Button(image = IMAGES["gwen"],
                                  x = 25,
                                  y = 175)
        self.gwen.scale = 4.0
        self.gwen_descript = text.TextBox(x = 100,
                                          y = 300,
                                          font_name = config.FONT_TYPE,
                                          font_size = self.font_size,
                                          color = (0, 0, 0, 255),
                                          text = """
Gwendayln was once
a promissing young
snowmancer until
she turned rotten
with greed.""")
