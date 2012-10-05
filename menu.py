import pyglet
import screen
import button
import config
import messenger

IMAGES = {}
IMAGES["title_screen"] = pyglet.image.load(r"resources/art/title_screen.png")
IMAGES["start_button"] = pyglet.image.load(r"resources/art/start_button.png")
IMAGES["quit_button"] = pyglet.image.load(r"resources/art/quit_button.png")
IMAGES["char_button"] = pyglet.image.load(r"resources/art/char_button.png")

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
        self.start_button = button.Button(image = IMAGES["start_button"],
                                          x = config.SCREEN_WIDTH / 2,
                                          y = config.SCREEN_HEIGHT / 2)
        self.start_button.x -= self.start_button.width / 2
        self.start_button.y -= self.start_button.height / 2
        self.start_button.command = lambda : messenger.Messenger.change_mode("GameScreen")

        self.char_button = button.Button(image = IMAGES["char_button"],
                                         x = config.SCREEN_WIDTH / 2,
                                         y = config.SCREEN_HEIGHT / 2)
        self.char_button.x -= self.char_button.width / 2
        self.char_button.y -= self.char_button.height * 2
        self.char_button.command = lambda : messenger.Messenger.change_mode("CharScreen")
        self.quit_button = button.Button(image = IMAGES["quit_button"],
                                          x = config.SCREEN_WIDTH / 2,
                                          y = config.SCREEN_HEIGHT / 2)
        self.quit_button.x -= self.quit_button.width / 2
        self.quit_button.y -= self.quit_button.height * 3.5
        self.quit_button.command = lambda : messenger.Messenger.quit()
    def on_mouse_press(self, x, y, button, modifiers):
        self.start_button.click(x, y)
        self.char_button.click(x, y)
        self.quit_button.click(x, y)
