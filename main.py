import time
from gpiozero import Servo

# --- Configuration ---

# Set the GPIO pin number (using BCM numbering)
# You specified GPIO 2, which is Pin 3 on the header.
SERVO_PIN = 2

# --- Main Program ---

print(f"Starting servo control on GPIO {SERVO_PIN}...")
print("Press CTRL+C to stop.")

# Create a Servo object linked to your pin
# By default, gpiozero uses a standard pulse width range
# (1ms for min, 1.5ms for mid, 2ms for max)
# If your servo behaves strangely, you might need to
# calibrate these values.
servo = Servo(SERVO_PIN)

try:
    # Loop forever to move the servo back and forth
    while True:
        # Move to the minimum position (approx. 0 degrees)
        print("Moving to min...")
        servo.min()
        time.sleep(2)

        # Move to the middle position (approx. 90 degrees)
        print("Moving to mid...")
        servo.mid()
        time.sleep(2)

        # Move to the maximum position (approx. 180 degrees)
        print("Moving to max...")
        servo.max()
        time.sleep(2)

except KeyboardInterrupt:
    # This block runs when you press CTRL+C
    print("\nStopping program.")

finally:
    # Clean up the GPIO pin
    servo.close()
    print("GPIO cleanup complete. Exiting.")
