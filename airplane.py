# airplane.py
import turtle
from const import *
from bullet import *
import time
import math

class Airplane:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int], shape: str, health: int, size=20):
        self.size = size  
        self._shape = shape
        self._position = position
        self._velocity = velocity
        self._health = health

        self._turtle = turtle.Turtle()
        self._turtle.shape(shape)
        self._turtle.penup()
        self._turtle.goto(self._position)
        self._turtle.showturtle()

        self._bullets = []

        # Explosion-related variables
        self._explosion_images = ["EXPLOSION_1.gif", "EXPLOSION_2.gif", "EXPLOSION_3.gif", "EXPLOSION_4.gif"]
        self._explosion_frame = 0

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
        self._health -= amount
        if self._health <= 0:
            self.destroy()

    def destroy(self):
        """Handle airplane destruction."""
        self._handle_explosion_step()
        print(f"{self._shape} airplane destroyed!")

    def _handle_explosion_step(self):
        """Handle each step of the explosion animation."""
        if self._explosion_frame < len(self._explosion_images):
            # Register and set the current frame's shape
            self._turtle.screen.register_shape(self._explosion_images[self._explosion_frame])
            self._turtle.shape(self._explosion_images[self._explosion_frame])
            self._explosion_frame += 1

            # Schedule the next frame after 200ms
            self._turtle.screen.ontimer(self._handle_explosion_step, 200)
        else:
            # After the explosion sequence ends, hide the airplane
            self._turtle.hideturtle()

    def add_bullet(self, bullet: 'Bullet'):
        """Add a bullet to the active bullets list."""
        self._bullets.append(bullet)

    def update_bullets(self, target: 'Airplane'):
        """Update all active bullets."""


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
        # Create a new bullet at the airplane's current position
        bullet = Bullet(
            x=self.x,
            y=self.y + self.size + 5,  # Slightly above the airplane
            vx=0,
            vy=BULLET_SPEED,          # Upward velocity
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
        if -SCREEN_WIDTH / 2 < new_x < SCREEN_WIDTH / 2 and -SCREEN_HEIGHT / 2 < new_y < SCREEN_HEIGHT / 2:
            self.position = (new_x, new_y)

        turtle.update()

    def update(self, target):
        """Update the airplane and its bullets."""
        self.move_airplane_directional()
        self.update_bullets(target)

    def update_bullets(self, target):
        """Update all active bullets and handle collisions."""
        for bullet in self._bullets:
            bullet.move()
            if bullet.is_off_screen():
                bullet.hide_bullet()
                self._bullets.remove(bullet)  # Remove bullet from the list if it's off-screen
            else:
                # Check for collisions with target
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
            vx = 0 #math.cos(angle) * 10  # Bullet speed in x
            vy = -5  # Bullet speed in y
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

    def update_bullets(self, target):
        """Update all active bullets and handle collisions."""
        for bullet in self._bullets:
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
        self._bullets.remove(bullet)  # Remove bullet from the list
    
# Final fixed game loop function
def game_loop():
    p.move_airplane_directional()
    p.update(target=enemy)  # Update bullets and check for collisions
    screen.update()  # Manually update the screen
    screen.ontimer(game_loop, 16)  # Call this every 16ms


# Initialize the screen
screen = turtle.Screen()
screen.title("Airplane and Ball Shooting")
screen.bgcolor("skyblue")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.register_shape("AIRPLANE.gif")  # Register the airplane shape
screen.register_shape("AIRPLANE_4.gif")
turtle.tracer(0)  # Disable auto-screen updates
turtle.hideturtle()  # Hide the main turtle

# Initialize player airplane
p = PlayerAirplane((0, 0), (5, 5), "AIRPLANE.gif", 3, size=20)
enemy = EnemyAirplane((0, 100), (0, 0), "AIRPLANE_4.gif", 3, size=20)
# Setup key bindings
screen.onkeypress(p.press_up, "Up")
screen.onkeyrelease(p.release_up, "Up")
screen.onkeypress(p.press_left, "Left")
screen.onkeyrelease(p.release_left, "Left")
screen.onkeypress(p.press_right, "Right")
screen.onkeyrelease(p.release_right, "Right")
screen.onkeypress(p.press_down, "Down")
screen.onkeyrelease(p.release_down, "Down")
screen.onkeypress(p.press_space, "space")
screen.onkeyrelease(p.release_space, "space")

screen.listen()  # Start listening to key presses
game_loop()  # Start the game loop
screen.mainloop()  # Keep the window open
