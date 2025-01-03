import easyocr
from pywinauto.application import Application
import os
import time


# CONSTANTS
CURR_CRIT_NAME = "Blighted Flue"
IMG_FILE_DIR = "example_images/"
BUILD_DIR = "build"

class McritsClient:
    def __init__(self, w, h, window, rect):
        self.w = w
        self.h = h
        self.center = [w // 2, h // 2]
        self.window = window
        self.rect = rect

    def strong_attack(self):
        self.window.wrapper_object().click_input(coords=(self.w // 3, (self.h // 20) * 19))
    
    def weak_attack(self):
        #NOT IMPLEMENTED
        return

    def search(self):
        self.window.wrapper_object().click_input(coords=(self.center[0], self.center[1]))

    def exit_battle(self):
        self.window.wrapper_object().click_input(coords=(self.w // 2, (self.h // 20) * 16))
    
def run_farm():
    # Load text classifier
    reader = easyocr.Reader(['en'])

    mc_client = create_client("Miscrits (DEBUG)")
    os.makedirs(BUILD_DIR + "/crit_images", exist_ok=True)

    try:
        while True:
            print("Searching for Miscrit...")
            mc_client.search() 

            time.sleep(3)
            handle_battle(mc_client, reader)

    except KeyboardInterrupt:
        print("\nReceived Ctrl + C. Stopping farm...")

    return 

def handle_battle(mc_client, reader):
    time.sleep(3)
    curr_misc = ['NULL']

    while len(curr_misc):
        curr_misc = identify_miscrit(mc_client, reader) 
        if not len(curr_misc):
            break
        
        if CURR_CRIT_NAME not in curr_misc:
            print("Non-target Miscrit found, attacking")
            mc_client.strong_attack()
            time.sleep(3)
        else:
            print("Target Miscrit found, attempting to catch")
            attempt_capture(mc_client, reader)
            mc_client.weak_attack()
            time.sleep(3)

    time.sleep(2)
    print("Exiting Battle")
    mc_client.exit_battle()
    time.sleep(2)

def attempt_capture(mc_client, reader):
    time.sleep(5)
    #NOT IMPLEMENTED
    return

def identify_miscrit(mc_client, reader):
    # Check Miscrit
    region_left   = int(mc_client.w  * 0.60)
    region_top    = int(mc_client.h * 0.05)
    region_width  = int(mc_client.w  * 0.10)
    region_height = int(mc_client.h * 0.08)

    window = mc_client.window
    full_img = window.capture_as_image()

    crop_box = (
        region_left,
        region_top,
        region_left + region_width,
        region_top + region_height
    )
    sub_img = full_img.crop(crop_box)

    sub_img.save(os.path.join(BUILD_DIR, "crit_images", "curr_crit.png"))
    curr_misc = reader.readtext(os.path.join(BUILD_DIR, "crit_images", "curr_crit.png"), detail = 0)
    
    return curr_misc

def create_client(app_title):
    app = Application(backend="win32").connect(title=app_title)
    window = app.window(title=app_title)
    rect = window.wrapper_object().rectangle()

    return McritsClient(rect.width(), rect.height(), window, rect)
