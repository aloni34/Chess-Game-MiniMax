from ViewObjects.View_Board import *
from ViewObjects.Image_Collection import *
from ViewObjects.View_Turn import *

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk

class ViewGamePlay(object):

    # region Constructer
    def __init__(self, root, image_collection):
        # region info
        """
            This class creates all the graphical related objects during the game.
            Creates some button which are created only when this class is being created.
            Also creates two additonal classes for other gameplay related view.

            :param self.root: the root to the main tkinter page
            :type self.root: TK
            :param self.image_collection: connection for the image class
            :type self.image_collection: ImageCollection
            :param self.view_turn: connection for the view turn class
            :type self.view_turn: ViewTurn
            :param self.view_board: connection for the view board class
            :type self.view_board: ViewBoard

            :return: Nothing
            :rtype: None
        """
        # endregion
        self.root = root
        self.image_collection = image_collection
        self.view_turn = ViewTurn(root, image_collection)
        self.create_reset_button()
        self.create_test_button()
        self.view_board = ViewBoard(root, image_collection, self.view_turn, self)

    # endregion

    # region Methods
    # Add Resetart button
    def create_reset_button(self):
        # region info
        """
            this function restars the game to the beginning

            :param self.reset_button: a button to make a restart for the game
            :type self.reset_button: Tk (button)

            :return: Nothing
            :rtype: None
        """
        # endregion
        self.reset_button = ttk.Button(self.root, text='Restart', image = self.image_collection.get_image_list()[12])
        self.reset_button.place(relx=0.725, rely=0.02 , relwidth=0.15, relheight=0.1)

    def create_test_button(self):
        # region info
        """
            this function restars the game to the beginning

            :param self.reset_button: a button to make tests for the game
            :type self.reset_button: Tk (button)

            :return: Nothing
            :rtype: None
        """
        # endregion
        self.test_button = ttk.Button(self.root, image = self.image_collection.get_image_list()[42])
        self.test_button.place(relx=0.725, rely=0.15 , relwidth=0.15, relheight=0.1)

    # endregion
