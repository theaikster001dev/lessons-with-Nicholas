import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 17  # GPIO 17
SWITCH_PIN = 27  # GPIO 27

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Main loop
try:
    while True:
        if GPIO.input(SWITCH_PIN) == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        else:
            GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        time.sleep(0.1)  # Debounce delay
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()