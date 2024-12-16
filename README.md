# Airplane Shooting Game

## Project Title
Airplane Shooting Game

## Description
A fast-paced arcade-style game where players control an airplane to shoot enemies, dodge bullets, and collect power-ups while progressing through increasingly challenging waves of enemies.

---

## Overview
The **Airplane Shooting Game** is an interactive, event-driven game combining action and strategy. Players control a customizable airplane, striving to survive enemy waves using strategic shooting and dodging techniques. Exciting features include power-ups, dynamic enemy AI, visually engaging effects, sound effects (SFX), and score tracking.

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
- **Sound Effects (SFX):**
  - Start sound when entering the login screen.
  - Shooting sound when firing bullets.
  - Power-up sound when collecting mystery balls.
  - Explosion sound when destroying airplanes.
- **Score Tracking:**
  - Records the player’s username and score in a CSV file (`scores.csv`).
  - Displays a scoreboard after the game ends.
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
4. **View Scoreboard:**
   - After the game ends, view the top scores from the `scores.csv` file.

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
  - Records player scores into a CSV file and displays a scoreboard.
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
- **`SoundManager`:**
  - Handles all sound effects (e.g., shooting, explosions, power-ups, and game start).

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
- Score recording and display using a CSV file (`scores.csv`).
- Immersive sound effects (SFX) to enhance gameplay.

---

## Testing
- **Collision Handling:** Tested for accuracy with enemies and power-ups.
- **Power-up Activation:** Verified correct activation and deactivation timing.
- **Game State Transitions:** Ensured smooth transitions between login, gameplay, and game-over states.
- **Performance:** Optimized for smooth gameplay even with high object counts.
- **Score Recording:** Verified correct appending and sorting in `scores.csv`.

### Known Bugs
- Occasional overlapping of enemy spawns.
- Rare delays in power-up deactivation due to frame timing.

---

## Project Sophistication Level
- **Rating:** 95/100
- Features dynamic AI interactions, engaging mechanics like tri-directional shooting, sound effects, and a persistent scoring system.

---

## UML Class Diagram

Here’s the UML class diagram illustrating the structure of the game and how the classes interact.

```mermaid
classDiagram
    %% Main Game Controller
    class GameController {
        - screen : TurtleScreen
        - player : PlayerAirplane
        - enemies : List[EnemyAirplane]
        - mystery_balls : List[MysteryBall]
        - username : str
        - score_text : Turtle
        + login_screen() void
        + start_game() void
        + display_game_over() void
        + save_score_to_csv() void
        + show_scoreboard() void
        + game_loop() void
    }

    %% Sound Management
    class SoundManager {
        + START_SOUND : Sound
        + POWERUP_SOUND : Sound
        + EXPLOSION_SOUND : Sound
        + SHOOTING_SOUND : Sound
        + play_start_sound() void
        + play_powerup_sound() void
        + play_explosion_sound() void
        + play_shooting_sound() void
    }

    %% Airplanes
    class Airplane {
        - position : Tuple[float, float]
        - velocity : Tuple[float, float]
        - health : int
        - size : int
        - bullets : List[Bullet]
        + move() void
        + take_damage(amount : int) void
        + destroy() void
        + update_bullets(target : Airplane) void
    }

    Airplane <|-- PlayerAirplane : Inherits
    Airplane <|-- EnemyAirplane : Inherits

    class PlayerAirplane {
        - is_tridirectional : bool
        - speed_multiplier : float
        + press_up() void
        + release_up() void
        + activate_tridirectional_shooting() void
        + deactivate_ability() void
        + move_airplane_directional() void
        + shoot() void
    }

    class EnemyAirplane {
        - state : str
        - patrol_bounds : Tuple[float, float]
        + handle_state_machine(target : Airplane) void
        + move_patrol() void
        + move_attack(target : Airplane) void
        + shoot_based_on_shape() void
    }

    %% Mystery Ball
    class MysteryBall {
        - type : int
        + move() void
        + activate_ability(player : PlayerAirplane) void
        + is_ability_active(player : PlayerAirplane) bool
    }

    MysteryBall <|-- Ball : Inherits

    %% Bullets
    class Bullet {
        - owner : str
        + hide_bullet() void
        + is_off_screen() bool
        + move() void
    }

    Bullet <|-- Ball : Inherits

    %% Base Ball Class
    class Ball {
        - size : int
        - position : Tuple[float, float]
        - velocity : Tuple[float, float]
        - mass : float
        + bounce_off_wall() void
        + bounce_off(ball : Ball) void
        + distance(ball : Ball) float
    }

    %% Relationships
    GameController --> SoundManager : Uses
    GameController --> PlayerAirplane : Manages
    GameController --> EnemyAirplane : Manages
    GameController --> MysteryBall : Manages
    GameController --> Bullet : Manages
    PlayerAirplane --> Bullet : Fires
    EnemyAirplane --> Bullet : Fires
    MysteryBall --> PlayerAirplane : Activates Abilities