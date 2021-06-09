from tkinter import *
from ViewObjects.View_Page import *
from Utilities.Tools import *
from Main import *
from PIL import Image, ImageTk

# region info

# This class controls all the menu / lobby look until we begin the game or quit
# nothing special besides this

# endregion


class GameMenu(object):

    # region Constructer
    def __init__(self, root, image_collection, main_start):


        self.main_start = main_start
        self.root = root
        self.image_collection = image_collection
        self.button_list = []
        self.view_page = ViewPage(self.root, self.main_start, self.image_collection, self)
        self.help_picture = self.save_help_picture()

        self.menu_frame_center = None
        self.construct_menu()

    def save_help_picture(self):

        temp_image = Image.open("Images" + '\\' + "chess_rules.png")
        temp_image = temp_image.resize((int(S_T.HEIGHT // 1.3), int(S_T.HEIGHT // 1.5)), Image.ANTIALIAS)
        logo1 = ImageTk.PhotoImage(temp_image)

        return logo1
    # endregion

    # region Option Bars
    def construct_menu(self):

        self.menu_frame_center = self.construct_frame()
        self.construct_options()

    def restart_menu(self):

        self.main_start.root.destroy()
        self.main_start.start_menu()

    def construct_frame(self):

        frame1 = ttk.Frame(self.root)
        frame1.place(relx=0.425, rely=0.075, relwidth=0.2, relheight=0.7)
        frame1.config(padding=(30, 15), style='My2.TFrame')

        return frame1

    def construct_options(self):

        self.clear_exist_buttons()

        play_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[16])
        play_button.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.12)
        play_button.config(command=self.play_game)

        #load_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[17])
        #load_button.place(relx=0.1, rely=0.22, relwidth=0.8, relheight=0.12)

        settings_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[18])
        settings_button.place(relx=0.1, rely=0.22, relwidth=0.8, relheight=0.12)
        settings_button.config(command=self.construct_settings)

        help_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[19])
        help_button.place(relx=0.1, rely=0.39, relwidth=0.8, relheight=0.12)
        help_button.config(command=self.construct_help)

        quit_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[32])
        quit_button.place(relx=0.1, rely=0.77, relwidth=0.8, relheight=0.12)
        quit_button.config(command= self.quit)

        self.button_list.append(play_button)
        #self.button_list.append(load_button)
        self.button_list.append(settings_button)
        self.button_list.append(help_button)
        self.button_list.append(quit_button)

    def construct_help(self):

        self.clear_exist_buttons()

        canvas = Canvas(width= (S_T.WIDTH // 2.2), height = (S_T.HEIGHT // 1.5), bg=C_V.PAGE_COLOR)
        canvas.place(relx = 0.3, rely = 0.00)
        canvas.create_image(S_T.WIDTH / 4.5, S_T.HEIGHT / 3, image=self.help_picture)

        back_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[20])
        back_button.place(relx=0.1, rely=0.88, relwidth=0.8, relheight=0.12)
        back_button.config(command=lambda:self.destroy_canvas_and_go_back(canvas))

        self.button_list.append(back_button)

    def construct_settings(self):

        self.clear_exist_buttons()

        play_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[21])
        play_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.12)
        play_button.config(command=self.construct_size_settings)

        mode_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[27])
        mode_button.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.12)
        mode_button.config(command=self.construct_mode_settings)

        back_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[20])
        back_button.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.12)
        back_button.config(command=self.construct_options)

        self.button_list.append(play_button)
        self.button_list.append(mode_button)
        self.button_list.append(back_button)


    def construct_size_settings(self):

        self.clear_exist_buttons()

        size1_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[22])
        size1_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.12)
        size1_button.config(command=lambda: self.update_size(1920, 1080))

        size2_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[23])
        size2_button.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.12)
        size2_button.config(command=lambda: self.update_size(1632, 810))

        size3_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[24])
        size3_button.place(relx=0.1, rely=0.42, relwidth=0.8, relheight=0.12)
        size3_button.config(command=lambda: self.update_size(1200, 680))

        size4_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[25])
        size4_button.place(relx=0.1, rely=0.59, relwidth=0.8, relheight=0.12)
        size4_button.config(command=lambda: self.update_size(960, 540))

        back_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[20])
        back_button.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.12)
        back_button.config(command=self.construct_settings)

        self.button_list.append(size1_button)
        self.button_list.append(size2_button)
        self.button_list.append(size3_button)
        self.button_list.append(size4_button)
        self.button_list.append(back_button)

    def construct_mode_settings(self):

        self.clear_exist_buttons()

        difficulty_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[28])
        difficulty_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.12)
        difficulty_button.config(command=self.construct_difficulty_settings)

        color_start_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[33])
        color_start_button.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.12)
        color_start_button.config(command=self.construct_color_side_settings)

        ai_player_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[40])
        ai_player_button.place(relx=0.1, rely=0.42, relwidth=0.8, relheight=0.12)
        ai_player_button.config(command=self.construct_ai_player_settings)

        back_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[20])
        back_button.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.12)
        back_button.config(command=self.construct_settings)

        self.button_list.append(difficulty_button)
        self.button_list.append(color_start_button)
        self.button_list.append(ai_player_button)
        self.button_list.append(back_button)

    def construct_difficulty_settings(self):

        self.clear_exist_buttons()

        easy_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[29])
        easy_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.12)
        easy_button.config(command= lambda: self.update_difficulty(2))

        medium_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[30])
        medium_button.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.12)
        medium_button.config(command= lambda: self.update_difficulty(3))

        hard_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[31])
        hard_button.place(relx=0.1, rely=0.42, relwidth=0.8, relheight=0.12)
        hard_button.config(command= lambda: self.update_difficulty(4))

        back_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[20])
        back_button.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.12)
        back_button.config(command=self.construct_mode_settings)

        self.button_list.append(easy_button)
        self.button_list.append(medium_button)
        self.button_list.append(hard_button)
        self.button_list.append(back_button)

    def construct_color_side_settings(self):

        self.clear_exist_buttons()

        black_start_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[34])
        black_start_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.12)
        black_start_button.config(command= lambda: self.color_start(0))

        white_start_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[35])
        white_start_button.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.12)
        white_start_button.config(command= lambda: self.color_start(1))

        back_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[20])
        back_button.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.12)
        back_button.config(command=self.construct_mode_settings)

        self.button_list.append(black_start_button)
        self.button_list.append(white_start_button)
        self.button_list.append(back_button)

    def construct_ai_player_settings(self):

        self.clear_exist_buttons()

        black_ai_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[36])
        black_ai_button.place(relx=0.1, rely=0.08, relwidth=0.8, relheight=0.12)
        black_ai_button.config(command=lambda: self.ai_player(True, True))


        black_player_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[38])
        black_player_button.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.12)
        black_player_button.config(command=lambda: self.ai_player(True, False))

        white_ai_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[37])
        white_ai_button.place(relx=0.1, rely=0.42, relwidth=0.8, relheight=0.12)
        white_ai_button.config(command=lambda: self.ai_player(False, True))

        white_player_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[39])
        white_player_button.place(relx=0.1, rely=0.59, relwidth=0.8, relheight=0.12)
        white_player_button.config(command=lambda: self.ai_player(False, False))


        back_button = ttk.Button(self.menu_frame_center, image=self.image_collection.get_image_list()[20])
        back_button.place(relx=0.1, rely=0.76, relwidth=0.8, relheight=0.12)
        back_button.config(command=self.construct_mode_settings)

        self.button_list.append(black_ai_button)
        self.button_list.append(black_player_button)
        self.button_list.append(white_ai_button)
        self.button_list.append(white_player_button)
        self.button_list.append(back_button)

    # endregion

    # region Methods
    def update_difficulty(self, depth):
        S_T.AI_DEPTH = depth
        self.construct_mode_settings()

    def clear_exist_buttons(self):

        for i in range(len(self.button_list)):
            self.button_list[i].destroy()

    def update_size(self, width, height):

        S_T.HEIGHT = height
        S_T.WIDTH = width

        self.main_start.root.destroy()
        self.main_start.start_menu()

    def quit(self):
        self.main_start.root.destroy()

    def color_start(self, check):
        if check:
            S_T.PLAYER_TURN = 1
        else:
            S_T.PLAYER_TURN = 0

    def ai_player(self, check1, check2):
        if check1:
            if check2:
                S_T.PLAY_AGAINSET_AI_BLACK = True
            else:
                S_T.PLAY_AGAINSET_AI_BLACK = False
        else:
            if check2:
                S_T.PLAY_AGAINSET_AI_WHITE = True
            else:
                S_T.PLAY_AGAINSET_AI_WHITE = False

        if S_T.PLAY_AGAINSET_AI_BLACK and S_T.PLAY_AGAINSET_AI_WHITE:
            S_T.AI_VS_AI = True

    def play_game(self):

        self.clear_exist_buttons()
        self.menu_frame_center.destroy()
        self.view_page.start_game()

    def destroy_canvas_and_go_back(self, canvas):
        canvas.destroy()
        self.construct_options()
    # endregion

