import random
import time
from const import *
from ball import Ball
from airplane import PlayerAirplane


class MysteryBall(Ball):
    def __init__(self, size, x, y, vx, vy, color, ball_type):
        super().__init__(size, x, y, vx, vy, color)
        self.type = ball_type
        self.time_collected = None

        self._shape = f"MYSTERY_BALL{self.type}.gif"
        self.turtle.screen.register_shape(self._shape)
        self.turtle.shape(self._shape)
        self.turtle.goto(self.x, self.y)

    def move(self):
        self.y += self.vy
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)

    def is_off_screen(self):
        return self.y < -SCREEN_HEIGHT / 2

    def activate_ability(self, player: PlayerAirplane):
        if self.type == MYSTERY_BALL1:
            player.activate_tridirectional_shooting()
        elif self.type == MYSTERY_BALL2:
            player.increase_health()
        elif self.type == MYSTERY_BALL3:
            player.double_speed()
        self.time_collected = time.time()
        self._hide_ball()  # ซ่อน MysteryBall หลังจากเก็บรวบรวม

    def is_ability_active(self, player: PlayerAirplane):
        if self.time_collected and (time.time() - self.time_collected) > MYSTERY_BALL_LIFETIME:
            player.deactivate_ability()
            return False
        return True

    def _hide_ball(self):
        self.turtle.hideturtle()
        self.turtle.clear()
