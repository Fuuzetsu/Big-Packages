import pyglet
import screen
import button
import messenger
import config
import text

IMAGES = {}
IMAGES["background"] = pyglet.image.load(r"resources/art/background1.png")
IMAGES["menu_button"] = pyglet.image.load(r"resources/art/menu_button.png")

class CreditScreen(screen.AbstractScreen):
    def __init__(self):
        messenger.Messenger.creditScreen = self
        self.font_size = 40
        self.color = (0, 0, 0, 255)
        self.background = IMAGES["background"]
        self.make_buttons()
        self.make_labels()
    def on_draw(self):
        self.background.blit(0, 0)
        self.menu_button.draw()
        self.score_label.draw()
        self.score_comment.draw()
    def make_score_comment(self):
        score = messenger.Messenger.gameScreen.score
        if score == 0:
            _text = """
This is the only easter egg
in the game, you truly
understand the Christmas spirit.
THANKS FOR PLAYING!"""
        elif score < 500:
            _text = """
Did you even try? At this rate
you'll never get that white
iPhone!"""
        elif score < 2000:
            _text = """
A decent amount of kids won't
be getting parents this year,
you bastard."""
        elif score < 5000:
            _text = """
You have a fair portion of
toys, but even with so many
childhood dreams ruined...
You really have not made an
impact on a global scale."""
        elif messenger.Messenger.score < 6000:
            _text = """
You're colder than Jack Frost.
Thanks for ruining Christmas,
asshole."""
        elif messenger.Messenger.score < 7000:
            _text = """
There. Are. No. Presents. Left."""
        elif messenger.Messenger.score < 8000:
            _text = """
If you cheat you get put on
the naughty list. You know
that, right?"""
        else:
            _text = """
Stop. Messing. With. The.
Config. File. You. Asshat."""

        self.score_comment = text.TextBox(font_name = config.FONT_TYPE,
                                          font_size = self.font_size,
                                          text = _text,
                                          color = self.color,
                                          x = 25,
                                          y = config.SCREEN_HEIGHT - 50)
    def on_mouse_press(self, x, y, button, modifiers):
        self.menu_button.click(x, y)
    def make_labels(self):
        self.score_label = pyglet.text.Label(text = "Final Score: %d" % 0,
                                             font_name = config.FONT_TYPE,
                                             font_size = self.font_size,
                                             x = config.SCREEN_WIDTH / 4,
                                             y = config.SCREEN_HEIGHT / 2,
                                             color = self.color)
        self.score_label.x -= 175 #Hard coded offset
        self.score_comment = text.TextBox(font_name = config.FONT_TYPE,
                                          font_size = self.font_size,
                                          text = "If this text appears the developer is retarded.",
                                          color = self.color,
                                          x = config.SCREEN_WIDTH / 4,
                                          y = config.SCREEN_HEIGHT / 4 * 2)
    def make_buttons(self):
        self.menu_button = button.Button(image = IMAGES["menu_button"],
                                          x = config.SCREEN_WIDTH / 4,
                                          y = config.SCREEN_HEIGHT / 4)
        self.menu_button.x -= self.menu_button.width / 2
        self.menu_button.y -= self.menu_button.height / 2
        self.menu_button.command = lambda : messenger.Messenger.change_mode("MenuScreen")
