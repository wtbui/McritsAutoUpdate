import easyocr
import win32gui
import win32api
import win32con

# CONSTANTS
CURR_CRIT_NAME = "blighted flue"
IMG_FILE_DIR = "example_images/"

def run_farm():
    reader = easyocr.Reader(['ch_sim','en'])
    res = reader.readtext(IMG_FILE_DIR + "shellbee.jpg")
    print(res)

    hwnd = win32gui.FindWindow(None, "Miscrits (DEBUG)")

    x, y = 100, 200

    # Press down
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, (y << 16) | x)
    # Release
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, (y << 16) | x)

    return 
