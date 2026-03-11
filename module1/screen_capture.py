# mss grabs pixel data gives back as grid of numbers
# each screenshot - 3D array (1080,1920,3)

#mss.mss() -> screen capture objuct
# .monitors gives list of displays -> monitors[1] is primary
#.grab(monitor) captures region and returns pixel data
# wrap in numpy.array so we can work with it

# OpenCV match template -> small image and slides across big image & scores how well each position mtaches
# function returns a score at every postion -> perfect match is 1.0 and total mismatch would be 0
# cv2.imread() loads image file
# cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED) does the matching Full doc: https://docs.opencv.org/4.x/df/dfb/group__imgproc__object.html
# cv2.minMaxLoc(result) - finds the pos of best match

import mss
import numpy as np
import pathlib
import cv2

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"

class ScreenCapture:
    def __init__ (self):
        self.sct = mss.mss()

    def template_match(self):
        # load template
        test_path = (TEMPLATE_DIR/"test_template.png").resolve()
        template = cv2.imread(str(test_path))
        if template is None:
            raise FileNotFoundError(f"Could not find file at {test_path}")
        
        # take screenshot
        monitor = self.sct.monitors[1] 
        print(monitor["width"], monitor["height"])
        raw_data = self.sct.grab(monitor)
        output = np.asarray(raw_data)
        screen = cv2.cvtColor(output,cv2.COLOR_BGRA2BGR)
        print(screen.shape)

        # template matching
        result = cv2.matchTemplate(screen,template, cv2.TM_CCOEFF_NORMED)
        pos = cv2.minMaxLoc(result) # gives us min_val,max_val, min_loc, max_loc - coeff needs to be maxed
        print(pos[1],pos[3])

 
def main():
    print("Hello Word")
    try:
        screencapt1 = ScreenCapture()
        screencapt1.template_match()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
     main()



