# 3D Car Obstacle Game

**3D Car Obstacle Game** is a Python-based 3D driving game where players navigate a car along a road filled with obstacles like other vehicles and roadside trees. The game uses OpenGL for rendering, and includes both first-person and third-person camera views, real-time scoring, and interactive environmental controls such as day/night mode.

## Features

- Smooth third-person and first-person camera switching
- Dynamic obstacle generation (enemy cars and trees)
- Collision detection with Game Over screen
- Score tracking and restart system
- Pause and resume functionality
- Toggleable cheat mode to bypass collisions
- Adjustable scene lighting for day/night environments

## Technologies Used

- Python 3
- PyOpenGL
- GLUT
- NumPy

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/3d-car-obstacle-game.git
cd 3d-car-obstacle-game

pip install PyOpenGL PyOpenGL_accelerate numpy

```

Run the Game:
python game.py

Control:
| Key   | Function                               |
| ----- | -------------------------------------- |
| W     | Accelerate                             |
| S     | Decelerate                             |
| A     | Move Left                              |
| D     | Move Right                             |
| V     | Switch between first/third person view |
| P     | Pause / Resume                         |
| R     | Restart Game                           |
| C     | Toggle Cheat Mode (disable collisions) |
| K     | Switch to Day Mode                     |
| L     | Switch to Night Mode                   |
| Q     | Quit the game                          |
| ↑ / ↓ | Adjust camera angle (in third-person)  |

