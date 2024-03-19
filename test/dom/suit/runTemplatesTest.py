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

    source = cv2.imread("test/dom/res/v2/1679401778.131217.jpg", 0) 
    template = cv2.imread("res/dom/cards/v2/41679406379.076814.jpg", 0) 
    #template = cv2.imread("test/461668876079.894669.jpg", 0)
    
    mcd = SettingsUtils.getMainCards()[0]
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    
    result = TemplateUtils.find_similar_by_template(source, template, 0.9)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 10
    
    result = TemplateUtils.find_similar_by_template(source, template, 0.92)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 6
    
    result = TemplateUtils.find_similar_by_template(source, template, 0.94)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 2
    
def test_main_cards_template():
    LoggerUtils.logStartMethod("runTemplatesTest:test_main_cards_template")
    mainCardsSettings = SettingsUtils.getMainCards()[0]
    source = cv2.imread("test/dom/res/v2/1679401778.131217.jpg", 0) 
    template = cv2.imread("res/dom/cards/v2/41679406379.076814.jpg", 0) 
    mcd = mainCardsSettings
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    
    result = TemplateUtils.find_similar_main_cards_by_template(source, template)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 2
    
    source = cv2.imread("test/dom/res/v2/1679401952.108456.jpg", 0) 
    template = cv2.imread("res/dom/cards/v2/1301679406379.360202.jpg", 0) 
    mcd = mainCardsSettings
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    
    result = TemplateUtils.find_similar_main_cards_by_template(source, template)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 1
    
    source = cv2.imread("test/dom/res/v2/1679401952.108456.jpg", 0) 
    template = cv2.imread("res/dom/cards/v2/21679406379.074813.jpg", 0) 
    mcd = mainCardsSettings
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    
    result = TemplateUtils.find_similar_main_cards_by_template(source, template)
    
    #displayResults(source, result)
    
    LoggerUtils.debug(result)
    assert len(result) == 3
    
    
def test_main_cards_find_ranks_and_suits():
    LoggerUtils.logStartMethod("runTemplatesTest:test_main_cards_find_ranks_and_suits")
    mcd = SettingsUtils.getMainCards()[0]
    
    source = cv2.imread("test/dom/res/v2/1679401903.243217.jpg", 0) 
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 3
    assert result[0]['rank'] == 'A'
    assert result[0]['suit'] == 'c'
    assert result[1]['rank'] == '9'
    assert result[1]['suit'] == 's'
    assert result[2]['rank'] == '5'
    assert result[2]['suit'] == 'c'
    
    source = cv2.imread("test/dom/res/v2/1679401944.219546.jpg", 0) 
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 3
    assert result[0]['rank'] == '5'
    assert result[0]['suit'] == 'c'
    assert result[1]['rank'] == 'K'
    assert result[1]['suit'] == 's'
    assert result[2]['rank'] == '4'
    assert result[2]['suit'] == 's'
    
    source = cv2.imread("test/dom/res/v2/1679401952.108456.jpg", 0) 
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 5
    assert result[0]['rank'] == '5'
    assert result[0]['suit'] == 'c'
    assert result[1]['rank'] == 'K'
    assert result[1]['suit'] == 's'
    assert result[2]['rank'] == '4'
    assert result[2]['suit'] == 's'
    assert result[3]['rank'] == 'J'
    assert result[3]['suit'] == 's'
    assert result[4]['rank'] == 'Q'
    assert result[4]['suit'] == 'd'
    
    
    source = cv2.imread("test/dom/res/v2/1679402100.597856.jpg", 0) 
    source = source[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 3
    assert result[0]['rank'] == 'Q'
    assert result[0]['suit'] == 'd'
    assert result[1]['rank'] == '6'
    assert result[1]['suit'] == 'h'
    assert result[2]['rank'] == '6'
    assert result[2]['suit'] == 'c'
    
def test_player_cards_find_ranks_and_suits():
    LoggerUtils.logStartMethod("runTemplatesTest:test_player_cards_find_ranks_and_suits")
    playersSettings = SettingsUtils.getPlayers()
    sourceOriginal = cv2.imread("test/dom/res/v2/1679401952.108456.jpg", 0) 
    
    
    mcd = playersSettings[0]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 0

    mcd = playersSettings[1]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[2]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[3]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[4]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 0
    
    mcd = playersSettings[5]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 2
    assert result[0]['rank'] == 'A'
    assert result[0]['suit'] == 's'
    assert result[1]['rank'] == '9'
    assert result[1]['suit'] == 's'
    
    sourceOriginal = cv2.imread("test/dom/res/v2/1679401827.46219.jpg", 0) 
    mcd = playersSettings[4]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)

    assert len(result) == 2
    assert result[0]['rank'] == '6'
    assert result[0]['suit'] == 'd'
    assert result[1]['rank'] == '9'
    assert result[1]['suit'] == 'h'
    
    mcd = playersSettings[3]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 2
    assert result[0]['rank'] == 'Q'
    assert result[0]['suit'] == 'c'
    assert result[1]['rank'] == 'Q'
    assert result[1]['suit'] == 'h'
    
    sourceOriginal = cv2.imread("test/dom/res/v2/1679401903.243217.jpg", 0) 
    mcd = playersSettings[5]
    source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    result = TemplateUtils.find_cards(source)
    LoggerUtils.debug(result)
    assert len(result) == 2
    assert result[0]['rank'] == 'K'
    assert result[0]['suit'] == 'c'
    assert result[1]['rank'] == 'J'
    assert result[1]['suit'] == 'h'
        
    
def test_controls():
    LoggerUtils.logStartMethod("runTemplatesTest:test_controls")
    buttonsSettings = SettingsUtils.getButtons()
    buttonsTemplatesSettings = SettingsUtils.getButtonsTemplates()
    sourceOriginal = cv2.imread("test/dom/res/v2/1679401952.108456.jpg", cv2.IMREAD_UNCHANGED) 
    #sourceOriginal2 = cv2.imread("test/1668592929.400012.jpg", 0) 
    
    
    #LoggerUtils.info(str(TemplateUtils.get_buttons(sourceOriginal2, buttonsTemplatesSettings))) 
    result = TemplateUtils.get_controls_data(sourceOriginal, buttonsSettings, buttonsTemplatesSettings)
    LoggerUtils.debug(str(result)) 
    
    #assert result["is_control_panel_active"] == True
    #assert result["is_common_buttons"] == True
    assert result["buttons"][0]['type'] == 'fold'
    assert result["buttons"][1]['type'] == 'check'
    assert result["buttons"][2]['type'] == 'bet'
    
    sourceOriginal = cv2.imread("test/dom/res/v2/1679402208.137112.jpg", cv2.IMREAD_UNCHANGED) 
    result = TemplateUtils.get_controls_data(sourceOriginal, buttonsSettings, buttonsTemplatesSettings)
    LoggerUtils.debug(str(result)) 
    
    assert result["buttons"][0]['type'] == 'fold'
    assert result["buttons"][1]['type'] == 'call'
    assert result["buttons"][2]['type'] == 'raise'
    
    
    sourceOriginal = cv2.imread("test/dom/res/v2/1679402962.152902.jpg", cv2.IMREAD_UNCHANGED) 
    result = TemplateUtils.get_controls_data(sourceOriginal, buttonsSettings, buttonsTemplatesSettings)
    LoggerUtils.debug(str(result)) 

    assert result["buttons"][0]['type'] == 'fold'
    assert result["buttons"][1]['type'] == 'allin'

def test_find_text():
    LoggerUtils.logStartMethod("runTemplatesTest:test_find_text")
    buttonsSettings = SettingsUtils.getButtons()
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/1679402208.137112.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_text(call_source)
    lines = data.splitlines()
    
    assert lines[0] == "Уравнять"
    assert lines[1] == "10"
    
    
    mcd = buttonsSettings[1]
    check_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_text(check_source)
    lines = data.splitlines()
    
    assert lines[1] == "Фолд"
    
def test_find_number():
    LoggerUtils.logStartMethod("runTemplatesTest:test_find_text")
    buttonsSettings = SettingsUtils.getButtons()
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/1679402208.137112.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 10
    
    mcd = buttonsSettings[1]
    check_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(check_source)
    assert data == None
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639254.441465.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 5
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639270.750575.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 11
    
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639298.332969.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 2
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639333.135507.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 6
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639355.433722.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 4
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639372.533629.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 5
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639437.832071.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    assert data == 3
    
    mcd = buttonsSettings[4]
    sourceOriginal = cv2.imread("test/dom/res/v2/numbers/1681639465.116258.jpg", cv2.IMREAD_UNCHANGED) 
    call_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
    data = TemplateUtils.find_number(call_source)
    
    text = TemplateUtils.find_text(call_source)
    print(text.splitlines())
    #assert data == 1