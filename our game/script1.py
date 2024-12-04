import tkinter as tk

window = tk.Tk()
window.title("Maze Navigator")


grid_size = 10  
cell_size = 50  
start_position = (0, 0)
end_position = (9, 9)


player_position = list(start_position)


canvas = tk.Canvas(window, width=grid_size * cell_size, height=grid_size * cell_size, bg="white")

canvas.pack()


for i in range(grid_size):
    for j in range(grid_size):
        x1, y1 = i * cell_size, j * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")


canvas.create_rectangle(start_position[0] * cell_size, start_position[1] * cell_size,
                        start_position[0] * cell_size + cell_size, start_position[1] * cell_size + cell_size,
                        fill="green")
canvas.create_rectangle(end_position[0] * cell_size, end_position[1] * cell_size,
                        end_position[0] * cell_size + cell_size, end_position[1] * cell_size + cell_size,
                        fill="red")


player = canvas.create_oval(player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
                            player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10,
                            fill="blue")


def move_player(postal_code):
    global player_position
    moves = {
        "1": (0, -1),  
        "2": (-1, 0),   
        "3": (0, 1),  
        "4": (1,0 )    
    }
    if postal_code in moves:
        dx, dy = moves[postal_code]
        new_x, new_y = player_position[0] + dx, player_position[1] + dy

        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            player_position = [new_x, new_y]
            update_player_position()


def update_player_position():
    canvas.coords(player, player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
                  player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10)
    check_win_condition()


def check_win_condition():
    if tuple(player_position) == end_position:
        canvas.create_text(grid_size * cell_size // 2, grid_size * cell_size // 2, text="You Win!", font=("Arial", 24), fill="green")


def handle_keypress(event):
    key_to_postal = {
        "w": "1",  
        "a": "2",  
        "s": "3",  
        "d": "4"   
    }
    if event.char in key_to_postal:
        move_player(key_to_postal[event.char])

window.bind("<Key>", handle_keypress)


window.mainloop()
