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

   
    
#def test_controls():
#   LoggerUtils.logStartMethod("runTemplatesTest:test_controls")
#    buttonsSettings = SettingsUtils.getButtons()
#    sourceOriginal = cv2.imread("test/1668592929.400012.jpg", cv2.IMREAD_UNCHANGED) 
    
#    LoggerUtils.debug(TemplateUtils.get_controls_data(sourceOriginal, buttonsSettings))


def test_update_table_data():
    LoggerUtils.logStartMethod("runTemplatesTest:test_update_table_data")
    sourceOriginal = cv2.imread("test/1668592929.400012.jpg", cv2.IMREAD_UNCHANGED)
    
    cv2.imwrite("test/updateTableData____.png", cv2.imread("test/1668592929.400012.jpg", 0))
    tableManager = TableManager()
    tableManager.initTableData()
    tableManager.updateTableData(sourceOriginal)
    LoggerUtils.debug(json.dumps(tableManager.table.controls))
    LoggerUtils.debug("========================================================================")
    LoggerUtils.debug(json.dumps(tableManager.table.cards))
    LoggerUtils.debug("========================================================================")
    LoggerUtils.debug(json.dumps(tableManager.table.players))
    
#def test_click():
    #LoggerUtils.logStartMethod("runTemplatesTest:test_click")
    #PokerWindow.clickCheckButton()
    
def test_run2():
    LoggerUtils.logStartMethod("runTemplatesTest:test_run2")
    tableManager = TableManager()
    tableManager.isMock = True
    tableManager.initTable()
    LoggerUtils.debug ("=-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-=")
    LoggerUtils.debug(glob.glob("/test/play_1/*"))
    tableManager.pokerWindow.mockFrames = glob.glob("N:/train/open_cv_card/test/play_1/*")
    tableManager.play2()
    