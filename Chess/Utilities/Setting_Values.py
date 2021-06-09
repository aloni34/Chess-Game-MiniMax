class SettingValues(object):

    def __init__(self):

        self.HEIGHT = 1080
        self.WIDTH = 1920

        self.PLAYER_TURN = 1 # 1 white starts, 0 black starts
        self.PLAY_AGAINSET_AI_BLACK = True
        self.PLAY_AGAINSET_AI_WHITE = False

        self.AI_VS_AI = False
        self.AI_DEPTH = 3

S_T = SettingValues()