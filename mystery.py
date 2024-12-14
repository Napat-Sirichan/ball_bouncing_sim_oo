import random
import time
from ball import *
from airplane import *
from bullet import *

class MysteryBall(Ball):
    def __init__(self, size, x, y, vx, vy, color, type):
        super().__init__(size, x, y, vx, vy, color)
        self.type = type  # Type of the MysteryBall (1, 2, or 3)
        self.time_collected = None  # Time when the ability was collected

        # Register the mystery ball images
        if self.type == 1:
            self._shape = "MYSTERY_BALL1.gif"
        elif self.type == 2:
            self._shape = "MYSTERY_BALL2.gif"
        elif self.type == 3:
            self._shape = "MYSTERY_BALL3.gif"

        # Register the image before using it in shape
        self.turtle.screen.register_shape(self._shape)

        # Set the shape of the ball
        self.turtle.shape(self._shape)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)  # Set the initial position

    def move(self):
        """Move the mystery ball downwards."""
        self.y += self.vy  # Move downward
        self.turtle.clear()  # Clear previous position
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)  # Update the position

    def is_off_screen(self):
        """Check if the ball has moved off-screen (below the bottom of the screen)."""
        return self.y < -SCREEN_HEIGHT / 2

    def activate_ability(self, player):
        """Activate the ability of the mystery ball based on type."""
        if self.type == 1:  # Tri-directional shooting
            self._hide_ball()
            player.activate_tridirectional_shooting()
            print("Ability Activated: Tri-Directional Shooting!")
        elif self.type == 2:  # Increase bullet size
            self._hide_ball()
            player.increase_health()  # Increase health instead of bullet size
            print("Ability Activated: Increased Health!")
        elif self.type == 3:  # Double movement speed
            self._hide_ball()
            player.double_speed()
            print("Ability Activated: Double Speed!")

        self.time_collected = time.time()  # Store the time when ability is activated

    def is_ability_active(self, player):
        """Check if the ability should still be active (lasts for 5 seconds)."""
        if self.time_collected and (time.time() - self.time_collected) > 5:
            player.deactivate_ability()
            return False
        return True

    def _hide_ball(self):
        """Hide the ball after collection or after it goes off-screen."""
        self.turtle.hideturtle()  # Hide the turtle
        self.turtle.clear()  # Clear any trail left by the turtle 

