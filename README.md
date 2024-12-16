# Airplane Shooting Game

## Project Title
Airplane Shooting Game

## Description
A fast-paced arcade-style game where players control an airplane to shoot enemies, dodge bullets, and collect power-ups while progressing through increasingly challenging waves of enemies.

---

## Overview
The **Airplane Shooting Game** is an interactive, event-driven game combining action and strategy. Players control a customizable airplane, striving to survive enemy waves using strategic shooting and dodging techniques. Exciting features include power-ups, dynamic enemy AI, and visually engaging effects.

---

## Features
- **Player Control:** 
  - Move the airplane using arrow keys.
  - Shoot bullets using the spacebar.
- **Enemies:**
  - Different AI behaviors such as patrolling and attacking.
- **Power-ups:**
  - Collectible mystery balls grant abilities like increased speed or health recovery.
- **Dynamic Background:**
  - Smooth scrolling for an immersive experience.
- **Game States:**
  - Includes login screen, gameplay mode, and game-over state.
  - Displays health and score on the interface.

---

## How to Install and Run
1. **Clone the Repository:** 
   - Clone the game repository from GitHub.
2. **Install Dependencies:** 
   - Ensure Python (3.10+) is installed.
   - Install required libraries using `pip install -r requirements.txt`.
3. **Run the Game:**
   - Execute `main.py` in the terminal or Python IDE.

---

## Controls
- **Arrow Keys:** Move the airplane (Up, Down, Left, Right).
- **Spacebar:** Shoot bullets.

---

## Objective
- Survive by shooting enemies, dodging bullets, and collecting power-ups.
- The game ends when the player's health reaches zero.

---

## How to Play
1. **Login Screen:** Enter your username to start the game.
2. **Gameplay:**
   - Move your airplane with arrow keys.
   - Fire bullets at enemies using the spacebar.
   - Collect MysteryBalls to gain temporary power-ups.
3. **Score Points:**
   - Earn 1 point for each enemy destroyed.
   - MysteryBalls spawn based on your score milestones.

---

## Demo Video
Watch the gameplay demo [here](https://youtu.be/HlaEf7U2GXU).

---

## Game Rules
- **Player Controls:**
  - Move using arrow keys; shoot using the spacebar.
- **Objective:**
  - Destroy enemies, collect power-ups, and avoid damage.
- **Scoring:**
  - 1 point is awarded for each destroyed enemy.
- **MysteryBalls:**
  - Provide temporary boosts such as Health or Tri-bullet abilities.
- **Health:**
  - Start with 3 lives (hearts).
  - Lose a life upon getting hit or colliding with an enemy.

---

## Project Design and Implementation

### Overview
The game is built using object-oriented programming principles for maintainability and scalability.

### Key Classes and Concepts
- **`GameController`:**
  - Manages the game lifecycle, UI, scoring, and background elements.
- **`PlayerAirplane`:**
  - Handles player controls, movement, and shooting.
- **`EnemyAirplane`:**
  - Implements AI for patrolling and attacking behaviors.
- **`Bullet`:**
  - Manages player and enemy bullets, including movement and collision.
- **`Ball`:**
  - Base class for `Bullet` and `MysteryBall`, defining physics-based behavior.
- **`MysteryBall`:**
  - Spawns based on score milestones, providing power-ups.

### Power-ups and MysteryBalls
- MysteryBalls spawn randomly at score milestones.
- Grants temporary abilities such as:
  - **Health Boost:** Restores player health.
  - **Tri-Bullet:** Fires three bullets simultaneously.
    
---

## Key Functionalities
- Smooth player movement and shooting using key events.
- Collision detection for bullets, enemies, and power-ups.
- AI-driven enemy behavior with attack and patrol states.
- Randomly spawned power-ups managed via timers.

---

## Testing
- **Collision Handling:** Tested for accuracy with enemies and power-ups.
- **Power-up Activation:** Verified correct activation and deactivation timing.
- **Game State Transitions:** Ensured smooth transitions between login, gameplay, and game-over states.
- **Performance:** Optimized for smooth gameplay even with high object counts.

### Known Bugs
- Occasional overlapping of enemy spawns.
- Rare delays in power-up deactivation due to frame timing.

---

## Project Sophistication Level
- **Rating:** 90/100
- Includes dynamic AI interactions, engaging mechanics like tri-directional shooting, and state-driven enemy behavior.

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
