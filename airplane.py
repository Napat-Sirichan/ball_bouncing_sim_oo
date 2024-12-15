import turtle
from const import *
from bullet import Bullet
import time
import math

STATE_PATROL = "Patrol"
STATE_ATTACK = "Attack"

class Airplane:
    def __init__(self, position, velocity, shape, health, size=40):
        self.size = size
        self._shape = shape
        self._position = position
        self._velocity = velocity
        self._health = health

        self._turtle = turtle.Turtle()
        self._turtle.penup()
        self._turtle.screen.register_shape(shape)
        self._turtle.shape(shape)
        self._turtle.goto(self._position)
        self._turtle.showturtle()

        self._bullets = []

        self._explosion_images = EXPLOSION_FRAMES
        self._explosion_frame = 0
        self._is_destroyed = False

        self._explosion_turtle = turtle.Turtle()
        self._explosion_turtle.hideturtle()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
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
        self._turtle.screen.register_shape(other)
        self._turtle.shape(other)

    def move(self):
        new_x = self._position[0] + self._velocity[0]
        new_y = self._position[1] + self._velocity[1]
        self._position = (new_x, new_y)
        self._turtle.goto(self._position)

    def take_damage(self, amount):
        if self._is_destroyed:
            return
        self._health = max(0, self._health - amount)
        if self._health <= 0:
            self.destroy()

    def destroy(self):
        self._is_destroyed = True
        self._health = 0 
        self._turtle.hideturtle()
        self._turtle.clear()
        self.remove_bullets()
        self._handle_explosion_step()
        self._turtle.screen.update()
        self._explosion_turtle.clear()

    def _handle_explosion_step(self):
        self._explosion_turtle.penup()
        self._turtle.clear()

        if self._explosion_frame < len(self._explosion_images):
            self._explosion_turtle.screen.register_shape(self._explosion_images[self._explosion_frame])
            self._explosion_turtle.shape(self._explosion_images[self._explosion_frame])
            self._explosion_turtle.goto(self._position)
            self._explosion_turtle.showturtle()
            self._explosion_frame += 1
            self._explosion_turtle.screen.ontimer(self._handle_explosion_step, EXPLOSION_DELAY)
        else:
            self._explosion_turtle.hideturtle()
            self._turtle.hideturtle()

    def add_bullet(self, bullet):
        self._bullets.append(bullet)

    def update_bullets(self, target):
        for bullet in self._bullets[:]:
            bullet.move()
            if self._check_bullet_collision(bullet, target):
                bullet.hide_bullet()
                self._bullets.remove(bullet)
                target.take_damage(1)
            elif bullet.is_off_screen():
                bullet.hide_bullet()
                self._bullets.remove(bullet)

    def _check_bullet_collision(self, bullet, target):
        return bullet.distance(target) < target.size + bullet.size

    def draw_bullets(self):
        for bullet in self._bullets:
            bullet.turtle.showturtle()

    def remove_bullets(self):
        for bullet in self._bullets:
            bullet.hide_bullet()
        self._bullets.clear()


class PlayerAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self._is_up_pressed = False
        self._is_left_pressed = False
        self._is_right_pressed = False
        self._is_down_pressed = False
        self._is_space_pressed = False

        self.is_tridirectional = False
        self.bullet_size = size
        self.speed_multiplier = 1
        self.last_shot_time = 0
        self.shot_cooldown = 0.2
        self.score = 0
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
        self.shoot()

    def release_space(self):
        self._is_space_pressed = False

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def activate_tridirectional_shooting(self):
        self.is_tridirectional = True
        self.ability_activation_time = time.time()

    def increase_health(self):
        self._health = min(3, self._health + 1)

    def double_speed(self):
        self.speed_multiplier = 1.8
        self.ability_activation_time = time.time()

    def deactivate_ability(self):
        self.is_tridirectional = False
        self.speed_multiplier = 1.0

    def move_airplane_directional(self):
        dx, dy = 0, 0

        if self._is_up_pressed:
            dy += PLAYER_SPEED * self.speed_multiplier + 0.5
        if self._is_down_pressed:
            dy -= PLAYER_SPEED * self.speed_multiplier + 0.5
        if self._is_left_pressed:
            dx -= PLAYER_SPEED * self.speed_multiplier
        if self._is_right_pressed:
            dx += PLAYER_SPEED * self.speed_multiplier

        new_x = self.x + dx
        new_y = self.y + dy

        if -SCREEN_WIDTH / 2 + self.size < new_x < SCREEN_WIDTH / 2 - self.size and \
           -SCREEN_HEIGHT / 2 + self.size < new_y < SCREEN_HEIGHT / 2 - self.size:
            self.position = (new_x, new_y)

        turtle.update()

    def update(self, enemies):
        current_time = time.time()

        if self.is_tridirectional and (current_time - self.ability_activation_time) > MYSTERY_BALL_LIFETIME:
            self.deactivate_ability()

        self.move_airplane_directional()
        self.update_bullets(enemies)

    def update_bullets(self, enemies):
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
        target.take_damage(10)
        bullet.hide_bullet()
        self._bullets.remove(bullet)

    def shoot(self):
        current_time = time.time()

        cooldown = 0.5 if self.is_tridirectional else self.shot_cooldown

        if current_time - self.last_shot_time > cooldown:
            self.last_shot_time = current_time

            if self.is_tridirectional:
                angles = [120, 90, 60]
                for angle in angles:
                    dx = math.cos(math.radians(angle)) * 5
                    dy = math.sin(math.radians(angle)) * 5
                    bullet = Bullet(
                        x=self.x,
                        y=self.y + self.bullet_size + 5,
                        vx=dx,
                        vy=dy,
                        owner=PLAYER
                    )
                    self.add_bullet(bullet)
            else:
                bullet = Bullet(
                    x=self.x,
                    y=self.y + self.size + 5,
                    vx=0,
                    vy=BULLET_SPEED,
                    owner=PLAYER
                )
                self.add_bullet(bullet)


class EnemyAirplane(Airplane):
    def __init__(self, position, velocity, shape, health, size=20):
        super().__init__(position, velocity, shape, health, size)
        self.last_shot_time = 0
        self.shot_cooldown = 1.0
        self.max_bullets = 5
        self.bullet_count = 0

        # Attack_distance เพิ่ม 1.5 เท่า
        # เดิมคือ 200 -> 200 * 1.5 = 300
        self.attack_distance = 300

        # ความเร็วลงใน Attack state
        self.attack_speed = 8

        self.state = STATE_PATROL
        self.patrol_left_bound = -100
        self.patrol_right_bound = 100
        self.patrol_speed = 2
        self.moving_right = True

    def handle_state_machine(self, target):
        if self._is_destroyed:
            return

        dist = self.distance(target)
        # ตรวจสอบก่อนว่า enemy อยู่เหนือ player หรือไม่
        if self.y > target.y:
            # ถ้าอยู่เหนือผู้เล่นแล้ว และระยะน้อยกว่า attack_distance ให้เป็น Attack
            if dist < self.attack_distance:
                self.state = STATE_ATTACK
            else:
                self.state = STATE_PATROL
        else:
            # ถ้าไม่อยู่เหนือผู้เล่น ให้กลับไป Patrol
            self.state = STATE_PATROL

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

    def move_patrol(self):
        # Move left and right within patrol bounds
        if self.moving_right:
            new_x = self.x + self.patrol_speed
            if new_x > self.patrol_right_bound:
                new_x = self.patrol_right_bound
                self.moving_right = False
        else:
            new_x = self.x - self.patrol_speed
            if new_x < self.patrol_left_bound:
                new_x = self.patrol_left_bound
                self.moving_right = True

        new_y = self.y - ENEMY_SPEED
        if new_y < -SCREEN_HEIGHT / 2 + self.size:
            self.position = (new_x, new_y)
        else:
            self.position = (new_x, new_y)

    def move_attack(self, target):
        new_x = self.x
        new_y = self.y - self.attack_speed
        if new_y < -SCREEN_HEIGHT / 2 + self.size:
            self.position = (new_x, new_y)
        else:
            self.position = (new_x, new_y)

    def handle_shooting(self, target):
        if self._is_destroyed:
            return

        # In Attack state, we shoot faster and bullet vy *1.8
        if self.state == STATE_ATTACK:
            attack_cooldown = max(0.5, self.shot_cooldown / 2.0)
            self.shoot_based_on_shape(target, attack_cooldown, enhanced_vy_multiplier=1.8)
        else:
            # ใช้ค่าปกติ
            self.shoot_based_on_shape(target, self.shot_cooldown, enhanced_vy_multiplier=1.0)

    def shoot_based_on_shape(self, target, cooldown, enhanced_vy_multiplier=1.0):
        current_time = time.time()
        # ส่ง enhanced_vy_multiplier ไปยังฟังก์ชันยิงเพื่อปรับความเร็วกระสุน
        if self.shape == AIRPLANE_2:
            self.shoot_normal(current_time, cooldown, enhanced_vy_multiplier)
        elif self.shape == AIRPLANE_3:
            self.shoot_tri_directional(current_time, cooldown, enhanced_vy_multiplier)
        elif self.shape == AIRPLANE_4:
            self.shoot_with_limit(current_time, cooldown, enhanced_vy_multiplier)
        elif self.shape == AIRPLANE_5:
            self.shoot_fast(current_time, cooldown, enhanced_vy_multiplier)

    def shoot_normal(self, current_time, cooldown, enhanced_vy_multiplier):
        if current_time - self.last_shot_time > cooldown:
            self.last_shot_time = current_time
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,
                vx=0,
                vy=-5 * enhanced_vy_multiplier,
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def shoot_tri_directional(self, current_time, cooldown, enhanced_vy_multiplier):
        if current_time - self.last_shot_time > cooldown:
            self.last_shot_time = current_time
            angles = [-100, -90, -80]
            for angle in angles:
                dx = math.cos(math.radians(angle)) * 5
                dy = math.sin(math.radians(angle)) * 5 * enhanced_vy_multiplier
                bullet = Bullet(
                    x=self.x,
                    y=self.y - self.size - 5,
                    vx=dx,
                    vy=dy,
                    owner=ENEMY
                )
                self.add_bullet(bullet)

    def shoot_with_limit(self, current_time, cooldown, enhanced_vy_multiplier):
        if len(self._bullets) >= self.max_bullets:
            self._bullets[0].hide_bullet()
            self._bullets.pop(0)

        if current_time - self.last_shot_time > cooldown:
            self.last_shot_time = current_time
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,
                vx=0,
                vy=-5 * enhanced_vy_multiplier,
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def shoot_fast(self, current_time, cooldown, enhanced_vy_multiplier):
        if current_time - self.last_shot_time > cooldown:
            self.last_shot_time = current_time
            bullet = Bullet(
                x=self.x,
                y=self.y - self.size - 5,
                vx=0,
                vy=-5 * enhanced_vy_multiplier,
                owner=ENEMY
            )
            self.add_bullet(bullet)

    def update(self, target):
        if not self._is_destroyed:
            self.handle_state_machine(target)

            if self.state == STATE_PATROL:
                self.move_patrol()
            elif self.state == STATE_ATTACK:
                self.move_attack(target)

            # หลังจาก move เสร็จแล้ว เช็คว่าตกขอบล่างหรือยัง
            if self.y < -SCREEN_HEIGHT / 2 + self.size:
                # เมื่อตกขอบล่าง: ลด hp ของ target ลง 1 แล้วทำลายตนเอง
                target.take_damage(1)
                self.destroy()

            self.update_bullets(target)
            self.handle_shooting(target)
        else:
            self.update_bullets(target)

    def update_bullets(self, target):
        for bullet in self._bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullet.hide_bullet()
                self._bullets.remove(bullet)
            elif self._check_bullet_collision(bullet, target):
                self.handle_bullet_collision(bullet, target)

    def handle_bullet_collision(self, bullet, target):
        target.take_damage(1)
        bullet.hide_bullet()
        self._bullets.remove(bullet)

    def remove_bullets(self):
        for bullet in self._bullets:
            bullet.hide_bullet()
        self._bullets.clear()
