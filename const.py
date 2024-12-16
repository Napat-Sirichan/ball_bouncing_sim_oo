# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 820

# Colors
ORANGE = "orange"
RED = "red"
WHITE = "white"
SKYBLUE = "#3696d5"
BLACK = "#000000"

# Owners
PLAYER = 1
ENEMY = 2

# Explosion properties
EXPLOSION_FRAMES = [
    "picture/EXPLOSION_1.gif",
    "picture/EXPLOSION_2.gif",
    "picture/EXPLOSION_3.gif",
    "picture/EXPLOSION_4.gif"
]
EXPLOSION_DELAY = 200  # milliseconds between explosion frames

FPS = 1000
SCROLL_SPEED = 6

BG_IMAGE_PATHS = ["picture/bg1.gif", "picture/bg2.gif"]
ENEMY_PIC = [
    "picture/AIRPLANE_2.gif",
    "picture/AIRPLANE_3.gif",
    "picture/AIRPLANE_4.gif",
    "picture/AIRPLANE_5.gif"
]
PLAYER_PIC = "picture/AIRPLANE.gif"
HEART_FULL = "picture/HEART_FULL.gif"
HEART_BROKE = "picture/HEART_BROKE.gif"

# Player and Enemy Speeds
PLAYER_SPEED = 5
BULLET_SPEED = 15
ENEMY_SPEED = 3

# Mystery Ball Constants
MYSTERY_BALL1 = 1
MYSTERY_BALL2 = 2
MYSTERY_BALL3 = 3


MYSTERY_BALL_SPAWN_RATE = 5  # Percentage chance of spawning a mystery ball (1-100)
MYSTERY_BALL_LIFETIME = 5    # Seconds the ability lasts

# Game Over Constants
GAME_OVER_TEXT = "Game Over"
GAME_OVER_FONT = ("Arial", 80, "bold")
GAME_OVER_COLOR = WHITE
GAME_OVER_BG_COLOR = BLACK

# Airplane Shapes
AIRPLANE_2 = "picture/AIRPLANE_2.gif"
AIRPLANE_3 = "picture/AIRPLANE_3.gif"
AIRPLANE_4 = "picture/AIRPLANE_4.gif"
AIRPLANE_5 = "picture/AIRPLANE_5.gif"


# Login Screen Constants
LOGIN_BG_COLORS = ["#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#A833FF"] 
AIRPLANE_LOGO = "picture/AIRPLANE_LOGO.gif"
LOGO_ROTATION_SPEED = 5  
LOGO_FLIP_INTERVAL = 500 

#SFX 
SHOOT = "sfx/Shooting.wav"
EXPLOSION = "sfx/Explosion_sound.wav"
POWERUP = "sfx/Powerup_sound.wav"
START = "sfx/Start.wav"