import pyglet
import config
import messenger
import random
import screen
from main import list_pj
from pyglet.gl import * #Neccesary to prevent linear scaling

SPRITE_SHEET_MERGED = pyglet.image.load(list_pj(["resources", "art", "sprite_sheet.png"])) #Non-divided sprite_sheet
SPRITE_SHEET_DIVIDED = pyglet.image.ImageGrid(SPRITE_SHEET_MERGED, 8, 8) #Divided sprite_sheet
IMAGES = {} #A hash of all the images in the game with the appropriate names
PLAYER_IMAGES = [SPRITE_SHEET_DIVIDED[63],
                 SPRITE_SHEET_DIVIDED[62]]
PRESENT_IMAGES = [SPRITE_SHEET_DIVIDED[56],
                  SPRITE_SHEET_DIVIDED[57],
                  SPRITE_SHEET_DIVIDED[58]]

SOUNDS = {}
SOUNDS["beep"] = pyglet.media.load(list_pj(["resources", "music", "bell-ring-01.mp3"]), streaming = False)
SOUNDS["end"] = pyglet.media.load(list_pj(["resources", "music", "bell-ringing-01.mp3"]), streaming = False)
SOUNDS["crumple"] = pyglet.media.load(list_pj(["resources", "music", "paper-rustle-8.mp3"]), streaming = False)
BACKGROUND_IMAGES = [pyglet.image.load(list_pj(["resources", "art", "background1.png"])),
                     pyglet.image.load(list_pj(["resources", "art", "background2.png"])),
                     pyglet.image.load(list_pj(["resources", "art", "background3.png"])),
                     pyglet.image.load(list_pj(["resources", "art", "background4.png"]))]

class GameScreen(screen.AbstractScreen):
    "Screen describing the actual game part of the game."
    def __init__(self):
        messenger.Messenger.gameScreen = self
        self.background = random.choice(BACKGROUND_IMAGES)
        self.player = Player()
        self.time_amount = config.START_TIME
        self.time =  self.time_amount
        self.lives = config.START_LIVES
        self.score = config.START_SCORE
        self.keys = set() #A set containg currently held down keys
        self.present_size = config.START_PRESENT_SIZE
        self.present_amount = config.START_PRESENT_AMOUNT
        self.present_worth = config.START_PRESENT_WORTH
        self.presents = [] #total list of current presents
        self.labels = {}
        self.present_batch = pyglet.graphics.Batch()
        self.create_labels()
        self.spawn_presents()
        self.lambdas = [] #keeps a list of functions to schedule and unschedule
    def start_updates(self):
        "Begins scheduling 'GameScreen' updates and saving them for unscheduling."
        lambdas = [(lambda dt : self.collect_present(), 0.05),
                   (lambda dt : self.player.move(dt, self.keys), 0.05),
                   (lambda dt : self.back_to_screen(), 0.01),
                   (lambda dt : self.self_update_labels(), 0.05),
                   (lambda dt : self.update_time(), 1.0)]
        for _lambda in lambdas:
            self.lambdas.append(_lambda)
            pyglet.clock.schedule_interval(_lambda[0], _lambda[1])        
    def end_updates(self):
        "Unschedules all 'GameScreen' updates."
        for _lambda in self.lambdas: pyglet.clock.unschedule(_lambda[0])
    def update_time(self):
        self.time -= 1
        if self.time < 0:
            SOUNDS["end"].play()
            messenger.Messenger.change_mode("CreditScreen")
        elif self.time < 10:
            self.labels["timer"].color = (0, 0, 0, 255)
            pyglet.clock.schedule_once(lambda dt: SOUNDS["beep"].play(), 0.01)
        elif self.time < 5:
            self.labels["timer"].color = (0, 0, 0, 255)
            pyglet.clock.schedule_once(lambda dt: SOUNDS["beep"].play(), 0.01)
            pyglet.clock.schedule_once(lambda dt: SOUNDS["beep"].play(), 0.5)
    def self_update_labels(self):
        self.labels["timer"].text = "%.2f" % self.time
        self.labels["score"].text = "Score: %d" % self.score
    def create_labels(self):
        font_size = 60
        self.labels["score"] = pyglet.text.Label(text = "Score: %d" % self.score,
                                                 font_name = config.FONT_TYPE,
                                                 font_size = font_size,
                                                 y = config.SCREEN_HEIGHT - font_size)
        self.labels["timer"] = pyglet.text.Label(text = "%.2f" % self.time,
                                                 font_name = config.FONT_TYPE,
                                                 font_size = font_size,
                                                 y = config.SCREEN_HEIGHT - font_size * 2)
    def back_to_screen(self):
        if self.player.x + self.player.width > config.SCREEN_WIDTH:
            self.player.x = config.SCREEN_WIDTH - self.player.width
        if self.player.x < 0:
            self.player.x = 0
        if self.player.y + self.player.height > config.SCREEN_HEIGHT:
            self.player.y = config.SCREEN_HEIGHT - self.player.height
        if self.player.y < 0:
            self.player.y = 0
    def on_key_press(self, symbol, modifiers):
        "Adds keys to set of currently held down keys."
        self.keys.add(symbol)
    def on_key_release(self, symbol, modifiers):
        "Removes keys from set of currently held down keys."
        if symbol in self.keys: self.keys.remove(symbol)
    def on_draw(self):
        self.background.blit(0,0)
        self.present_batch.draw()
        for key in self.labels:
            item = self.labels[key]
            item.draw()
        self.player.draw()
    def collect_present(self):
        for present in self.presents[:]:
            if self.player.collide(present):
                SOUNDS["crumple"].play()
                self.increment_score(self.present_worth)
                self.presents.remove(present)
        if not self.presents:
            self.present_size_reduce()
            self.present_amount_increase()
            self.present_worth_increase()
            self.spawn_presents()
    def spawn_presents(self):
        "Spawns presents in batches"
        self.time_amount -= config.TIME_INCREMENT
        self.time = self.time_amount
        self.labels["timer"].color = (255, 255, 255, 255)
        for i in range(self.present_amount):
            self.presents.append(Present(self.present_batch,
                                         self.present_size))
    def present_size_reduce(self):
        "A setter for the size of a present sprite."
        if self.present_size - config.PRESENT_SIZE_INCREMENT < config.MIN_PRESENT_SIZE:
            self.present_size = config.MIN_PRESENT_SIZE
        else:
            self.present_size -= config.PRESENT_SIZE_INCREMENT
    def present_amount_increase(self):
        "A setter for the amount of presents per present spawn."
        self.present_amount += config.PRESENT_AMOUNT_INCREMENT
    def present_worth_increase(self):
        "A setter for pointer per present."
        self.present_worth += config.PRESENT_WORTH_INCREMENT
    def player_speed_boost(self):
        if self.player.speed + config.PLAYER_SPEED_INCREMENT > config.MAX_PLAYER_SPEED:
            self.player.speed = config.MAX_PLAYER_SPEED
        else:
            self.player.speed += config.PLAYER_SPEED_INCREMENT
    def lose_life(self):
        "Handles running out of lives properly, a life setter."
        lives -= 1
        if lives < 0:
            messenger.change_state("credit_screen", score)
    def increment_score(self, points):
        "Handles score increments correctly, a score setter."
        self.score += points

class Collide(object):
    "Class that adds collsion methods."
    def collide(self, other):
        "Checks if one objects collides with another."
        if other.x < self.x + (self.width / 2) < other.x + other.width:
            if other.y < self.y + (self.height / 2) < other.y + other.height:
                return True
        if self.x < other.x + (other.width / 2) < self.x + self.width:
            if self.y < other.y + (other.height / 2) < self.y + self.height:
                return True
        return False
    
class Interpolate(object):
    "Adds methods for tweening."
    def interpolate(self, number, steps, form):
        "Allows for various forms of interpolation."
        if form == "step":
            return [number / steps for i in range(steps)]
        elif form == "accelerate":
            return [number / step for steps in range(1, steps + 1)]

class Player(pyglet.sprite.Sprite, Collide, Interpolate):
    "A player object, can be controlled with input."
    def __init__(self):
        super(Player, self).__init__(random.choice(PLAYER_IMAGES))
        self.x, self.y = config.PLAYER_START
        self.speed = config.PLAYER_START_SPEED
        self.time = 0.5
        self.scale = 2.0
        self.steps = config.PLAYER_STEPS
    def draw(self):
        super(Player, self).draw()
        glEnable(GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    def axis_move(self, dt, axis, amount):
        if axis == "x":
            distance = self.interpolate(amount + amount * dt, self.steps, "step")
            time = self.interpolate(self.time, self.steps, "step")
            both = zip(distance, time)
            for distance, time in both:
                pyglet.clock.schedule_once(lambda dt : self._axis_move("x", distance), time)
        if axis == "y":
            distance = self.interpolate(amount + amount * dt, self.steps, "step")
            time = self.interpolate(self.time, self.steps, "step")
            both = zip(distance, time)
            for distance, time in both:
                pyglet.clock.schedule_once(lambda dt : self._axis_move("y", distance), time)
    def _axis_move(self, axis, pos):
        if axis == "x": self.x += pos
        elif axis == "y": self.y += pos
    def move(self, dt, keys):
        if pyglet.window.key.W in keys:
            self.axis_move(dt, "y", self.speed)
        if pyglet.window.key.S in keys:
            self.axis_move(dt, "y", -1 * self.speed)
        if pyglet.window.key.D in keys:
            self.axis_move(dt, "x", self.speed)
        if pyglet.window.key.A in keys:
            self.axis_move(dt, "x", -1 * self.speed)

class Present(pyglet.sprite.Sprite, Collide):
    "A collectible present object."
    def __init__(self, batch, scale):
        super(Present, self).__init__(random.choice(PRESENT_IMAGES))
        self.scale = scale
        self.x = random.randint(0, config.SCREEN_WIDTH - self.width)
        self.y = random.randint(0, config.SCREEN_HEIGHT - self.height)
        self.batch = batch
    def draw(self):
        super(Player, self).draw()
        glEnable(GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        
    
        
        
