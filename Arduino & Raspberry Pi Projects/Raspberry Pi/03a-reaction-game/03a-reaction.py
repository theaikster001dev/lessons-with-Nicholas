import RPi.GPIO as GPIO
import time
import random

# Pin Definitions
BUTTON1 = 17
BUTTON2 = 27
LED = 22

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

# Helper to reset LED
def reset_led():
    GPIO.output(LED, GPIO.LOW)

try:
    print("Single LED Reaction Game Starting...")
    while True:
        reset_led()
        time.sleep(random.uniform(2, 5))  # Random delay
        GPIO.output(LED, GPIO.HIGH)  # Light up LED as signal
        print("Go!")

        start_time = time.time()
        winner = None
        while winner is None:
            if GPIO.input(BUTTON1) == GPIO.HIGH:
                winner = "Player 1"
            elif GPIO.input(BUTTON2) == GPIO.HIGH:
                winner = "Player 2"

        reaction_time = time.time() - start_time
        GPIO.output(LED, GPIO.LOW)  # Turn off LED after button press
        print(f"{winner} wins! Reaction time: {reaction_time:.3f} seconds")

        time.sleep(2)  # Pause before the next round
except KeyboardInterrupt:
    print("Game Exiting...")
finally:
    reset_led()
    GPIO.cleanup()