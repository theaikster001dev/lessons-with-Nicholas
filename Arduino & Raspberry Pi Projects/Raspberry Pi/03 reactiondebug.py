import RPi.GPIO as GPIO
import time

# Pin Definition
BUTTON = 27

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    print("Press the button connected to GPIO pin 27...")
    while True:
        if GPIO.input(BUTTON) == GPIO.HIGH:
            print("Button pressed!")
        else:
            print("Button not pressed.")
        time.sleep(0.2)  # Check every 200ms
except KeyboardInterrupt:
    print("Exiting button test...")
finally:
    GPIO.cleanup()