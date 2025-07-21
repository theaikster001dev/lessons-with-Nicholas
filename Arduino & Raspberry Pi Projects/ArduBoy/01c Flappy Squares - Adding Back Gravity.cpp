#include <Arduboy2.h>
Arduboy2 arduboy;

// Player constants
const int PLAYER_SIZE = 5;
const int PLAYER_X = 20;
float playerY;
float playerVelocity;
const float GRAVITY = 0.05;      // Very gentle gravity pull
const float CONTROL_ACCEL = 0.15; // Acceleration when pressing A or B

// Obstacle constants
const int OBSTACLE_WIDTH = 10;
int obstacleX;
int gapY;
const int GAP_HEIGHT = 50;       // Large gap for easier navigation
const int OBSTACLE_SPEED = 1;    // Slow moving obstacle

// Game state
bool gameOver = false;

void resetGame() {
  playerY = (64 - PLAYER_SIZE) / 2.0; // Center the player vertically
  playerVelocity = 0;
  obstacleX = 128;                    // Start at right edge
  gapY = random(0, 64 - GAP_HEIGHT);    // Random gap position
  gameOver = false;
}

void setup() {
  arduboy.begin();
  arduboy.setFrameRate(60);
  resetGame();
}

void updateGame() {
  if (gameOver) {
    // Restart the game if either button is pressed after game over.
    if (arduboy.justPressed(A_BUTTON) || arduboy.justPressed(B_BUTTON)) {
      resetGame();
    }
    return;
  }
  
  // Manual control: A moves up, B moves down.
  if (arduboy.pressed(A_BUTTON)) {
    playerVelocity -= CONTROL_ACCEL;
  }
  if (arduboy.pressed(B_BUTTON)) {
    playerVelocity += CONTROL_ACCEL;
  }
  
  // Apply gravity (pulls the square down slowly)
  playerVelocity += GRAVITY;
  playerY += playerVelocity;
  
  // Clamp the player's position within the screen boundaries.
  if (playerY < 0) {
    playerY = 0;
    playerVelocity = 0;
  }
  if (playerY > 64 - PLAYER_SIZE) {
    playerY = 64 - PLAYER_SIZE;
    playerVelocity = 0;
  }
  
  // Move the obstacle from right to left.
  obstacleX -= OBSTACLE_SPEED;
  
  // Reset obstacle when it goes off-screen.
  if (obstacleX < -OBSTACLE_WIDTH) {
    obstacleX = 128;
    gapY = random(0, 64 - GAP_HEIGHT);
  }
  
  // Check for collision:
  // When the player's horizontal range overlaps the obstacle,
  // and the player's vertical position is not within the gap.
  if (PLAYER_X + PLAYER_SIZE > obstacleX && PLAYER_X < obstacleX + OBSTACLE_WIDTH) {
    if (playerY < gapY || playerY + PLAYER_SIZE > gapY + GAP_HEIGHT) {
      gameOver = true;
    }
  }
}

void drawGame() {
  arduboy.clear();
  
  // Draw the player square (casting playerY to int for drawing).
  arduboy.fillRect(PLAYER_X, (int)playerY, PLAYER_SIZE, PLAYER_SIZE, WHITE);
  
  // Draw the obstacle in two parts: above and below the gap.
  arduboy.fillRect(obstacleX, 0, OBSTACLE_WIDTH, gapY, WHITE);
  arduboy.fillRect(obstacleX, gapY + GAP_HEIGHT, OBSTACLE_WIDTH, 64 - (gapY + GAP_HEIGHT), WHITE);
  
  // Display game over message if needed.
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
