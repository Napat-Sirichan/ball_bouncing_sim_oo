from const import *
from ball import Ball


class Bullet(Ball):
    def __init__(self, x, y, vx, vy, owner):
        color = ORANGE if owner == PLAYER else RED
        super().__init__(size=5, x=x, y=y, vx=vx, vy=vy, color=color)
        self.owner = owner
        self.turtle.setheading(90 if owner == PLAYER else 270)
        self.draw()

    def hide_bullet(self):
        self.turtle.clear()
        self.turtle.hideturtle()

    def is_off_screen(self):
        return not (-SCREEN_WIDTH / 2 < self.x < SCREEN_WIDTH / 2 and -SCREEN_HEIGHT / 2 < self.y < SCREEN_HEIGHT / 2)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.draw()

    def draw(self):
        self.turtle.color(self.color)
        self.turtle.fillcolor(self.color)
        self.turtle.goto(self.x, self.y - self.size)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(self.size)
        self.turtle.end_fill()
        self.turtle.hideturtle()

    def __str__(self):
        return f"Bullet at ({self.x}, {self.y}) with velocity ({self.vx}, {self.vy})"
