# bullet.py
import turtle
import math
import const
from ball import Ball

class Bullet(Ball):
    def __init__(
        self,
        size=5,              # Smaller size for bullets
        x=0,                 # Initial x-coordinate
        y=0,                 # Initial y-coordinate
        vx=0,                # Velocity in the x-direction
        vy=10,               # Velocity in the y-direction (positive for upward)
        color=const.ORANGE,  # Bullet color
        id=0,                # Unique identifier
        owner=const.PLAYER,  # Owner of the bullet
    ):
        """
        Initialize a Bullet object inheriting from Ball.

        Args:
            size (int): Size of the bullet.
            x (int): Initial x-coordinate.
            y (int): Initial y-coordinate.
            vx (int): Velocity in the x-direction.
            vy (int): Velocity in the y-direction.
            color (str): Color of the bullet.
            id (int): Unique identifier.
            owner (int): Identifier for the owner (e.g., PLAYER or ENEMY).
        """
        super().__init__(size, x, y, vx, vy, color, id)
        self.owner = owner

        # Customize the turtle for bullets
        self._turtle.shape("triangle")  # Different shape for bullets
        self._turtle.setheading(90)      # Point upwards by default

    def update(self, dt):
        """Update bullet position."""
        self.move(dt)

    def hide_bullet(self):
        """Hide the bullet's turtle."""
        self.hide()
