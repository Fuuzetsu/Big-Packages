import pyglet
import sys
import os
import config
import messenger
import menu
import game
import credit
import char
import random
import os.path

# Joins a list of paths into a single path (OS independent)
list_pj = lambda l: reduce(os.path.join, l) 

# Composition of join and load
load_join_i = lambda l: pyglet.image.load(reduce(os.path.join(l)))
load_join_m = lambda l: pyglet.media.load(reduce(os.path.join(l)))

def resourceInit():
    try: #This will install avbin if needed, and it works on windows and linux!
        load_join_i(["resources", "art", "background1.png"])
    except:
        if sys.platform.startswith("win"):
            print "Error: avbin.dll not found."
            quit()
        elif sys.platform.startswith("linux"):
            path32 = list_pj(["avbin-linux-x86-32-7", "install.sh"])
            path64 = list_pj(["avbin-linux-x86-64-7", "install.sh"])
            if sys.maxsize > 2 ** 32:
                if os.system(path32) != 0:
                    print "You must install avbin manually by running" + \
                    " the install.sh script in avbin-linux-x86-64-7."
                    quit()
            else:
                if os.system(path64) != 0:
                    print "You must install avbin manually by running" + \
                    " the install.sh script in avbin-linux-x86-64-7."
                    quit()
        elif sys.platform == "darwin":
            raise "Error: This game is not supported on OSX."


class Game(pyglet.window.Window):
    def __init__(self, width, height):
        self.MUSIC = { 
            "JingleBellsA"    : ["resources", "music", "Jingle Bells.mp3"],
            "JingleBellsB"    : ["resources", "music", "Jingle Bells 3.mp3"],
            "OhChristmasTree" : ["resources", "music", "Oh Xmas.mp3"],
            "UpOnAHouseTop"   : ["resources", "music", "Up on a Housetop.mp3"],
            "WeWishYou"       : ["resources", "music", "We Wish You.mp3"],
            "Grinch1"         : ["resources", "music", "grinch.mp3"]
            # Grinch2 refuses to load, comment out for now
            # "Grinch2"         : ["resources", "music", "02-Grinch.mp3)"]
            }
        
        for k, v in self.MUSIC.iteritems(): 
            self.MUSIC[k] = pyglet.media.load(list_pj(v))

        messenger.Messenger.game = self
        self.create_music_player()
        self.fps_display = pyglet.clock.ClockDisplay()
        pyglet.clock.set_fps_limit(90)
        super(Game, self).__init__(width,
                                   height,
                                   vsync = False,
                                   caption = "Big Packages")
        self.mode_hash = {}
        self.mode_hash["MenuScreen"] = menu.MenuScreen()
        self.mode_hash["GameScreen"] = game.GameScreen()
        self.mode_hash["CreditScreen"] = credit.CreditScreen()
        self.mode_hash["CharScreen"] = char.CharScreen()
        #TESTING PURPOSES
        self.mode = self.mode_hash["MenuScreen"]
        #self.mode = self.mode_hash["GameScreen"]
        #TESTING PURPOSES

    def create_music_player(self):
        """Creates a music player and loads all the fun christmas music."""
        self.music_player = pyglet.media.Player()
        #self.music_player.eos_action = "loop" #disabling looping

        music_list = []
        for song in self.MUSIC.values():
            music_list.append(song)

        random.shuffle(music_list)
        for song in music_list:
            self.music_player.queue(song)

        self.music_player.play()
        pyglet.clock.schedule_interval(lambda _: self.music_player.play(), 2.0)

    def on_draw(self):
        self.clear()
        self.mode.on_draw()
        #self.fps_display.draw() # Hide FPS during regular play

    def on_key_press(self, symbol, modifiers):
        self.mode.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.mode.on_key_release(symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mode.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mode.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.mode.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mode.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_close(self):
        self.music_player.pause()
        self.music_player = None
        super(Game, self).on_close()


if __name__ == "__main__":
    root = Game(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    pyglet.app.run()
