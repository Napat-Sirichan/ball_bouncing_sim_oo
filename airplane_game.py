import turtle
import tkinter as tk
from const import *  # Make sure SCREEN_WIDTH, SCREEN_HEIGHT, BG_IMAGE_PATHS are defined here
import airplane as A

SCROLL_SPEED = 6  # Adjust scroll speed to a smoother rate
FPS = 16  # 30 FPS for the game loop (33 ms per frame)

class GameControl:
    def __init__(self):
        # Initialize the screen
        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title("Airplane and Ball Shooting")
        self.screen.bgcolor("#3696d5")
        self.screen.tracer(0)  # Disable automatic updates to improve performance
        turtle.hideturtle()  # Hide the main turtle cursor

        # Player and enemy airplanes
        self.player = A.PlayerAirplane((0, 0), (5, 5), "AIRPLANE.gif", 3, size=20)
        self.enemy = A.EnemyAirplane((0, 100), (0, 0), "AIRPLANE_4.gif", 3, size=20)

        # Background initialization
        self.canvas = self.screen.getcanvas()
        self.bg_images = []
        for path in BG_IMAGE_PATHS:
            img = tk.PhotoImage(file=path)
            self.bg_images.append(img)

        self.bg_width = self.bg_images[0].width()
        self.bg_height = self.bg_images[0].height()

        self.bg_ids = []
        self.x_position = (SCREEN_WIDTH - self.bg_width) // 2 - 300
        self._initialize_background()

        # Key bindings for player control
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

        self.screen.listen()  # Start listening to key presses

    def _initialize_background(self):
        """Initialize the background images."""
        for i in range(len(self.bg_images)):
            bg_id = self.canvas.create_image(self.x_position, i * self.bg_height, anchor='nw', image=self.bg_images[i])
            self.bg_ids.append(bg_id)

    def scroll_background(self):
        """Move the background images down smoothly."""
        for bg_id in self.bg_ids:
            self.canvas.move(bg_id, 0, SCROLL_SPEED)
            x, y = self.canvas.coords(bg_id)

            # If the image scrolls past the bottom, reset its position to the top
            if y >= SCREEN_HEIGHT:  # If the image goes beyond the bottom of the screen
                max_y = min([self.canvas.coords(b)[1] for b in self.bg_ids])
                self.canvas.coords(bg_id, self.x_position, max_y - self.bg_height)

        self.screen.update()  # Update the screen after background scroll
        self.screen.ontimer(self.scroll_background, FPS)  # Set the timer for 30 FPS (33ms per frame)

    def game_loop(self):
        """Main game loop, updating the game state."""
        # Move and update player and enemy airplanes
        self.player.move_airplane_directional()
        self.player.update(target=self.enemy)
        
        # Update the screen after updating game objects
        self.screen.update()

        # Keep the frame rate consistent (60 FPS)
        self.screen.ontimer(self.game_loop, FPS)  # Run the game loop at 30 FPS (33ms per frame)

    def start_game(self):
        """Start the game loop and background scrolling."""
        self.scroll_background()
        self.game_loop()
        self.screen.mainloop()

# This ensures that the game only runs when the script is executed directly
if __name__ == "__main__":
    # Initialize the game control and start the game
    game_control = GameControl()
    game_control.start_game()
