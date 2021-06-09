
from Utilities.Tools import *

# region info
# All of this classes are static ones. It means that I use them for only their functions and don't create them.

# endregion

class Bishop(object):

    # region Methods
    @staticmethod
    def available_moves(board, row, col, turn = 1, length = 8, is_king = 0):  # return Highlight

        moves = []



        Tools.check_lines(board, row, col, -1, -1, moves, length, turn)
        Tools.check_lines(board, row, col, -1, 1, moves, length, turn)
        Tools.check_lines(board, row, col, 1, -1, moves, length, turn)
        Tools.check_lines(board, row, col, 1, 1, moves, length, turn)
        King.not_in_danger(moves, board, is_king, row, col, 6, turn)

        return moves
    # endregion

class Rook(object):

    # region Methods
    @staticmethod
    def available_moves(board, row, col, turn = 1, length = 8, is_king = 0):  # return Highlight

        moves = []




        Tools.check_lines(board, row, col, 0, -1, moves, length, turn)
        Tools.check_lines(board, row, col, -1, 0, moves, length, turn)
        Tools.check_lines(board, row, col, 1, 0, moves, length, turn)
        Tools.check_lines(board, row, col, 0, 1, moves, length, turn)
        King.not_in_danger(moves, board, is_king, row, col, 6, turn)


        return moves
    # endregion

class Knight(object):

    # region Methods
    @staticmethod
    def available_moves(board, row, col, turn = 1):  # return Highlight

        moves = []

        Tools.check_lines(board, row, col, 2, 1, moves, 2, turn)
        Tools.check_lines(board, row, col, 2, -1, moves, 2, turn)
        Tools.check_lines(board, row, col, 1, 2, moves, 2, turn)
        Tools.check_lines(board, row, col, 1, -2, moves, 2, turn)
        Tools.check_lines(board, row, col, -2, 1, moves, 2, turn)
        Tools.check_lines(board, row, col, -2, -1, moves, 2, turn)
        Tools.check_lines(board, row, col, -1, 2, moves, 2, turn)
        Tools.check_lines(board, row, col, -1, -2, moves, 2, turn)
        King.not_in_danger(moves, board, 0, row, col, 6, turn)

        return moves
    # endregion

class Pawn(object):

    # region Methods
    @ staticmethod
    def available_moves(board, row, col, turn = 1): # return Highlight

        moves = []
        side_decider = 1

        if turn == 1:

            if row == 6: # beginning

                if board[row-1][col] == 0:
                    moves.append([row-1, col])
                    if board[row-2][col] == 0:
                        moves.append([row - 2, col])

            # Regular Moves

            elif row - 1 >= 0 and board[row-1][col] == 0:
                moves.append([row - 1, col])

            # Enemy in the fronts

            if Tools.not_out_of_borders(row - 1, col - 1) and board[row - 1][col - 1] < 0:

                moves.append([row - 1, col - 1])

            if Tools.not_out_of_borders(row - 1, col + 1) and board[row - 1][col + 1] < 0:

                moves.append([row - 1, col + 1])

            King.not_in_danger(moves, board, 0, row, col, 6 ,turn)

        elif turn == 0:

            if row == 1: # beginning

                if board[row+1][col] == 0:
                    moves.append([row+1, col])
                    if board[row+2][col] == 0:
                        moves.append([row + 2, col])

            # Regular Moves

            elif row + 1 <= 7 and board[row+1][col] == 0:
                moves.append([row + 1, col])

            # Enemy in the fronts

            if Tools.not_out_of_borders(row + 1, col + 1) and board[row + 1][col + 1] > 0:

                moves.append([row + 1, col + 1])

            if Tools.not_out_of_borders(row + 1, col - 1) and board[row + 1][col - 1] > 0:

                moves.append([row + 1, col - 1])

            King.not_in_danger(moves, board, 0, row, col, 6, turn)


        return moves
    # endregion

class King(Bishop, Rook):

    # region Methods
    @staticmethod
    def available_moves(board, row, col, turn = 1):  # return Highlight

        moves = []

        moves += Bishop.available_moves(board, row, col, turn, 2, is_king = 1)
        moves += Rook.available_moves(board, row, col, turn, 2, is_king = 1)
        King.not_in_danger(moves, board, 1, row, col, 6, turn)

        return moves

    @staticmethod
    def not_in_danger(moves, board, who_move, row = -1, col = -1, value = 6, turn = 1): # who_move = 1 (The King wants to move), who_move = 0 (Other soldiers are moving)


        if turn == 1:
            if who_move == 1:

                removable_list = []
                temp = board[row][col]
                temp_row = row
                temp_col = col
                board[row][col] = 0

                for i in range(len(moves)):

                    row = moves[i][0]
                    col = moves[i][1]

                    # Check all the enemy soldiers and see if they danger the king


                    if King.Check_all_enemy_soldiers(1, board, row, col):
                        removable_list.append(moves[i])

                for i in removable_list:

                    moves.remove(i)

                board[temp_row][temp_col] = temp
                temp = 0

                return

            elif who_move == 0:

                removable_list = []

                king_row, king_col = King.Find_soldier_place(value, board)
                dummy_board = Tools.create_dummy_board(board)

                for i in range(len(moves)):

                    temp_row = moves[i][0]
                    temp_col = moves[i][1]
                    temp_value = dummy_board[temp_row][temp_col]

                    dummy_board[temp_row][temp_col] = dummy_board[row][col]
                    dummy_board[row][col] = 0

                    if King.Check_all_enemy_soldiers(turn, dummy_board, king_row, king_col):
                        removable_list.append(moves[i])

                    dummy_board[row][col] = dummy_board[temp_row][temp_col]
                    dummy_board[temp_row][temp_col] = temp_value



                for i in removable_list:

                    moves.remove(i)



        elif turn == 0:

            if who_move == 1:

                removable_list = []
                temp = board[row][col]
                temp_row = row
                temp_col = col
                board[row][col] = 0

                for i in range(len(moves)):

                    row = moves[i][0]
                    col = moves[i][1]

                    # Check all the enemy soldiers and see if they danger the king


                    if King.Check_all_enemy_soldiers(0, board, row, col):
                        removable_list.append(moves[i])

                for i in removable_list:
                    moves.remove(i)

                board[temp_row][temp_col] = temp
                temp = 0

                return

            elif who_move == 0:

                removable_list = []

                king_row, king_col = King.Find_soldier_place(-6, board)
                dummy_board = Tools.create_dummy_board(board)

                for i in range(len(moves)):

                    temp_row = moves[i][0]
                    temp_col = moves[i][1]
                    temp_value = dummy_board[temp_row][temp_col]

                    dummy_board[temp_row][temp_col] = dummy_board[row][col]
                    dummy_board[row][col] = 0

                    if King.Check_all_enemy_soldiers(0, dummy_board, king_row, king_col):
                        removable_list.append(moves[i])

                    dummy_board[row][col] = dummy_board[temp_row][temp_col]
                    dummy_board[temp_row][temp_col] = temp_value

                for i in removable_list:
                    moves.remove(i)

    @staticmethod
    def Free_Space(board, row, col, x, y, amount=2, character1 = 1, character2 = -10):

        for i in range(1, amount):

            if Tools.not_out_of_borders(row + x * i, col + y * i):

                if board[row + x * i][col + y * i] == character1 or board[row + x * i][col + y * i] == character2:
                    return False

                if board[row + x * i][col + y * i] != 0:
                    return True
            else:
                return True
        return True

    # region Shortcuts


    # region King is safe
    @staticmethod
    def Check_all_enemy_soldiers(sign, board, row, col):


        if sign == 1:
            return not King.Free_Space(board, row, col, -1, -1, 8, -4, -5) or not King.Free_Space(board, row, col, -1, 1, 8, -4, -5) or not King.Free_Space(board, row, col, 1, -1, 8, -4, -5) or not King.Free_Space(board, row, col, 1, 1, 8, -4, -5) or not King.Free_Space(board, row, col, 1, 0, 8, -2, -5) or not King.Free_Space(board, row, col, -1, 0, 8, -2, -5) or not King.Free_Space(board, row, col, 0, 1, 8, -2, -5) or not King.Free_Space(board, row, col, 0, -1, 8, -2, -5) or not King.Free_Space(board, row, col, 1, 2, 2, -3) or not King.Free_Space(board, row, col, 1, -2, 2, -3) or not King.Free_Space(board, row, col, -1, 2, 2, -3) or not King.Free_Space(board, row, col, -1, -2, 2, -3) or not King.Free_Space(board, row, col, 2, 1, 2, -3) or not King.Free_Space(board, row, col, 2, -1, 2, -3)  or not King.Free_Space(board, row, col, -2, 1, 2, -3)  or not King.Free_Space(board, row, col, -2, -1, 2, -3) or not King.Free_Space(board, row, col, -1, 1, 2, -1) or not King.Free_Space(board, row, col, -1, -1, 2, -1) or King.Check_near_by_king(1, board, row, col) or not King.special_rows(1, board, row, col)
        else:
            return not King.Free_Space(board, row, col, -1, -1, 8, 4, 5) or not King.Free_Space(board, row, col, -1, 1, 8, 4, 5) or not King.Free_Space(board, row, col, 1, -1, 8, 4, 5) or not King.Free_Space(board, row, col, 1, 1, 8, 4, 5) or not King.Free_Space(board, row, col, 1, 0, 8, 2, 5) or not King.Free_Space(board, row, col, -1, 0, 8, 2, 5) or not King.Free_Space(board, row, col, 0, 1, 8, 2, 5) or not King.Free_Space(board, row, col, 0, -1, 8, 2, 5) or not King.Free_Space(board, row, col, 1, 2, 2, 3) or not King.Free_Space(board, row, col, 1, -2, 2, 3) or not King.Free_Space(board, row, col, -1, 2, 2, 3) or not King.Free_Space(board, row, col, -1, -2, 2, 3) or not King.Free_Space(board, row, col, 2, 1, 2, 3) or not King.Free_Space(board, row, col, 2, -1, 2, 3)  or not King.Free_Space(board, row, col, -2, 1, 2, 3)  or not King.Free_Space(board, row, col, -2, -1, 2, 3) or not King.Free_Space(board, row, col, 1, -1, 2, 1) or not King.Free_Space(board, row, col, 1, 1, 2, 1) or King.Check_near_by_king(-1, board, row, col) or not King.special_rows(0, board, row, col)

    @staticmethod
    def Check_near_by_king(sign, board, row, col):

        if sign == 1:

            return not King.Free_Space(board, row, col, -1, -1, 2, -6) or not King.Free_Space(board, row, col, -1, 1, 2, -6) or not King.Free_Space(board, row, col, 1, -1, 2, -6) or not King.Free_Space(board, row, col, 1, 1, 2, -6) or not King.Free_Space(board, row, col, -1, 0, 2, -6) or not King.Free_Space(board, row, col, 1, 0, 2, -6) or not King.Free_Space(board, row, col, 0, -1, 2, -6) or not King.Free_Space(board, row, col, 0, 1, 2, -6)
        else:

            return not King.Free_Space(board, row, col, -1, -1, 2, 6) or not King.Free_Space(board, row, col, -1, 1, 2, 6) or not King.Free_Space(board, row, col, 1, -1, 2, 6) or not King.Free_Space(board, row, col, 1, 1, 2, 6) or not King.Free_Space(board, row, col, -1, 0, 2, 6) or not King.Free_Space(board, row, col, 1, 0, 2, 6) or not King.Free_Space(board, row, col, 0, -1, 2, 6) or not King.Free_Space(board, row, col, 0, 1, 2, 6)

    # check if there is soldiers in the rows where pawns can move two pads
    @staticmethod
    def special_rows(sign, board, row, col):

        if sign == 1 and row == 3 and ((Tools.not_out_of_borders(row - 1, col - 1) and board[row - 1][col -1] == -1) or (Tools.not_out_of_borders(row - 1, col + 1) and board[row - 1][col + 1] == -1)):
            return False
        if sign == 0 and row == 4 and ((Tools.not_out_of_borders(row + 1, col - 1) and board[row + 1][col -1] == -1) or (Tools.not_out_of_borders(row + 1, col + 1) and board[row + 1][col + 1] == -1)):
            return False
        return True


    # endregion

    @staticmethod
    def Find_soldier_place(value, board):

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == value:
                    return i, j

        return -1, -1



    # endregion
    # endregion

class Queen(Bishop, Rook):

    # region Methods
    @staticmethod
    def available_moves(board, row, col, turn = 1):  # return Highlight

        moves = []

        moves += Bishop.available_moves(board, row, col, turn, 8)
        moves += Rook.available_moves(board, row, col, turn, 8)

        return moves
    # endregion
