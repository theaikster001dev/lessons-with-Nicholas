#include <Arduboy2.h>

Arduboy2 arduboy;

void setup() {
    arduboy.begin();
    arduboy.clear();
    arduboy.setCursor(20, 30);
    arduboy.print("Hello, World!");
    arduboy.display();
}

void loop() {
    // Do nothing, as we only display text
}