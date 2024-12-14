# bullet.py
import turtle
from const import *
from utility import check_collision

class Bullet:
    def __init__(self, x, y, vx, vy, owner):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = 5
        self.owner = owner
        self.color = ORANGE if owner == PLAYER else RED

        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(self.color)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.setheading(90 if owner == PLAYER else 270)
        self.turtle.showturtle()

    def move(self):
        """เคลื่อนที่ลูกกระสุนตามความเร็ว"""
        self.x += self.vx
        self.y += self.vy
        self.turtle.goto(self.x, self.y)

    def hide_bullet(self):
        """ซ่อนลูกกระสุนจากหน้าจอ"""
        self.turtle.hideturtle()

    def is_off_screen(self, screen_width, screen_height):
        """ตรวจสอบว่าลูกกระสุนออกนอกหน้าจอหรือไม่"""
        return not (-screen_width/2 < self.x < screen_width/2 and -screen_height/2 < self.y < screen_height/2)
