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

        # Remove all bullets associated with this enemy
        self.remove_bullets()

        # Handle the explosion sequence
        self._handle_explosion_step()

        # Print out the message and ensure the screen is clean
        print(f"{self._shape} airplane destroyed!")
        # Clear the screen and any lingering traces of the turtle
        self._turtle.getscreen().update()  # Ensure screen is updated after destruction
        self._explosion_turtle.clear()  # Clear any explosion remnants

    def score(self): 
        self.score += 1

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

    def remove_bullets(self):
        """Remove all bullets associated with this enemy when destroyed."""
        for bullet in self._bullets:
            bullet.hide_bullet()  # Hide bullet from the screen
        self._bullets.clear()  # Clear the list of bullets



class PlayerAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self._is_up_pressed = False
        self._is_left_pressed = False
        self._is_right_pressed = False
        self._is_down_pressed = False
        self._is_space_pressed = False

        self._turtle.penup()
        self._turtle.goto(self._position)
        self._turtle.showturtle()

        # Abilities and settings
        self.is_tridirectional = False  # Flag for tri-directional shooting
        self.bullet_size = size  # Default bullet size
        self.speed_multiplier = 1  # Default speed multiplier
        self.last_shot_time = 0  # Last shot time for cooldown
        self.shot_cooldown = 0.2  # Cooldown time between shots (in seconds)
        self.score = 0  # Initialize score as an integer attribute
        self.ability_activation_time = 0 


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
        self.shoot()  # Trigger the shoot method when space is pressed

    def release_space(self):
        self._is_space_pressed = False

    def distance(self, other):
        """Calculate the distance between the player and another object."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

    def activate_tridirectional_shooting(self):
        """Activate tri-directional shooting ability."""
        self.is_tridirectional = True
        self.ability_activation_time = time.time()  # Store the time when ability is activated
        print("Tri-Directional Shooting Activated!")


    def increase_health(self):
        """Increase player's health."""
        self._health += 1  # Increase health by 10 points
        print(f"Health increased! Current health: {self._health}")

    def double_speed(self):
        """Increase the player's movement speed."""
        self.speed_multiplier = 1.8  # Increase speed multiplier to 1.4
        self.ability_activation_time = time.time()
        print("Speed Increased to 1.8x!")

    def deactivate_ability(self):
        """Deactivate the ability after 5 seconds."""
        self.is_tridirectional = False
        self.speed_multiplier = 1.0  # Reset speed multiplier to normal
        
        print("Abilities deactivated.")

    def move_airplane_directional(self):
        """Update position based on keypresses, considering speed multiplier."""
        dx, dy = 0, 0

        # Diagonal movement handling
        if self._is_up_pressed and self._is_left_pressed:
            dy += PLAYER_SPEED * self.speed_multiplier
            dx -= PLAYER_SPEED * self.speed_multiplier

        if self._is_up_pressed and self._is_right_pressed:
            dy += PLAYER_SPEED * self.speed_multiplier
            dx += PLAYER_SPEED * self.speed_multiplier

        if self._is_down_pressed and self._is_left_pressed:
            dy -= PLAYER_SPEED * self.speed_multiplier
            dx -= PLAYER_SPEED * self.speed_multiplier

        if self._is_down_pressed and self._is_right_pressed:
            dy -= PLAYER_SPEED * self.speed_multiplier
            dx += PLAYER_SPEED * self.speed_multiplier

        if self._is_up_pressed:
            dy += PLAYER_SPEED * self.speed_multiplier+0.5

        if self._is_down_pressed:
            dy -= PLAYER_SPEED * self.speed_multiplier+0.5

        if self._is_left_pressed:
            dx -= PLAYER_SPEED * self.speed_multiplier

        if self._is_right_pressed:
            dx += PLAYER_SPEED * self.speed_multiplier

        # Update position and make sure the airplane stays within the screen bounds
        new_x = self.x + dx
        new_y = self.y + dy

        if -SCREEN_WIDTH / 2 + self.size < new_x < SCREEN_WIDTH / 2 - self.size and -SCREEN_HEIGHT /2 + self.size < new_y < SCREEN_HEIGHT /2 - self.size:
            self.position = (new_x, new_y)

        turtle.update()

    def update(self, target):
        """Update the airplane and its bullets."""
        current_time = time.time()
        
        # Check if 5 seconds have passed since ability activation
        if self.is_tridirectional and current_time - self.ability_activation_time > 5:
            self.deactivate_ability()  # Deactivate the ability after 5 seconds
        
        self.move_airplane_directional()
        self.update_bullets(target)

    def update_bullets(self, enemies):
        """Update all active bullets and check for collision with all enemies."""
        for bullet in self._bullets[:]:
            bullet.move()

            for enemy in enemies:
                if self._check_bullet_collision(bullet, enemy):
                    self.handle_bullet_collision(bullet, enemy)
                    break

            if bullet.is_off_screen():
                bullet.hide_bullet()
                self._bullets.remove(bullet)

    def handle_bullet_collision(self, bullet, target):
        """Handle the effect of a bullet collision."""
        target.take_damage(10)  # Reduce the health of the target
        bullet.hide_bullet()  # Hide the bullet
        self._bullets.remove(bullet)  # Remove bullet from the list

    def shoot(self):
        """Handle shooting logic, including tri-directional shooting."""
        current_time = time.time()

        # Adjust cooldown for Tri-Directional Shooting
        if self.is_tridirectional:
            cooldown = 0.5  # Longer cooldown for Tri-Directional Shooting
        else:
            cooldown = self.shot_cooldown  # Default cooldown

        # Check if the cooldown time has passed before shooting
        if current_time - self.last_shot_time > cooldown:
            self.last_shot_time = current_time  # Update last shot time

            if self.is_tridirectional:
                # Tri-directional shooting: Angles for left, center, right (upward direction)
                angles = [120, 90, 60]  # Adjust angles to shoot upwards
                for angle in angles:
                    # dx is horizontal movement (small for upward direction), dy is vertical movement
                    dx = math.cos(math.radians(angle)) * 5  # Horizontal movement (left/right)
                    dy = math.sin(math.radians(angle)) * 5  # Vertical movement (upward)
                    bullet = Bullet(
                        x=self.x,
                        y=self.y + self.bullet_size + 5,  # Slightly above the plane
                        vx=dx,
                        vy=dy,
                        owner=PLAYER
                    )
                    self.add_bullet(bullet)

                print("Tri-Directional Shooting Activated!")  # Print message when Tri-Directional Shooting is active
            else:
                # Normal shooting behavior
                bullet = Bullet(
                    x=self.x,
                    y=self.y + self.size + 5,  # Slightly above the plane
                    vx=0,
                    vy=BULLET_SPEED,  # Normal bullet speed
                    owner=PLAYER
                )
                self.add_bullet(bullet)
        else:
            print("Shooting is on cooldown!")




class EnemyAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self.last_shot_time = 0
        self.shot_cooldown = 1.0  # Default shooting cooldown
        self.max_bullets = 5  # Max bullets for AIRPLANE_4 behavior
        self.bullet_count = 0  # Track how many bullets have been shot

    def move_enemy_airplane(self,target):
        """Move the enemy airplane downward."""
        new_x, new_y = self.x, self.y - ENEMY_SPEED  # Move downward
        if new_y < -SCREEN_HEIGHT / 2 + self.size:
            target.take_damage(1)
            self.destroy()
        else:
            self.position = (new_x, new_y)

    def handle_shooting(self, target):
        """Handle enemy shooting logic based on airplane type."""
        if self._is_destroyed:  # If the enemy is destroyed, stop shooting
            return

        current_time = time.time()

        if self.shape == "AIRPLANE_2.gif":
            self.shoot_normal(current_time)
        elif self.shape == "AIRPLANE_3.gif":
            self.shoot_tri_directional(current_time)
        elif self.shape == "AIRPLANE_4.gif":
            self.shoot_with_limit(current_time)
        elif self.shape == "AIRPLANE_5.gif":
            self.shoot_fast(current_time)

    def shoot_normal(self, current_time):
        """Shoot normally (one bullet at a time)."""
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,  # Slightly below the enemy
                vx=0,
                vy=-5,  # Bullet speed in y
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def shoot_tri_directional(self, current_time):
        """Shoot bullets in a tri-directional spread."""
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            angles = [-100, -90, -80]  # Three directions: left, center, right (downward spread)
            for angle in angles:
                dx = math.cos(math.radians(angle)) * 5  # Horizontal movement (left/right)
                dy = math.sin(math.radians(angle)) * 5  # Vertical movement (downward)
                bullet = Bullet(
                    x=self.x,
                    y=self.y - self.size - 5,  # Slightly below the enemy
                    vx=dx,
                    vy=dy,
                    owner=ENEMY
                )
                self.add_bullet(bullet)



    def shoot_with_limit(self, current_time):
        """Shoot with a limit of 5 bullets. If there are more, remove the oldest bullet."""
        if len(self._bullets) >= self.max_bullets:
            self._bullets[0].hide_bullet()  # Hide the first bullet if exceeding max
            self._bullets.pop(0)  # Remove it from the list

        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,  # Slightly below the enemy
                vx=0,
                vy=-5,  # Bullet speed in y
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def shoot_fast(self, current_time):
        """Shoot fast with a cooldown of 0.2 seconds."""
        if current_time - self.last_shot_time > 0.5:  # Fast shooting
            self.last_shot_time = current_time
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,  # Slightly below the enemy
                vx=0,
                vy=-5,  # Bullet speed in y
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def update(self, target):
        """Update the enemy airplane and handle collisions."""
        if not self._is_destroyed:  # Only update movement and shooting if the airplane is not destroyed
            self.move_enemy_airplane(target)
            self.update_bullets(target)
            self.handle_shooting(target)  # Implement enemy shooting logic
        else:
            # Even when destroyed, update bullets so they keep moving
            self.update_bullets(target)

    def update_bullets(self, target):
        """Update all active bullets and handle collisions."""
        for bullet in self._bullets[:]:  # Iterate over a copy to allow removal
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
        target.take_damage(1)  # Reduce the health of the target
        bullet.hide_bullet()  # Hide the bullet
        self._bullets.remove(bullet)  # Remove bullet from the list

    def remove_bullets(self):
        """Remove all bullets associated with this enemy when destroyed."""
        for bullet in self._bullets:
            bullet.hide_bullet()  # Hide bullet from the screen
        self._bullets.clear()  # Clear the list of bullets

