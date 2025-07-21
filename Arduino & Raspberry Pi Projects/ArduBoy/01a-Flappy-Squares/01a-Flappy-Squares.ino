#include <Arduboy2.h>
Arduboy2 arduboy;

// Player constants
const int PLAYER_SIZE = 5;
const int PLAYER_X = 20;
float playerY;
float playerVelocity;
const float GRAVITY = 0.3;
const float JUMP_STRENGTH = -5.0;

// Obstacle constants
const int OBSTACLE_WIDTH = 10;
int obstacleX;
int gapY;
const int GAP_HEIGHT = 20;
const int OBSTACLE_SPEED = 2;

// Game state
bool gameOver = false;

void resetGame() {
  // Center the player vertically
  playerY = (64 - PLAYER_SIZE) / 2;
  playerVelocity = 0;
  // Start the obstacle at the right edge
  obstacleX = 128;
  // Randomize the gap position (keep a margin at top and bottom)
  gapY = random(10, 64 - GAP_HEIGHT - 10);
  gameOver = false;
}

void setup() {
  arduboy.begin();
  arduboy.setFrameRate(60);
  resetGame();
}

void updateGame() {
  // Jump when the A button is pressed
  if (arduboy.justPressed(A_BUTTON)) {
    // If the game is over, restart; otherwise, jump.
    if (gameOver) {
      resetGame();
    } else {
      playerVelocity = JUMP_STRENGTH;
    }
  }
  
  if (!gameOver) {
    // Apply gravity to player
    playerVelocity += GRAVITY;
    playerY += playerVelocity;
  
    // Move obstacle from right to left
    obstacleX -= OBSTACLE_SPEED;
  
    // Reset obstacle when it moves off-screen
    if (obstacleX < -OBSTACLE_WIDTH) {
      obstacleX = 128;
      gapY = random(10, 64 - GAP_HEIGHT - 10);
    }
  
    // Check for collision with top or bottom of screen
    if (playerY < 0 || playerY > 64 - PLAYER_SIZE) {
      gameOver = true;
    }
  
    // Check for collision with obstacle:
    // If the player's x-range overlaps with the obstacle's and the player is not within the gap.
    if (PLAYER_X + PLAYER_SIZE > obstacleX && PLAYER_X < obstacleX + OBSTACLE_WIDTH) {
      if (playerY < gapY || playerY + PLAYER_SIZE > gapY + GAP_HEIGHT) {
        gameOver = true;
      }
    }
  }
}

void drawGame() {
  arduboy.clear();

  // Draw the player square
  arduboy.fillRect(PLAYER_X, playerY, PLAYER_SIZE, PLAYER_SIZE, WHITE);

  // Draw the obstacle as two rectangles:
  // Top obstacle from the top to the gap.
  arduboy.fillRect(obstacleX, 0, OBSTACLE_WIDTH, gapY, WHITE);
  // Bottom obstacle from the gap's bottom to the screen bottom.
  arduboy.fillRect(obstacleX, gapY + GAP_HEIGHT, OBSTACLE_WIDTH, 64 - (gapY + GAP_HEIGHT), WHITE);

  // If game over, display a message
  if (gameOver) {
    arduboy.setCursor(30, 30);
    arduboy.print("Game Over");
  }

  arduboy.display();
}

void loop() {
  if (!arduboy.nextFrame()) return;
  arduboy.pollButtons();
  
  updateGame();
  drawGame();
}