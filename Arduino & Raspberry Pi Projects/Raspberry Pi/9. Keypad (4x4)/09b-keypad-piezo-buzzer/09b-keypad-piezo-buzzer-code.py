import RPi.GPIO as GPIO
import time
import random

# GPIO pin definitions for keypad
L1 = 24
L2 = 25
L3 = 8
L4 = 7
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# GPIO pin for the buzzer
BUZZER = 18

# The PIN code to stop the alarm
PIN_CODE = "1234"

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup keypad GPIO pins
GPIO.setup([L1, L2, L3, L4], GPIO.OUT)
GPIO.setup([C1, C2, C3, C4], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup buzzer GPIO pin
GPIO.setup(BUZZER, GPIO.OUT)

# Global variables
input_code = ""  # To store the entered PIN
alarm_active = False  # Alarm state


def buzz(state):
    """Turn the buzzer on or off."""
    GPIO.output(BUZZER, state)


def read_line(line, characters):
    """Read input from the keypad."""
    global input_code, alarm_active

    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        process_key(characters[0])
    if GPIO.input(C2) == 1:
        process_key(characters[1])
    if GPIO.input(C3) == 1:
        process_key(characters[2])
    if GPIO.input(C4) == 1:
        process_key(characters[3])
    GPIO.output(line, GPIO.LOW)


def process_key(key):
    """Handle key press events."""
    global input_code, alarm_active

    if alarm_active:  # Only process keys if the alarm is active
        print(f"Key pressed: {key}")
        input_code += key

        if len(input_code) >= len(PIN_CODE):  # Check PIN code
            if input_code == PIN_CODE:
                print("Correct PIN entered. Alarm deactivated.")
                buzz(False)  # Turn off the buzzer
                alarm_active = False
            else:
                print("Incorrect PIN. Try again.")
            input_code = ""  # Reset the entered PIN


try:
    # Main program loop
    print("System initialized. Waiting for alarm...")
    time.sleep(random.randint(5, 15))  # Random delay before alarm activates
    print("ALARM TRIGGERED!")
    buzz(True)  # Activate the buzzer
    alarm_active = True

    while True:
        # Continuously check the keypad
        read_line(L1, ["1", "2", "3", "A"])
        read_line(L2, ["4", "5", "6", "B"])
        read_line(L3, ["7", "8", "9", "C"])
        read_line(L4, ["*", "0", "#", "D"])
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nApplication stopped!")

finally:
    GPIO.cleanup()
