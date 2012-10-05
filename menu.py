import pyglet
import screen
import button
import config
import messenger
from utility import load_join_i

import os.path
load_join_i = lambda l: pyglet.image.load(reduce(os.path.join, l)) 

IMAGES = dict(zip(["title_screen", "start_button", 
                   "quit_button", "char_button"],
                  map(load_join_i, [["resources", "art", "title_screen.png"],
                                    ["resources", "art", "start_button.png"],
                                    ["resources", "art", "quit_button.png"],
                                    ["resources", "art", "char_button.png"]])))

class MenuScreen(screen.AbstractScreen):
    def __init__(self):
        self.color = (0, 0, 0, 255)
        self.make_buttons()
        self.background = IMAGES["title_screen"]

    def on_draw(self):
        self.background.blit(0,0)
        self.start_button.draw()
        self.char_button.draw()
        self.quit_button.draw()

    def make_buttons(self):
        msngr = messenger.Messenger
        self.start_button = button.Button(image = IMAGES["start_button"],
                                          x = config.SCREEN_WIDTH / 2,
                                          y = config.SCREEN_HEIGHT / 2)
        self.start_button.x -= self.start_button.width / 2
        self.start_button.y -= self.start_button.height / 2
        self.start_button.command = lambda : msngr.change_mode("GameScreen")

        self.char_button = button.Button(image = IMAGES["char_button"],
                                         x = config.SCREEN_WIDTH / 2,
                                         y = config.SCREEN_HEIGHT / 2)
        self.char_button.x -= self.char_button.width / 2
        self.char_button.y -= self.char_button.height * 2
        self.char_button.command = lambda : msngr.change_mode("CharScreen")
        self.quit_button = button.Button(image = IMAGES["quit_button"],
                                          x = config.SCREEN_WIDTH / 2,
                                          y = config.SCREEN_HEIGHT / 2)
        self.quit_button.x -= self.quit_button.width / 2
        self.quit_button.y -= self.quit_button.height * 3.5
        self.quit_button.command = lambda : msngr.quit()

    def on_mouse_press(self, x, y, button, modifiers):
        self.start_button.click(x, y)
        self.char_button.click(x, y)
        self.quit_button.click(x, y)
