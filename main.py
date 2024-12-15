import turtle
import tkinter as tk
import random
from const import *
from airplane import PlayerAirplane, EnemyAirplane
from mystery import MysteryBall
from bullet import Bullet

class GameController:
    def __init__(self):
        # Initial Setup
        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title("Airplane Shooting Game")
        self.screen.bgcolor(BLACK)
        self.screen.tracer(0)  # ปิดการอัปเดตอัตโนมัติ
        self.canvas = self.screen.getcanvas()  # กำหนด canvas ก่อนใช้งาน

        # Register image shapes
        self.screen.register_shape(HEART_FULL)
        self.screen.register_shape(HEART_BROKE)
        self.screen.register_shape(AIRPLANE_LOGO)  # ลงทะเบียนโลโก้
        self.screen.register_shape(PLAYER_PIC)

        # สร้าง Turtle สำหรับหน้าจอเข้าสู่ระบบ
        self.logo_turtle = turtle.Turtle()
        self.logo_turtle.hideturtle()
        self.logo_turtle.penup()
        self.logo_turtle.shape(AIRPLANE_LOGO)
        self.logo_turtle.goto(0, 100)
        self.logo_turtle.showturtle()

        self.welcome_turtle = turtle.Turtle()
        self.welcome_turtle.hideturtle()
        self.welcome_turtle.penup()
        self.welcome_turtle.color(WHITE)
        self.welcome_turtle.goto(0, -50)
        self.welcome_turtle.write(
            "Welcome to Airplane Shooting Game!",
            align="center",
            font=("Arial", 24, "bold")
        )

        # สร้าง Turtle สำหรับแสดงคำแนะนำ
        self.instruction_turtle = turtle.Turtle()
        self.instruction_turtle.hideturtle()
        self.instruction_turtle.penup()
        self.instruction_turtle.color(WHITE)
        self.instruction_turtle.goto(0, -150)
        self.instruction_turtle.write(
            "Please enter your username:",
            align="center",
            font=("Arial", 16, "normal")
        )

        # สร้าง Turtle สำหรับข้อความ Game Over
        self.game_over_turtle = turtle.Turtle()
        self.game_over_turtle.hideturtle()
        self.game_over_turtle.penup()

        # สร้าง Turtle สำหรับแสดงข้อความและหัวใจ
        self.display_turtle = turtle.Turtle()
        self.display_turtle.hideturtle()
        self.display_turtle.penup()

        # กำหนดตัวแปร global
        self.score_text = None  # กำหนดค่าเริ่มต้นให้กับ score_text
        self.player = None      # กำหนดค่าเริ่มต้นให้กับ player
        self.username = ""      # กำหนดค่าเริ่มต้นให้กับ username
        self.current_input = "" # ตัวแปรสำหรับเก็บ input ขณะกรอก username

        # Initialize other attributes
        self.bg_images = []
        self.bg_ids = []
        self.mystery_balls = []
        self.enemies = []
        self.last_score_used_to_spawn = -1
        self.game_started = False  # Flag เพื่อระบุว่าเกมเริ่มต้นแล้ว

        # Start login screen
        self.login_screen()

    def login_screen(self):
        # เริ่มการเปลี่ยนสีพื้นหลัง
        self.change_background_color()

        # เริ่มการหมุนโลโก้
        self.rotate_logo()
        self.flip_logo()

        # ผูกการกดปุ่มเพื่อรับ input ของ username
        self.screen.listen()
        self.screen.onkeypress(self.start_game, "Return")  # เมื่อกด Enter เริ่มเกม
        self.screen.onkeypress(self.add_char, "a")  # กำหนดตัวอักษรต่างๆ
        # เพิ่มตัวอักษรอื่นๆ ตามต้องการ

        # ผูกการกดปุ่มสำหรับ backspace
        self.screen.onkeypress(self.backspace, "BackSpace")

        # ผูกการกดปุ่มตัวอักษร (A-Z)
        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            self.screen.onkeypress(lambda c=char: self.add_char(c), char)

    def add_char(self, char):
        if not self.game_started:
            self.current_input += char
            self.update_username_display()

    def backspace(self):
        if not self.game_started and len(self.current_input) > 0:
            self.current_input = self.current_input[:-1]
            self.update_username_display()

    def update_username_display(self):
        # ล้างข้อความเก่า
        self.instruction_turtle.clear()
        # เขียนข้อความใหม่พร้อมกับ input
        self.instruction_turtle.write(
            f"Please enter your username: {self.current_input}",
            align="center",
            font=("Arial", 16, "normal")
        )

    def start_game(self):
        if self.game_started:
            return  # หยุดการทำงานถ้าเกมเริ่มแล้ว

        self.game_started = True  # ตั้งค่า flag ว่าเกมเริ่มแล้ว

        # กำหนด username
        self.username = self.current_input if self.current_input else "Player"

        # ซ่อนหน้าจอเข้าสู่ระบบ
        self.logo_turtle.hideturtle()
        self.welcome_turtle.clear()
        self.instruction_turtle.clear()

        # เปลี่ยนพื้นหลังเป็น SKYBLUE และหยุดการเปลี่ยนสี
        self.screen.bgcolor(SKYBLUE)

        # เริ่มต้นเกม
        self.spawn_background()
        self.initialize_game_objects()
        self.bind_keys()
        self.game_loop()

    def change_background_color(self):
        if self.game_started:
            return  # หยุดการเปลี่ยนสีถ้าเกมเริ่มแล้ว

        new_color = random.choice(LOGIN_BG_COLORS)
        self.screen.bgcolor(new_color)
        self.screen.ontimer(self.change_background_color, 1000)  # เปลี่ยนสีทุก 1 วินาที

    def rotate_logo(self, angle=0):
        if self.game_started:
            return  # หยุดการหมุนถ้าเกมเริ่มแล้ว

        self.logo_turtle.setheading(angle)
        self.screen.update()
        self.screen.ontimer(lambda: self.rotate_logo((angle + LOGO_ROTATION_SPEED) % 360), 50)

    def flip_logo(self):
        if self.game_started:
            return  # หยุดการพลิกถ้าเกมเริ่มแล้ว

        current_heading = self.logo_turtle.heading()
        new_heading = (current_heading + 180) % 360
        self.logo_turtle.setheading(new_heading)
        self.screen.update()
        self.screen.ontimer(self.flip_logo, LOGO_FLIP_INTERVAL)

    def spawn_background(self):
        for path in BG_IMAGE_PATHS:
            try:
                img = tk.PhotoImage(file=path)
                self.bg_images.append(img)
            except tk.TclError:
                print(f"Error loading background image: {path}")

        if not self.bg_images:
            print("No background images loaded.")
            return

        bg_width = self.bg_images[0].width()
        bg_height = self.bg_images[0].height()
        x_position = (SCREEN_WIDTH - bg_width) // 2 - 300

        for i in range(len(self.bg_images)):
            bg_id = self.canvas.create_image(
                x_position, i * bg_height, anchor='nw', image=self.bg_images[i]
            )
            self.bg_ids.append(bg_id)

        self.scroll_background()

    def scroll_background(self):
        """Move the background images down smoothly."""
        for bg_id in self.bg_ids:
            self.canvas.move(bg_id, 0, SCROLL_SPEED)
            x, y = self.canvas.coords(bg_id)
            if y >= SCREEN_HEIGHT:
                max_y = min([self.canvas.coords(b)[1] for b in self.bg_ids])
                self.canvas.coords(bg_id, self.canvas.coords(bg_id)[0], max_y - self.bg_images[0].height())
        self.screen.update()
        self.screen.ontimer(self.scroll_background, int(1000 / FPS))

    def initialize_game_objects(self):
        # Player initialization
        self.player = PlayerAirplane(
            position=(0, -200),
            velocity=(0, 0),
            shape=PLAYER_PIC,
            health=3,
            size=40
        )

    def bind_keys(self):
        self.screen.onkeypress(self.player.press_up, "Up")
        self.screen.onkeyrelease(self.player.release_up, "Up")
        self.screen.onkeypress(self.player.press_left, "Left")
        self.screen.onkeyrelease(self.player.release_left, "Left")
        self.screen.onkeypress(self.player.press_right, "Right")
        self.screen.onkeyrelease(self.player.release_right, "Right")
        self.screen.onkeypress(self.player.press_down, "Down")
        self.screen.onkeyrelease(self.player.release_down, "Down")
        self.screen.onkeypress(self.player.press_space, "space")
        self.screen.onkeyrelease(self.player.release_space, "space")
        self.screen.listen()

    def display_score(self):
        if self.score_text:
            self.score_text.clear()
        else:
            self.score_text = turtle.Turtle()
            self.score_text.hideturtle()
            self.score_text.penup()
            self.score_text.color(WHITE)
        self.score_text.goto(0, SCREEN_HEIGHT / 2 - 50)
        self.score_text.write(
            f"{self.username} Score: {self.player.score}",
            align="center",
            font=("Arial", 20, "normal")
        )

    def health_ui(self):
        self.display_turtle.clear()

        health = max(0, min(self.player._health, 3))  # Clamp health between 0 and 3
        hearts = [HEART_FULL] * health + [HEART_BROKE] * (3 - health)
        for i, heart in enumerate(hearts):
            self.display_image(-200 + i * 40, -300, heart)

    def display_image(self, x, y, image_shape):
        self.display_turtle.goto(x, y)
        self.display_turtle.shape(image_shape)
        self.display_turtle.stamp()

    def spawn_mystery_ball(self):
        """Randomly spawn a mystery ball and drop it from the top."""
        mystery_types = [1, 2, 3]  # Assuming MYSTERY_BALL1, MYSTERY_BALL2, MYSTERY_BALL3 are 1, 2, 3
        mystery_type = random.choice(mystery_types)
        mystery_ball = MysteryBall(
            size=20,
            x=random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50),
            y=SCREEN_HEIGHT // 2 - 50,
            vx=0,
            vy=-5,
            color="red",
            ball_type=mystery_type
        )
        self.mystery_balls.append(mystery_ball)

    def spawn_enemy(self):
        shapes = [AIRPLANE_2, AIRPLANE_3, AIRPLANE_4, AIRPLANE_5]
        random_shape = random.choice(shapes)
        while True:
            x_pos = random.randint(-SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 - 50)
            y_pos = SCREEN_HEIGHT // 2 - 50
            overlap = False
            for enemy in self.enemies:
                if abs(x_pos - enemy.x) < enemy.size * 2 and abs(y_pos - enemy.y) < enemy.size * 2:
                    overlap = True
                    break
            if not overlap:
                new_enemy = EnemyAirplane(
                    position=(x_pos, y_pos),
                    velocity=(0, 0),
                    shape=random_shape,
                    health=3,
                    size=40
                )
                self.enemies.append(new_enemy)
                break

    def display_game_over(self):
        self.screen.bgcolor(GAME_OVER_BG_COLOR)
        self.game_over_turtle.goto(0, 0)
        self.game_over_turtle.color(GAME_OVER_COLOR)
        self.game_over_turtle.write(
            GAME_OVER_TEXT,
            align="center",
            font=GAME_OVER_FONT
        )
        self.health_ui()  # แสดงหัวใจแตกทั้งหมด

    def game_loop(self):
        self.player.update(self.enemies)
        self.health_ui()
        self.display_score()

        if self.player._health <= 0:
            self.display_game_over()
            self.screen.update()
            return

        for ball in self.mystery_balls[:]:
            ball.move()
            if self.player.distance(ball) < self.player.size + ball.size:
                ball.activate_ability(self.player)
                self.mystery_balls.remove(ball)
            elif ball.is_off_screen():
                ball._hide_ball()
                self.mystery_balls.remove(ball)  # ลบจากรายการเพื่อป้องกันไม่ให้เกิดซ้ำ

        for enemy in self.enemies[:]:
            enemy.update(self.player)
            if enemy._is_destroyed:
                self.enemies.remove(enemy)
                self.player.score += 1

        if not self.enemies:
            for _ in range(random.randint(1, 4)):
                self.spawn_enemy()

        if self.player.score % 7 == 0 and self.player.score != self.last_score_used_to_spawn:
            self.spawn_mystery_ball()
            self.last_score_used_to_spawn = self.player.score

        self.screen.update()
        self.screen.ontimer(self.game_loop, int(1000 / FPS))


if __name__ == "__main__":
    game = GameController()
    turtle.tracer(0)
    turtle.mainloop()
