import game

class Messenger(object):
    """Used to allow objects to communicate with each other."""
    game = None
    gameScreen = None
    menuScreen = None
    creditScreen = None
    score = None

    @staticmethod
    def change_mode(new_mode):
        """Changes game mode, makes me wish we had symbols in Python."""
        if new_mode == "CreditScreen":
            score = "Final Score: %d" % Messenger.gameScreen.score
            Messenger.creditScreen.score_label.text = score
            Messenger.creditScreen.make_score_comment()

        if Messenger.game.mode == Messenger.game.mode_hash["GameScreen"]:
            Messenger.game.mode.end_updates()
            Messenger.game.mode_hash["GameScreen"] = game.GameScreen()

        Messenger.game.mode = Messenger.game.mode_hash[new_mode]
        if new_mode == "GameScreen":
            Messenger.game.mode.start_updates()

    @staticmethod
    def quit():
        Messenger.game.on_close()
