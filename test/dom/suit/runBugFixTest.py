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
    
def test_b1_main_cards_find_ranks_and_suits():
    LoggerUtils.logStartMethod("runTemplatesTest:test_main_cards_find_ranks_and_suits")
    mcd = SettingsUtils.getMainCards()[0]
    
    source = cv2.imread("test/dom/res/bugs/b1.png", 0) 
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 3
    assert result[0]['rank'] == '9'
    assert result[0]['suit'] == 'h'
    assert result[1]['rank'] == '6'
    assert result[1]['suit'] == 's'
    assert result[2]['rank'] == 'J'
    assert result[2]['suit'] == 'd'
    
    
def test_b1_player_cards_find_ranks_and_suits():
    LoggerUtils.logStartMethod("runTemplatesTest:test_player_cards_find_ranks_and_suits")
    playersSettings = SettingsUtils.getPlayers()
    sourceOriginal = cv2.imread("test/dom/res/bugs/b1.png", 0) 
     
    mcd = playersSettings[3]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 2
    assert result[0]['rank'] == 'Q'
    assert result[0]['suit'] == 's'
    assert result[1]['rank'] == 'Q'
    assert result[1]['suit'] == 'h'
    
    