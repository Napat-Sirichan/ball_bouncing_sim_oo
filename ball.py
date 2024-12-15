# ball.py

import turtle
import math
from const import *


class Ball:
    def __init__(self, size, x, y, vx, vy, color):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100 * size ** 2
        self.count = 0
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        self.turtle = turtle.Turtle()
        self.turtle.penup()

    def bounce_off_vertical_wall(self):
        self.vx = -self.vx
        self.count += 1

    def bounce_off_horizontal_wall(self):
        self.vy = -self.vy
        self.count += 1

    def bounce_off(self, that):
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        dist = self.size + that.size

        magnitude = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)

        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        self.count += 1
        that.count += 1

    def distance(self, that):
        return math.sqrt((that.y - self.y) ** 2 + (that.x - self.x) ** 2)

    def time_to_hit(self, that):
        if self is that:
            return math.inf
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy
        if dvdr > 0:
            return math.inf
        dvdv = dvx ** 2 + dvy ** 2
        if dvdv == 0:
            return math.inf
        drdr = dx ** 2 + dy ** 2
        sigma = self.size + that.size
        d = (dvdr ** 2) - dvdv * (drdr - sigma ** 2)
        if d < 0:
            return math.inf
        t = -(dvdr + math.sqrt(d)) / dvdv
        return t if t > 0 else math.inf

    def time_to_hit_vertical_wall(self):
        if self.vx > 0:
            return (self.canvas_width - self.x - self.size) / self.vx
        elif self.vx < 0:
            return (self.canvas_width + self.x - self.size) / (-self.vx)
        return math.inf

    def time_to_hit_horizontal_wall(self):
        if self.vy > 0:
            return (self.canvas_height - self.y - self.size) / self.vy
        elif self.vy < 0:
            return (self.canvas_height + self.y - self.size) / (-self.vy)
        return math.inf

    def time_to_hit_paddle(self, paddle):
        if (self.vy > 0) and ((self.y + self.size) > (paddle.location[1] - paddle.height / 2)):
            return math.inf
        if (self.vy < 0) and ((self.y - self.size) < (paddle.location[1] + paddle.height / 2)):
            return math.inf

        dt = (math.sqrt((paddle.location[1] - self.y) ** 2) - self.size - paddle.height / 2) / abs(self.vy)
        paddle_left_edge = paddle.location[0] - paddle.width / 2
        paddle_right_edge = paddle.location[0] + paddle.width / 2
        if paddle_left_edge - self.size <= self.x + (self.vx * dt) <= paddle_right_edge + self.size:
            return dt
        return math.inf

    def bounce_off_paddle(self):
        self.vy = -self.vy
        self.count += 1

    def __str__(self):
        return f"{self.x}:{self.y}:{self.vx}:{self.vy}:{self.count}"
