    def shoot_tri_directional(self, current_time):
        """Shoot bullets in a tri-directional spread."""
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            angles = [-30, 0, 30]  # Three directions: left, center, right
            for angle in angles:
                dx = math.cos(math.radians(angle)) * 5  # Horizontal movement (left/right)
                dy = -math.sin(math.radians(angle)) * 5  # Vertical movement (downward)
                bullet = Bullet(
                    x=self.x,
                    y=self.y - self.size - 5,  # Slightly below the enemy
                    vx=dx,
                    vy=dy,
                    owner=ENEMY
                )
                self.add_bullet(bullet)