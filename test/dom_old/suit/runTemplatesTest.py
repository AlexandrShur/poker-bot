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

def test_template():
    LoggerUtils.logStartMethod("runTemplatesTest:test_template")

    source = cv2.imread("test/1668593213.089405.jpg", 0) 
    template = cv2.imread("test/441668876079.892667.jpg", 0) 
    #template = cv2.imread("test/461668876079.894669.jpg", 0)
    
    mcd = SettingsUtils.getMainCards()[0]
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    
    result = TemplateUtils.find_similar_by_template(source, template, 0.9)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 10
    
    result = TemplateUtils.find_similar_by_template(source, template, 0.97)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 3
    
def test_main_cards_template():
    LoggerUtils.logStartMethod("runTemplatesTest:test_main_cards_template")
    mainCardsSettings = SettingsUtils.getMainCards()[0]
    source = cv2.imread("test/1668593213.089405.jpg", 0) 
    template = cv2.imread("test/441668876079.892667.jpg", 0) 
    mcd = mainCardsSettings
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    
    result = TemplateUtils.find_similar_main_cards_by_template(source, template)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 2
    
    source = cv2.imread("test/1668593213.089405.jpg", 0) 
    template = cv2.imread("test/461668876079.894669.jpg", 0) 
    mcd = mainCardsSettings
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    
    result = TemplateUtils.find_similar_main_cards_by_template(source, template)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 3
    
    
def test_main_cards_find_ranks_and_suits():
    LoggerUtils.logStartMethod("runTemplatesTest:test_main_cards_find_ranks_and_suits")
    source = cv2.imread("test/1668593213.089405.jpg", 0) 
    mcd = SettingsUtils.getMainCards()[0]
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 5
    
def test_player_cards_find_ranks_and_suits():
    LoggerUtils.logStartMethod("runTemplatesTest:test_player_cards_find_ranks_and_suits")
    playersSettings = SettingsUtils.getPlayers()
    sourceOriginal = cv2.imread("test/1668592929.400012.jpg", 0) 
    
    
    mcd = playersSettings[0]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[1]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[2]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[3]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[4]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 2
    assert result[0]['rank'] == 'J'
    assert result[0]['suit'] == 'd'
    assert result[1]['rank'] == 'K'
    assert result[1]['suit'] == 'd'
    
    
    mcd = playersSettings[5]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    sourceOriginal = cv2.imread("test/1668592954.611824.jpg", 0) 
    mcd = playersSettings[4]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 2
    assert result[0]['rank'] == '8'
    assert result[0]['suit'] == 'c'
    assert result[1]['rank'] == '8'
    assert result[1]['suit'] == 'd'
    
    sourceOriginal = cv2.imread("test/1668593033.539413.jpg", 0) 
    mcd = playersSettings[4]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.main_cards_find_ranks_and_suits(source)
    LoggerUtils.debug(result)
    assert len(result) == 2
    assert result[0]['rank'] == '5'
    assert result[0]['suit'] == 'h'
    assert result[1]['rank'] == '6'
    assert result[1]['suit'] == 's'
        
    
def test_controls():
    LoggerUtils.logStartMethod("runTemplatesTest:test_controls")
    buttonsSettings = SettingsUtils.getButtons()
    buttonsTemplatesSettings = SettingsUtils.getButtonsTemplates()
    sourceOriginal = cv2.imread("test/1668592929.400012.jpg", cv2.IMREAD_UNCHANGED) 
    #sourceOriginal2 = cv2.imread("test/1668592929.400012.jpg", 0) 
    
    
    #LoggerUtils.info(str(TemplateUtils.get_buttons(sourceOriginal2, buttonsTemplatesSettings))) 
    result = TemplateUtils.get_controls_data(sourceOriginal, buttonsSettings, buttonsTemplatesSettings)
    LoggerUtils.info(str(result)) 
    
    
    assert result["is_control_panel_active"] == True
    assert result["is_common_buttons"] == True
    assert result["buttons"][0]['type'] == 'fold'
    assert result["buttons"][1]['type'] == 'check'
    assert result["buttons"][2]['type'] == 'bet'
    
    sourceOriginal = cv2.imread("test/1668592920.229711.jpg", cv2.IMREAD_UNCHANGED) 
    
    result = TemplateUtils.get_controls_data(sourceOriginal, buttonsSettings, buttonsTemplatesSettings)
    LoggerUtils.info(str(result)) 
    
    
    #assert result["is_control_panel_active"] == True
    #assert result["is_common_buttons"] == True
    assert result["buttons"][0]['type'] == 'fold'
    assert result["buttons"][1]['type'] == 'call'
    assert result["buttons"][2]['type'] == 'raise'
   
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
#    LoggerUtils.logStartMethod("runTemplatesTest:test_click")
#    PokerWindow.clickCheckButton()
    
#def test_run2():
#    LoggerUtils.logStartMethod("runTemplatesTest:test_run2")
#    tableManager = TableManager()
#    tableManager.isMock = True
#    tableManager.initTable()
#    LoggerUtils.debug ("=-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-=")
#    LoggerUtils.debug(glob.glob("/test/play_1/*"))
#    tableManager.pokerWindow.mockFrames = glob.glob("N:/train/open_cv_card/test/play_1/*")
#    tableManager.play2()
    