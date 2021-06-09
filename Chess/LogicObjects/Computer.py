from Utilities.Tools import *
from Utilities.Stack import *
from Utilities.Constant_Values import *
from Utilities.Setting_Values import *
import random

class Computer(object):

    # region Constructer
    def __init__(self, model):

        # region info
        """
            This Class responsible for the computer gameplay.
            It has connection to a smart player (Nega Max) and test player

            :param self.model: the connection to the model class.
            :type self.model: Model
            :param self.ai: class which is about the smart moves of the computer (Nega Max)
            :type self.ai: AI
            :param self.test_player: class which is about to test different moves based on the logic I want the computer to follow
            :type self.test_player: TestPlayer



            :return: Nothing
            :rtype: None
        """
        # endregion

        self.model = model
        self.ai = AI(self.model)
        self.test_player = TestPlayer(self.model, self.ai)

    # endregion

    # region Methods

    def play_ai(self, update_depth_for_turn=False):

        # region info
        """
            This function responsible for calling the ai to play and return moves.

            :param self.update_depth_for_turn: a variable which helps to understand which turn the computer play
            :type self.update_depth_for_turn: bool
            :param self.move_from: list of indexes to where to move from (row, col)
            :type self.move_from: list
            :param self.move_to: list of indexes to where to move to (row, col)
            :type self.move_to: list



            :return: moves (from point a to point b)
            :rtype: list, list
        """
        # endregion

        move_from, move_to = self.ai.play_ai(update_depth_for_turn)
        return move_from, move_to

    def play_test_player(self, turn):

        # region info
        """
            This function responsible for calling the test player to play and return moves.

            :param turn: allows to udnerstand which color to return moves for
            :type turn: bool
            :param self.move_from: list of indexes to where to move from (row, col)
            :type self.move_from: list
            :param self.move_to: list of indexes to where to move to (row, col)
            :type self.move_to: list



            :return: moves (from point a to point b)
            :rtype: list, list
        """
        # endregion

        move_from, move_to = self.test_player.play_test_player(turn)
        return move_from, move_to

    def default_state(self):
        self.ai.default_state()
    # endregion

class AI(object):

    # region Constructer
    def __init__(self, model):

        # region info
        """
            This Class responsible for the the smart (Nega Max) gameplay of the computer.

            :param self.model: the connection to the model class.
            :type self.model: Model
            :param self.board: allow to work with the same board as in the model
            :type self.board: list (of lists)
            :param self.location_nikud_dict: dictionary which helps to give score for each move (based on location on the board)
            :type self.location_nikud_dict: dict
            :param self.piece_nikud_dict: dictionary which helps to give score for each move (based on the soldier on the board)
            :type self.piece_nikud_dict: dict
            :param self.stack: helps to save moves which were made and undo them, so bascially nothing have happened. I use this since the changes are being made on the original board
            :type self.stack: Stack
            :param self.no_repeating_moves: mechanism which allows to prevent infinte loop ove moves, due to the NegaMax. Since the computer wants to do the best move and if play against himself there is a chance he will get stuck in a loop of best moves
            :type self.no_repeating_moves: list
            :param self.no_repeat_list_length: determine the amount of moves to save since the last one
            :type self.no_repeat_list_length: int
            :param self.no_repeat_list_length: a variables which helps to determine which color to use the NegaMax for. Since I dont use turn over here, it helps to make it happen. (switches from 1 to -1, or in another words from min to max)
            :type self.no_repeat_list_length: int


            :return: Nothing
            :rtype: None
        """
        # endregion

        self.model = model
        self.board = self.model.get_board()
        self.location_nikud_dict = self.create_location_dictionary()
        self.piece_nikud_dict = self.create_piece_dictionary()
        # for the ai checks inside the negmax tree
        self.stack = Stack()

        # against infinite loop and used only only when the pc is against himself
        self.no_repeating_moves = []
        self.default_state()
        self.no_repeat_list_length = 13

        self.total_checks = 0
        self.optimiser = self.set_optimiser()
    # endregion

    # region Play the computer turn
    def play_ai(self, update_depth_for_turn=False):

        # region info
        """
            This function is the layer before the NegaMax. This class makes sure everything is correct before we call the NegaMax.
            Since the model makes changs in the board, I have to update the refernce to the same board, therfore, I does it (1).
            Afterwards I sums the amount of checks in roots of the NegaMax (2). Then I use the ai_depth variable for the depth of the ai to
            check. I does it becuase the AI knows which color to check for based on the setting depth % 2. Mathematically it works so I
            use this like that (3). Later, if I have to make changes to for setting depth, I does it from the reason above and undo the change when the check was made (4) (5).
            Between I set the optimizer for the check in the NegaMax (6) and later call the NegaMax and make the checks (7). After, I return the moves (from point A to point B)

            :param self.update_depth_for_turn: allows to distinguish if to check for the black or white best option.
            :type self.update_depth_for_turn: bool
            :param self.total_checks: variable which helped to check the amout of times the AI went in the bottom of the NegaMax root
            :type self.total_checks: int
            :param ai_depth: variable which helps with the amount of checks in the ai
            :type ai_depth: int



            :return: Nothing
            :rtype: None
        """
        # endregion


        # (1)
        # update refence each time (if I wont do this the refence to main board is gone)
        self.board = self.model.get_board()
        # (2)
        self.total_checks = 0

        # (3)
        ai_depth = S_T.AI_DEPTH

        # (4)
        # have to make a change for the optimizer and constant depth for this to work on both sides
        if update_depth_for_turn:
            S_T.AI_DEPTH = S_T.AI_DEPTH + 1

        # (6)
        self.optimiser = self.set_optimiser()

        # (7)
        move_from, move_to = self.nega_max_root(ai_depth)

        # (5)
        if update_depth_for_turn:
            S_T.AI_DEPTH = S_T.AI_DEPTH - 1

        return move_from, move_to


    # Play based on the mini max root logic
    def nega_max_root(self, depth):

        # region info
        """
            This function is the head of the NegaMax tree. Therefore, in this function we do more things than the normal NegaMax.
            I begin by bringing all the available soldiers and their moves (1). Later, I set few default states for variables which will help me later on (2).
            After that, I use two mechanismes to prevent infinte best moves loops. Both of them work only when it is on AI vs AI mode. The first one is the one which checks for not repeating moves in the
            last amount of moves I chose to remember (3). If the mechanism found the same move again and there is not atleast one new move which is not remembered, then we go in.
            if the amount of players is less than 5, I chose to call it a draw (4). if there are more than 5, then it get a random move (5). Note that I dont return the best or third best moves,
            since they can lead as well to infinte loop quite often, therfore, I chose to use random move. It happens quite rare so it doesn't really effect anything.

            later I move to the second mechanism which works only in computer against computer mode. This mechanism make a random move one in 1 / RANDOMNEES_POSSIBILITY. I does it to make more
            complex games and not repeat the same game in every interval. It prevents more determinism and makes new situations we never saw before (6).

            If both of this mechanismes didn't work, then we actually move to the NegaMax (7). The NegaMax works as it should. Note, that becuase we work on the same board as the origin one, I save in
            a stack the moves which were made to undo them and make no changes however in the game.

            After all the checks if it was computer VS computer mode, I remove the oldest move in the repeating sequence and load the new one (8).
            After all of this I return the best move (point A to point B).


            :param depth: the depth the ai has to check
            :type depth: int
            :param new_game_places: saves all the available places
            :type new_game_places: list (of lists)
            :param new_game_moves: saves all the available moves
            :type new_game_moves: list (of lists)
            :param best_move: helps to check what is the best move (starts in a high number so new moves can be found easily)
            :type best_move: int
            :param best_move_place: saves the location for the soldier with the best move found (The location to move from)
            :type best_move_place: list
            :param best_move_found: saves the best move which was found (The location where to move to)
            :type best_move_found: list



            :return: from point A to point B
            :rtype: list, list
        """
        # endregion

        # (1)
        new_game_places, new_game_moves = Tools.all_soldiers_moves(S_T.AI_DEPTH - depth, self.model, self.board)
        new_game_places, new_game_moves = Tools.convert_to_one_dimensional_lists(new_game_places, new_game_moves)

        # (2)
        best_move = -9999
        best_move_found = []
        best_move_place = -1

        # if there are no new moves which lead to the other situation this will make it a draw (In the case there are only 4 pieces left make it draw and if there are more make random move)
        # (3)
        if S_T.AI_VS_AI and not self.check_draw_state(new_game_moves):

            # (4)
            if Tools.find_amount_of_soldiers(self.board) < 5 or new_game_places == []:
                return [], []
            # (5)
            else:
                if len(new_game_moves) > 1:
                    random_index = int(random.randint(0, len(new_game_moves) - 1))
                else:
                    random_index = 0
                return new_game_places[random_index], new_game_moves[random_index]
        # make a small chance 1 / RANDOMNEES_POSSIBILITY to make random move. I do this to make the game more random and not determinst
        # (6)
        elif S_T.AI_VS_AI and int(random.randint(0, C_V.RANDOMNEES_POSSIBILITY)) == 1:
            random_value = int(random.randint(0, len(new_game_moves) - 1))
            return new_game_places[random_value], new_game_moves[random_value]

        # start the nega max (if it is in the case of (the RANDOMNEES_POSSIBILITY - 1) / RANDOMNEES_POSSIBILITY)
        # (7)
        for i in range(len(new_game_moves)):

            new_game_move = new_game_moves[i]

            if new_game_move != []:

                self.ugly_move(new_game_places[i], new_game_move)
                value = -self.nega_max(depth - 1, -10000, 10000)
                self.undo()

                if value >= best_move and (not S_T.AI_VS_AI or self.check_it_is_not_exist(value, new_game_move)):
                    best_move = value
                    best_move_found = new_game_move
                    best_move_place = new_game_places[i]

        # (8)
        if S_T.AI_VS_AI:
            self.remove_oldest_state_and_update()
            self.save_state(best_move, best_move_found)

        return best_move_place, best_move_found

    # Play based on the mini max root logic
    def nega_max(self, depth, alpha, beta):

        # region info
        """
            Basically the same as the NegaMax part in the NegaMax root, only with check if it is in the bottom of the tree.
            If it is, it checks the value and return it.



            :return: the value of the game due to the move after checks in a certin level.
            :rtype: int
        """
        # endregion

        if depth == 0:
            self.total_checks += 1
            return self.optimiser * self.evaluate_board()

        new_game_places, new_game_moves = Tools.all_soldiers_moves((S_T.AI_DEPTH - depth) % 2, self.model, self.board)
        new_game_places, new_game_moves = Tools.convert_to_one_dimensional_lists(new_game_places, new_game_moves)

        best_move = -9999

        for i in range(len(new_game_moves)):

            if new_game_moves[i] != []:

                self.ugly_move(new_game_places[i], new_game_moves[i])
                best_move = max(best_move, -self.nega_max(depth - 1, -beta, -alpha))

                self.undo()

                alpha = max(alpha, best_move)

                if beta <= alpha:
                    return best_move

        return best_move

    # endregion

    # region Methods

    def ugly_move(self, place, move):

        # region info
        """
            loads the latest move (from where to where and the values in both locations)
            # Creates the ugly move for the minimax A I and saves the changes in a stack object


            :return: Nothing
            :rtype: None
        """
        # endregion

        # Saves the move in a stack object so we can undo the move
        place_x = place[0]
        place_y = place[1]

        move_x = move[0]
        move_y = move[1]

        new_move = [[place_x, place_y, self.board[place_x][place_y]], [move_x, move_y, self.board[move_x][move_y]]]
        self.stack.push(new_move)

        # make the move

        self.board[move_x][move_y] = self.board[place_x][place_y]
        self.board[place_x][place_y] = 0

    def undo(self):

        # region info
        """
            Unloads the latest move (from where to where and the values in both locations)
            # Undo the last move saved in the stack


            :return: Nothing
            :rtype: None
        """
        # endregion

        old_move = self.stack.pop()

        move_active = old_move[0]
        move_static = old_move[1]

        self.board[move_active[0]][move_active[1]] = move_active[2]
        self.board[move_static[0]][move_static[1]] = move_static[2]

    def check_it_is_not_exist(self, value, move):

        # region info
        """
            # Save move and check it didnt happen twice, for no duplicate moves


            :return: Nothing
            :rtype: None
        """
        # endregion

        for i in range(self.no_repeat_list_length):

            if self.no_repeating_moves[i][0] == value and self.no_repeating_moves[i][1][0] == move[0] and \
                    self.no_repeating_moves[i][1][1] == move[1]:
                return False
        return True

    # region no duplicate moves

    def default_state(self):

        # region info
        """
            # restart the duplicate list


            :return: Nothing
            :rtype: None
        """
        # endregion

        self.no_repeating_moves = [[0, [0, 0]], [0, [0, 0]], [0, [0, 0]], [0, [0, 0]], [0, [0, 0]], [0, [0, 0]],
                                   [0, [0, 0]], [0, [0, 0]], [0, [0, 0]], [0, [0, 0]], [0, [0, 0]], [0, [0, 0]],
                                   [0, [0, 0]]]

    def save_state(self, value, move):

        # region info
        """
            # function which saves the state of the game (The last move)


            :return: Nothing
            :rtype: None
        """
        # endregion

        self.no_repeating_moves[self.no_repeat_list_length - 1] = [value, move]

    def remove_oldest_state_and_update(self):

        # region info
        """
            # removes the oldest move and store the last move in


            :return: Nothing
            :rtype: None
        """
        # endregion

        for i in range(self.no_repeat_list_length - 1):
            self.no_repeating_moves[i] = self.no_repeating_moves[i + 1]

    def check_draw_state(self, new_game_moves):

        # region info
        """
            # In the case of a draw these function will find it based on the way i told it to


            :return: False / True
            :rtype: bool
        """
        # endregion

        new_move_can_be_made = False
        for i in range(len(new_game_moves)):

            new_move_can_be_made = True

            for j in range(len(self.no_repeating_moves)):

                if new_game_moves[i][0] == self.no_repeating_moves[j][1][0] and new_game_moves[i][1] == \
                        self.no_repeating_moves[j][1][1]:
                    new_move_can_be_made = False
                    break

            if new_move_can_be_made:
                return True

        return False

    # endregion

    def evaluate_board(self):

        # region info
        """
            # return the value of the entire board


            :return: value of the state of the board
            :rtype: int
        """
        # endregion

        total_evaluation = 0
        for i in range(8):
            for j in range(8):
                total_evaluation = total_evaluation + self.get_piece_value(self.board[i][j], i, j)

        return total_evaluation

    def get_piece_value(self, value, x, y):

        # region info
        """
            # return the value of each piece


            :return: value of the piece (by his type + location)
            :rtype: int
        """
        # endregion

        if value == 0:
            return 0

        # black
        if value < 0:
            return -(self.piece_nikud_dict.get(abs(value)) + self.location_nikud_dict.get(value)[y][x])

        # white
        else:
            return self.piece_nikud_dict.get(abs(value)) + self.location_nikud_dict.get(value)[y][x]

    def create_location_dictionary(self):

        # region info
        """
            # Logical arrays which help to point the reward of each move (by location on the board)


            :return: Nothing
            :rtype: None
        """
        # endregion

        temp = 0

        # 1
        pawnEvalWhite = \
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ]


        # -1

        pawnEvalBlack = Tools.reverse_2d_list(pawnEvalWhite)


        # 2 / -2
        knightEval = \
            [
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
            ]

        # 3
        bishopEvalWhite = \
            [
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
            ]

        # -3


        bishopEvalBlack = Tools.reverse_2d_list(bishopEvalWhite)

        # 4
        rookEvalWhite = \
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
            ]

        # -4

        rookEvalBlack = Tools.reverse_2d_list(rookEvalWhite)

        # 5 / -5
        evalQueen = \
            [
                [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
            ]

        # 6
        kingEvalWhite = \
            [
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
            ]

        # -6

        kingEvalBlack = Tools.reverse_2d_list(kingEvalWhite)

        nikud_dict = \
            {
                1: pawnEvalWhite,
                2: rookEvalWhite,
                3: knightEval,
                4: bishopEvalWhite,
                5: evalQueen,
                6: kingEvalWhite,

                -1: pawnEvalBlack,
                -2: rookEvalBlack,
                -3: knightEval,
                -4: bishopEvalBlack,
                -5: evalQueen,
                -6: kingEvalBlack

            }

        '''
        1: pawnEvalWhite,
                2: knightEval,
                3: bishopEvalWhite,
                4: rookEvalWhite,
                5: evalQueen,
                6: kingEvalWhite,

                -1: pawnEvalBlack,
                -2: knightEval,
                -3: bishopEvalBlack,
                -4: rookEvalBlack,
                -5: evalQueen,
                -6: kingEvalBlack
        '''

        return nikud_dict

        # endregion

    def create_piece_dictionary(self):

        # region info
        """
            # create a dictionary for the pieces points (base on the soldier type)


            :return: Nothing
            :rtype: None
        """
        # endregion

        nikud_dict = \
            {
                1: 10,
                2: 50,
                3: 30,
                4: 30,
                5: 90,
                6: 900

            }

        return nikud_dict

    def set_optimiser(self):

        # region info
        """
                # define the value to be 1 or -1 to change from negative and positive values for the evaluted boards in the NegaMax AI becuase when there are even
                # depth returns on even the -value of the board we dont want, so we have to modify the value. if it is not even it returns + value, like I need


            :return: value of the state of the board
            :rtype: int
        """
        # endregion

        if S_T.AI_DEPTH % 2 == 0:
            return -1
        else:
            return 1
    # endregion

# class which is responsibles for the test player (can be smart AI with nega max brain or just random move, whatever I choose to test and find)
class TestPlayer(object):

    # region Constructer
    def __init__(self, model, ai):

        # region info
        """
            This Class is pretty simple.
            It has connection to a smart player (Nega Max) and the model.
            The purpose of this class is to test different type of computer players.
            Can be smart (NegaMax brain or random one). I chose in this case it will be
            stupid (random).

            :param self.model: the connection to the model class.
            :type self.model: Model
            :param self.ai: class which is about the smart moves of the computer (Nega Max)
            :type self.ai: AI




            :return: Nothing
            :rtype: None
        """
        # endregion

        self.model = model
        self.ai = ai

    # endregion

    # region Methods

    # make the test player make his move based on what logic I want it to do (In this case random move)
    def play_test_player(self, turn):

        new_game_places, new_game_moves = Tools.all_soldiers_moves(turn, self.model, self.model.get_board())
        new_game_places, new_game_moves = Tools.convert_to_one_dimensional_lists(new_game_places, new_game_moves)

        if new_game_places != []:

            if len(new_game_moves) > 0:
                random_index = int(random.randint(0, (len(new_game_moves)-1)))
            else:
                random_index = 0

            return new_game_places[random_index], new_game_moves[random_index]

        return [], []

    # endregion