import tkinter as tk
import random
import time

DIE_SIZE = 200      
PIP_RADIUS = 10       
ANIMATION_FRAMES = 10  
ANIMATION_DELAY = 40 

def pip_positions(size):
    margin = size * 0.18
    center = size / 2
    left = margin
    right = size - margin
    top = margin
    bottom = size - margin
    return {
        "tl": (left, top),
        "tc": (center, top),
        "tr": (right, top),
        "cl": (left, center),
        "cc": (center, center),
        "cr": (right, center),
        "bl": (left, bottom),
        "bc": (center, bottom),
        "br": (right, bottom),
    }

PIP_MAP = {
    1: ("cc",),
    2: ("tl", "br"),
    3: ("tl", "cc", "br"),
    4: ("tl", "tr", "bl", "br"),
    5: ("tl", "tr", "cc", "bl", "br"),
    6: ("tl", "tr", "cl", "cr", "bl", "br"),
}

class DiceApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Virtual Dice Roller")
        root.resizable(False, False)
        self.rolling = False

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=DIE_SIZE, height=DIE_SIZE, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.positions = pip_positions(DIE_SIZE)

        self.result_label = tk.Label(frame, text="Press Space / Click / Roll", font=("Helvetica", 14))
        self.result_label.grid(row=1, column=0, columnspan=2, pady=(8, 0))

        self.roll_button = tk.Button(frame, text="Roll", command=self.roll_button_clicked, width=10)
        self.roll_button.grid(row=2, column=0, pady=10)

        self.quit_button = tk.Button(frame, text="Quit", command=root.quit, width=10)
        self.quit_button.grid(row=2, column=1, pady=10)

        root.bind("<Button-1>", self.window_clicked)      # left click anywhere
        root.bind("<space>", self.key_pressed)
        root.bind("<Return>", self.key_pressed)

        self.draw_die(1)

    def draw_die(self, value):
        self.canvas.delete("all")

        x0, y0, x1, y1 = 2, 2, DIE_SIZE - 2, DIE_SIZE - 2
        self.canvas.create_rectangle(
            x0, y0, x1, y1,
            fill="#ffffff",
            outline="#333333",
            width=3
        )

        for key in PIP_MAP[value]:
            cx, cy = self.positions[key]
            self.canvas.create_oval(
                cx - PIP_RADIUS, cy - PIP_RADIUS,
                cx + PIP_RADIUS, cy + PIP_RADIUS,
                fill="#222222",
                outline=""
            )

        

    def animate_and_roll(self):
        if self.roll_button['state'] == "disabled" or self.rolling:
            print("Roll in progress, please wait...")
            return
        self.rolling = True
        self.roll_button.config(state="disabled")

        for _ in range(ANIMATION_FRAMES):
            temp = random.randint(1, 6)
            self.draw_die(temp)
            self.root.update_idletasks()
            self.root.after(ANIMATION_DELAY)

        final = random.randint(1, 6)
        self.draw_die(final)
        self.result_label.config(text=f"Result: {final}")
        self.roll_button.config(state="normal")
        self.rolling = False

    def roll_button_clicked(self):
        if not self.rolling:
            self.animate_and_roll()

    def window_clicked(self, event):
        if not self.rolling:
            self.animate_and_roll()

    def key_pressed(self, event):
        if not self.rolling:    
            self.animate_and_roll()


if __name__ == "__main__":

    root = tk.Tk()
    app = DiceApp(root)
    root.mainloop()
