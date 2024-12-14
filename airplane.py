# airplane.py
import turtle
from const import *
from bullet import *
import time
import math


class Airplane:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int], shape: str, health: int, size=40):
        self.size = size
        self._shape = shape
        self._position = position
        self._velocity = velocity
        self._health = health

        self._turtle = turtle.Turtle()
        self._turtle.penup()
        self._turtle.screen.register_shape(shape)
        self._turtle.shape(shape)
        self._turtle.penup()
        self._turtle.goto(self._position)
        self._turtle.showturtle()

        self._bullets = []

        # Explosion-related variables
        self._explosion_images = [
            "EXPLOSION_1.gif", "EXPLOSION_2.gif", "EXPLOSION_3.gif", "EXPLOSION_4.gif"]
        self._explosion_frame = 0
        self._is_destroyed = False  # Flag to check if the airplane is destroyed

        # Explosion Turtle (temporary object for explosions)
        self._explosion_turtle = turtle.Turtle()
        self._explosion_turtle.hideturtle()

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

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, other):
        self._turtle.register_shape(other)
        self._turtle.shape(other)

    def move(self):
        """Update the position of the airplane based on its velocity."""
        new_x = self._position[0] + self._velocity[0]
        new_y = self._position[1] + self._velocity[1]
        self._position = (new_x, new_y)
        self._turtle.goto(self._position)

    def take_damage(self, amount: int):
        """Reduce the health of the airplane."""
        if self._is_destroyed:
            return  # Prevent damage after destruction

        self._health -= amount
        if self._health <= 0:
            self.destroy()

    def destroy(self):
        """Handle airplane destruction."""
        self._is_destroyed = True  # Set destroyed flag
        self._turtle.hideturtle()  # Hide the airplane turtle
        self._turtle.clear()  # Remove any trail or line left by the airplane

        # Handle the explosion sequence
        self._handle_explosion_step()

        # Print out the message and ensure the screen is clean
        print(f"{self._shape} airplane destroyed!")
        # Clear the screen and any lingering traces of the turtle
        self._turtle.getscreen().update()  # Ensure screen is updated after destruction
        self._explosion_turtle.clear()  # Clear any explosion remnants

    def _check_bullet_collision(self, bullet, target):
        """Check for bullet collision with target airplane."""
        if bullet.distance(target) < target.size + bullet.size:
            return True
        return False

    def _handle_explosion_step(self):
        """Handle each step of the explosion animation."""
        self._explosion_turtle.penup()  # Make sure the explosion turtle does not leave a trail
        self._turtle.clear()  # Clear any trails left by the main airplane turtle

        if self._explosion_frame < len(self._explosion_images):
            # Register and set the current frame's shape for the explosion
            self._explosion_turtle.screen.register_shape(
                self._explosion_images[self._explosion_frame])
            self._explosion_turtle.shape(
                self._explosion_images[self._explosion_frame])
            # Position explosion at airplane's location
            self._explosion_turtle.goto(self._position)
            self._explosion_turtle.showturtle()
            self._explosion_frame += 1

            # Schedule the next frame after 200ms
            self._explosion_turtle.screen.ontimer(
                self._handle_explosion_step, 200)
        else:
            # After the explosion sequence ends, hide the airplane and explosion turtle
            self._explosion_turtle.hideturtle()
            self._turtle.hideturtle()  # Ensure the main airplane is hidden after explosion

    def add_bullet(self, bullet: 'Bullet'):
        """Add a bullet to the active bullets list."""
        self._bullets.append(bullet)

    def update_bullets(self, target):
        """Update all active bullets."""
        for bullet in self._bullets[:]:  # Iterate over a copy to allow removal
            bullet.move()
            if self._check_bullet_collision(bullet, target):
                bullet.hide_bullet()
                self._bullets.remove(bullet)
                target.take_damage(1)
                # Update score
                # self.update_score(10)
                if self.owner == PLAYER:
                    target.respawn()
            else:
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

        self._turtle.penup()  # ยกปากกา
        self._turtle.goto(self._position)  # ย้ายเครื่องบินไปตำแหน่งที่กำหนด
        self._turtle.showturtle()  # แสดงเต่า

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
        self._is_space_pressed = True
        # สร้างกระสุนใหม่ที่ตำแหน่งของเครื่องบิน
        bullet = Bullet(
            x=self.x,
            y=self.y + self.size + 5,  # อยู่เหนือเครื่องบินเล็กน้อย
            vx=0,
            vy=BULLET_SPEED,           # ความเร็วในการเคลื่อนที่
            owner=PLAYER
        )
        self.add_bullet(bullet)

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
        if -SCREEN_WIDTH / 2 + self.size < new_x < SCREEN_WIDTH / 2 - self.size and -SCREEN_HEIGHT / 2 + self.size < new_y < SCREEN_HEIGHT / 2 - self.size:
            self.position = (new_x, new_y)

        # Print the new position
        print(f"Player Airplane Position - X: {new_x}, Y: {new_y}")

        turtle.update()

    def update(self, target):
        """Update the airplane and its bullets."""
        self.move_airplane_directional()
        self.update_bullets(target)

    def update_bullets(self, enemies):
        """Update all active bullets and check for collision with all enemies."""
        for bullet in self._bullets[:]:
            bullet.move()  # Move the bullet

            # Check collision with all enemies
            for enemy in enemies:
                if self._check_bullet_collision(bullet, enemy):
                    self.handle_bullet_collision(bullet, enemy)
                    break  # Stop checking further once the bullet hits an enemy

            # If the bullet goes off screen, remove it
            if bullet.is_off_screen():
                bullet.hide_bullet()
                self._bullets.remove(bullet)

    def handle_bullet_collision(self, bullet, target):
        """Handle the effect of a bullet collision."""
        target.take_damage(10)  # Reduce the health of the target
        bullet.hide_bullet()  # Hide the bullet
        self._bullets.remove(bullet)  # Remove bullet from the list


class EnemyAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self.last_shot_time = 0
        self.shot_cooldown = 1.0  # Enemy shoots every 1 second

    def move_enemy_airplane(self):
        """Move the enemy airplane downward."""
        new_x, new_y = self.x, self.y - ENEMY_SPEED  # Move downward
        if new_y < -SCREEN_HEIGHT / 2 + self.size:
            self.position = (new_x, SCREEN_HEIGHT / 2 -
                             self.size)  # Reset to the top
        else:
            self.position = (new_x, new_y)

    def handle_shooting(self, target):
        """Handle enemy shooting logic only if the enemy is not destroyed."""
        if self._is_destroyed:  # If the enemy is destroyed, stop shooting
            return

        current_time = time.time()
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            # Create a bullet aimed at the player's current position
            dx = target.x - self.x
            dy = target.y - self.y
            angle = math.atan2(dy, dx)
            vx = 0  # Bullet speed in x
            vy = -5  # Bullet speed in y
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,  # Slightly below the enemy
                vx=vx,
                vy=vy,
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def destroy(self):
        """Handle enemy destruction, including removing all its bullets."""
        self._is_destroyed = True
        self._turtle.hideturtle()  # Hide the enemy airplane turtle
        self._turtle.clear()  # Remove any trail or line left by the airplane

        # Remove all bullets associated with this enemy
        for bullet in self._bullets[:]:
            bullet.hide_bullet()  # Hide the bullet
            self._bullets.remove(bullet)  # Remove the bullet from the list

        # Handle the explosion sequence
        self._handle_explosion_step()

        # Print out the message and ensure the screen is clean
        print(f"{self._shape} airplane destroyed!")
        self._turtle.getscreen().update()  # Ensure screen is updated after destruction
        self._explosion_turtle.clear()  # Clear any explosion remnants

    def update(self, target):
        """Update the enemy airplane and handle collisions."""
        if not self._is_destroyed:  # Only update movement and shooting if the airplane is not destroyed
            self.move_enemy_airplane()
            self.update_bullets(target)
            self.handle_shooting(target)
        else:
            # Even when destroyed, update bullets so they keep moving
            self.update_bullets(target)

    def update_bullets(self, target):
        """Update all active bullets and handle collisions."""
        for bullet in self._bullets[:]:  # Iterate over a copy of the list to avoid modification during iteration
            bullet.move()
            if bullet.is_off_screen():
                bullet.hide_bullet()
                self._bullets.remove(bullet)  # Remove bullet if off-screen
            else:
                if self.check_bullet_collision(bullet, target):
                    self.handle_bullet_collision(bullet, target)

    def check_bullet_collision(self, bullet, target):
        """Check for bullet collision with target airplane."""
        if bullet.distance(target) < target.size + bullet.size:
            return True
        return False

    def handle_bullet_collision(self, bullet, target):
        """Handle the effect of a bullet collision."""
        target.take_damage(10)  # Reduce the health of the target
        bullet.hide_bullet()  # Hide the bullet
        self._bullets.remove(bullet)  # Remove bullet from the li

    def remove_bullets(self):
        """Remove all bullets associated with this enemy when destroyed."""
        for bullet in self._bullets:
            bullet.hide_bullet()  # Hide bullet from the screen
        self._bullets.clear()  # Clear the list of bullets
