# Snake Game 🐍

A classic Snake game built using Python and Pygame.

I created this project to practice Python and game development using Pygame.

## Features

- Classic snake movement.
- Snake grows when it eats food.
- Random food spawning, including walls and corners.
- Collision detection with walls and the snake's own body.
- Background music and sound effects.
- Main menu, restart, and exit functionality.

## Controls

| Key | Action     |
| --- | ---------- |
| W   | Move Up    |
| A   | Move Left  |
| S   | Move Down  |
| D   | Move Right |

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/haadi-aamir/Snake-Game.git
   ```

2. Navigate to the project directory:

   ```bash
   cd snake_game
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:

   ```bash
   python snake.py
   ```

## Requirements

- Python 3
- Pygame

## Assets

The game uses images and audio files stored in the `Resources` and `music` directories.

## Improvements for future
- The movement is fps based, meaning it is affected by how fast or slow a pc is, it can be improved by implementing a time based movement system.
- sprites for snake and balls.
- better collision handling.