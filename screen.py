import turtle
import tkinter as tk
import random
from const import *
from airplane import *
from mystery import *

# Initial Setup
screen = turtle.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("Loading Screen")
screen.bgcolor(BLACK)
screen.tracer(0)

# Display loading screen
loading_turtle = turtle.Turtle()
loading_turtle.hideturtle()
loading_turtle.penup()
loading_turtle.color(WHITE)
loading_turtle.goto(0, 0)
loading_turtle.write("Loading... Please enter your username", align="center", font=("Arial", 16, "normal"))
screen.update()

# Get username input
username = screen.textinput("Login", "Please enter your username:")
loading_turtle.clear()
screen.clear()

# Game Setup
screen.title("Airplane Shooting Game")
screen.bgcolor(SKYBLUE)
screen.tracer(0)
canvas = screen.getcanvas()

# Register image shapes
heart_full = "HEART_FULL.gif"
heart_broke = "HEART_BROKE.gif"
screen.register_shape(heart_full)
screen.register_shape(heart_broke)

bg_images = []
for path in BG_IMAGE_PATHS:
    img = tk.PhotoImage(file=path)
    bg_images.append(img)

bg_width = bg_images[0].width()
bg_height = bg_images[0].height()
bg_ids = []
x_position = (SCREEN_WIDTH - bg_width) // 2 - 300

# Load background images
for i in range(len(bg_images)):
    bg_id = canvas.create_image(x_position, i * bg_height, anchor='nw', image=bg_images[i])
    bg_ids.append(bg_id)

# Function to scroll the background
def scroll_background():
    """Move the background images down smoothly."""
    for bg_id in bg_ids:
        canvas.move(bg_id, 0, SCROLL_SPEED)
        x, y = canvas.coords(bg_id)
        if y >= SCREEN_HEIGHT:
            max_y = min([canvas.coords(b)[1] for b in bg_ids])
            canvas.coords(bg_id, x_position, max_y - bg_height)
    screen.update()
    screen.ontimer(scroll_background, FPS)

# Player initialization
screen.register_shape(PLAYER_PIC)
p = PlayerAirplane((0, 0), (5, 5), PLAYER_PIC, 3, size=40)

# Function to display text on the screen (using one turtle object)
display_turtle = turtle.Turtle()
display_turtle.hideturtle()
display_turtle.penup()
display_turtle.color(WHITE)

def display_text(x, y, text, font=("Arial", 20, "normal")):
    display_turtle.goto(x, y)
    display_turtle.clear()  # Clear old text before drawing new text
    display_turtle.write(text, font=font)

# Score management
def display_score():
    # Display username at a fixed position (static text)
    display_turtle.goto(0, 270)  # Positioning the username at the top
    display_turtle.clear()
    display_turtle.write(f"Player: {username}", align="center", font=("Arial", 16, "normal"))

    # Display score at a fixed position
    display_turtle.goto(0, 250)  # Adjust the score position lower than the username
    display_turtle.write(f"Score: {p.score}", align="center", font=("Arial", 20, "normal"))

# Function to display health (hearts)
def display_image(x, y, image_shape):
    display_turtle.goto(x, y)
    display_turtle.shape(image_shape)
    display_turtle.stamp()  # Display the image

# ฟังก์ชันเพื่อสร้าง mystery ball
def spawn_mystery_ball():
    """Randomly spawn a mystery ball and drop it from the top."""
    mystery_types = [1, 2, 3] 
    mystery_type = random.choice(mystery_types)
    mystery_ball = MysteryBall(20, random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50), SCREEN_HEIGHT // 2 - 50, 0, -5, "red", mystery_type)
    return mystery_ball

# Game loop
last_score_used_to_spawn = -1
enemies = []
mystery_balls = []

def spawn_enemy():
    shapes = ENEMY_PIC
    random_shape = random.choice(shapes)
    while True:
        x_position = random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50)
        y_position = SCREEN_HEIGHT // 2 - 50
        overlap = False
        for enemy in enemies:
            if abs(x_position - enemy.x) < enemy.size * 2 and abs(y_position - enemy.y) < enemy.size * 2:
                overlap = True
                break
        if not overlap:
            new_enemy = EnemyAirplane((x_position, y_position), (0, 0), random_shape, 3, size=40)
            return new_enemy

def game_loop():
    global last_score_used_to_spawn

    # Update player position
    p.update(target=enemies)

    # Update health and score UI
    display_score()  # Update the score and username display

    # Check and update mystery balls
    for ball in mystery_balls[:]:
        ball.move()
        if p.distance(ball) < p.size + ball.size:
            ball.activate_ability(p)
            mystery_balls.remove(ball)

    # Update enemies
    for enemy in enemies[:]:
        enemy.update(target=p)
        if enemy._is_destroyed:
            enemies.remove(enemy)
            p.score += 1  # Increase score when enemy is destroyed

    # Spawn new enemies if there are none
    if not enemies:
        for _ in range(random.randint(1, 3)):
            enemies.append(spawn_enemy())

    # Spawn mystery balls when score reaches multiples of 5
    if p.score % 5 == 0 and p.score != last_score_used_to_spawn:
        mystery_balls.append(spawn_mystery_ball())
        last_score_used_to_spawn = p.score

    # Remove unused mystery balls
    for ball in mystery_balls[:]:
        if not ball.is_ability_active(p):
            mystery_balls.remove(ball)

    # Check if space is pressed for shooting
    if p._is_space_pressed:
        p.shoot()

    screen.update()
    screen.ontimer(game_loop, FPS)  # Loop every frame

# Keyboard bindings
screen.onkeypress(p.press_up, "Up")
screen.onkeyrelease(p.release_up, "Up")
screen.onkeypress(p.press_left, "Left")
screen.onkeyrelease(p.release_left, "Left")
screen.onkeypress(p.press_right, "Right")
screen.onkeyrelease(p.release_right, "Right")
screen.onkeypress(p.press_down, "Down")
screen.onkeyrelease(p.release_down, "Down")
screen.onkeypress(p.press_space, "space")
screen.onkeyrelease(p.release_space, "space")
screen.listen()

# Start the game
scroll_background()
game_loop()
screen.tracer(0)
turtle.mainloop()
