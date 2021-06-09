from ViewObjects.Option_Menu import *
from Utilities.Setting_Values import *
from ViewObjects.Image_Collection import *

class Start(object):

    def __init__(self):

        # region info
        """
            This class allows to start the menu and work with it

            :param self.root: the root to the main tkinter page
            :type self.root: TK
            :param self.menu: the connection to the menu class
            :type self.menu: GameMenu
            :param self.image_collection: the connection to the image collection class
            :type self.image_collection: ImageCollection

            :return: Nothing
            :rtype: None
        """

        # endregion

        self.root = ""
        self.menu = ""
        self.image_collection = ""
        self.start_menu()

    def start_menu(self):

        # region info
        """
            start the menu from the main class

            :return: Nothing
            :rtype: None
        """

        # endregion


        self.root = Tk()
        self.root.title("Chess")
        self.root.geometry(str(S_T.WIDTH)+"x"+str(S_T.HEIGHT))
        self.root.resizable(0, 0)
        self.root['bg'] = C_V.PAGE_COLOR
        self.image_collection = ImageCollection(self.root)
        self.menu = GameMenu(self.root, self.image_collection, self)







        self.root.mainloop()


def Main():
    #try:
    start = Start()
    #except:
    #    print("There was an error")

if __name__ == "__main__":
    Main()