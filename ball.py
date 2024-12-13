# ball.py
import turtle
import math

class Ball:
    def __init__(self, size, x, y, vx, vy, color, id):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.id = id
        self.mass = 100 * size ** 2
        self.count = 0

        # Initialize a turtle for this ball
        self._turtle = turtle.Turtle()
        self._turtle.shape("circle")  # Default shape; can be overridden
        self._turtle.color(self.color)
        self._turtle.penup()
        self._turtle.goto(self.x, self.y)
        self._turtle.shapesize(stretch_wid=self.size / 10, stretch_len=self.size / 10)
        self._turtle.speed(0)  # Fastest animation
        self._turtle.showturtle()

    def draw(self):
        """Draw the ball using its turtle."""
        self._turtle.showturtle()
        self._turtle.goto(self.x, self.y)

    def move(self, dt):
        """Move the ball based on its velocity and update its turtle position."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self._turtle.goto(self.x, self.y)

    def distance(self, that):
        """Calculate the distance between this ball and another object."""
        return math.sqrt((self.x - that.x) ** 2 + (self.y - that.y) ** 2)

    def check_collision(self, that):
        """Check if this ball collides with another object."""
        return self.distance(that) < (self.size + that.size)

    def hide(self):
        """Hide the turtle representing the ball."""
        self._turtle.hideturtle()
