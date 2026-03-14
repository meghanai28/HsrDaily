# mss grabs pixel data gives back as grid of numbers
# each screenshot - 3D array (1080,1920,3)

# mss.mss() -> screen capture objuct
# .monitors gives list of displays -> monitors[1] is primary
#.grab(monitor) captures region and returns pixel data
# wrap in numpy.array so we can work with it

# OpenCV match template -> small image and slides across big image & scores how well each position mtaches
# function returns a score at every postion -> perfect match is 1.0 and total mismatch would be 0
# cv2.imread() loads image file
# cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED) does the matching Full doc: https://docs.opencv.org/4.x/df/dfb/group__imgproc__object.html
# cv2.minMaxLoc(result) - finds the pos of best match

# pyautogui 
# pyautogui clicks at pos : pyautogui.click(x,y), press some key: pyautogui.press('esc'), pyautogui.FAILSAFE = True (move mouse top left corner it will exit script)

import mss
import numpy as np
import pathlib
import cv2
import pyautogui
import time
import keyboard

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"

class TimeOutError(Exception):
    pass

class EmergencyStop(Exception):
    pass

class ScreenCapture:
    def __init__ (self):
        self.sct = mss.mss()
        self.stopped = False
        keyboard.add_hotkey('F10', self.on_hotkey_trigger)

    def template_match(self,template_name):
        # load template
        self.check_stop()
        test_path = (TEMPLATE_DIR/template_name).resolve()
        template = cv2.imread(str(test_path))
        width = template.shape[1] # rows
        height = template.shape[0] # cols
        if template is None: 
            raise FileNotFoundError(f"Could not find file at {test_path}")
        
        # take screenshot
        monitor = self.sct.monitors[1] 
        # print(monitor["width"], monitor["height"])
        raw_data = self.sct.grab(monitor)
        output = np.asarray(raw_data)
        screen = cv2.cvtColor(output,cv2.COLOR_BGRA2BGR)
        print(screen.shape)

        # template matching
        result = cv2.matchTemplate(screen,template, cv2.TM_CCOEFF_NORMED)
        pos = cv2.minMaxLoc(result) # gives us min_val,max_val, min_loc, max_loc - coeff needs to be maxed
        return pos[1],pos[3],width,height

    def find_and_click(self,template_name):
        self.check_stop()
        conf_value, top_left, temp_width, temp_height,  = self.template_match(template_name)
        if conf_value > 0.85:
            center_x = top_left[0] + (temp_width/2)
            center_y = top_left[1] + (temp_height/2)
            pyautogui.click(center_x,center_y)
            return True
        return False


    # call template match in loop every 0.5 seconds. Finds template (score > 0.85) within timeout return position.
    # time.time()
    def wait_for(self,template_name,timeout=10):
        start = time.time()
        while (time.time() - start) < timeout:
            self.check_stop()
            conf_value, top_left, temp_width, temp_height = self.template_match(template_name)
            if conf_value > 0.85:
                return top_left,temp_width,temp_height
            time.sleep(0.5)
        raise TimeOutError(f"Ran out of time: {timeout}")

    # if wait=True use wait for first, then click. if wait=False, check once and click only if found
    #return true or false
    def click_template(self,template_name, wait=True,timeout=10):
        self.check_stop()
        if wait:
            try:
                pos,temp_width,temp_height = self.wait_for(template_name,timeout)
            except TimeOutError as e:
                return False
            center_x = pos[0] + (temp_width/2)
            center_y = pos[1] + (temp_height/2)
            pyautogui.click(center_x,center_y)
            return True
        else:
            return self.find_and_click(template_name)

    
    def on_hotkey_trigger(self):
        self.stopped = True
        print("F10 hotkey pressed")
    
    
    def check_stop(self):
        if self.stopped:
            raise EmergencyStop(f"F10 Emergency Key Clicked")
        
    # emergencey stop check flag at start of key methods and raise Exception if its true

def main():
    try:
        screencapt1 = ScreenCapture()
        screencapt1.find_and_click("test_template.png")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
     main()



