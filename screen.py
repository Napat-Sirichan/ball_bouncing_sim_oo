import turtle
import tkinter as tk
import random
import time
from const import *  
from airplane import *
from mystery import *  

screen = turtle.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("Loading Screen")
screen.bgcolor("#000000")
screen.tracer(0)
loading_turtle = turtle.Turtle()
loading_turtle.hideturtle()
loading_turtle.penup()
loading_turtle.color("white")
loading_turtle.goto(0, 0)
loading_turtle.write("Loading... Please enter your username", align="center", font=("Arial", 16, "normal"))
screen.update()
username = screen.textinput("Login", "Please enter your username:")
loading_turtle.clear()
screen.clear()  
screen.title("Seamless Scrolling Background with Two Images")
screen.bgcolor("#3696d5")
screen.tracer(0) 
canvas = screen.getcanvas()

bg_images = []
for path in BG_IMAGE_PATHS:
    img = tk.PhotoImage(file=path)
    bg_images.append(img)

bg_width = bg_images[0].width()
bg_height = bg_images[0].height()
bg_ids = []
last_score_used_to_spawn = -1 
x_position = (SCREEN_WIDTH - bg_width) // 2 - 300

for i in range(len(bg_images)):
    bg_id = canvas.create_image(x_position, i * bg_height, anchor='nw', image=bg_images[i])
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
    screen.ontimer(scroll_background, FPS)  

def spawn_mystery_ball():
    """Randomly spawn a mystery ball and drop it from the top."""
    mystery_types = [1, 2, 3] 
    mystery_type = random.choice(mystery_types)
    mystery_ball = MysteryBall(20, random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50), SCREEN_HEIGHT // 2 - 50, 0, -5, "red", mystery_type)
    return mystery_ball



def spawn_enemy():
    """Spawn a new enemy airplane with a random shape."""
    shapes = ["AIRPLANE_2.gif", "AIRPLANE_3.gif", "AIRPLANE_4.gif", "AIRPLANE_5.gif"]
    random_shape = random.choice(shapes)
    
    while True:
        x_position = random.randint(-SCREEN_WIDTH//2 + 50, SCREEN_WIDTH//2 - 50)  
        y_position = SCREEN_HEIGHT // 2 - 50 
        
        overlap = False
        for enemy in enemies:
            if abs(x_position - enemy.x) < enemy.size * 2 and abs(y_position - enemy.y) < enemy.size * 2:
                overlap = True
                break
        if not overlap:
            new_enemy = EnemyAirplane((x_position, y_position), (0, 0), random_shape, 3, size=40)
            return new_enemy

screen.register_shape("AIRPLANE.gif")
p = PlayerAirplane((0, 0), (5, 5), "AIRPLANE.gif", 3, size=40)

enemies = []
mystery_balls = []

for _ in range(random.randint(1, 3)):
    enemies.append(spawn_enemy())

def game_loop():
    global last_score_used_to_spawn  
    p.update(target=enemies)  
    
    for ball in mystery_balls[:]:
        ball.move()  

        if p.distance(ball) < p.size + ball.size:  
            ball.activate_ability(p)  
            mystery_balls.remove(ball)  

    for enemy in enemies[:]:  
        enemy.update(target=p)

        if enemy._is_destroyed:
            enemies.remove(enemy)
            p.score += 1 

    if not enemies:
        for _ in range(random.randint(1, 3)):  
            enemies.append(spawn_enemy())

    if p.score % 5 == 0 and p.score != last_score_used_to_spawn: 
        mystery_balls.append(spawn_mystery_ball())
        last_score_used_to_spawn = p.score 

    for ball in mystery_balls[:]:
        if not ball.is_ability_active(p):
            mystery_balls.remove(ball)

    if p._is_space_pressed:
        p.shoot() 

    screen.update()  
    screen.ontimer(game_loop, FPS)  

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

scroll_background()
game_loop()

turtle.mainloop()
