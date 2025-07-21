import RPi.GPIO as GPIO
import time

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number to which the buzzer is connected
BUZZER_PIN = 18

# Set up the GPIO pin as an output
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Constants for note names and their corresponding frequencies (in Hz)
C4 = 261
D4 = 293
E4 = 329
F4 = 349
G4 = 392
A4 = 440
B4 = 493

# Dictionary to map numeric values to note names
note_names = {
    C4: "C4",
    D4: "D4",
    E4: "E4",
    F4: "F4",
    G4: "G4",
    A4: "A4",
    B4: "B4",
}

# Jingle Bells melody (notes in order)
melody = [
    E4, E4, E4,  # "Jingle bells"
    E4, E4, E4,  # "Jingle all"
    E4, G4, C4, D4, E4,  # "the way"
    F4, F4, F4, F4, F4, E4, E4, E4, E4,  # "Oh what fun it is to ride"
    E4, D4, D4, E4, D4, G4  # "In a one horse open sleigh"
]

# Note durations (in milliseconds, 400ms = quarter note)
note_durations = [
    400, 400, 800,  # "Jingle bells"
    400, 400, 800,  # "Jingle all"
    400, 400, 400, 400, 800,  # "the way"
    400, 400, 400, 400, 400, 400, 400, 400, 400,  # "Oh what fun it is to ride"
    400, 400, 400, 400, 400, 800  # "In a one horse open sleigh"
]

# Pause duration between notes (in milliseconds)
pause_duration = 150

def play_tone(pin, frequency, duration):
    """
    Play a tone on the piezo buzzer.
    """
    if frequency == 0:  # Silent note (pause)
        time.sleep(duration)
        return

    # Calculate the period of the wave
    period = 1.0 / frequency
    half_period = period / 2
    cycles = int(duration * frequency)

    for _ in range(cycles):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(half_period)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(half_period)

try:
    while True:  # Infinite loop
        print("Playing Jingle Bells...")
        for i in range(len(melody)):
            note_freq = melody[i]
            note_duration = note_durations[i] / 1000.0  # Convert to seconds
            note_name = note_names.get(note_freq, "Pause")
            
            print(f"Playing {note_name} (Frequency: {note_freq} Hz) for {note_duration} seconds")
            
            # Play the note
            play_tone(BUZZER_PIN, note_freq, note_duration)
            
            # Brief pause between notes
            time.sleep(pause_duration / 1000.0)
        
        # Pause before repeating the melody
        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping Jingle Bells...")
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.cleanup()