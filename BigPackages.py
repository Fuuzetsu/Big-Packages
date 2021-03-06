import pyglet
import sys
import os
try: #This will install avbin if needed, and it works on windows and linux!
    pyglet.resource.image("resources/art/background1.png")
except:
    if sys.platform.startswith("win"):
        print "Error: avbin.dll not found."
        quit()
    elif sys.platform.startswith("linux"):
        if sys.maxsize > 2 ** 32:
            if os.system("avbin-linux-x86-64-7/install.sh") != 0:
                print "You must install avbin manually by running the install.sh script in avbin-linux-x86-64-7."
                quit()
        else:
            if os.system("avbin-linux-x86-32-7/install.sh") !=0:
                print "You must install avbin manually by running the install.sh script in avbin-linux-x86-64-7."
                quit()
    elif sys.platform == "dawrwin":
        #Note, osx doesn't work because the avbin devs don't care about it
        #and left it in the dust. Just a small town OS living in a
        #dangerious dog eat world. Lost it all at the gambling games.
        #Working hard to fight the man. Didn't even really have a plan.
        #But hey, man? You gotta work. Work. Work this out. Get ahead.
        #You gotta work. Work. Work this out. Get ahead. Ah yeah!
        raise "Error: This game is not supported on OSX."
        os.system("avbin-darwin-universal-5/install.sh")
import config
import messenger
import menu
import game
import credit
import char
import random


MUSIC = {"JingleBellsA" : pyglet.media.load(r"resources\music\Jingle Bells.mp3"),
         "JingleBellsB" : pyglet.media.load(r"resources\music\Jingle Bells 3.mp3"),
         "OhChristmasTree" : pyglet.media.load(r"resources\music\Oh Xmas.mp3"),
         "UpOnAHouseTop" : pyglet.media.load(r"resources\music\Up on a Housetop.mp3"),
         "WeWishYou" : pyglet.media.load(r"resources\music\We Wish You.mp3"),
         "Grinch1" : pyglet.media.load(r"resources\music\grinch.mp3"),
         "Grinch2" : pyglet.media.load(r"resources\music\02-Grinch.mp3")}
      

class Game(pyglet.window.Window):
    def __init__(self, width, height):
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
        "Creates a music player and loads all the fun christmas music on it."
        self.music_player = pyglet.media.Player()
        #self.music_player.eos_action = "loop" #disabling looping
        music_list = []
        for key in MUSIC:
            item = MUSIC[key]
            music_list.append(item)
        random.shuffle(music_list)
        for song in music_list:
            self.music_player.queue(song)
        self.music_player.play()
        pyglet.clock.schedule_interval(lambda dt : self.music_player.play(), 2.0)
    def on_draw(self):
        self.clear()
        self.mode.on_draw()
        #self.fps_display.draw() #FPS should not be displayed during normal gameplay
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
