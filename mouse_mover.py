import argparse
import random
import time
import sys

try:
    import pyautogui
except ImportError:
    sys.exit("Please install pyautogui module: pip install pyautogui")

def random_mouse_movement(duration, speed, screen_range, motion_type):
    end_time = time.time() + duration
    screen_width, screen_height = pyautogui.size()

    while time.time() < end_time:
        if screen_range == 'full':
            x, y = random.randint(0, screen_width), random.randint(0, screen_height)
        else:
            x, y = map(int, screen_range.split(','))

        if motion_type == 'human':
            pyautogui.moveTo(x, y, duration=speed)
        else:
            pyautogui.moveTo(x, y)

        time.sleep(speed)

def main():
    parser = argparse.ArgumentParser(description='Control mouse movement in random directions.')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Duration of mouse movement (default: 60 minutes)')
    parser.add_argument('-s', '--speed', type=float, default=4, help='Speed of mouse movement (default: 4 seconds)')
    parser.add_argument('-r', '--range', type=str, default='full', help='Range of motion (default: full screen or specify x,y)')
    parser.add_argument('-m', '--motion', type=str, default='human', choices=['human', 'linear', 'jittery'], help='Type of motion (default: human)')
   
    args = parser.parse_args()
    args.duration *= 60    

    try:
        random_mouse_movement(args.duration, args.speed, args.range, args.motion)
    except KeyboardInterrupt:
        print("Mouse movement interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == '__main__':
    main()
