import pyglet

class TextBox(object):
    def __init__(self, x, y, font_name, font_size, text, color):
        self.x = x
        self.y = y
        self.font_name = font_name
        self.font_size = font_size
        self.text = text
        self.color = color
        self.labels = []
        for num, line in enumerate(self.text.splitlines()):
            self.labels.append(pyglet.text.Label(text = line,
                                                 font_name = self.font_name,
                                                 font_size = self.font_size,
                                                 color = self.color,
                                                 x = self.x,
                                                 y = self.y - num * self.font_size + 10)
)
    def draw(self):
        for label in self.labels: label.draw()
