# Airplane Shooting Game

## Project Title
**Airplane Shooting Game**

## Description
A fast-paced arcade-style game where the player controls an airplane to shoot enemies, dodge bullets, and collect power-ups while progressing through increasingly challenging waves of enemies.

---

## Game Rules

Here are the detailed rules and mechanics of the game:

- **Player Controls**:
  - Use the **arrow keys** to move the airplane (Up, Down, Left, Right).
  - Press the **Spacebar** to shoot bullets.

- **Objective**:
  - The main goal is to destroy enemy airplanes while avoiding their bullets and collecting MysteryBalls.
  - The game ends when the player's health reaches 0.

- **Scoring**:
  - Destroying an enemy airplane gives **1 point**.
  - The player's score is displayed at the top of the screen.
  - As the player earns points, MysteryBalls will spawn at certain milestones.

- **MysteryBalls**:
  - MysteryBalls spawn randomly based on the player's score.
  - Collecting a MysteryBall grants one of the following power-ups:
    - **Health Boost**: Restores some of the player's health.
    - **Tri**: Doubles the score for a limited time.
    - **Invincibility**: Makes the player invincible for a short time.
  - MysteryBalls disappear if not collected in time.

- **Health**:
  - The player starts with **3 lives (hearts)**.
  - The player loses a life if hit by an enemy bullet or collides with an enemy airplane.
  - The game is over when all hearts are lost.

- **Enemy Airplanes**:
  - Enemies spawn with different behaviors.
  - Enemies can shoot bullets at the player.
  - Some enemies follow predictable paths, while others use advanced AI (e.g., zigzagging, retreating).
  - When an enemy is destroyed, it drops points and may spawn a MysteryBall.

- **Collision and Damage**:
  - The player's airplane and enemies both take damage when they collide.
  - If the player collides with an enemy, they lose **one life (heart)**.
  - If the player's bullet hits an enemy, the enemy is destroyed, and the player gains points.
  - If the player is hit by an enemy bullet, they lose **one life (heart)**.

- **Enemy Shooting Behavior**:
  - Enemies have three states:
    - **Idle**: The enemy does not shoot.
    - **Attacking**: The enemy actively shoots bullets at the player.
    - **Retreating**: The enemy moves away from the player and does not shoot.

- **Losing the Game**:
  - The game ends when the player loses all lives (hearts).
  - A **Game Over** screen will appear, and the player can restart or exit the game.

- **Game Restart**:
  - If the player loses all hearts, the game can be restarted from the beginning.

---

## Project Design and Implementation

### Overview
The **Airplane Shooting Game** is an interactive, event-driven arcade game where the player controls an airplane to shoot enemies and collect power-ups. I used object-oriented programming principles to manage the game logic and enhance code maintainability.

### Key Classes and Concepts

1. **Ball Class**:
   - The `Ball` class is the foundation for both **Bullet** and **MysteryBall**. It defines properties like size, position, and velocity, which are extended to create the functionality of bullets and mystery balls.
   - The `Ball` class also includes movement and collision detection methods.

2. **Bullet Class**:
   - **Bullet** inherits from the `Ball` class.
   - It represents the bullets fired by both the player and the enemies.
   - The `Bullet` class handles the movement of bullets, checks if they go off-screen, and draws them on the canvas.

3. **MysteryBall Class**:
   - **MysteryBall** is another subclass of `Ball`.
   - It spawns when the player's score hits certain milestones.
   - The **MysteryBall** provides power-ups such as health boosts, score multipliers, or invincibility when collected.

4. **Enemy Airplanes**:
   - Enemies use a **State Machine** to control their behavior. Depending on their state, enemies can:
The **EnemyAirplane** class uses a state machine to control its behavior:
  - **Attacking**: The enemy shoots bullets at the player.
  - **patrol**: The enemy move left and right within patrol bounds.

5. **Game Controller**:
   - The **GameController** class manages all game objects (player, enemies, bullets, etc.).
   - It includes methods for initializing the game, displaying the score and health, spawning enemies, and running the main game loop.

### Power-ups and MysteryBalls
MysteryBalls are special items that spawn based on the player’s score. Collecting them grants random power-ups like:
  - **Health Boost**: Restores health to the player.
  - **Score Multiplier**: Doubles the points for a limited time.
  - **Invincibility**: Grants temporary invincibility.

This adds variety and challenge to the game, making each encounter with enemies unique.

---

## UML Class Diagram

Here’s the UML class diagram illustrating the structure of the game and how the classes interact.

```mermaid
classDiagram
    %% Define the classes
    class GameController {
        +screen
        +canvas
        +bg_images
        +bg_ids
        +mystery_balls
        +enemies
        +last_score_used_to_spawn
        +game_started
        +username
        +current_input
        +player
        +score_text
        +display_turtle
        +logo_turtle
        +welcome_turtle
        +instruction_turtle
        +game_over_turtle
        +login_screen()
        +change_background_color()
        +rotate_logo()
        +flip_logo()
        +spawn_background()
        +scroll_background()
        +initialize_game_objects()
        +bind_keys()
        +display_score()
        +health_ui()
        +spawn_mystery_ball()
        +spawn_enemy()
        +display_game_over()
        +game_loop()
    }

    class Airplane {
        +position
        +velocity
        +shape
        +health
        +size
        +update()
    }

    class PlayerAirplane {
        +score
        +press_up()
        +release_up()
        +press_left()
        +release_left()
        +press_right()
        +release_right()
        +press_down()
        +release_down()
        +press_space()
        +release_space()
    }

    class EnemyAirplane {
        +destroy()
    }

    class Ball {
        +size
        +x
        +y
        +vx
        +vy
        +color
        +mass
        +count
        +canvas_width
        +canvas_height
        +bounce_off_vertical_wall()
        +bounce_off_horizontal_wall()
        +bounce_off()
        +distance()
        +time_to_hit()
        +time_to_hit_vertical_wall()
        +time_to_hit_horizontal_wall()
        +time_to_hit_paddle()
        +bounce_off_paddle()
        +__str__()
    }

    class Bullet {
        +owner
        +hide_bullet()
        +is_off_screen()
        +move()
        +draw()
        +__str__()
    }

    class MysteryBall {
        +size
        +x
        +y
        +vx
        +vy
        +color
        +ball_type
        +move()
        +activate_ability()
        +is_off_screen()
        +_hide_ball()
    }

    %% Relationships between classes
    GameController "1" -- "1" PlayerAirplane : "has"
    GameController "1" -- "*" EnemyAirplane : "spawns"
    GameController "1" -- "*" Bullet : "fires"
    GameController "1" -- "*" MysteryBall : "spawns"
    Ball <|-- Bullet : "inherits"
    Ball <|-- MysteryBall : "inherits"
    PlayerAirplane "1" -- "*" Bullet : "fires"
    EnemyAirplane "1" -- "*" Bullet : "fires"
    Airplane <|-- PlayerAirplane : "inherits"
    Airplane <|-- EnemyAirplane : "inherits"
