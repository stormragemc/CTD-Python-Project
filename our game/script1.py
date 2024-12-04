import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Maze Navigator")

grid_size = 10
cell_size = 50
start_position = (0, 0)
end_position = (9, 9)
player_position = list(start_position)

grid_clues = {
    (2, 2): "Try moving to the top-right corner!",
    (5, 5): "You're halfway there. Keep moving east!",
    (7, 7): "Almost there! Head south to win!"
}

canvas = tk.Canvas(window, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()

background_image = tk.PhotoImage(file="background.png")
canvas.create_image(0, 0, image=background_image, anchor="nw")

for i in range(grid_size):
    for j in range(grid_size):
        x1, y1 = i * cell_size, j * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, outline="black")

canvas.create_rectangle(start_position[0] * cell_size, start_position[1] * cell_size,
                        start_position[0] * cell_size + cell_size, start_position[1] * cell_size + cell_size,
                        fill="green")
canvas.create_rectangle(end_position[0] * cell_size, end_position[1] * cell_size,
                        end_position[0] * cell_size + cell_size, end_position[1] * cell_size + cell_size,
                        fill="red")

player = canvas.create_oval(player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
                            player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10,
                            fill="blue")

def show_instructions():
    messagebox.showinfo(
        "Instructions",
        "Welcome to Maze Navigator!\n\n"
        "Use the W, A, S, D keys to move:\n"
        "W = Up, S = Down, A = Left, D = Right.\n\n"
        "Your goal is to reach the red square."
    )

def show_clue():
    messagebox.showinfo(
        "Clue",
        "Clue: The destination lies in the bottom-right corner of the maze. Move wisely!"
    )

def check_clues():
    pos = tuple(player_position)
    if pos in grid_clues:
        messagebox.showinfo("Hint", grid_clues[pos])

def move_player(postal_code):
    global player_position
    moves = {"1": (-1, 0), "2": (1, 0), "3": (0, -1), "4": (0, 1)}
    if postal_code in moves:
        dx, dy = moves[postal_code]
        new_x = player_position[0] + dx
        new_y = player_position[1] + dy
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            player_position = [new_x, new_y]
            update_player_position()

def update_player_position():
    canvas.coords(player, player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
                  player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10)
    check_win_condition()
    check_clues()

def check_win_condition():
    if tuple(player_position) == end_position:
        messagebox.showinfo("Congratulations!", "You Win!")
        canvas.create_text(
            grid_size * cell_size // 2,
            grid_size * cell_size // 2,
            text="You Win!",
            font=("Arial", 24),
            fill="green"
        )

def handle_keypress(event):
    key_to_postal = {"w": "1", "s": "2", "a": "3", "d": "4"}
    if event.char in key_to_postal:
        move_player(key_to_postal[event.char])

show_instructions()
show_clue()

window.bind("<Key>", handle_keypress)

window.mainloop()
