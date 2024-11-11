import pyautogui
import cv2
import numpy as np
import time
import winsound  # Importing winsound to play sound

# Global variable to track the bot's running state
bot_running = True  # Set the bot to start running by default

# Function to find the image on the screen
def find_image_on_screen(image_path, threshold=0.8):
    """
    Searches for the given image on the screen and returns the coordinates of the match.
    :param image_path: Path to the image file (e.g., DPOLT.PNG).
    :param threshold: Matching threshold (default is 0.8 for 80% similarity).
    :return: Coordinates of the top-left corner of the matched image, or None if not found.
    """
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    target_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(screenshot_gray, target_image, cv2.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)

    if locations[0].size == 0:
        return None

    top_left = (locations[1][0], locations[0][0])
    return top_left

def simulate_click_at_coordinates(coordinates):
    """
    Simulates a click at the specified coordinates without moving the mouse.
    :param coordinates: Coordinates (x, y) to simulate the click.
    """
    if coordinates:
        current_position = pyautogui.position()
        pyautogui.click(coordinates[0], coordinates[1])
        pyautogui.moveTo(current_position)

def play_sound():
    """Plays a notification sound."""
    print("FELISFOUND.PNG found! Playing sound...")
    winsound.Beep(1000, 1000)

def stage_1():
    """Stage 1: Clicks on DPOLT.PNG and looks for BATTLEUI.PNG to transition to Stage 2."""
    print("Stage 1: Looking for DPOLT.PNG...")
    image_path = r"C:\Bot\DPOLT.PNG"
    
    click_coordinates = find_image_on_screen(image_path)
    if click_coordinates:
        simulate_click_at_coordinates(click_coordinates)
    
    if find_image_on_screen(r"C:\Bot\BATTLEUI.PNG"):
        print("BATTLEUI.PNG found. Transitioning to Stage 2...")
        return 2
    return 1

def stage_2():
    """Stage 2: Looks for FELISFOUND.PNG first, then clicks on VETO.PNG and looks for BATTLEFINISHED.PNG to transition to Stage 3."""
    print("Stage 2: Looking for FELISFOUND.PNG...")
    felis_found_path = r"C:\Bot\DPOLTFOUND.PNG"
    
    felis_coordinates = find_image_on_screen(felis_found_path)
    if felis_coordinates:
        play_sound()
        print("Felis is found!!!!!!")
        return 2
    
    print("Looking for VETO.PNG...")
    image_path = r"C:\Bot\VETO.PNG"
    
    veto_coordinates = find_image_on_screen(image_path)
    if veto_coordinates:
        simulate_click_at_coordinates(veto_coordinates)
    
    if find_image_on_screen(r"C:\Bot\BATTLEFINISHED.PNG"):
        print("BATTLEFINISHED.PNG found. Transitioning to Stage 3...")
        return 3
    return 2

def stage_3():
    """Stage 3: Clicks on CLOSE.PNG and returns to Stage 1."""
    print("Stage 3: Looking for CLOSE.PNG...")
    image_path = r"C:\Bot\CLOSE.PNG"
    
    close_coordinates = find_image_on_screen(image_path)
    if close_coordinates:
        simulate_click_at_coordinates(close_coordinates)
    
    print("Returning to Stage 1...")
    return 1

if __name__ == "__main__":
    stage = 1
    
    while True:
        if bot_running:
            if stage == 1:
                stage = stage_1()
            elif stage == 2:
                stage = stage_2()
            elif stage == 3:
                stage = stage_3()
        
        time.sleep(1)  # Wait for 1 second before checking again