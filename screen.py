class AbstractScreen(object):
    "An abstract class for values in the 'Game' 'mode_hash' member."
    def on_draw(self):
        pass
    def on_key_press(self, symbol, modifiers):
        pass
    def on_key_release(self, symbol, modifiers):
        pass
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    def on_mouse_press(self, x, y, button, modifiers):
        pass
    def on_mouse_release(self, x, y, button, modifiers):
        pass
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
