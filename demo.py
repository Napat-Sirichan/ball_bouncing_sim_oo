import turtle
import random

# Screen boundaries
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400



# Variables to track key states
is_up_pressed = False
is_left_pressed = False
is_right_pressed = False
is_down_pressed = False
is_space_pressed = False  # Track the Spacebar state


# Function to set up the screen
def setup_screen():
    screen = turtle.Screen()
    screen.title("Airplane and Ball Shooting")
    screen.bgcolor("skyblue")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.register_shape("AIRPLANE.gif")  # Register the airplane shape
    turtle.colormode(255)  # Enable RGB color mode
    return screen


# Function to create and return the airplane turtle
def setup_airplane():
    airplane = turtle.Turtle()
    airplane.shape("AIRPLANE.gif")  # Default shape is right-facing
    airplane.penup()  # Lift the pen to prevent drawing lines
    return airplane


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
    global is_space_pressed
    is_space_pressed = True


def release_space():
    global is_space_pressed
    is_space_pressed = False


# Function to update the airplane's movement
def move_airplane():
    global is_up_pressed, is_down_pressed, is_left_pressed, is_right_pressed, is_space_pressed, balls

    x, y = airplane.position()  # Get current position

    # Handle Spacebar movement (create a ball)
    if is_space_pressed:
        pass

    # Diagonal Up-Left
    if is_up_pressed and is_left_pressed and y < SCREEN_HEIGHT / 2 - 10 and x > -SCREEN_WIDTH / 2 + 10:
        airplane.setheading(135)  # 135 degrees for Up-Left
        airplane.forward(15)

    # Diagonal Up-Right
    elif is_up_pressed and is_right_pressed and y < SCREEN_HEIGHT / 2 - 10 and x < SCREEN_WIDTH / 2 - 10:
        airplane.setheading(45)  # 45 degrees for Up-Right
        airplane.forward(15)

    # Diagonal Down-Left
    elif is_down_pressed and is_left_pressed and y > -SCREEN_HEIGHT / 2 + 10 and x > -SCREEN_WIDTH / 2 + 10:
        airplane.setheading(225)  # 225 degrees for Down-Left
        airplane.forward(15)

    # Diagonal Down-Right
    elif is_down_pressed and is_right_pressed and y > -SCREEN_HEIGHT / 2 + 10 and x < SCREEN_WIDTH / 2 - 10:
        airplane.setheading(315)  # 315 degrees for Down-Right
        airplane.forward(15)

    # Move up
    elif is_up_pressed and y < SCREEN_HEIGHT / 2 - 10:  # Check upper boundary
        airplane.setheading(90)
        airplane.forward(15)

    # Move down
    elif is_down_pressed and y > -SCREEN_HEIGHT / 2 + 10:  # Check lower boundary
        airplane.setheading(270)
        airplane.forward(15)

    # Move left
    elif is_left_pressed and x > -SCREEN_WIDTH / 2 + 10:  # Check left boundary
        airplane.setheading(180)
        airplane.forward(15)

    # Move right
    elif is_right_pressed and x < SCREEN_WIDTH / 2 - 10:  # Check right boundary
        airplane.setheading(0)
        airplane.forward(15)

    # Schedule the next update
    screen.ontimer(move_airplane, 1)  # Adjust the timer for smoothness


# Main program
if __name__ == "__main__":
    # Set up the screen
    screen = setup_screen()

    # Set up the airplane turtle
    airplane = setup_airplane()

    # Bind key press and release events
    screen.onkeypress(press_up, "Up")
    screen.onkeyrelease(release_up, "Up")
    screen.onkeypress(press_left, "Left")
    screen.onkeyrelease(release_left, "Left")
    screen.onkeypress(press_right, "Right")
    screen.onkeyrelease(release_right, "Right")
    screen.onkeypress(press_down, "Down")
    screen.onkeyrelease(release_down, "Down")
    screen.onkeypress(press_space, "space")  # Spacebar press for creating balls
    screen.onkeyrelease(release_space, "space")  # Spacebar release to reset

    # Start listening to key events
    screen.listen()

    # Start the movement loop
    move_airplane()

    # Keep the window open
    screen.mainloop()