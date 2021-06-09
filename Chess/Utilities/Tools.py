

# Useful functions class (contains as many generic functions as possible -> used in many classes)
class Tools(object):

    # region Methods
    @staticmethod
    def not_out_of_borders(row, col):
        if row < 8 and row >= 0 and col < 8 and col >= 0:
            return True
        return False

    @ staticmethod
    def check_lines(board, row, col, x, y, moves, amount=2, turn=1):

        for i in range(1, amount):

            if Tools.not_out_of_borders(row + x * i, col + y * i):
                if board[row + x * i][col + y * i] == 0:
                    moves.append([row + x * i, col + y * i])
                elif turn == 1 and board[row + x * i][col + y * i] < 0:
                    moves.append([row + x * i, col + y * i])
                    break
                elif turn == 0 and board[row + x * i][col + y * i] > 0:
                    moves.append([row + x * i, col + y * i])
                    break
                else:
                    break
            else:
                break

    @staticmethod
    def all_soldiers_moves(turn, model, board):

        soldier_places = []
        soldier_moves = []

        # Find all the soldiers on the board and their moves

        # black side
        if turn == 0:

            # Find soldiers

            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] < 0:
                        soldier_places.append([i, j])

            # Find moves

            for i in range(len(soldier_places)):
                temp = model.onaction(soldier_places[i][0], soldier_places[i][1], 0, -1, -1, 0)
                soldier_moves.append(temp)

        # white side
        else:

            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] > 0:
                        soldier_places.append([i, j])

            for i in range(len(soldier_places)):
                temp = model.onaction(soldier_places[i][0], soldier_places[i][1], 0)
                soldier_moves.append(temp)

        return soldier_places, soldier_moves

    @ staticmethod
    def create_dummy_board(board):

        dummy_board = []

        for i in range(len(board)):

            temp_list = []

            for j in range(len(board[i])):
                temp_list.append(board[i][j])

            dummy_board.append(temp_list)

        return dummy_board

    # Print the board
    @staticmethod
    def print_board(board):

        for i in board:

            print(i)

    @staticmethod
    def convert_to_one_dimensional_lists(old_list_places, old_list_moves):

        one_d_list_move = []
        one_d_list_places = []


        for i in range(len(old_list_moves)):

            if type(old_list_moves[i]) == list:
                for j in old_list_moves[i]:

                    one_d_list_move.append(j)
                    one_d_list_places.append(old_list_places[i])

        return one_d_list_places, one_d_list_move

    @staticmethod
    def find_amount_of_soldiers(board):

        sum_soldiers = 0

        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    sum_soldiers += 1

        return sum_soldiers

    @staticmethod
    def reverse_2d_list(input_list):

        # reverese items inside list
        input_list.reverse()

        # reverse each item inside the list using map function(Better than doing loops...)
        input_list = list(map(lambda x: x[::-1], input_list))

        # return
        return input_list
    # endregion