import RPi.GPIO as GPIO
import time

# GPIO pin definitions for ultrasonic sensor
TRIG = 6
ECHO = 5

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

# Alarm state
alarm_active = False
input_code = ""

# Distance threshold for triggering the alarm (in cm)
DISTANCE_THRESHOLD = 30

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup ultrasonic sensor GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Setup keypad GPIO pins
GPIO.setup([L1, L2, L3, L4], GPIO.OUT)
GPIO.setup([C1, C2, C3, C4], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup buzzer GPIO pin
GPIO.setup(BUZZER, GPIO.OUT)

def buzz(state):
    """Turn the buzzer on or off."""
    GPIO.output(BUZZER, state)

def measure_distance():
    """Measure distance using the ultrasonic sensor."""
    # Send a 10us pulse to the TRIG pin
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for the ECHO pin to go HIGH
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for the ECHO pin to go LOW
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate the distance based on the time of the echo
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound: 34300 cm/s
    distance = round(distance, 2)
    return distance

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

    if alarm_active:
        print(f"Key pressed: {key}")
        input_code += key

        if len(input_code) >= len(PIN_CODE):
            if input_code == PIN_CODE:
                print("Correct PIN entered. Alarm deactivated.")
                buzz(False)
                alarm_active = False
            else:
                print("Incorrect PIN. Try again.")
            input_code = ""

try:
    print("System initialized. Monitoring for motion...")

    while True:
        # Measure distance
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        if distance < DISTANCE_THRESHOLD and not alarm_active:
            print("Motion detected! Alarm triggered!")
            buzz(True)
            alarm_active = True

        if alarm_active:
            # Check keypad for PIN entry
            read_line(L1, ["1", "2", "3", "A"])
            read_line(L2, ["4", "5", "6", "B"])
            read_line(L3, ["7", "8", "9", "C"])
            read_line(L4, ["*", "0", "#", "D"])

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nApplication stopped!")

finally:
    GPIO.cleanup()
