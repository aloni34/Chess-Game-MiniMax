from LogicObjects.Model import *

# Include the control panell which connects the logical structure to the view structure
class Controller(object):

    # region Constructer
    def __init__(self, view_board):

        self.view_board = view_board
        self.model = Model()
        self.computer = Computer(self.model)

    # endregion

    # region Methods
    def onaction(self, row, col, move = 1, active_row = -1, active_col = -1, turn = 1):

        # return the valid places we can move on the board
        return self.model.onaction(row, col, move, active_row, active_col, turn)

    # The player pressed already a player and didnt move him or disabled him.
    def update_movement(self, row, col):

        self.model.replacer(row, col)

    # checks if there is a checkmate for the current player
    def check_mate(self, turn):
        return self.model.check_mate(turn)

    def restart_game(self):
        self.model.restart_game()

    def create_soldiers(self):
        return self.model.create_soldiers()

    def play_ai(self, update_depth_for_turn = False):
        return self.computer.play_ai(update_depth_for_turn)

    def play_test_player(self, turn):
        return self.computer.play_test_player(turn)

    def default_state(self):
        self.computer.default_state()

    def get_model(self):
        return self.model

    def get_computer(self):
        return self.computer

    # endregion
