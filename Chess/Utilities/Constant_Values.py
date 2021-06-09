class ConstantValues(object):

    def __init__(self):

        self.PAGE_COLOR = "Black"
        self.BOARD_COLOR_1 = "silver"
        self.BOARD_COLOR_2 = "DodgerBlue2"

        self.MOVEABLE_LABEL_COLORS = "red"
        self.ACTIVE_POSITION_COLOR = "orange"

        self.AMOUNT_OF_TESTS_TO_PLAY = 10

        self.DELAY_MODIFIER = 0.1 # seconds

        self.RANDOMNEES_POSSIBILITY = 50 # 1 / number for random move

        # Soldier identities

        self.WHITE_PAWN = 1
        self.WHITE_ROCK = 2
        self.WHITE_KNIGHT = 3
        self.WHITE_BISHOP = 4
        self.WHITE_QUEEN = 5
        self.WHITE_KING = 6

        self.BLACK_PAWN = -1
        self.BLACK_ROCK = -2
        self.BLACK_KNIGHT = -3
        self.BLACK_BISHOP = -4
        self.BLACK_QUEEN = -5
        self.BLACK_KING = -6

C_V = ConstantValues()






