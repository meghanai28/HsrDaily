# mss grabs pixel data gives back as grid of numbers
# each screenshot - 3D array (1080,1920,3)

#mss.mss() -> screen capture objuct
# .monitors gives list of displays -> monitors[1] is primary
#.grab(monitor) captures region and returns pixel data
# wrap in numpy.array so we can work with it
import mss
import numpy as np

class ScreenCapture:
    def __init__ (self):
        self.sct = mss.mss()
    
    def test(self):
        monitor = self.sct.monitors[1]
        print(monitor["width"],monitor["height"])
        raw_data = self.sct.grab(monitor)
        region = np.asarray(raw_data)
        print(region.shape)
    
def main():
    print("Hello Word")
    try:
        screencapt1 = ScreenCapture()
        screencapt1.test()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
     main()

