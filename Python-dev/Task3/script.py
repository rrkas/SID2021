import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quizzit")

    from app.screens.home_screen import HomeScreen

    HomeScreen(root)
    root.mainloop()
