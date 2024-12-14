# airplane.py
import turtle
from const import *
from bullet import Bullet
from utility import check_collision
import time
import math


class Airplane:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int], shape: str, health: int, size=20):
        self.size = size  
        self._position = position
        self._velocity = velocity
        self._health = health

        self._turtle = turtle.Turtle()
        self._turtle.shape(shape)
        self._turtle.penup()
        self._turtle.goto(self._position)
        self._turtle.showturtle()

        self._bullets = []

    @property 
    def position(self):
        return self._position

    @position.setter
    def position(self, position: tuple[int, int]):
        self._position = position
        self._turtle.goto(self._position)

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    def move(self):
        """Update the position of the airplane based on its velocity."""
        new_x = self._position[0] + self._velocity[0]
        new_y = self._position[1] + self._velocity[1]
        self._position = (new_x, new_y)
        self._turtle.goto(self._position)

    def take_damage(self, amount: int):
        """Reduce the health of the airplane."""
        self._health -= amount
        if self._health <= 0:
            self.destroy()

    def destroy(self):
        """Handle airplane destruction."""
        self._turtle.hideturtle()
        print(f"{self._shape} airplane destroyed!")
        # Trigger explosion animation
        # handle_explosion(self.x, self.y)
        # Optional: Respawn the airplane
        self.respawn()

    def add_bullet(self, bullet: Bullet):
        """Add a bullet to the active bullets list."""
        self._bullets.append(bullet)

    def update_bullets(self, target):
        """Update all active bullets."""
        for bullet in self._bullets[:]:  # Iterate over a copy to allow removal
            bullet.move()
            if check_collision(bullet, target):
                bullet.hide_bullet()
                self._bullets.remove(bullet)
                target.take_damage(1)  # Assuming target has take_damage
                # Trigger explosion at enemy's position
                handle_explosion(target.x, target.y)
                # Update score
                update_score(10)
                if self.owner == PLAYER:
                    target.respawn()
            else:
                # Check if bullet is off-screen
                if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    bullet.hide_bullet()
                    self._bullets.remove(bullet)

    def draw_bullets(self):
        """Draw all active bullets."""
        for bullet in self._bullets:
            bullet.turtle.showturtle()

class PlayerAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self._is_up_pressed = False
        self._is_left_pressed = False
        self._is_right_pressed = False
        self._is_down_pressed = False
        self._is_space_pressed = False
        self.last_shot_time = 0
        self.shot_cooldown = 0.3  # 300 milliseconds between shots

    def press_up(self):
        self._is_up_pressed = True

    def release_up(self):
        self._is_up_pressed = False

    def press_down(self):
        self._is_down_pressed = True

    def release_down(self):
        self._is_down_pressed = False

    def press_left(self):
        self._is_left_pressed = True

    def release_left(self):
        self._is_left_pressed = False

    def press_right(self):
        self._is_right_pressed = True

    def release_right(self):
        self._is_right_pressed = False

    def press_space(self):
        current_time = time.time()
        if (not self._is_space_pressed) and (current_time - self.last_shot_time > self.shot_cooldown):
            self._is_space_pressed = True
            # Create a new bullet at the airplane's current position
            bullet = Bullet(
                x=self.x,
                y=self.y + self.size + 5,  # Slightly above the airplane
                vx=0,
                vy=BULLET_SPEED,          # Upward velocity
                owner=PLAYER
            )
            self.add_bullet(bullet)
            self.last_shot_time = current_time

    def release_space(self):
        self._is_space_pressed = False

    def move_airplane_directional(self):
        """Update position based on keypresses."""
        dx, dy = 0, 0

        # Diagonal Up-Left
        if self._is_up_pressed and self._is_left_pressed and self.y < SCREEN_HEIGHT / 2 - self.size and self.x > -SCREEN_WIDTH / 2 + self.size:
            dy += PLAYER_SPEED
            dx -= PLAYER_SPEED

        # Diagonal Up-Right
        if self._is_up_pressed and self._is_right_pressed and self.y < SCREEN_HEIGHT / 2 - self.size and self.x < SCREEN_WIDTH / 2 - self.size:
            dy += PLAYER_SPEED
            dx += PLAYER_SPEED

        # Diagonal Down-Left
        if self._is_down_pressed and self._is_left_pressed and self.y > -SCREEN_HEIGHT / 2 + self.size and self.x > -SCREEN_WIDTH / 2 + self.size:
            dy -= PLAYER_SPEED
            dx -= PLAYER_SPEED

        # Diagonal Down-Right
        if self._is_down_pressed and self._is_right_pressed and self.y > -SCREEN_HEIGHT / 2 + self.size and self.x < SCREEN_WIDTH / 2 - self.size:
            dy -= PLAYER_SPEED
            dx += PLAYER_SPEED

        # Move up
        if self._is_up_pressed and self.y < SCREEN_HEIGHT / 2 - self.size:
            dy += PLAYER_SPEED

        # Move down
        if self._is_down_pressed and self.y > -SCREEN_HEIGHT / 2 + self.size:
            dy -= PLAYER_SPEED

        # Move left
        if self._is_left_pressed and self.x > -SCREEN_WIDTH / 2 + self.size:
            dx -= PLAYER_SPEED

        # Move right
        if self._is_right_pressed and self.x < SCREEN_WIDTH / 2 - self.size:
            dx += PLAYER_SPEED

        new_x = self.x + dx
        new_y = self.y + dy

        # Update position if within boundaries
        if -SCREEN_WIDTH / 2 < new_x < SCREEN_WIDTH / 2 and -SCREEN_HEIGHT / 2 < new_y < SCREEN_HEIGHT / 2:
            self.position = (new_x, new_y)

    def update(self, target):
        """Update the airplane and its bullets."""
        self.move_airplane_directional()
        self.update_bullets(target)

class EnemyAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self.last_shot_time = 0
        self.shot_cooldown = 1.0  # Enemy shoots every 1 second

    def move_enemy_airplane(self):
        """Move the enemy airplane downward."""
        new_x, new_y = self.x, self.y - ENEMY_SPEED  # Move downward
        if new_y < -SCREEN_HEIGHT / 2 + self.size:
            new_y = SCREEN_HEIGHT / 2 - self.size  # Reset to the top slightly inside the screen
        self.position = (new_x, new_y)

    def handle_shooting(self, target):
        """Handle enemy shooting logic."""
        current_time = time.time()
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            # Create a bullet aimed at the player's current position
            dx = target.x - self.x
            dy = target.y - self.y
            angle = math.atan2(dy, dx)
            vx = 0#math.cos(angle) * 10  # Bullet speed in x
            vy = -5#math.sin(angle) * 10  # Bullet speed in y
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,  # Slightly below the enemy
                vx=vx,
                vy=vy,
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def update(self, target):
        """Update the enemy airplane and handle collisions."""
        self.move_enemy_airplane()
        self.update_bullets(target)
        self.handle_shooting(target)  # Implement enemy shooting logic
