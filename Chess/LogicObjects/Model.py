# Include the data structure of each item
from LogicObjects.Soldiers import *
from LogicObjects.Computer import *
from Utilities.Tools import *

class Model(object):

    # region Constructer
    def __init__(self):

        # region info
        """
            This class allows to start the menu and work with it

            :param board: the game board in list of lists format
            :type board: list (list)
            :param self.active_row: the active row we use
            :type self.active_row: int
            :param self.active_col: the active col we use
            :type self.active_col: int
            :param self.soldier_dict: dictionary containing the moves of each type
            :type self.soldier_dict: dict

            :return: Nothing
            :rtype: None
        """

        # endregion

        self.board = ""
        self.active_row = ""
        self.active_col = ""

        self.restart_game()

        self.soldier_dict = self.create_dictionary()
    # endregion

    # region Methods

    def onaction(self, row, col, move, active_row = -1, active_col =-1, turn = 1):

        # region info
        """
            This function make changes based on the parameters which are given. It is used when event happened. The function being called from the controller
            # Manage the changes in the logic level

            :param row: row we check now
            :type row: int
            :param col: col we check now
            :type col: int
            :param move: allows to know if to call the replacer function or not
            :type move: int
            :param active_row: the active row we have
            :type active_row: int
            :param active_col: the active col we have
            :type active_col: int
            :param turn: the turn of the player
            :type turn: int

            :return: Nothing
            :rtype: None
        """

        # endregion

        if move == 1:

            self.replacer(row, col)


        moves = []

        # Update the old place for the new place
        self.active_row = row
        self.active_col = col



        value = self.board[self.active_row][self.active_col]

        # All the Illegal movements (Clicked on a empty place) (Will just do nothing) (clicked on a soldier not in the correct turn)
        if self.get_index_value(row, col) == 0 or (turn == 1 and value < 0) or (turn == 0 and value > 0):
            return True

        value = abs(value)

        # All Moves

        # First player (White)
        if turn == 1:

            # returns a function
            function_type = self.soldier_dict.get(value)
            # return all the valid movements based on the returned function
            moves = function_type(self.board, self.active_row, self.active_col)


        # Enemy moves (Black)
        elif turn == 0:

            # same as in the first if but for the second player
            function_type = self.soldier_dict.get(value)
            moves = function_type(self.board, self.active_row, self.active_col, 0)



        return moves

    def restart_game(self):

        # region info
        """
            This function restart the default values. Therefore, it is used when we restart and when we first create the class
            # Restart the game in the logic level

            :return: Nothing
            :rtype: None
        """

        # endregion

        self.board = [[C_V.BLACK_ROCK ,C_V.BLACK_KNIGHT ,C_V.BLACK_BISHOP ,C_V.BLACK_QUEEN ,C_V.BLACK_KING ,C_V.BLACK_BISHOP ,C_V.BLACK_KNIGHT ,C_V.BLACK_ROCK],
                      [C_V.BLACK_PAWN, C_V.BLACK_PAWN, C_V.BLACK_PAWN, C_V.BLACK_PAWN, C_V.BLACK_PAWN, C_V.BLACK_PAWN, C_V.BLACK_PAWN, C_V.BLACK_PAWN],
                      [0  ,0  ,0  ,0  ,0  ,0  ,0 , 0],
                      [0  ,0  ,0  ,0  ,0  ,0  ,0 , 0],
                      [0  ,0  ,0  ,0  ,0  ,0  ,0 , 0],
                      [0  ,0  ,0  ,0  ,0  ,0  ,0 , 0],
                      [C_V.WHITE_PAWN  ,C_V.WHITE_PAWN  ,C_V.WHITE_PAWN  ,C_V.WHITE_PAWN  ,C_V.WHITE_PAWN  ,C_V.WHITE_PAWN  ,C_V.WHITE_PAWN , C_V.WHITE_PAWN],
                      [C_V.WHITE_ROCK  ,C_V.WHITE_KNIGHT  ,C_V.WHITE_BISHOP  ,C_V.WHITE_QUEEN  ,C_V.WHITE_KING  ,C_V.WHITE_BISHOP  ,C_V.WHITE_KNIGHT , C_V.WHITE_ROCK],]

        self.active_row = -1
        self.active_col = -1

    def check_mate(self, turn):

        # region info
        """
            This function checks for checkmate case

            :param places: list containing the places we can move from
            :type places: list
            :param moves: list containing the places we can move to (the moves)
            :type moves: list

            :return: False / True
            :rtype: bool
        """

        # endregion

        places, moves = Tools.all_soldiers_moves(turn, self, self.board)

        # if there are only empty lists in the moves variable it means there is a check mate
        for i in range(len(moves)):
            if moves[i] != []:
                return False

        return True

    def get_index_value(self, row, col):
        return self.board[row][col]

    def create_dictionary(self):

        # region info
        """

            # Create dictionary containing functions (The moves of each type of soldier)

            :return: False / True
            :rtype: bool
        """

        # endregion

        soldier_dict = \
        {
            1: Pawn.available_moves,
            2: Rook.available_moves,
            3: Knight.available_moves,
            4: Bishop.available_moves,
            5: Queen.available_moves,
            6: King.available_moves
        }

        return soldier_dict

    def replacer(self, row , col):

        # region info
        """

            # replace the new rows and new cols with the old rows and old cols (active row / col)
            # Replace the value in a place

            :return: False / True
            :rtype: bool
        """

        # endregion

        self.board[row][col] = self.board[self.active_row][self.active_col]
        self.board[self.active_row][self.active_col] = 0

    def get_board(self):
        return self.board

    def create_soldiers(self):

        # region info
        """

            # returns the soldiers which have to be created in other classes, synchronized with locations. being used in the ViewBoard class
            # Based on the board structure


            :return: False / True
            :rtype: bool
        """

        # endregion

        soldier_array = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    soldier_array.append([i, j, self.board[i][j]])

        return soldier_array

    # endregion