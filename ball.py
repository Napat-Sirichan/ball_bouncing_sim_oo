# ball.py
import turtle
import math
import time
from const import SCREEN_WIDTH, SCREEN_HEIGHT, ORANGE, RED

class Ball:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int], shape: str, color: str, health: int, size=20):
        """
        Initialize a Ball object.

        Args:
            position (tuple[int, int]): (x, y) position of the ball.
            velocity (tuple[int, int]): (vx, vy) velocity of the ball.
            shape (str): Shape of the turtle.
            color (str): Color of the ball.
            health (int): Health points of the ball.
            size (int, optional): Size of the ball. Defaults to 20.
        """
        self.size = size
        self.position = position
        self.velocity = velocity
        self.shape = shape
        self.color = color
        self.health = health

        # Initialize turtle for the ball
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(color)
        self.turtle.penup()
        self.turtle.goto(self.position)
        self.turtle.shapesize(stretch_wid=self.size / 10, stretch_len=self.size / 10)
        self.turtle.showturtle()

        # List to hold active bullets (if applicable)
        self.bullets = []

    def move(self):
        """Update the position of the ball based on its velocity."""
        new_x = self.position[0] + self.velocity[0]
        new_y = self.position[1] + self.velocity[1]
        self.position = (new_x, new_y)
        self.turtle.goto(self.position)

    def draw(self):
        """Draw the ball on the screen."""
        self.turtle.goto(self.position)
        self.turtle.showturtle()

    def take_damage(self, amount: int):
        """Reduce the health of the ball."""
        self.health -= amount
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        """Handle ball destruction."""
        self.turtle.hideturtle()
        print(f"{self.shape} object destroyed at position {self.position}!")
        # Trigger explosion animation if needed
        self.explosion(self.position[0], self.position[1])
        self.respawn()

    def explosion(self, x, y):
        """Display explosion animation at (x, y)."""
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

    def add_bullet(self, bullet):
        """Add a bullet to the active bullets list."""
        self.bullets.append(bullet)

    def update_bullets(self, target, update_score_callback=None):
        """
        Update all active bullets.

        Args:
            target (Ball): The target ball to check collisions with.
            update_score_callback (function, optional): Callback function to update the score. Defaults to None.
        """
        for bullet in self.bullets[:]:  # Iterate over a copy to allow removal
            bullet.move()
            if check_collision(bullet, target):
                bullet.hide_bullet()
                self.bullets.remove(bullet)
                target.take_damage(1)  # Assuming target has take_damage
                handle_explosion(target.x, target.y)
                if update_score_callback and self.color == ORANGE:  # Assuming ORANGE is PLAYER
                    update_score_callback(10)
                if self.color == ORANGE:  # If player destroyed enemy
                    target.respawn()
            else:
                # Check if bullet is off-screen
                if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    bullet.hide_bullet()
                    self.bullets.remove(bullet)

    def draw_bullets(self):
        """Draw all active bullets."""
        for bullet in self.bullets:
            bullet.draw()

    def respawn(self):
        """Respawn the ball at initial position or designated respawn point."""
        # To be implemented based on specific game logic
        pass

# Utility function for collision
def check_collision(obj1, obj2):
    """Check if two objects have collided."""
    distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
    return distance < (obj1.size + obj2.size)
