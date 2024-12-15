import turtle
import tkinter as tk
import random
from const import *
from airplane import PlayerAirplane, EnemyAirplane
from mystery import MysteryBall
from bullet import Bullet

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
loading_turtle.write(
    "Loading... Please enter your username",
    align="center",
    font=("Arial", 16, "normal")
)
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
screen.register_shape(HEART_FULL)
screen.register_shape(HEART_BROKE)

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
    bg_id = canvas.create_image(
        x_position, i * bg_height, anchor='nw', image=bg_images[i]
    )
    bg_ids.append(bg_id)


def scroll_background():
    """Move the background images down smoothly."""
    for bg_id in bg_ids:
        canvas.move(bg_id, 0, SCROLL_SPEED)
        x, y = canvas.coords(bg_id)
        if y >= SCREEN_HEIGHT:
            max_y = min([canvas.coords(b)[1] for b in bg_ids])
            canvas.coords(bg_id, x_position, max_y - bg_height)
    screen.update()
    screen.ontimer(scroll_background, int(1000 / FPS))


# Player initialization
screen.register_shape(PLAYER_PIC)
player = PlayerAirplane(
    position=(0, 0),
    velocity=(5, 5),
    shape=PLAYER_PIC,
    health=3,
    size=40
)

# Function to display text on the screen
display_turtle = turtle.Turtle()
display_turtle.hideturtle()
display_turtle.penup()

# สร้าง Turtle สำหรับแสดงข้อความ Game Over
game_over_turtle = turtle.Turtle()
game_over_turtle.hideturtle()
game_over_turtle.penup()


def display_text(x, y, text, font=("Arial", 20, "normal")):
    display_turtle.goto(x, y)
    display_turtle.write(text, font=font)


# Score management
score_text = None  # Global variable to store the score text turtle


def display_score():
    global score_text
    if score_text:
        score_text.clear()
    score_text = turtle.Turtle()
    score_text.hideturtle()
    score_text.penup()
    score_text.color(WHITE)
    score_text.goto(0, 250)
    score_text.write(
        f"{username} Score: {player.score}",
        align="center",
        font=("Arial", 20, "normal")
    )


# Function to display health (hearts)
def health_ui():
    display_turtle.clear()

    health = max(0, min(player._health, 3))  # Clamp health between 0 and 3
    hearts = [HEART_FULL] * health + [HEART_BROKE] * (3 - health)
    for i, heart in enumerate(hearts):
        display_image(-200 + i * 40, -300, heart)


def display_image(x, y, image_shape):
    display_turtle.goto(x, y)
    display_turtle.shape(image_shape)
    display_turtle.stamp()


# Function to create mystery ball
def spawn_mystery_ball():
    """Randomly spawn a mystery ball and drop it from the top."""
    mystery_types = [MYSTERY_BALL1, MYSTERY_BALL2, MYSTERY_BALL3]
    mystery_type = random.choice(mystery_types)
    mystery_ball = MysteryBall(
        size=20,
        x=random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50),
        y=SCREEN_HEIGHT // 2 - 50,
        vx=0,
        vy=-5,
        color="red",
        ball_type=mystery_type
    )
    mystery_balls.append(mystery_ball)


# Game loop
last_score_used_to_spawn = -1
enemies = []
mystery_balls = []


def spawn_enemy():
    shapes = [AIRPLANE_2, AIRPLANE_3, AIRPLANE_4, AIRPLANE_5]
    random_shape = random.choice(shapes)
    while True:
        x_pos = random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50)
        y_pos = SCREEN_HEIGHT // 2 - 50
        overlap = False
        for enemy in enemies:
            if abs(x_pos - enemy.x) < enemy.size * 2 and abs(y_pos - enemy.y) < enemy.size * 2:
                overlap = True
                break
        if not overlap:
            new_enemy = EnemyAirplane(
                position=(x_pos, y_pos),
                velocity=(0, 0),
                shape=random_shape,
                health=3,
                size=40
            )
            enemies.append(new_enemy)
            break


def display_game_over():
    screen.bgcolor(GAME_OVER_BG_COLOR)
    game_over_turtle.goto(0, 0)
    game_over_turtle.color(GAME_OVER_COLOR)
    game_over_turtle.write(
        GAME_OVER_TEXT,
        align="center",
        font=GAME_OVER_FONT
    )
    health_ui()  # แสดงหัวใจแตกทั้งหมด


def game_loop():
    global last_score_used_to_spawn

    player.update(enemies)

    if player._health <= 0:
        display_game_over()
        return

    health_ui()
    display_score()

    for ball in mystery_balls[:]:
        ball.move()
        if player.distance(ball) < player.size + ball.size:
            ball.activate_ability(player)
            mystery_balls.remove(ball)
        elif ball.is_off_screen():
            ball._hide_ball()
            mystery_balls.remove(ball)  # ลบจากรายการเพื่อป้องกันไม่ให้เกิดซ้ำ

    for enemy in enemies[:]:
        enemy.update(player)
        if enemy._is_destroyed:
            enemies.remove(enemy)
            player.score += 1

    if not enemies:
        for _ in range(random.randint(1, 3)):
            spawn_enemy()

    if player.score % 5 == 0 and player.score != last_score_used_to_spawn:
        spawn_mystery_ball()
        last_score_used_to_spawn = player.score

    screen.update()
    screen.ontimer(game_loop, int(1000 / FPS))

if __name__ == "__main__" : 

    # Keyboard bindings
    screen.onkeypress(player.press_up, "Up")
    screen.onkeyrelease(player.release_up, "Up")
    screen.onkeypress(player.press_left, "Left")
    screen.onkeyrelease(player.release_left, "Left")
    screen.onkeypress(player.press_right, "Right")
    screen.onkeyrelease(player.release_right, "Right")
    screen.onkeypress(player.press_down, "Down")
    screen.onkeyrelease(player.release_down, "Down")
    screen.onkeypress(player.press_space, "space")
    screen.onkeyrelease(player.release_space, "space")
    screen.listen()

    # Start the game
    scroll_background()
    game_loop()

    turtle.mainloop()
