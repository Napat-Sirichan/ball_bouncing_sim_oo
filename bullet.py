import turtle
import math
import time 
from ball import Ball
import random

class Bullet(Ball):
    def __init__(self, size, x, y, vx, vy, color, id, owner):
        super().__init__(size, x, y, vx, vy, color, id)
        self.owner = owner

class Airplane:
    pass

# Initialize and run the game
# controller = TurtleController()
# controller.start()

