from ViewObjects.Image_Collection import *
from Utilities.Constant_Values import *

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk

class ViewTurn(object):

    # region Constructer
    def __init__(self, root, image_collection):

        # region info
        """
            This class which shows check mate case and which turn it is

            :param self.root: the root to the main tkinter page
            :type self.root: TK
            :param self.image_collection: connection for the image class
            :type self.image_collection: ImageCollection
            :param self.switch_label_one: a label to show in some cases (for black)
            :type self.switch_label_one: label
            :param self.image_collection: a label to show in some cases (for white)
            :type self.image_collection: label
            :param self.image_collection: a label to show in some cases (in checkmate)
            :type self.image_collection: label



            :return: Nothing
            :rtype: None
        """
        # endregion

        self.root = root
        self.image_collection = image_collection

        self.s2 = Style()
        self.s2.configure('My2.TFrame', anchor= CENTER, background = C_V.PAGE_COLOR)
        self.upper_frame = ttk.Frame(root)
        self.upper_frame.config(style='My2.TFrame')
        self.upper_frame.place(relx = 0.075, rely = 0, relwidth = 0.5667, relheight = 0.14)
        self.upper_frame.config(padding=(30, 15))

        self.switch_label_one = ttk.Label(self.upper_frame, anchor = CENTER, background = C_V.PAGE_COLOR)
        self.switch_label_one.place(relx = 0, rely = -0.02, relwidth = 0.333, relheight = 1)

        self.check_label = ttk.Label(self.upper_frame, image=self.image_collection.get_image_list()[15], anchor=CENTER, background=C_V.PAGE_COLOR)
        self.check_label.place(relx=0.333, rely=-0.02, relwidth=0.333, relheight=1)

        self.switch_label_two = ttk.Label(self.upper_frame, anchor = CENTER, background = C_V.PAGE_COLOR)
        self.switch_label_two.place(relx = 0.666, rely = 0, relwidth = 0.333, relheight = 1)

        self.is_in_check_flag = False

        self.reset_turn()
    # endregion

    # region Methods

    def reset_values(self):

        # region info
        """
            reset values to default state

            :return: Nothing
            :rtype: None
        """
        # endregion

        self.reset_turn()
        self.reset_check()

    # Update the board based on the turn
    def update_turn(self, turn):

        # region info
        """
            updates the turn view labels base on the given turn

            :param turn: which turn it is
            :type turn: int

            :return: Nothing
            :rtype: None
        """
        # endregion

        if turn == 0:

            self.switch_label_one.config(image=self.image_collection.get_image_list()[13])
            self.switch_label_two.config(image=self.image_collection.get_image_list()[15])

        else:

            self.switch_label_one.config(image=self.image_collection.get_image_list()[15])
            self.switch_label_two.config(image=self.image_collection.get_image_list()[14])

    def reset_turn(self):

        # region info
        """
            default state for switched labels

            :return: Nothing
            :rtype: None
        """
        # endregion

        if S_T.PLAYER_TURN == 1:

            self.switch_label_one.config(image=self.image_collection.get_image_list()[13])
            self.switch_label_two.config(image=self.image_collection.get_image_list()[15])

        else:

            self.switch_label_one.config(image=self.image_collection.get_image_list()[15])
            self.switch_label_two.config(image=self.image_collection.get_image_list()[14])

    def update_check(self):

        # region info
        """
            updates the check label base on the case

            :return: Nothing
            :rtype: None
        """
        # endregion

        if self.is_in_check_flag:
            self.check_label.config(image=self.image_collection.get_image_list()[15])
            self.is_in_check_flag = False
        else:
            self.check_label.config(image=self.image_collection.get_image_list()[43])
            self.is_in_check_flag = True

    def reset_check(self):

        # region info
        """
            default state for the check label

            :return: Nothing
            :rtype: None
        """
        # endregion

        self.check_label.config(image=self.image_collection.get_image_list()[15])

    # endregion
