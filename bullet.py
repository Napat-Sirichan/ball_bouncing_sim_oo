from ball import Ball

class Bullet(Ball):
    def __init__(self, size, x, y, vx, vy, color, id, owner):
        super().__init__(size, x, y, vx, vy, color, id)
        self.owner = owner  # Identify if the bullet belongs to player or enemy

    def move(self, dt):
        # Move the bullet straight in its direction
        self.x += self.vx * dt
        self.y += self.vy * dt

    def check_out_of_bounds(self):
        # Check if the bullet has moved outside the screen bounds
        if (
            self.x < -self.canvas_width or self.x > self.canvas_width or
            self.y < -self.canvas_height or self.y > self.canvas_height
        ):
            return True
        return False

    def __str__(self):
        return f"Bullet: ({self.x}, {self.y}), Owner: {self.owner}"

# Create a player bullet
player_bullet = Bullet(size=5, x=100, y=100, vx=0, vy=20, color='blue', id='p1', owner='player')

# Create an enemy bullet
enemy_bullet = Bullet(size=5, x=-50, y=200, vx=0, vy=-15, color='red', id='e1', owner='enemy')

# Game loop (simplified)
bullets = [player_bullet, enemy_bullet]
dt = 0.1  # Time step

for bullet in bullets:
    bullet.move(dt)
    if bullet.check_out_of_bounds():
        print(f"Removing {bullet}")
        bullets.remove(bullet)