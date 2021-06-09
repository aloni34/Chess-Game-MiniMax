from ViewObjects.View_GamePlay import *
from ViewObjects.Image_Collection import *

from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk

class ViewPage(object):

    # region Constructer
    def __init__(self, root, main_start, image_collection, menu):
        # region info
        """
            This Class responsible for what we see in the page after we press start the game

            :param self.root: the root to the main tkinter page
            :type self.root: TK
            :param self.main_start: connection to the class of the main, in the case we want to go back and start from the loading screen
            :type self.main_start: Start
            :param self.image_collection: connection for the image class
            :type self.image_collection: ImageCollection
            :param self.menu: connection to the menu class
            :type self.menu: GameMenu


            :return: Nothing
            :rtype: None
        """
        # endregion
        self.root = root
        self.main_start = main_start
        self.image_collection = image_collection
        self.menu = menu


        self.view_gameplay = None
    # endregion

    # region Methods
    # Starts the game after the user have chosen to play the game from the option menu
    def start_game(self):
        # region info
        """
            this function creates the following game by creating buttons and creating the classes which are responsible for the gameplay view

            :return: Nothing
            :rtype: None
        """
        # endregion
        self.create_menu_button()
        self.view_gameplay= ViewGamePlay(self.root, self.image_collection)


    def create_menu_button(self):
        # region info
        """
            this function creates the menu button which when pressed goes back to the menu

            :param self.back_button: the button to the menu
            :type self.back_button: TK (button)

            :return: Nothing
            :rtype: None
        """
        # endregion
        self.back_button = ttk.Button(self.root, text='Restart', image = self.image_collection.get_image_list()[26])
        self.back_button.place(relx=0.725, rely=0.85 , relwidth=0.15, relheight=0.1)
        self.back_button.config(command = self.menu.restart_menu)
    # endregion