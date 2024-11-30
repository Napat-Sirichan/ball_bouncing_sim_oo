import turtle
import random

# Screen boundaries
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Ball properties
xpos = []
ypos = []
vx = []
vy = []
ball_color = []
ball_radius = 10  # Radius of each ball
num_balls = 0  # Counter for balls

# Time step for motion
dt = 1  # Smaller value for smoother motion

# Variables to track key states
is_up_pressed = False
is_left_pressed = False
is_right_pressed = False
is_down_pressed = False
is_space_pressed = False  # Track the Spacebar state


def draw_ball(color, size, x, y):
    """Draw a ball at (x, y) with a specified color and size."""
    # Normalize the RGB color to 0-1 range
    normalized_color = (color[0] / 255, color[1] / 255, color[2] / 255)

    turtle.penup()
    turtle.goto(x, y - size)
    turtle.pendown()
    turtle.color(normalized_color)
    turtle.fillcolor(normalized_color)
    turtle.begin_fill()
    turtle.circle(size)
    turtle.end_fill()
    turtle.penup()


def move_ball(index):
    """Move the ball based on its velocity and update position."""
    global xpos, ypos, vx, vy

    xpos[index] += vx[index] * dt
    ypos[index] += vy[index] * dt

    # Handle boundary collisions (reverse velocity when hitting walls)
    # if abs(xpos[index]) > (SCREEN_WIDTH // 2 - ball_radius):
    #     vx[index] = -vx[index]
    # if abs(ypos[index]) > (SCREEN_HEIGHT // 2 - ball_radius):
    #     vy[index] = -vy[index]


# Function to set up the screen
def setup_screen():
    screen = turtle.Screen()
    screen.title("Airplane and Ball Shooting")
    screen.bgcolor("skyblue")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.register_shape("AIRPLANE.gif")  # Register the airplane shape
    screen.register_shape("AIRPLANE_3.gif")
    turtle.tracer(0)  # Disable auto-screen updates
    turtle.hideturtle()  # Hide the main turtle
    return screen


# Function to create and return the airplane turtle
def setup_airplane():
    airplane = turtle.Turtle()
    airplane.shape("AIRPLANE.gif")  # Default shape is right-facing
    airplane.penup()  # Lift the pen to prevent drawing lines
    return airplane


def setup_enemy_airplane():
    enemy_airplane = turtle.Turtle()
    enemy_airplane.shape("AIRPLANE_3.gif")  # Default shape
    enemy_airplane.penup()  # Lift the pen to prevent drawing lines
    enemy_airplane.goto(100, 200)  # Position the enemy airplane
    return enemy_airplane

# Key press handlers
def press_up():
    global is_up_pressed
    is_up_pressed = True


def release_up():
    global is_up_pressed
    is_up_pressed = False


def press_left():
    global is_left_pressed
    is_left_pressed = True


def release_left():
    global is_left_pressed
    is_left_pressed = False


def press_right():
    global is_right_pressed
    is_right_pressed = True


def release_right():
    global is_right_pressed
    is_right_pressed = False


def press_down():
    global is_down_pressed
    is_down_pressed = True


def release_down():
    global is_down_pressed
    is_down_pressed = False


def press_space():
    global is_space_pressed, xpos, ypos, vx, vy, ball_color, num_balls

    is_space_pressed = True

    # Create a new ball at the airplane's position
    x, y = airplane.position()
    xpos.append(x)
    ypos.append(y)
    vx.append(0)  # Random x velocity
    vy.append(10)  # Random y velocity
    ball_color.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    num_balls += 1


def release_space():
    global is_space_pressed
    is_space_pressed = False


# Function to update the airplane's movement
def move_airplane():
    global is_up_pressed, is_down_pressed, is_left_pressed, is_right_pressed

    x, y = airplane.position()  # Get current position

    # Diagonal Up-Left
    if is_up_pressed and is_left_pressed and y < SCREEN_HEIGHT / 2 - 10 and x > -SCREEN_WIDTH / 2 + 10:
        airplane.setheading(135)
        airplane.forward(5)

    # Diagonal Up-Right
    elif is_up_pressed and is_right_pressed and y < SCREEN_HEIGHT / 2 - 10 and x < SCREEN_WIDTH / 2 - 10:
        airplane.setheading(45)
        airplane.forward(5)

    # Diagonal Down-Left
    elif is_down_pressed and is_left_pressed and y > -SCREEN_HEIGHT / 2 + 10 and x > -SCREEN_WIDTH / 2 + 10:
        airplane.setheading(225)
        airplane.forward(5)

    # Diagonal Down-Right
    elif is_down_pressed and is_right_pressed and y > -SCREEN_HEIGHT / 2 + 10 and x < SCREEN_WIDTH / 2 - 10:
        airplane.setheading(315)
        airplane.forward(5)

    # Move up
    elif is_up_pressed and y < SCREEN_HEIGHT / 2 - 10:
        airplane.setheading(90)
        airplane.forward(5)

    # Move down
    elif is_down_pressed and y > -SCREEN_HEIGHT / 2 + 10:
        airplane.setheading(270)
        airplane.forward(5)

    # Move left
    elif is_left_pressed and x > -SCREEN_WIDTH / 2 + 10:
        airplane.setheading(180)
        airplane.forward(5)

    # Move right
    elif is_right_pressed and x < SCREEN_WIDTH / 2 - 10:
        airplane.setheading(0)
        airplane.forward(5)

def handle_explosion_step(frame=0):
    """Handle each step of the explosion animation."""
    global enemy_airplane

    explosion_images = ["EXPLOSION_1.gif", "EXPLOSION_2.gif", "EXPLOSION_3.gif", "EXPLOSION_4.gif"]
    
    # Check if we are still within the explosion sequence
    if frame < len(explosion_images):
        # Register and set the current frame's shape
        screen.register_shape(explosion_images[frame])
        enemy_airplane.shape(explosion_images[frame])
        screen.update()
        
        # Schedule the next frame
        screen.ontimer(lambda: handle_explosion_step(frame + 1), 200)  # 200ms delay for each frame
    else:
        # Hide the enemy airplane after the last frame
        enemy_airplane.hideturtle()

def check_collision_with_enemy():
    global xpos, ypos, enemy_airplane

    for i in range(num_balls):
        # Calculate distance between the ball and the enemy airplane
        ball_x, ball_y = xpos[i], ypos[i]
        enemy_x, enemy_y = enemy_airplane.position()
        distance = ((ball_x - enemy_x) ** 2 + (ball_y - enemy_y) ** 2) ** 0.5

        # Check if distance is less than collision threshold (radius of ball + approximate airplane radius)
        if distance < ball_radius + 20:  # Adjust 20 to the size of the airplane
            handle_explosion_step()  # Trigger explosion animation
            return True  # Stop checking further balls after a hit
    return False

def game_loop():
    global xpos, ypos, vx, vy, ball_color

    # Clear the screen
    turtle.clear()

    # Draw and move all balls
    for i in range(num_balls):
        draw_ball(ball_color[i], ball_radius, xpos[i], ypos[i])
        move_ball(i)

    # Check for collisions with the enemy airplane
    check_collision_with_enemy()

    # Update the airplane's movement
    move_airplane()

    # Update the screen and schedule the next frame
    turtle.update()
    screen.ontimer(game_loop, 16)  # Smooth motion at ~60 FPS

# Main program
if __name__ == "__main__":
    # Set up the screen
    screen = setup_screen()

    # Set up the airplane turtle
    airplane = setup_airplane()
    enemy_airplane = setup_enemy_airplane()

    # Bind key press and release events
    screen.onkeypress(press_up, "Up")
    screen.onkeyrelease(release_up, "Up")
    screen.onkeypress(press_left, "Left")
    screen.onkeyrelease(release_left, "Left")
    screen.onkeypress(press_right, "Right")
    screen.onkeyrelease(release_right, "Right")
    screen.onkeypress(press_down, "Down")
    screen.onkeyrelease(release_down, "Down")
    screen.onkeypress(press_space, "space")
    screen.onkeyrelease(release_space, "space")

    # Start listening to key events
    screen.listen()

    # Start the game loop
    game_loop()

    # Keep the window open
    screen.mainloop()