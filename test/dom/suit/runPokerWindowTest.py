# test.py

import pytest
#from CardDetector import CardDetector
from TemplateUtils import TemplateUtils
from TableManager import TableManager
from SettingsUtils import SettingsUtils
from LoggerUtils import LoggerUtils
import cv2
import numpy as np
from PIL import Image
import json
from PokerWindow import PokerWindow
import glob
import time

def displayResults(image, results):
    for res in results:
        pt = res['pt']
        x = res['x']
        y = res['y']
        h = res['height']
        w = res['width']
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    quit = 0 # Loop control variable
    while quit == 0:
        cv2.imshow("Poker table data display(from image)", image)
        key = cv2.waitKey(3) & 0xFF
        if key == ord("q"):
            quit = 1
    cv2.destroyAllWindows()

def test_clickFoldButton():
    PokerWindow.clickFoldButton()
    time.sleep(2)
    
    PokerWindow.clickAllinButton()
    time.sleep(2)
    PokerWindow.clickCheckButton()
    time.sleep(2)
    PokerWindow.clickCallButton()
    
    time.sleep(2)
    PokerWindow.clickRaiseButton()
    time.sleep(2)
    PokerWindow.clickBetButton()
    
    
    #assert len(result) == 2
    