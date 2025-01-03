import easyocr
from pywinauto.application import Application
import os
import time


# CONSTANTS
CURR_CRIT_NAME = "Blighted Flue"
IMG_FILE_DIR = "example_images/"
BUILD_DIR = "build"

class McritsWindow:
    def __init__(self, w, h, window, rect):
        self.w = w
        self.h = h
        self.center = [w // 2, h // 2]
        self.window = window
        self.rect = rect
        
    
def run_farm():
    # Load text classifier
    # res = reader.readtext(IMG_FILE_DIR + "shellbee.jpg")
    reader = easyocr.Reader(['en'])

    mc_window = create_client("Miscrits (DEBUG)")
    window = mc_window.window

    try:
        while True:
            print("Searching for Miscrit...")
            window.wrapper_object().click_input(coords=(mc_window.center[0], mc_window.center[1]))

            os.makedirs(BUILD_DIR + "/crit_images", exist_ok=True)
            time.sleep(3)
            handle_battle(mc_window, reader)

    except KeyboardInterrupt:
        print("\nReceived Ctrl + C. Stopping farm...")

    return 

def handle_battle(mc_window, reader):
    curr_misc = [1]

    while len(curr_misc):
    # Check Miscrit
        region_left   = int(mc_window.w  * 0.60)
        region_top    = int(mc_window.h * 0.05)
        region_width  = int(mc_window.w  * 0.10)
        region_height = int(mc_window.h * 0.08)

        window = mc_window.window
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
        
        time.sleep(3)
        if not len(curr_misc):
            break
        
        print("Miscrit found, Attacking")
        window.wrapper_object().click_input(coords=(mc_window.w // 3, (mc_window.h // 20) * 19))

    time.sleep(2)
    print("Exiting Battle")
    window.wrapper_object().click_input(coords=(mc_window.w // 2, (mc_window.h // 20) * 16))
    time.sleep(2)

def create_client(app_title):
    app = Application(backend="win32").connect(title=app_title)
    window = app.window(title=app_title)
    rect = window.wrapper_object().rectangle()

    return McritsWindow(rect.width(), rect.height(), window, rect)