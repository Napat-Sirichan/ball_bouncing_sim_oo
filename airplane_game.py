# airplane_game.py
import turtle
from const import *
from airplane import *
import time
import os
import math

# ตั้งค่าหน้าจอ
screen = turtle.Screen()
screen.title("Airplane Shooting Game")
screen.bgcolor(SKYBLUE)
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)  # ปิดการอัปเดตอัตโนมัติ

# ลงทะเบียนรูปแบบ `.gif` สำหรับเครื่องบิน
def register_shapes():
    shapes = ["AIRPLANE.gif", "AIRPLANE_4.gif"]
    for shape in shapes:
        if os.path.exists(shape):
            screen.register_shape(shape)
        else:
            print(f"Warning: Shape file '{shape}' not found. Using default shape instead.")
            # คุณสามารถตั้งค่ารูปแบบเริ่มต้นหรือรูปแบบอื่นๆ แทนได้ เช่น "triangle"
            screen.register_shape("triangle")

register_shapes()

# สร้างเครื่องบินผู้เล่นและศัตรู
player = PlayerAirplane(
    position=(0, -SCREEN_HEIGHT/2 + 50),
    velocity=(0, 0),
    shape="AIRPLANE.gif",
    health=300,
    size=20
)

enemy = EnemyAirplane(
    position=(0, SCREEN_HEIGHT/2 - 50),
    velocity=(0, 0),
    shape="AIRPLANE_4.gif",
    health=3,
    size=20
)

# def handle_explosion(x, y):
#     """Handle explosion animation at (x, y)."""
#     explosion_turtle = turtle.Turtle()
#     explosion_turtle.hideturtle()
#     explosion_turtle.penup()
#     explosion_turtle.goto(x, y)
#     explosion_turtle.shape("circle")
#     explosion_turtle.color("red")
#     explosion_turtle.shapesize(stretch_wid=2, stretch_len=2)
#     explosion_turtle.showturtle()

#     # Simple fade-out effect
#     for i in range(5):
#         explosion_turtle.shapesize(stretch_wid=2 + i, stretch_len=2 + i)
#         explosion_turtle.color("red", "yellow")  # Change color for effect
#         time.sleep(0.05)  # Short delay
#     explosion_turtle.hideturtle()

# สร้างแสดงคะแนน
score = 0
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(-SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 - 40)
score_display.color("black")
score_display.write(f"Score: {score}", align="left", font=("Arial", 14, "normal"))

def update_score_display(points):
    """Update the player's score."""
    global score
    score += points
    score_display.clear()
    score_display.write(f"Score: {score}", align="left", font=("Arial", 14, "normal"))

# เปลี่ยนฟังก์ชัน update_score ใน airplane.py ให้เรียก update_score_display ในที่นี้

player.update_score = update_score_display

def move_up():
    player.press_up()

def move_down():
    player.press_down()

def move_left():
    player.press_left()

def move_right():
    player.press_right()

def release_up():
    player.release_up()

def release_down():
    player.release_down()

def release_left():
    player.release_left()

def release_right():
    player.release_right()

def shoot():
    player.press_space()

def release_space():
    player.release_space()

# กำหนดการกดปุ่ม
screen.listen()
screen.onkeypress(move_up, "Up")
screen.onkeyrelease(release_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeyrelease(release_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeyrelease(release_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeyrelease(release_right, "Right")
screen.onkeypress(shoot, "space")
screen.onkeyrelease(release_space, "space")

def game_loop():
    """Main game loop to update game state."""
    # Update player and enemy airplanes
    player.update(enemy)
    enemy.update(player)  # Enemy shooting logic is handled here

    # Draw bullets
    player.draw_bullets()
    enemy.draw_bullets()

    # Update the screen
    screen.update()

    # Schedule the next frame
    screen.ontimer(game_loop, 16)  # Approximately 60 FPS

# เริ่มเกม

game_loop()

# รอจนกว่าจะปิดหน้าจอ
screen.mainloop()
