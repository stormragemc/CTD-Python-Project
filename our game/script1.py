import tkinter as tk
from tkinter.ttk import Style, Button
from tkinter import simpledialog, messagebox
import requests
import random
import time  
from copy import deepcopy
#initialize the variables
window = tk.Tk() #assign tkinter UI window
window.title("Maze Navigator") #title of UI window
style = Style() #for clue button style
grid_size = 20   #20x20 grid
cell_size = 25  #25 pixel cell size
player_position = [0, 0] #starting position of player
attempts = 0  #what round
total_time = 0  #initialize total time taken to complete the game
player = None #initialize player state
final_destination = None #initialize final destination
final_destination_name = None #initialize final destination's name
walls = [(0, 13),(0, 14), (1, 10), (1, 11), (1, 12),(1,13),(1,14),(2,10),(2,11),(2,12),(2,13),(2,14),(2,16),(2,17),(3,12),(3,13),(3,14),(3,16),(3,17),(3,18),(4,12),(4,13),(4,14),(4,16),(4,17),(4,18),(5,6),(5,7),(5,8),(5,9),(6,12),(6,13),(6,14),(6,16),(6,17),(6,18),(7,9),(7,11),(7,12),(7,13),(7,14),(7,16),(7,17),(7,18),(8,7),(8,9),(9,3),(10,1),(10,4),(10,8),(10,12),(10,13),(10,14),(11,11),(11,14),(12,6),(13,0),(13,3),(13,7),(14,1),(14,4),(15,2),(15,5),(15,9),(16,3),(16,9),(16,10),(17,7),(18,8),(18,10),(18,11),(18,12),(19,5),(19,6),(19,10),(19,11)]
#Obstacles position coordinates
getStarURL = requests.get('https://i.ibb.co/JpyHGwB/star.png') #make HTTP request to acquire our web-hosted image URL
getStarURL.raise_for_status() 
with open("star.png", "wb") as file: #After url acquired, save the image into file
    file.write(getStarURL.content)
getbgImageURL = requests.get('https://i.ibb.co/r3gDFzx/bgImage.png')
getbgImageURL.raise_for_status()
with open("bgImage.png", "wb") as file:
    file.write(getbgImageURL.content)
rawStar = tk.PhotoImage(file = 'star.png')
star = rawStar.subsample(10,10)
bgImage = tk.PhotoImage(file = 'bgImage.png')
resizedImage = bgImage.zoom(25,25).subsample(9,9)

timer_label = tk.Label(window, text="Time: 0s", font=("Arial", 12)) #label for the timer value
timer_label.pack(side="top", anchor="ne")

Locations = { #Coordinates of each important site's markers
     "Tang Zheng Tang Chinese Pavilion":  (10, 2),
    "Gym":  (16, 7) ,
    "T-lab":  (5, 15) ,
    "OneStop Centre":  (9, 15) ,
    "Albert Hong Lecture Theatre":  (5, 17) ,
    "Scrapyard":  (8,8) ,
    "Swimming pool":  (17,5) ,
    "Fab-Lab":  (6, 9) ,
    "Upper Changi MRT":  (2, 15) ,
    "D'Star Bistro":  (7, 15) ,
    "Campus Centre":  (8, 15) ,
    "Vending machines":  (5, 13),   
}   
Locations_clue = {"Tang Zheng Tang Chinese Pavilion" : "Building is between housing blocks",  #Clue for each location
             "Gym" : "Look to the far right",
             "T-lab": "Building 2 area",
             "OneStop Centre" : "Inside the Campus Centre",
             "Albert Hong Lecture Theatre" : "Building 1 Area",
             "Scrapyard" : "Located within the Fab Lab Area",
             "Swimming pool" : "Sports and Recreation Area",
             "Fab-Lab" : "Find Building 5",
             "Upper Changi MRT" : "The leftmost location",
             "D'Star Bistro": "The path between Building 1 and 2",
             "Campus Centre" : "The site that connects the three main buildings",
             "Vending machines" : "Come to our Canteen"} #dictionary for clues

BackupLocationsDictionary = deepcopy(Locations) #backup dictionary so when Locations gets popped all other values are maintained using this backup 

style.configure('clue.TButton', font =("Courier New", 15, 'bold'),foreground = 'red') #font style for clue button
canvas = tk.Canvas(window, width=grid_size * cell_size, height=grid_size * cell_size)  #use canvas from tkinter
canvas.pack() #renders canvas into GUI

def get_player_name():
    name = simpledialog.askstring("Player Name", "Hello there Player, what is your name?")
    return name



def display_welcome_message(name):
    popup = tk.Toplevel(window) #popup instructions on how to play the game
    popup.geometry("400x200")
    label = tk.Label(popup, text="", wraplength=350, justify="left", padx=10, pady=10)
    label.pack(expand=True, fill="both")
    messages = [
        (
            "Welcome to the Game!",
            f"Hello {name}, welcome to our game of navigating through SUTD.\n\n"
            "This game was made possible by Srihari, Zhi Ying, Marcel, Kris, and Sherelle.\n\n"
            "You will be navigating through the world-class SUTD campus, located in the heart of Singapore's innovation district.\n\n P.S: Press Spacebar to skip Instructions"
        ),
        (
            "Controls",
            "You can navigate using W to go up, S to go down, A to go left, and D to go right.\n\n"
            "To quit the game, you can press ESC at any time."
        ),
        (
            "Gameplay",
            "We will give you a description of a specific location, and you will have to make your way there.\n\n"
            "If you reach the wrong spot, a clue will be given to guide you."
        ),
        (
            "Start the Adventure",
            f"Enjoy your adventure ahead, {name}!"
        )
    ]
    # Initialize the pop-up window with the first message
    index =0 #use index to define the sequence of popup messages
    title, message = messages[index] #get the message title and content from the tuple within the list
    popup.title(title)
    label.config(text=message)
    def on_spacebar(event):
        popup.destroy()  # Close the pop-up immediately when spacebar is pressed
    def on_enter(event):
        nonlocal index  # To access the index variable from the outer scope
        index += 1
        if index < len(messages):  # Check if we still have messages to show
            title, message = messages[index]
            popup.title(title)
            label.config(text=message)
        else:
            popup.destroy()  # Close the pop-up when all messages have been shown
    
    # Start cycling through messages automatically after 2 seconds

   
    #click button to manually cycle through messages
    def on_button_click():
        nonlocal index
        if index < len(messages):
            title, message = messages[index]
            popup.title(title)
            label.config(text=message)
            index += 1
        else:
            popup.destroy()  # Close the pop-up when all messages have been shown

    # Create a button to manually cycle through messages
    button = tk.Button(popup, text="Next", command=on_button_click)
    button.pack(pady=10)

    # Bind spacebar to immediately close the pop-up
    popup.bind("<space>", on_spacebar) 
    popup.bind("<Return>", on_enter)
    
    #Close the popup when the window is closed using the close button
    popup.protocol("WM_DELETE_WINDOW", popup.destroy)

def get_clue():
    clue = Locations_clue[final_destination_name] #loop final destination clue to keep getting new clue for every round
    messagebox.showinfo("Clue", f"{clue}\n")

def choose_final_destination():
    global final_destination, final_destination_name
    final_destination_name = random.choice(list(Locations.keys()))
    final_destination = Locations[final_destination_name] 
    Locations.pop(final_destination_name) #prevent the same location from being used as a final destination more than once a round
    destination_label.config(text=f"Find: {final_destination_name}")
    return final_destination_name

def update_player_position():
    canvas.coords(player, 
                  player_position[0] * cell_size + 10, 
                  player_position[1] * cell_size + 10,
                  player_position[0] * cell_size + cell_size - 10, 
                  player_position[1] * cell_size + cell_size - 10)
    if tuple(player_position) in  BackupLocationsDictionary.values() and tuple(player_position) != final_destination:
        for key, val in BackupLocationsDictionary.items():
            if val == tuple(player_position):
                messagebox.showinfo("Key Area", key)
    check_win_condition()

def check_win_condition():
    global attempts, total_time
    if tuple(player_position) == final_destination:
        end_time = time.time() - start_time
        total_time += end_time
        attempts += 1  # new round
        messagebox.showinfo("Congratulations!", f"You reached {final_destination_name}! You win!")
        canvas.create_text(
            grid_size * cell_size // 2,
            grid_size * cell_size // 2,
            text="You Win!",
            font=("Arial", 24),
            fill="green"
        )
        if attempts >= 3:
            messagebox.showinfo("Game Over", f"Total time: {total_time:.2f} seconds.\nClick Restart to play again.")
            Locations.clear()
            Locations.update(BackupLocationsDictionary)
            attempts = 0
            restart_button.config(state="normal")  # Enable restart button after 10 rounds
        else:
            restart_game()

def move_player(postal_code):
    global player_position
    moves = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
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
    if event.keysym == 'Escape':
        exit_game()
    move_player(event.char)

def restart_game():
    global player_position, player, start_time,total_time
    if attempts==0: #every time start over the game, reinitialize the total_time and start_time variables
        total_time =0 
        start_time = time.time()
        print('time has been reset') 
    update_timer()
    
    print(total_time)
    player_position = [0, 0]
    canvas.delete("all")
    choose_final_destination()
    draw_grid()
    draw_start_end()
    player = canvas.create_oval(
        player_position[0] * cell_size + 10, 
        player_position[1] * cell_size + 10,
        player_position[0] * cell_size + cell_size - 10, 
        player_position[1] * cell_size + cell_size - 10,
        fill = "blue"
    )
    messagebox.showinfo('', 'Round {}'.format(attempts + 1))
    start_time = time.time()  # Reset the timer to the current time
    timer_label.config(text="Time: 0s")  # Reset the timer display
    restart_button.config(state="disabled")  # Disable restart button when a new game starts

def exit_game():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        window.destroy()

def draw_grid():
    bg = canvas.create_image(0, 0, anchor=tk.NW, image=resizedImage)
    for i in range(grid_size):
        for j in range(grid_size):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if (i, j) in BackupLocationsDictionary.values():
                canvas.create_image(x1, y1, anchor="nw", image=star)
            else:
                canvas.create_rectangle(x1, y1, x2, y2, outline="black")
    
def draw_start_end():
    canvas.create_rectangle(player_position[0] * cell_size, 
                            player_position[1] * cell_size,
                            player_position[0] * cell_size + cell_size, 
                            player_position[1] * cell_size + cell_size,
                            fill="green")
    canvas.create_image(final_destination[0] * cell_size, 
                        final_destination[1] * cell_size, 
                        anchor = "nw", image = star)
Clue_button = Button(window, text="Clue", command=get_clue, style = 'clue.TButton') #generates clues for where the destination is
Clue_button.pack(side="left", padx=20)
restart_button = tk.Button(window, text="Restart", command=restart_game, state="disabled")
restart_button.pack(side="left", padx=20)
exit_button = tk.Button(window, text="Exit", command=exit_game)
exit_button.pack(side="left", padx=20)
destination_label = tk.Label(window, text="", font=("Arial", 21))
destination_label.pack(side="left", padx=250) #text telling you which building you should find to win the round
player_name = get_player_name()
if player_name:
    display_welcome_message(player_name)
    choose_final_destination()
    draw_grid()
    draw_start_end()
    
    player = canvas.create_oval(
        player_position[0] * cell_size + 10, 
        player_position[1] * cell_size + 10,
        player_position[0] * cell_size + cell_size - 10, 
        player_position[1] * cell_size + cell_size - 10,
        fill="blue"
    )

start_time = time.time()
def update_timer():
    if attempts>=10:
        
        return
    
     #stop the timer after 10 attempts
    elapsed_time = time.time() - start_time
    timer_label.config(text=f"Time: {elapsed_time:.2f}s")
    window.after(100, update_timer)
update_timer()

window.bind("<Key>", handle_keypress)

window.mainloop()
