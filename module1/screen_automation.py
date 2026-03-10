import json
import logging 
import os
import sys
import time
from pathlib import Path
from typing import Optional

import cv2
import keyboard
import mms
import numpy as np
import pyautogui

pyautogui.PAUSE = 0.2 # pausing btwn actions
logger = logging.getLogger("hsr_daily_bot")
TEMPLATES_dir = Path(__file__).parent / "templates"

class EmergencyStop(Exception):
    pass

class ScreenAutomation:
    def __init__(self, config: dict):
        # self.config = config ill add the config stuff later
        # self.confidence = 0.85
        # self.click_delay = 0.3
        # self.load_wait = 3.0
        # self.retry_attempts = 3
        self.emergency_key = "F10"
        self.resolution = [1920,1080]

        self.capture_region = None # full screen for now
        self.sct = mss.mss() # fast screenshots
        self._template_cache = {}
        keyboard.on_press_key("F10", self._on_emergency)
        self._stopped = False

        logger.info("Screen automation initialized - resolution: [1920, 1080]")
        logger.info("Emergency stop, pls press F10")

    def _on_emergency (self):
        self._stopped = True
        logger.info("emergency stop triggered")

    def check_stop(self):
        if self._stopped:
            raise EmergencyStop("bot stopped by f10")

    def screenshot(self) -> np.ndarray:
        self.check_stop()

        # update when we add the captire region (i.e., the stuff where specific rectangle)
        monitor = self.sct.monitors[1]
        img = np.array(self.sct.grab(monitor))
        # mss does BGRA, we need bgr
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    

    # load templates
    # find template on screen
    # final all instances of template on screen

    # INPUT actions
        # click (human like misclicks) -idk if i need tbh
        # click template
        # click position
        # drag
        # scroll
        # press key

    # extra
        # wait for loading
        # open + close menues
        # navigate to 
        # check on screen
        # retry + cleanup


