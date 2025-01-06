import easyocr
from pywinauto.application import Application
import os
import time
import re
import logging

# CONSTANTS
CRIT_NAMES_PG = ['Peekly', 'Felis', 'Owlie']  
CRIT_NAMES_BF = ['Shellbee', 'Squibee', 'Crickin', 'Steamguin']

CRIT_NAMES = [CRIT_NAMES_BF, CRIT_NAMES_PG]

IMG_FILE_DIR = "example_images/"
BUILD_DIR = "build"

# Functions for Controlling Miscrits Window
class McritsClient:
    def __init__(self, w, h, window, rect):
        self.w = w
        self.h = h
        self.center = [w // 2, h // 2]
        self.window = window
        self.rect = rect

    # < BATTLE MENU >
    def first_attack(self):
        self.window.wrapper_object().click_input(coords=(self.w // 3, (self.h // 20) * 18))
    
    def third_attack(self):
        self.window.wrapper_object().click_input(coords=((self.w // 7) * 4, (self.h // 20) * 18))

    def second_attack(self):
        self.window.wrapper_object().click_input(coords=((self.w // 7) * 3, (self.h // 20) * 18))

    def last_attack(self):
        self.window.wrapper_object().click_input(coords=((self.w // 9) * 6, (self.h // 20) * 18))

    def scroll_right(self):
        self.window.wrapper_object().click_input(coords=((self.w // 31) * 23, (self.h // 22) * 20))

    def scroll_left(self):
        self.window.wrapper_object().click_input(coords=((self.w // 30) * 8, (self.h // 22) * 20))

    def capture(self):
        self.window.wrapper_object().click_input(coords=(self.w // 2, (self.h // 13) * 2))

    def capture_again(self):
        self.window.wrapper_object().click_input(coords=((self.w // 19) * 9, (self.h // 20) * 12))

    def skip(self):
        self.window.wrapper_object().click_input(coords=((self.w // 20) * 9, (self.h // 20) * 12))

    def exit_battle(self):
        self.window.wrapper_object().click_input(coords=(self.w // 2, (self.h // 20) * 16))
    # ... Battle

    # < OPEN WORLD > 
    def search(self):
        self.window.wrapper_object().click_input(coords=(self.center[0], self.center[1]))

    def heal(self):
        self.window.wrapper_object().click_input(coords=((self.w // 7) * 6, (self.h // 20) * 2))

    def keep(self):
        self.window.wrapper_object().click_input(coords=((self.w // 17) * 9, (self.h // 20) * 12))
    # ... Open World

    # < LEVEL UP MENU > 
    def level_open(self):
        self.window.wrapper_object().click_input(coords=((self.w // 7) * 2, (self.h // 20) * 2))

    def level_plat_train(self):
        self.window.wrapper_object().click_input(coords=((self.w // 17) * 7, (self.h // 21) * 19))

    def level_train(self):
        self.window.wrapper_object().click_input(coords=((self.w // 17) * 8, (self.h // 21) * 4))

    def level_continue(self):
        self.window.wrapper_object().click_input(coords=((self.w // 17) * 9, (self.h // 21) * 19))

    def level_ability_continue(self):
        self.window.wrapper_object().click_input(coords=((self.w // 15) * 7, (self.h // 20) * 13))

    def level_exit(self):
        self.window.wrapper_object().click_input(coords=((self.w // 26) * 18, (self.h // 25) * 4))

    def level_select_first_miscrit(self):
        self.window.wrapper_object().click_input(coords=((self.w // 7) * 2, (self.h // 20) * 5))

    def level_select_second_miscrit(self):
        self.window.wrapper_object().click_input(coords=((self.w // 7) * 2, (self.h // 20) * 6))
    
    def level_select_third_miscrit(self):
        self.window.wrapper_object().click_input(coords=((self.w // 7) * 2, (self.h // 20) * 7))
    # .. Level Up Menu

def run_farm(args):
    crit_names = CRIT_NAMES[args.farm - 1]

    # Load text classifier
    reader = easyocr.Reader(['en'])
    mc_client = create_client("Miscrits (DEBUG)")

    last_heal_time = time.time()
    last_search_time = time.time() - 30
    os.makedirs(BUILD_DIR + "/crit_images", exist_ok=True)

    try:
        while True:
            # Healing Logic
            current_time = time.time()
            heal_elapsed = current_time - last_heal_time

            if heal_elapsed >= 1300:  
                mc_client.heal()
                last_heal_time = current_time

            # Searching Logic
            current_time = time.time()
            search_elapsed = current_time - last_search_time

            if search_elapsed < 30:
                time.sleep(30 - search_elapsed + 0.5)

            logging.info("Searching for Miscrit...")
            last_search_time = time.time()
            mc_client.search() 

            time.sleep(4.5)
            handle_battle(mc_client, reader, crit_names, args.level)
            time.sleep(3)

    except KeyboardInterrupt:
        logging.info("\nReceived Ctrl + C. Stopping farm...")

    return 

def handle_battle(mc_client, reader, crit_names, level):
    misc_cnt = 0
    curr_misc = ['NULL']
    capture_attempt = False

    # < HANDLE BATTLE LOGIC >
    while len(curr_misc):
        curr_misc = identify_miscrit(mc_client, reader) 
        if not len(curr_misc):
            break
        
        misc_cnt += 1

        logging.info("Found " + str(curr_misc))
        target = True
        for crit in crit_names:
            if crit in curr_misc:
                target = False

        if not target:
            logging.info("Non-target Miscrit found, attacking")
            mc_client.scroll_left()
            mc_client.scroll_left()
            mc_client.first_attack()
            time.sleep(2.5)
        else:
            logging.info("Target Miscrit found, attempting to catch")
            time.sleep(3.5)
            attempt_capture(mc_client, reader, capture_attempt)
            capture_attempt = True
            time.sleep(3.5)

    # Search failed 
    if misc_cnt == 0:
        logging.info("No miscrit found")
        return
    
    time.sleep(1.2)
    
    # < BATTLE FINISHED >
    level_menu_data = []

    if level:
        time.sleep(1.5)
        sub_img = capture_section(mc_client, 0.25, 0.25, 0.4, 0.4)

        sub_img.save(os.path.join(BUILD_DIR, "crit_images", "level.jpg"))
        level_menu_data = reader.readtext(os.path.join(BUILD_DIR, "crit_images", "level.jpg"), detail = 0)
        logging.info("Level UP?: " + str(level_menu_data))

    logging.info("Exiting Battle")
    mc_client.exit_battle()

    # Checks and closes new miscrit dialogue
    
    if capture_attempt:
        time.sleep(1)

        sub_img = capture_section(mc_client, 0.35, 0.35, 0.3, 0.3)

        sub_img.save(os.path.join(BUILD_DIR, "crit_images", "new_misc.png"))
        new_misc_data = reader.readtext(os.path.join(BUILD_DIR, "crit_images", "new_misc.png"), detail = 0)

        if 'New Miscrit' in new_misc_data:
            logging.info("New Miscrit captured, closing dialogue")
            mc_client.keep()

            sub_img = capture_section(mc_client, 0.3, 0.3, 0.3, 0.3)

    # < LEVELS UP IF NEEDED > 
    if not level:
        return 
    
    level_ready = True
    for s in level_menu_data:
        if 'xp' in s.lower():
            level_ready = False
            break

    if level_ready:
        time.sleep(1.5)
        mc_client.level_open()
        time.sleep(0.2)
        mc_client.level_select_second_miscrit()
        time.sleep(0.2)
        mc_client.level_train()
        time.sleep(0.2)
        mc_client.level_plat_train()
        time.sleep(0.2)
        mc_client.level_continue()
        time.sleep(0.5)
        mc_client.level_ability_continue()
        time.sleep(0.2)
        mc_client.level_exit()

def capture_section(mc_client, left, top, width, height):
    # Check Miscrit
    region_left   = int(mc_client.w  * left)
    region_top    = int(mc_client.h * top)
    region_width  = int(mc_client.w  * width)
    region_height = int(mc_client.h * height)

    window = mc_client.window
    full_img = window.capture_as_image()

    crop_box = (
        region_left,
        region_top,
        region_left + region_width,
        region_top + region_height
    )
    sub_img = full_img.crop(crop_box)

    return sub_img

def attempt_capture(mc_client, reader, capture_attempt):
    sub_img = capture_section(mc_client, 0.45, 0.17, 0.13, 0.03)

    sub_img.save(os.path.join(BUILD_DIR, "crit_images", "capture.png"))
    cap_data = reader.readtext(os.path.join(BUILD_DIR, "crit_images", "capture.png"), detail = 0)

    if not len(cap_data):
        cap_num = 0
    else:
        cap_num = float(re.sub(r"\D+", "", cap_data[-1]))

    logging.info("Capture Percentage: " + str(cap_num))
    if not capture_attempt:
        mc_client.scroll_left()
        mc_client.scroll_left()
        mc_client.first_attack()
        time.sleep(7)

    while cap_num < 80:
        mc_client.scroll_right()
        mc_client.scroll_right()
        mc_client.last_attack()
        time.sleep(7)

        sub_img = capture_section(mc_client, 0.45, 0.17, 0.13, 0.03)

        sub_img.save(os.path.join(BUILD_DIR, "crit_images", "capture.png"))
        cap_data = reader.readtext(os.path.join(BUILD_DIR, "crit_images", "capture.png"), detail = 0)

        if not len(cap_data):
            cap_num = 0
        else:
            cap_num = float(re.sub(r"\D+", "", cap_data[-1]))

        logging.info("Capture Percentage: " + str(cap_num))

    logging.info("Capture percentage high enough, trying to catch now")
    mc_client.capture()
    time.sleep(1.5)
    mc_client.capture_again()
    time.sleep(6)
    mc_client.skip()

def identify_miscrit(mc_client, reader):
    # Check Miscrit
    sub_img = capture_section(mc_client, 0.6, 0.05, 0.1, 0.08)

    sub_img.save(os.path.join(BUILD_DIR, "crit_images", "curr_crit.png"))
    curr_misc_data = reader.readtext(os.path.join(BUILD_DIR, "crit_images", "curr_crit.png"), detail = 0)
    
    return curr_misc_data

def create_client(app_title):
    app = Application(backend="win32").connect(title=app_title)
    window = app.window(title=app_title)
    rect = window.wrapper_object().rectangle()

    return McritsClient(rect.width(), rect.height(), window, rect)
