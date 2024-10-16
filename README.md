# Snake Game 🐍🎮

Welcome to the classic **Snake Game**, where you control a snake as it slithers around the screen, eating food and growing longer. But beware: running into yourself or the walls will end the game!

## Game Demo

![Snake Game Demo](https://github.com/mudittiwari/SnakeGameWeb/blob/master/snakegame-master/demo.gif)

## Game Walkthrough

### Objective:
Guide the snake to eat food, avoid running into yourself, and try to grow as long as possible!

### Controls:
- **mouse click/tap**: Move the snake in the desired direction with tap on screen or mouse click (up, down, left, right).

### Gameplay:
1. **Start Screen**: The game starts with a welcome screen. Double-tap to start the game.
2. **Snake Movement**: Use the arrow keys to control the direction of the snake's movement.
3. **Eating Food**: Each time the snake eats food, it grows longer.
4. **Scoring**: The score increases as you eat more food and the snake grows longer.
5. **Game Over**: The game ends if the snake runs into itself or the walls.

### How I Converted the Game to Web Using WebAssembly:
- Like with Flappy Bird, I used **Pygbag** to compile this Python game into **WebAssembly**.
- This allows the game to run efficiently in web browsers, making it accessible to everyone, without needing to install Python or any extra dependencies.

## Play the Game:
The game is hosted on **GitHub Pages**. [Play Snake Game Now!](https://mudittiwari.github.io/SnakeGameWeb/)

## Technologies Used:
- **Python** for game mechanics and logic.
- **Pygame** for rendering the graphics.
- **Pygbag** for WebAssembly conversion and browser compatibility.
