from const import *
from ball import Ball

class Bullet(Ball):
    def __init__(self, x, y, vx, vy, owner):
        color = ORANGE if owner == PLAYER else RED
        super().__init__(size=5, x=x, y=y, vx=vx, vy=vy, color=color)
        self.turtle.setheading(90 if owner == PLAYER else 270)

    def hide_bullet(self):
        """Hide the bullet from the screen."""
        self.turtle.hideturtle()

    def is_off_screen(self):
        """Check if the bullet has gone off-screen."""
        return not (-self.canvas_width / 2 < self.x < self.canvas_width / 2 and -self.canvas_height / 2 < self.y < self.canvas_height / 2)

    def move(self):
        """Override move for Bullet-specific movement."""
        self.x += self.vx
        self.y += self.vy
        self.turtle.goto(self.x, self.y)

    def draw(self):
        """Override draw for Bullet-specific rendering."""
        self.turtle.penup()
        self.turtle.color(self.color)
        self.turtle.fillcolor(self.color)
        self.turtle.goto(self.x, self.y - self.size)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(self.size)
        self.turtle.end_fill()

    def __str__(self):
        return f"Bullet at ({self.x}, {self.y}) with velocity ({self.vx}, {self.vy})"
