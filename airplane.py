# airplane.py
import turtle
import math  # Import math module
import time  # Import time module for shooting cooldowns
from const import * 
from bullet import Bullet 
from ball import Ball

# Initialize score
score = 0

# Create a turtle to display the score
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(-SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 - 40)
score_display.color("black")
score_display.write(f"Score: {score}", align="left", font=("Arial", 14, "normal"))

def update_score(points):
    """Update the player's score."""
    global score
    score += points
    score_display.clear()
    score_display.write(f"Score: {score}", align="left", font=("Arial", 14, "normal"))

def handle_explosion(x, y):
    """Handle explosion animation at (x, y)."""
    explosion_turtle = turtle.Turtle()
    explosion_turtle.hideturtle()
    explosion_turtle.penup()
    explosion_turtle.goto(x, y)
    explosion_turtle.shape("circle")
    explosion_turtle.color("red")
    explosion_turtle.shapesize(stretch_wid=2, stretch_len=2)
    explosion_turtle.showturtle()

    # Simple fade-out effect
    for i in range(5):
        explosion_turtle.shapesize(stretch_wid=2 + i, stretch_len=2 + i)
        explosion_turtle.color("red", "yellow")  # Change color for effect
        time.sleep(0.05)  # Short delay
    explosion_turtle.hideturtle()

class Airplane:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int], shape: str, health: int, size=20):
        self.size = size  # Added size attribute
        self._position = position
        self._velocity = velocity
        self._shape = shape
        self._health = health

        # Initialize turtle for the airplane
        self._turtle = turtle.Turtle()
        self._turtle.shape(shape)
        self._turtle.penup()
        self._turtle.goto(self._position)
        self._turtle.shapesize(stretch_wid=self.size / 10, stretch_len=self.size / 10)  # Adjust based on size
        self._turtle.showturtle()

        # List to hold active bullets
        self._bullets = []

    @property 
    def position(self):
        return self._position

    @position.setter
    def position(self, position: tuple[int, int]):
        self._position = position
        self._turtle.goto(self._position)

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    def move(self):
        """Update the position of the airplane based on its velocity."""
        new_x = self._position[0] + self._velocity[0]
        new_y = self._position[1] + self._velocity[1]
        self._position = (new_x, new_y)
        self._turtle.goto(self._position)

    def take_damage(self, amount: int):
        """Reduce the health of the airplane."""
        self._health -= amount
        if self._health <= 0:
            self.destroy()

    def destroy(self):
        """Handle airplane destruction."""
        self._turtle.hideturtle()
        print(f"{self._shape} airplane destroyed!")
        # Optional: Trigger explosion animation here if allowed

    def add_bullet(self, bullet: Bullet):
        """Add a bullet to the active bullets list."""
        self._bullets.append(bullet)

    def update_bullets(self, target):
        """Update all active bullets."""
        for bullet in self._bullets[:]:  # Iterate over a copy to allow removal
            bullet.update(0.1)  # dt = 0.1
            if target is not None and bullet.check_collision(target):
                bullet.hide_bullet()
                self._bullets.remove(bullet)
                target.take_damage(1)  # Assuming target has take_damage
                # Trigger explosion at enemy's position
                handle_explosion(target.x, target.y)
                # Update score
                update_score(10)
            else:
                # Check if bullet is off-screen
                if not (-SCREEN_WIDTH / 2 < bullet.x < SCREEN_WIDTH / 2 and
                        -SCREEN_HEIGHT / 2 < bullet.y < SCREEN_HEIGHT / 2):
                    bullet.hide_bullet()
                    self._bullets.remove(bullet)

    def draw_bullets(self):
        """Draw all active bullets."""
        for bullet in self._bullets:
            bullet.draw()

class PlayerAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self._is_up_pressed = False
        self._is_left_pressed = False
        self._is_right_pressed = False
        self._is_down_pressed = False
        self._is_space_pressed = False
        self.last_shot_time = 0
        self.shot_cooldown = 0.3  # 300 milliseconds between shots

    def press_up(self):
        self._is_up_pressed = True

    def release_up(self):
        self._is_up_pressed = False

    def press_down(self):
        self._is_down_pressed = True

    def release_down(self):
        self._is_down_pressed = False

    def press_left(self):
        self._is_left_pressed = True

    def release_left(self):
        self._is_left_pressed = False

    def press_right(self):
        self._is_right_pressed = True

    def release_right(self):
        self._is_right_pressed = False

    def press_space(self):
        current_time = time.time()
        if (not self._is_space_pressed) and (current_time - self.last_shot_time > self.shot_cooldown):
            self._is_space_pressed = True
            # Create a new bullet at the airplane's current position
            bullet = Bullet(
                x=self.x,
                y=self.y + self.size + 5,  # Slightly above the airplane
                vy=15,          # Upward velocity
                owner=PLAYER
            )
            self.add_bullet(bullet)
            self.last_shot_time = current_time

    def release_space(self):
        self._is_space_pressed = False

    def move_airplane(self):
        """Update position based on keypresses."""
        dx, dy = 0, 0

        # Diagonal Up-Left
        if self._is_up_pressed and self._is_left_pressed and self.y < SCREEN_HEIGHT / 2 - self.size and self.x > -SCREEN_WIDTH / 2 + self.size:
            dy += 5
            dx -= 5

        # Diagonal Up-Right
        if self._is_up_pressed and self._is_right_pressed and self.y < SCREEN_HEIGHT / 2 - self.size and self.x < SCREEN_WIDTH / 2 - self.size:
            dy += 5
            dx += 5

        # Diagonal Down-Left
        if self._is_down_pressed and self._is_left_pressed and self.y > -SCREEN_HEIGHT / 2 + self.size and self.x > -SCREEN_WIDTH / 2 + self.size:
            dy -= 5
            dx -= 5

        # Diagonal Down-Right
        if self._is_down_pressed and self._is_right_pressed and self.y > -SCREEN_HEIGHT / 2 + self.size and self.x < SCREEN_WIDTH / 2 - self.size:
            dy -= 5
            dx += 5

        # Move up
        if self._is_up_pressed and self.y < SCREEN_HEIGHT / 2 - self.size:
            dy += 5

        # Move down
        if self._is_down_pressed and self.y > -SCREEN_HEIGHT / 2 + self.size:
            dy -= 5

        # Move left
        if self._is_left_pressed and self.x > -SCREEN_WIDTH / 2 + self.size:
            dx -= 5

        # Move right
        if self._is_right_pressed and self.x < SCREEN_WIDTH / 2 - self.size:
            dx += 5

        new_x = self.x + dx
        new_y = self.y + dy

        # Update position if within boundaries
        if -SCREEN_WIDTH / 2 < new_x < SCREEN_WIDTH / 2 and -SCREEN_HEIGHT / 2 < new_y < SCREEN_HEIGHT / 2:
            self.position = (new_x, new_y)

    def update(self, target):
        """Update the airplane and its bullets."""
        self.move_airplane()
        self.update_bullets(target)

class EnemyAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self.last_shot_time = 0
        self.shot_cooldown = 1.0  # Enemy shoots every 1 second

    def move_enemy_airplane(self):
        """Move the enemy airplane downward."""
        new_x, new_y = self.x, self.y - 2  # Move downward
        if new_y < -SCREEN_HEIGHT / 2 + self.size:
            new_y = SCREEN_HEIGHT / 2 - self.size  # Reset to the top slightly inside the screen
        self.position = (new_x, new_y)

    def handle_shooting(self, target):
        """Handle enemy shooting logic."""
        current_time = time.time()
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            # Create a bullet aimed at the player's current position
            dx = target.x - self.x
            dy = target.y - self.y
            angle = math.atan2(dy, dx)
            vx = math.cos(angle) * 10  # Bullet speed
            vy = math.sin(angle) * 10
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,  # Slightly below the enemy
                vx=vx,
                vy=vy,
                color=RED,
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def update(self, target):
        """Update the enemy airplane and handle collisions."""
        self.move_enemy_airplane()
        self.update_bullets(target)
        self.handle_shooting(target)  # Implement enemy shooting logic

def setup_screen():
    """Set up the game screen."""
    screen = turtle.Screen()
    screen.title("Airplane and Bullet Shooting")
    screen.bgcolor(SKYBLUE)
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.register_shape("AIRPLANE.gif")      # Ensure this file exists
    screen.register_shape("AIRPLANE_4.gif")    # Ensure this file exists
    turtle.tracer(0)                           # Disable auto-screen updates
    turtle.hideturtle()                        # Hide the main turtle
    return screen

def setup_airplane():
    """Create and return the player airplane."""
    airplane = PlayerAirplane(position=(0, -150), velocity=(0, 0), shape="AIRPLANE.gif", health=3, size=20)
    return airplane

def setup_enemy_airplane():
    """Create and return the enemy airplane."""
    enemy_airplane = EnemyAirplane(position=(0, 150), velocity=(0, 0), shape="AIRPLANE_4.gif", health=3, size=20)
    return enemy_airplane

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

# Main program
if __name__ == "__main__":
    # Set up the screen
    screen = setup_screen()

    # Set up the airplanes
    player = setup_airplane()
    enemy = setup_enemy_airplane()

    # Bind key press and release events
    screen.listen()
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

    # Start the game loop
    game_loop()

    # Keep the window open
    screen.mainloop()
