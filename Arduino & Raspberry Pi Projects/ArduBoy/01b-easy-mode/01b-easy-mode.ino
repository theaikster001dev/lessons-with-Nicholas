#include <Arduboy2.h>
Arduboy2 arduboy;

// Player constants
const int PLAYER_SIZE = 5;
const int PLAYER_X = 20;
int playerY;
const int PLAYER_SPEED = 2; // pixels per frame when moving up or down

// Obstacle constants
const int OBSTACLE_WIDTH = 10;
int obstacleX;
int gapY;
const int GAP_HEIGHT = 50;   // Large gap makes it easier
const int OBSTACLE_SPEED = 1; // Slow moving obstacle

// Game state
bool gameOver = false;

void resetGame() {
  playerY = (64 - PLAYER_SIZE) / 2; // Center vertically
  obstacleX = 128;                  // Start at right edge
  gapY = random(0, 64 - GAP_HEIGHT);  // Random gap position
  gameOver = false;
}

void setup() {
  arduboy.begin();
  arduboy.setFrameRate(60);
  resetGame();
}

void updateGame() {
  // If game over, wait for A or B to restart
  if (gameOver) {
    if (arduboy.justPressed(A_BUTTON) || arduboy.justPressed(B_BUTTON)) {
      resetGame();
    }
    return;
  }
  
  // Use A button to move up, B button to move down
  if (arduboy.pressed(A_BUTTON)) {
    playerY -= PLAYER_SPEED;
    if (playerY < 0) playerY = 0;
  }
  if (arduboy.pressed(B_BUTTON)) {
    playerY += PLAYER_SPEED;
    if (playerY > 64 - PLAYER_SIZE) playerY = 64 - PLAYER_SIZE;
  }
  
  // Move the obstacle from right to left
  obstacleX -= OBSTACLE_SPEED;
  
  // Reset obstacle when it goes off-screen
  if (obstacleX < -OBSTACLE_WIDTH) {
    obstacleX = 128;
    gapY = random(0, 64 - GAP_HEIGHT);
  }
  
  // Check for collision:
  // If the player's horizontal range overlaps the obstacle
  // and the player is not within the safe gap.
  if (PLAYER_X + PLAYER_SIZE > obstacleX && PLAYER_X < obstacleX + OBSTACLE_WIDTH) {
    if (playerY < gapY || playerY + PLAYER_SIZE > gapY + GAP_HEIGHT) {
      gameOver = true;
    }
  }
}

void drawGame() {
  arduboy.clear();
  
  // Draw the player square
  arduboy.fillRect(PLAYER_X, playerY, PLAYER_SIZE, PLAYER_SIZE, WHITE);
  
  // Draw the obstacle in two parts (top and bottom)
  arduboy.fillRect(obstacleX, 0, OBSTACLE_WIDTH, gapY, WHITE);
  arduboy.fillRect(obstacleX, gapY + GAP_HEIGHT, OBSTACLE_WIDTH, 64 - (gapY + GAP_HEIGHT), WHITE);
  
  // Show game over message
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
