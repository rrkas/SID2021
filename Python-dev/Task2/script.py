import tkinter as tk
import os
from PIL import Image, ImageTk
import random
from time import sleep


game_name = "The Game of Chances"
user_name = ""


def configure_bg(*obj):
    for i in obj:
        i["bg"] = "white"
        # obj.configure(background='white')


class Data:
    rock = "Rock"
    paper = "Paper"
    sessior = "Sessior"
    lizard = "Lizard"
    spock = "Spock"
    empty = "empty"

    actions = {
        rock: "stone.png",
        paper: "paper.png",
        sessior: "sessior.png",
        lizard: "lizard.jpg",
        spock: "spock.png",
        empty: "empty.png",
    }

    matches = {
        rock: [lizard, sessior],
        paper: [rock, spock],
        sessior: [paper, lizard],
        lizard: [spock, paper],
        spock: [sessior, rock],
    }

    @staticmethod
    def compute_winner_user(ku, ks):
        if ku == Data.empty:
            return False
        return ks in Data.matches[ku]


class WelcomeWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(padx=20, pady=20)

    def load_components(self):
        # title
        game_title_frame = tk.Frame(
            self.frame, highlightbackground="blue", highlightthickness=1
        )
        game_title1 = tk.Label(
            game_title_frame,
            text=" ".join(game_name.split()[:-1]).upper(),
            font=("Arial", 25),
        )
        game_title1.pack(padx=10)
        game_title2 = tk.Label(
            game_title_frame,
            text=game_name.split()[-1].upper(),
            font=("Arial", 30, "bold"),
        )
        game_title2.pack()
        game_title_frame.pack()
        configure_bg(game_title_frame, game_title1, game_title2)
        # name
        name_var = tk.StringVar()
        name_frame = tk.Frame(
            self.frame, highlightbackground="blue", highlightthickness=1
        )
        name_label = tk.Label(name_frame, text="Enter Name: ", font=("Arial", 18))
        name_label.pack(side=tk.LEFT)
        name_entry = tk.Entry(name_frame, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, padx=10)
        name_frame.pack(pady=10)
        configure_bg(name_entry, name_frame, name_label)

        # start button
        def save_user_name():
            global user_name
            user_name = name_var.get()
            self.start_game()

        button = tk.Button(self.frame, text="Start Game!", command=save_user_name)
        button.pack()
        configure_bg(button)

    def start_game(self):
        # open game window
        GameWindow(self.master)
        # close current window
        self.frame.destroy()


class GameWindow:
    def __init__(self, master):
        self.points_user = 0
        self.points_system = 0
        self.master = master
        self.frame = tk.Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    def load_components(self):
        random.SystemRandom()
        options_col_span, chosen_col_span, vs_col_span = 1, 3, 2
        player_col_span, points_col_span, points_users_col_span = 6, 2, 4

        # player labels
        label_user = tk.Label(self.frame, text=user_name)
        label_user.grid(row=0, column=0, columnspan=player_col_span)
        label_system = tk.Label(self.frame, text="COMPUTER")
        label_system.grid(row=0, column=player_col_span, columnspan=player_col_span)
        configure_bg(label_user, label_system)

        points_label = tk.Label(self.frame, text="POINTS")
        points_label.grid(row=7, column=0, columnspan=points_col_span)
        configure_bg(points_label)

        def update_points(pu=0, ps=0):
            self.points_user += pu
            self.points_system += ps
            user_frame = tk.Frame(
                self.frame, highlightbackground="blue", highlightthickness=1
            )
            points_user_label = tk.Label(
                user_frame, text=user_name + " => " + str(self.points_user)
            )
            points_user_label.pack()
            user_frame.grid(
                row=7, column=points_col_span, columnspan=points_users_col_span
            )

            system_frame = tk.Frame(
                self.frame, highlightbackground="blue", highlightthickness=1
            )
            points_system_label = tk.Label(
                system_frame, text="COMPUTER" + " => " + str(self.points_system)
            )
            points_system_label.pack()
            system_frame.grid(
                row=7,
                column=points_col_span + points_users_col_span,
                columnspan=points_users_col_span,
            )

            configure_bg(
                user_frame, system_frame, points_system_label, points_user_label
            )
            if self.points_system == 3:
                self.end_game()

        update_points()

        def show_chosen_system(k):
            size = 200
            img = Image.open(os.path.join(os.path.dirname(__file__), "assets", Data.actions[k]))
            img = img.resize((size, size))
            img = ImageTk.PhotoImage(img)
            system_option = tk.Label(self.frame, image=img)
            system_option.image = img
            system_option.grid(
                row=1,
                column=options_col_span + chosen_col_span + vs_col_span,
                rowspan=5,
                columnspan=chosen_col_span,
                padx=20,
            )
            configure_bg(system_option)

        option_size = 60
        # options and chosen
        for i in range(len(Data.actions.items())):
            k, v = list(Data.actions.items())[i]
            img = Image.open(os.path.join(os.path.dirname(__file__), "assets", v))
            img = img.resize((option_size, option_size))
            img = ImageTk.PhotoImage(img)
            option_user = tk.Label(self.frame, image=img)
            option_user.image = img
            option_user.grid(
                row=1 + i,
                column=options_col_span + chosen_col_span * 2 + vs_col_span,
                columnspan=options_col_span,
                pady=10,
            )
            configure_bg(option_user)

        def show_chosen_user(k, ignore=False):
            if self.points_system == 3:
                return
            size = 200
            img = Image.open(
                os.path.join(os.path.dirname(__file__), "assets", Data.actions[k])
            )
            img = img.resize((size, size))
            img = ImageTk.PhotoImage(img)
            user_option = tk.Label(self.frame, image=img)
            user_option.image = img
            user_option.grid(
                row=1,
                column=options_col_span,
                rowspan=5,
                columnspan=chosen_col_span,
                padx=20,
            )
            configure_bg(user_option)
            ks = list(Data.actions.keys())[random.randrange(0, len(Data.actions) - 1)]
            if not ignore:
                show_chosen_system(ks)
                if k != ks:
                    if Data.compute_winner_user(k, ks):
                        update_points(pu=1)
                    else:
                        update_points(ps=1)
            else:
                show_chosen_system(Data.empty)

        show_chosen_user(Data.empty, True)

        # options and chosen
        for i in range(len(Data.actions.items())):
            k, v = list(Data.actions.items())[i]
            img = Image.open(os.path.join(os.path.dirname(__file__), "assets", v))
            img = img.resize((option_size, option_size))
            img = ImageTk.PhotoImage(img)
            option_user = tk.Label(self.frame, image=img)
            option_user.image = img
            option_user.bind("<Button-1>", lambda _, b=k: show_chosen_user(b))
            option_user.grid(row=1 + i, column=0, columnspan=options_col_span, pady=10)
            configure_bg(option_user)

        vs_label = tk.Label(self.frame, text="VS")
        vs_label.grid(row=3, column=chosen_col_span + options_col_span)
        configure_bg(vs_label)

    def end_game(self):
        sleep(1)
        # open winner window
        WinnerWindow(self.master, self.points_user)
        # close current window
        self.frame.destroy()


class WinnerWindow:
    def __init__(self, master, score):
        self.score = score
        self.master = master
        self.frame = tk.Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(padx=20, pady=20)

    def load_components(self):
        player_frame = tk.Frame(
            self.frame, highlightbackground="blue", highlightthickness=1
        )
        player_name = tk.Label(
            player_frame,
            text=user_name + " Score: " + str(self.score).zfill(2),
            font=("Arial", 30),
        )
        player_name.pack(padx=10)
        player_frame.pack()
        configure_bg(player_frame, player_name)

        exit_btn = tk.Button(
            self.frame,
            text="EXIT",
            font=("Arial", 20),
            command=lambda: self.exit_game(),
        )
        exit_btn.pack(padx=10, side=tk.LEFT, pady=5)
        configure_bg(exit_btn)

        restart_btn = tk.Button(
            self.frame,
            text="START NEW\nGAME!",
            font=("Arial", 14),
            command=lambda: self.restart_game(),
        )
        restart_btn.pack(padx=10, side=tk.LEFT, pady=15)
        configure_bg(restart_btn)

    def restart_game(self):
        # open welcome window
        WelcomeWindow(self.master)
        # close current window
        self.frame.destroy()

    def exit_game(self):
        self.master.destroy()


# ========================== driver code ====================================
if __name__ == "__main__":
    window = tk.Tk()
    window.title("The Game of Chances")
    configure_bg(window)
    # window.state("zoomed") # for full screen

    WelcomeWindow(window)

    window.mainloop()
