import turtle
import tkinter as tk
from const import *  # Make sure SCREEN_WIDTH, SCREEN_HEIGHT, and BG_IMAGE_PATHS are defined here
import airplane as A

SCROLL_SPEED = 6  # Adjust scroll speed to a smoother rate

# Step 1: Create the main screen and show loading
screen = turtle.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("Loading Screen")
screen.bgcolor("#000000")
screen.tracer(0)

# Display a loading message
loading_turtle = turtle.Turtle()
loading_turtle.hideturtle()
loading_turtle.penup()
loading_turtle.color("white")
loading_turtle.goto(0, 0)
loading_turtle.write("Loading... Please enter your username", align="center", font=("Arial", 16, "normal"))

screen.update()

# Step 2: Prompt for username
username = screen.textinput("Login", "Please enter your username:")

# Once user input is received, clear the loading message
loading_turtle.clear()

# Step 3: Transition to scrolling background
screen.clear()  # Clear the loading screen turtles and text
screen.title("Seamless Scrolling Background with Two Images")
screen.bgcolor("#3696d5")
screen.tracer(0)  # Disable automatic updates to make the scroll smoother

# Access the Tkinter canvas inside the turtle screen
canvas = screen.getcanvas()

# Load background images
bg_images = []
for path in BG_IMAGE_PATHS:
    img = tk.PhotoImage(file=path)
    bg_images.append(img)

bg_width = bg_images[0].width()
bg_height = bg_images[0].height()

bg_ids = []

# Calculate the x-position to center the images and shift them left by 150 pixels if needed
x_position = (SCREEN_WIDTH - bg_width) // 2 - 300

# Place the background images
for i in range(len(bg_images)):
    bg_id = canvas.create_image(x_position, i * bg_height, anchor='nw', image=bg_images[i])
    bg_ids.append(bg_id)

def scroll_background():
    # Loop over each background image
    for bg_id in bg_ids:
        # Move the background down smoothly
        canvas.move(bg_id, 0, SCROLL_SPEED)
        x, y = canvas.coords(bg_id)
        
        # If the image scrolls past the bottom, move it to the top
        if y >= SCREEN_HEIGHT:  # If it goes beyond the bottom of the screen
            # Find the highest y-coordinate and place the image back at the top
            max_y = min([canvas.coords(b)[1] for b in bg_ids])
            canvas.coords(bg_id, x_position, max_y - bg_height)

    screen.update()  # Update the screen
    screen.ontimer(scroll_background, FPS)  # Set the timer for 30 FPS (33ms per frame)

# Start the scrolling background
screen.register_shape("AIRPLANE.gif") 
player = A.PlayerAirplane(position=(0, -150), velocity=(0, 0), shape="AIRPLANE.gif", health=3)

def game_loop():
    player.move()  # Make the player move
    screen.update()  # Update the screen
    screen.ontimer(game_loop, FPS)  # Run the game loop at 30 FPS (33ms per frame)

# Handle player controls
screen.onkeypress(player.press_up, "Up")
screen.onkeyrelease(player.release_up, "Up")
screen.onkeypress(player.press_down, "Down")
screen.onkeyrelease(player.release_down, "Down")
screen.onkeypress(player.press_left, "Left")
screen.onkeyrelease(player.release_left, "Left")
screen.onkeypress(player.press_right, "Right")
screen.onkeyrelease(player.release_right, "Right")
screen.onkeypress(player.press_space, "space")
screen.onkeyrelease(player.release_space, "space")
screen.listen()

# Start background scrolling and game loop
scroll_background()
game_loop()

# Keep the window open
turtle.mainloop()