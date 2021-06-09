from LogicObjects.Controls import *
from ViewObjects.Image_Collection import *
from ViewObjects.View_Turn import *
from Utilities.Constant_Values import *

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
import time

class ViewBoard(object):

    # region Constructer
    def __init__(self, root, image_collection, view_turn, view_game_play):

        # region info
        """
            This class is responsible to make the connections for the controller, the events and
            the graphical changes on the board and to tell the other graphical classes to make changes

            :param self.root: the root to the main tkinter page
            :type self.root: TK
            :param self.image_storage: connection for the image class
            :type self.image_storage: ImageCollection
            :param self.view_turn: connection for the view turn class
            :type self.view_turn: ViewTurn
            :param self.view_game_play: connection for the view gameplay class
            :type self.view_game_play: ViewGamePlay
            :param self.controller: connection for the controller class
            :type self.controller: Controller

            :param self.turn: integers which helps to distinguish the player turn
            :type self.turn: int
            :param self.list_of_labels_board: list of labels which create the board
            :type self.list_of_labels_board: list (labels)

            :param self.pressed_flag: responsible to know if the player chose soldier
            :type self.pressed_flag: bool
            :param self.is_to_continue_flag_on_loop: responsible to know if to continue on the loop of the game (if the computers needs to make a move or no)
            :type self.is_to_continue_flag_on_loop: bool
            :param self.is_game_over: responsible to know if we made a checkmate
            :type self.is_game_over: bool

            :param self.active_row: responsible to know the row the player pressed before
            :type self.active_row: int
            :param self.active_col: responsible to know the col the player pressed before
            :type self.active_col: int
            :param self.active_highlight: responsible to know which labels to highlight
            :type self.active_highlight: list

            :return: Nothing
            :rtype: None
        """
        # endregion

        # region Frame
        # Frame of the board
        self.s1 = Style()
        self.s1.configure('My.TFrame', anchor= CENTER, background = C_V.PAGE_COLOR)
        self.center_frame = ttk.Frame(root)
        self.center_frame.config(style='My.TFrame')
        self.center_frame.place(relx = 0.075, rely = 0.1, relwidth = 0.5667, relheight = 0.85)
        self.center_frame.config(padding=(30, 15))
        # endregion

        # region items
        # Label list
        self.list_of_labels_board = self.board_creator()

        # Image Storage
        self.image_storage = image_collection.get_image_list()


        # Create All the soldiers
        # endregion


        # region refernces

        self.controller = Controller(self)
        self.view_turn = view_turn
        self.view_game_play = view_game_play


        # endregion

        # region other variables
        # Turn of the players
        self.turn = S_T.PLAYER_TURN

        # Flags
        # State in the game (Nothing happened for False, chose soldier for True)
        self.pressed_flag = False
        self.is_to_continue_flag_on_loop = True
        self.is_game_over = False

        self.active_row = -1
        self.active_col = -1
        self.active_highlight = []
        self.root = root

        # endregion

        self.soldier_creator()
        self.view_game_play.reset_button.config(command = self.restart_game)
        self.view_game_play.test_button.config(command = self.start_test)
        self.start_automatically()



    # endregion

    # region Events
    def onaction(self, event):

        # region info
        """
            this function responsible for the gameplay on the board. On the case of an event from the player it starts.
            it identify what label he pressed and from there on calls the function which plays in a loop the gameplay until the next event or end

            :param event: a button to make tests for the game
            :type event: Tk (button)

            :param row: the row the player pressed
            :type row: int
            :param col: the col the player pressed
            :type col: int


            :return: Nothing
            :rtype: None
        """
        # endregion

        row, col = self.get_label_location(event)

        self.is_to_continue_flag_on_loop = True

        self.loop_turn_games(row, col)




    def play_turn_one(self, row, col):

        # region info
        """
            this function responsible for the gameplay when: white (start) = player and later black (end) = computer, or when white (start) = computer.
            the function starts by checking if white is the computer (1), if so it call the functions which makes the changes. Afterwards if it was white computer in the start
            it checks if black is computer aswell, if so it updates the flag to continue the loop of gameplay (2). If it was not white computer in the start then it checks if
            black is a player and if he pressed some valid label, if so it makes highlights (3). If the same player press again on a valid label from the valid highlighted moves then it makes
            the changes (4). if he didn't make a valid move then nothing happens. if pressed on the same label again it disables the highlight and give him the option to chose other soldiers (5).
            In the case he made a move then it checks if the black is computer, if so the computer makes a move and then we go back to the function since it is the white player turn (6).
            if black is a player, then he makes the valid changes and goes for the other function (play_turn_two) by ending the function (7).

            - Note that all the variables are class variables, so no need to tell what they do since they are begin described in the constructor.
            - For the play_turn_two function, the same happens but in reverse, I mean the same but for this:

                black (start) = player and later white (end) = computer, or when black (start) = computer.

            :return: Nothing
            :rtype: None
        """
        # endregion

        # (1)
        if S_T.PLAY_AGAINSET_AI_WHITE:

            self.duplicate_lines_two(0)

            # (2)
            if S_T.PLAY_AGAINSET_AI_BLACK:

                self.is_to_continue_flag_on_loop = True

        # (3)
        else:

            if not self.pressed_flag and Tools.not_out_of_borders(row, col):

                self.active_highlight = self.controller.onaction(row, col, 0)

                # if the type is bool it means that this is not valid place and no changes will be made
                if type(self.active_highlight) != bool:
                    self.update_on_new_action(row, col)


                self.is_to_continue_flag_on_loop = False

            # (4)
            else:

                # Not the same place
                if self.active_row != row or self.active_col != col:

                    # check if the pressed label is in the valid labels to move. False = means we check all the valid places we can move, True = cant move
                    if not self.in_high_light_labels(self.active_highlight, row, col):

                        self.is_to_continue_flag_on_loop = False
                        self.duplicate_lines_one(row, col, 0)
                        self.turn = 0


                        # (6)
                        if S_T.PLAY_AGAINSET_AI_BLACK:
                            if not self.duplicate_lines_two(1) and S_T.PLAY_AGAINSET_AI_WHITE:
                                self.is_to_continue_flag_on_loop = True

                        # (7)
                        else:
                            self.turn = 0


                # same place
                # (5)
                else:
                    self.reset_state()
                if not S_T.PLAY_AGAINSET_AI_WHITE:

                    self.is_to_continue_flag_on_loop = False

    def play_turn_two(self, row ,col):
        # region info
        """
            Same as play_turn_one function but for:

                black (start) = player and later white (end) = computer, or when black (start) = computer.

            :return: Nothing
            :rtype: None
        """
        # endregion

        if S_T.PLAY_AGAINSET_AI_BLACK:

            self.duplicate_lines_two(1)
            if S_T.PLAY_AGAINSET_AI_WHITE:
                self.is_to_continue_flag_on_loop = True


        else:
            if not self.pressed_flag:

                self.active_highlight = self.controller.onaction(row, col, 0, -1, -1, self.turn)

                if type(self.active_highlight) != bool:
                    self.update_on_new_action(row, col)


                self.is_to_continue_flag_on_loop = False

            else:

                if self.active_row != row or self.active_col != col:

                    if not self.in_high_light_labels(self.active_highlight, row, col):

                        self.is_to_continue_flag_on_loop = False
                        self.turn = 1
                        self.duplicate_lines_one(row, col, 1)
                        self.view_turn.update_turn(0)

                            # if AI mode is on you will play against the computer so no need to switch turns
                        if S_T.PLAY_AGAINSET_AI_WHITE:
                            if not self.duplicate_lines_two(0) and S_T.PLAY_AGAINSET_AI_BLACK:
                                self.is_to_continue_flag_on_loop = True

                        else:
                            self.turn = 1

                else:
                    self.reset_state()
                if not S_T.PLAY_AGAINSET_AI_BLACK:
                    self.is_to_continue_flag_on_loop = False

    def loop_turn_games(self, row, col):

        # region info
        """
            this function responsible for the loop of gameplay. I use loop to avoid recoursion and in the case of computer moves and where he plays against himself, this loop will allow to do it.
            As far as the flag of continue looping is true, the loop will keep going.


            :return: Nothing
            :rtype: None
        """
        # endregion

        self.is_to_continue_flag_on_loop = True

        while self.is_to_continue_flag_on_loop and not self.is_game_over:

            # First Player
            if self.turn == 1:
                self.play_turn_one(row, col)

            # Second Player
            if self.turn == 0 and self.is_to_continue_flag_on_loop and not self.is_game_over:
                self.play_turn_two(row, col)

    # endregion

    # region Shorcuts
    def case_computer_black(self, move_from, move_to):

        # region info
        """
            this function responsible for more graphical-logical level changes + allowing the model-logical changes through the controller
            # Starts by giving calling the controller to makes changes and retrive what to highlight or to update (based on the type). After
            it, it makes the changes, based on the type of returned value.

            In the case of list being returned, then changes happen. If it is bool, then we make no changes

            - Same happen for case_computer_black with different parameters

            :param self.active_highlight: a list which contains the indexes of what to highlight or if to makes changes
            :type self.active_highlight: list / bool

            :return: Nothing
            :rtype: None
        """
        # endregion

        self.active_highlight = self.controller.onaction(move_from[0], move_from[1], 0, -1, -1, 0)

        if type(self.active_highlight) != bool:
            self.update_on_new_action(move_from[0], move_from[1])
            self.turn = 0
            self.controller.update_movement(move_to[0], move_to[1])

            time.sleep(C_V.DELAY_MODIFIER)
            self.update_movement(move_to[0], move_to[1])
            self.root.update()
            self.reset_state()
            time.sleep(C_V.DELAY_MODIFIER)
            self.turn = 1

    def case_computer_white(self, move_from, move_to):

        # region info
        """

            Same as case_computer_black with some different parameters

            :return: Nothing
            :rtype: None
        """
        # endregion

        self.active_highlight = self.controller.onaction(move_from[0], move_from[1], 0)

        if type(self.active_highlight) != bool:
            self.update_on_new_action(move_from[0], move_from[1])
            self.turn = 1
            self.controller.update_movement(move_to[0], move_to[1])

            time.sleep(C_V.DELAY_MODIFIER)
            self.update_movement(move_to[0], move_to[1])
            self.root.update()
            self.reset_state()
            # Adding delay
            time.sleep(C_V.DELAY_MODIFIER)
            self.turn = 0

    def duplicate_lines_one(self, row, col, turn):

        # region info
        """
            this function responsible for more graphical-logical level changes + allowing the model-logical changes through the controller
            # Starts by making model changes and graphical ones, as well as reset the state to default. Afterward, it checks if there is a checkmate.
            # Works for both colors

            In the case of list being returned, then changes happen. If it is bool, then we make no changes

            - Same happen for case_computer_black with different parameters

            :param self.active_highlight: a list which contains the indexes of what to highlight or if to makes changes
            :type self.active_highlight: list / bool

            :return: False / True
            :rtype: bool
        """
        # endregion

        self.controller.update_movement(row, col)
        self.update_movement(row, col)
        self.reset_state()

        if self.is_in_check_mate(turn):
            self.is_game_over = True
            self.print_who_won(turn)

    def duplicate_lines_two(self, turn):

        # region info
        """
            this function responsible for calling the computer to play. after the computer made changes in the model-logical level,
            I make changes in the graphical level. After it made or didn't made a change, it checks for checkmate or draw. In the case of
            check mate or draw return True, else False

            # move_from and move_to are like before just to know to move from point A to point B.

            :return: False / True
            :rtype: bool
        """
        # endregion

        # update items before A I, becuase while it runs the main loop it doesnt update the delight (turn off highlight) as needed so we need to tell it to update
        self.root.update()

        # return the chosen move

        if turn == 0 and S_T.PLAY_AGAINSET_AI_WHITE:
            move_from, move_to = self.controller.play_ai(True)
        else:
            move_from, move_to = self.controller.play_ai()


        # Update movement
        if not (move_from == [] and move_to == []):

            self.make_update_base_on_player(move_from, move_to, turn)

        if self.is_in_check_mate(turn):

            self.is_game_over = True
            self.print_who_won(turn)
            return True

        elif self.is_draw(move_from, move_to):

            self.is_game_over = True
            print("Draw")
            return True

        return False

    # endregion

    # region Methods


    # function which play games where the computer plays against himself. I chose to play stupid computer against smart one and to see the results. It can be different if I want to change it
    def start_test(self):

        # region info
        """
            this function responsible for testing the computer base on the way I told it.
            In this case:
                # smart player and dumb player are fixed (black = dumb, white = smart). Note that by changing who starts and how deep the AI in the settings the test will follow

            sums the wins of the black, the white and the draws. Runs the loop until we finished the amount of tests requireds. In this case
            after one of the values from the 3 reached the amounts of tests required.

            :param sum_wins_black: amount of times black won
            :type sum_wins_black: int
            :param sum_wins_white: amount of times white won
            :type sum_wins_white: int
            :param sum_draws: amount of times black won
            :type sum_draws: int
            :param was_a_restart: checks if a restart was made and to shortage each interval in the loop
            :type was_a_restart: bool

            :return: Nothing
            :rtype: None
        """
        # endregion



        sum_wins_black = 0
        sum_wins_white = 0
        sum_draws = 0
        was_a_restart = False

        # restarts to default state to begin the tests
        self.restart_game(False)

        # Play games until we reach the cap limit I chose to put
        while C_V.AMOUNT_OF_TESTS_TO_PLAY > (max(sum_wins_black, max(sum_wins_white, sum_draws))):

            was_a_restart = False

            # region smart computer
            self.root.update()
            move_from, move_to = self.controller.play_ai(True)

            # starts as the smart computer and make changes according to the state
            # draw state in the first if
            if move_from == [] and move_to == []:
                sum_draws += 1
                self.restart_game()
                was_a_restart = True
            else:
                # update movement
                if self.turn  == 0:
                    self.case_computer_black(move_from, move_to)
                    # if black made a checkmate
                    if self.controller.check_mate(1):
                        sum_wins_black += 1
                        self.restart_game()
                        was_a_restart = True
                else:
                    # if white made a checkmate
                    self.case_computer_white(move_from, move_to)
                    if self.controller.check_mate(0):
                        sum_wins_white += 1
                        self.restart_game()
                        was_a_restart = True

            self.root.update()
            # endregion

            # important to disable if no need to get into this part of the loop (In the case where there was a restart for a new game)
            if not was_a_restart:

                # repeat the same logic with some small changes to the stupid computer
            # region stupid computer
                move_from, move_to = self.controller.play_test_player(self.turn)
                if move_from == [] and move_to == []:
                    sum_draws += 1
                    self.restart_game()

                else:
                    # Update movement
                    if self.turn  == 0:
                        self.case_computer_black(move_from, move_to)
                        if self.controller.check_mate(1):
                            sum_wins_black += 1
                            self.restart_game()

                    else:
                        self.case_computer_white(move_from, move_to)
                        if self.controller.check_mate(0):
                            sum_wins_white += 1
                            self.restart_game()
                # endregion


        # results of the tests

        print("Black: " + str(sum_wins_black))
        print("White: " + str(sum_wins_white))
        print("Draw: " + str(sum_draws))

    def is_draw(self, move_from, move_to):

        # region info
        """
            this function responsible for checking if it is draw state. In this case empty lists are the sign for draw

            :return: False / True
            :rtype: bool
        """
        # endregion

        if move_from == [] and move_to == []:
            return True
        return False

    def is_in_check_mate(self, turn):

        # region info
        """
            this function responsible to check if there is a checkmate and make a few graphical changes

            :return: False / True
            :rtype: bool
        """
        # endregion

        if self.controller.check_mate(turn):
            self.view_turn.update_check()
            return True

        return False

    def print_who_won(self, turn):

        # region info
        """
            this function responsible for printing the winner based on the turn

            :param turn: the turn for color which won
            :type int

            :return: Nothing
            :rtype: None
        """
        # endregion

        if turn == 0:
            print("white won")
        else:
            print("black won")

    def make_update_base_on_player(self, move_from, move_to, turn):

        # region info
        """
            this function responsible to manage which computer case to call (based on the turn)

            :param turn: the turn for the color we call the function
            :type int

            :return: Nothing
            :rtype: None
        """
        # endregion

        if turn == 0:
            self.case_computer_white(move_from, move_to)
        else:
            self.case_computer_black(move_from, move_to)

    def update_on_new_action(self, row, col):

        self.high_light(True, self.active_highlight)
        self.active_row = row
        self.active_col = col
        self.pressed_flag = True
        self.list_of_labels_board[row][col].config(background = C_V.ACTIVE_POSITION_COLOR)
        self.active_highlight.append([row, col])

    def update_movement(self, row, col):

        # region info
        """
            this function responsible to make hardcore graphical changes
            # Responsible for changing the images places

            :param row: the row of the label
            :type int
            :param col: the col of the label
            :type int
            :param index: the index of the label in the list of labels
            :type int


            :return: Nothing
            :rtype: None
        """
        # endregion

        index = int(self.list_of_labels_board[self.active_row][self.active_col]["image"][0][7:])
        index = index % 45
        self.image_placer(row, col, index - 1)
        self.relief_image(self.active_row, self.active_col)
        self.view_turn.update_turn(self.turn)

    def reset_state(self):

        # region info
        """
            this function responsible toreset the state where no one picked up a soldier
            # no labels are no longer marked

            :return: Nothing
            :rtype: None
        """
        # endregion

        self.active_highlight.append([self.active_row, self.active_col])
        self.high_light(False, self.active_highlight)
        self.pressed_flag = False

    def is_on_action(self):

        # region info
        """
            # return if the game is in a state where the player began a move and checking what he wants to do


            :return: Nothing
            :rtype: None
        """
        # endregion

        return self.pressed_flag

    def get_label_location(self, event):

        # region info
        """
            # return the event label location


            :return: Nothing
            :rtype: None
        """
        # endregion



        row = 0
        col = 0

        if not len(str(event.widget)) == 15:

            value = int(str(event.widget)[15:]) - 1
            row = value // 8
            col = value % 8


        #print(int(str(event.widget)[15:]) - 1)
        return row, col

    def in_high_light_labels(self, labels, row, col):

        # region info
        """
             # Check if the pressed label is in the possible moves (False - can Move, True - cant)


            :return: False / True
            :rtype: bool
        """
        # endregion

        for i in labels:
            if i[0] == row and i[1] == col:
                return False
        return True

    def image_placer(self, x, y, index):

        # region info
        """
            # Place Images on the board


            :return: Nothing
            :rtype: None
        """
        # endregion

        self.list_of_labels_board[x][y].config(image=self.image_storage[index])

    def relief_image(self, x, y):

        # region info
        """
            # Remove image from a certain location from the board


            :return: Nothing
            :rtype: None
        """
        # endregion

        self.list_of_labels_board[x][y].config(image="")

    def high_light(self, check, active_highlight):

        # region info
        """
            # Highlight specific labels


            :return: Nothing
            :rtype: None
        """
        # endregion

        # highlight
        if check == True:

            for i in active_highlight:

                self.list_of_labels_board[i[0]][i[1]].config(background = C_V.MOVEABLE_LABEL_COLORS)

        # default colors
        else:

            for i in self.active_highlight:

                row = i[0]
                col = i[1]

                if (row + col) % 2 == 0:

                    self.list_of_labels_board[row][col].config(background = C_V.BOARD_COLOR_1)
                else:
                    self.list_of_labels_board[row][col].config(background = C_V.BOARD_COLOR_2)

                self.active_highlight = []

    def restart_game(self, to_start_auto = True):

        # region info
        """
            # Restart the game (like in the constructor)


            :return: Nothing
            :rtype: None
        """
        # endregion



        # Create All the soldiers and clean the board
        self.clean_board()


        # Turn of the players
        self.turn = S_T.PLAYER_TURN
        # State in the game (Nothing happened for False, chose soldier for True)
        self.pressed_flag = False
        self.active_row = -1
        self.active_col = -1
        self.active_highlight = []
        self.is_to_continue_flag_on_loop = True
        self.is_game_over = False

        self.view_turn.reset_values()
        self.controller.restart_game()

        self.soldier_creator()

        # set default colors
        if type(self.active_highlight) != bool:
            self.high_light(False, self.list_of_labels_board)

        # restart the duplicate check list
        self.controller.get_computer().default_state()
        # start this function in the case the game is Ai against Ai (check and if it is true begin the game without an event from the player)
        if to_start_auto:
            self.start_automatically()

    def clean_board(self):

        # region info
        """
            # cleans the board


            :return: Nothing
            :rtype: None
        """
        # endregion

        # clean Images
        for i in range(0, 8):
            for j in range(0, 8):
                self.relief_image(i, j)

        # set default colors
        if type(self.active_highlight) != bool:
            self.high_light(False, self.list_of_labels_board)

    def board_creator(self):

        # region info
        """
            # creates the board


            :return: Nothing
            :rtype: None
        """
        # endregion

        list_of_labels_board = []

        for i in range(8):

            sub_list1 = []

            for j in range(8):

                label = ttk.Label(self.center_frame, text="", foreground="Yellow", anchor=CENTER, relief=RIDGE)
                label.bind("<Button-1>", self.onaction)

                if (j + i) % 2 == 0:

                    label.config(background = C_V.BOARD_COLOR_1)

                else:

                    label.config(background = C_V.BOARD_COLOR_2)

                label.place(relx=j * 0.125, rely=i * 0.125, relwidth=0.11875, relheight=0.11875)
                sub_list1.append(label)


            list_of_labels_board.append(sub_list1)
        return list_of_labels_board

    def soldier_creator(self):

        # region info
        """
            # creates the soldiers on the board


            :return: Nothing
            :rtype: None
        """
        # endregion

        soldiers_to_create = self.controller.create_soldiers()

        for i in range(len(soldiers_to_create)):
            if soldiers_to_create[i][2] < 0:
                self.image_placer(soldiers_to_create[i][0], soldiers_to_create[i][1], -(soldiers_to_create[i][2] * 2) - 2)
            elif soldiers_to_create[i][2] > 0:
                self.image_placer(soldiers_to_create[i][0], soldiers_to_create[i][1], soldiers_to_create[i][2] * 2 - 1)





        '''

        # Place Pawns

        for i in range(8):

            self.image_placer(1, i, 0)
            self.image_placer(6, i, 1)


        # Kings

        self.image_placer(0, 4, 10)
        self.image_placer(7, 4, 11)

        # Bishops

        self.image_placer(0, 2, 6)
        self.image_placer(0, 5, 6)

        self.image_placer(7, 2, 7)
        self.image_placer(7, 5, 7)

        #  Rook

        self.image_placer(0, 0, 2)
        self.image_placer(0, 7, 2)

        self.image_placer(7, 0, 3)
        self.image_placer(7, 7, 3)

        # Knights

        self.image_placer(0, 1, 4)
        self.image_placer(0, 6, 4)

        self.image_placer(7, 1, 5)
        self.image_placer(7, 6, 5)

        # Queens

        self.image_placer(0, 3, 8)
        self.image_placer(7, 3, 9)
'''

    def start_automatically(self):

        # region info
        """
            # To start auto when we load the page (without an event)


            :return: Nothing
            :rtype: None
        """
        # endregion

        self.root.update()
        if (S_T.PLAYER_TURN == 1 and S_T.PLAY_AGAINSET_AI_WHITE) or (S_T.PLAYER_TURN == 0 and S_T.PLAY_AGAINSET_AI_BLACK):
            self.loop_turn_games(-1, -1)

    # endregion