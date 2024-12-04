import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox
import random
import time  

window = tk.Tk()
window.title("Maze Navigator")

grid_size = 20  
cell_size = 25  
player_position = [0, 0]
attempts = 0  
total_time = 0  

image = Image.open("our game/photo_2024-12-04_13-54-20.png")
img = image.resize((860,620))
img = ImageTk.PhotoImage(img)
Locations = {
    "Tang Zheng Tang Chinese Pavilion":  (10, 1),
    "Gym":  (17, 7) ,
    "T-lab":  (4, 16) ,
    "OneStop Centre":  (7, 18) ,
    "Albert Hong Lecture Theatre":  (2, 19) ,
    "Scrapyard":  (7, 8) ,
    "Swimming pool":  (18, 6) ,
    "Fab-Lab":  (6, 9) ,
    "Upper Changi MRT":  (0, 14) ,
    "D'Star Bistro":  (5, 18) ,
    "Campus Centre":  (7, 17) ,
    "Vending machines":  (6, 12), 
}   

final_destination = None
final_destination_name = None


walls = []

canvas = tk.Canvas(window, width=grid_size * cell_size, height=grid_size * cell_size)
canvas.pack()


player = None


timer_label = tk.Label(window, text="Time: 0s", font=("Arial", 12))
timer_label.pack(side="top", anchor="ne")


def get_player_name():
    name = simpledialog.askstring("Player Name", "Hello there Player, what is your name?")
    return name


def display_welcome_message(name):
    messagebox.showinfo(
        "Welcome to the Game!",
        f"Hello {name}, welcome to our game of navigating through SUTD.\n\nPress the spacebar to skip.\n\n"
        "This game was made possible by Srihari, Zhi Ying, Marcel, Kris, and Sherelle.\n"
        "We welcome you into this game.\n\n"
        "You will be navigating through the world-class SUTD campus, located in the heart of Singapore's innovation district. "
        "The campus features state-of-the-art facilities designed to support interdisciplinary learning and cutting-edge research. "
        "In this game, you will be navigating through Level 1 of the SUTD campus and experiencing different areas around the ground level "
        "that are accessible to the public, without even having to touch the ground.\n"
    )
    messagebox.showinfo(
        "Controls",
        "You can navigate through the school compound using W to go up, S to go down, A to go left, and D to go right.\n\n"
        "To quit the game, you can press ESC at any time."
    )
    messagebox.showinfo(
        "Gameplay",
        "We will give you a description of a specific location, and you will have to make your way there.\n\n"
        "If you reach the wrong spot, a clue will be given to help guide you to the correct location."
    )
    messagebox.showinfo("Start the Adventure", f"Enjoy your adventure ahead, {name}!")


def choose_final_destination():
    global final_destination, final_destination_name
    final_destination_name = random.choice(list(Locations.keys()))
    final_destination = Locations[final_destination_name] 
    Locations.pop(final_destination_name)
    canvas.create_image(-90, -45, anchor = tk.NW, image=img)
    destination_label.config(text=f"Find: {final_destination_name}")
    return final_destination_name



def update_player_position():
    canvas.coords(player, player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
                  player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10)
    if tuple(player_position) in  Locations.values() and tuple(player_position) != final_destination: #i put the popup for every key building here so it can check every time the player changes position
                for key,val in Locations.items():
                    if val == tuple(player_position):
                        messagebox.showinfo("Key Area", key)
    check_win_condition()

def check_win_condition():
    global attempts, total_time
    if tuple(player_position) == final_destination: 
        
        end_time = time.time() - start_time  
        total_time += end_time  
        attempts += 1 
        messagebox.showinfo("Congratulations!", f"You reached {final_destination_name}! You win!")
        canvas.create_text(
            grid_size * cell_size // 2,
            grid_size * cell_size // 2,
            text="You Win!",
            font=("Arial", 24),
            fill="green"
        )
        
        if attempts >= 10:
            messagebox.showinfo("Game Over", f"Total time: {total_time:.2f} seconds.\nClick Restart to play again.")
            
            restart_button.config(state="normal")  
        else:
            restart_game()


def move_player(postal_code):
    global player_position
    moves = {"w": (0, -1),  
        "a": (-1, 0),   
        "s": (0, 1),  
        "d": (1,0 ) }
    if postal_code in moves:
        dx, dy = moves[postal_code]
        new_x = player_position[0] + dx
        new_y = player_position[1] + dy
        
        if (0 <= new_x < grid_size and 0 <= new_y < grid_size) and (new_x, new_y) not in walls:
            player_position = [new_x, new_y]
            
            update_player_position()
            
            
                
            
        else:
            messagebox.showinfo("Blocked", "You hit a wall! Try a different direction.")


def handle_keypress(event):
    move_player(event.char)


def restart_game():
    
    
    global player_position, player, start_time
    player_position = [0, 0]
    canvas.delete("all")
    
    choose_final_destination()
    draw_grid()
    draw_start_end()
    player = canvas.create_oval(
        player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
        player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10,
        fill = "blue"
    )
    messagebox.showinfo('','Round {}'.format(attempts+1))
    start_time = time.time()  


def exit_game():
    window.quit()


def draw_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if (i, j)  in Locations.values():
                canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")  
            else:
                canvas.create_rectangle(x1, y1, x2, y2, outline="black")  


def draw_start_end():
    canvas.create_rectangle(player_position[0] * cell_size, player_position[1] * cell_size,
                            player_position[0] * cell_size + cell_size, player_position[1] * cell_size + cell_size,
                            fill="green")
    canvas.create_rectangle(final_destination[0] * cell_size, final_destination[1] * cell_size,
                            final_destination[0] * cell_size + cell_size, final_destination[1] * cell_size + cell_size,
                            fill="red")



restart_button = tk.Button(window, text="Restart", command=restart_game, state="disabled")
restart_button.pack(side="left", padx=20)

exit_button = tk.Button(window, text="Exit", command=exit_game)
exit_button.pack(side="left", padx=20)

destination_label = tk.Label(window, text="", font=("Arial", 21))
destination_label.pack(side="left", padx=250) #text telling you which building to find
player_name = get_player_name()
if player_name:
    display_welcome_message(player_name)
    choose_final_destination()
    draw_grid()
    draw_start_end()
    player = canvas.create_oval(
        player_position[0] * cell_size + 10, player_position[1] * cell_size + 10,
        player_position[0] * cell_size + cell_size - 10, player_position[1] * cell_size + cell_size - 10,
        fill="blue"
    )


start_time = time.time()


def update_timer():
    if attempts>=10:
        return
    elapsed_time = time.time() - start_time
    timer_label.config(text=f"Time: {elapsed_time:.2f}s")
    window.after(100, update_timer)


update_timer()


window.bind("<Key>", handle_keypress)


window.mainloop()
