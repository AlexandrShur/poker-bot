# test.py

import pytest
from TemplateUtils import TemplateUtils
from TableManager import TableManager
from models.Table import Table
from bot.Bot import Bot
from SettingsUtils import SettingsUtils
from LoggerUtils import LoggerUtils
import cv2
import numpy as np
from PIL import Image
import json
from PokerWindow import PokerWindow
import glob


def test_getScore():
    LoggerUtils.logStartMethod("runBotTest:test_getScore")
    table = Table()
    
    assert Bot.getScore(table) == 8000
    
    
    table.players[0]["cards"] = [{}, {}]
    
    table.players[0]["cards"][0]["type"] = "3h"
    table.players[0]["cards"][1]["type"] = "2s"
    
    
    #assert Bot.getScore(table) == 8000
    
    #print("table123: " + str(table.cards))
    
    #table.players[0]["cards"].append({})
    table.players[0]["cards"][0]["type"] = "5s"
    table.players[0]["cards"][1]["type"] = "4s"
    table.clearMainCards()
    table.addedMainCard("7d")
    table.addedMainCard("5d")
    table.addedMainCard("9d")
    table.addedMainCard("Td")
    
    #table.cards[0]["type"] = "5d"
    #table.cards[1]["type"] = "7d"
    #table.cards[3]["type"] = "9d"
    
    #print("table1234: " + str(table.cards))
    assert Bot.getScore(table) == 5471
    
    table.players[0]["cards"][0]["type"] = "5s"
    table.players[0]["cards"][1]["type"] = "4s"
    table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("4d")
    table.addedMainCard("5h")
    table.addedMainCard("2h")
    table.addedMainCard("3h")
    
    assert Bot.getScore(table) == 284
    
    
    table.players[0]["cards"][0]["type"] = "5s"
    table.players[0]["cards"][1]["type"] = "4s"
    table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("5c")
    table.addedMainCard("5h")
    table.addedMainCard("2h")
    table.addedMainCard("3h")
    
    
    assert Bot.getScore(table) == 128

def test_getActionBasedOnCardsAndControls():
    LoggerUtils.logStartMethod("runBotTest:test_getActionBasedOnCardsAndControls")
    table = Table()
      
    table.players[0]["cards"] = [{}, {}]
    
    table.players[0]["cards"][0]["type"] = "3h"
    table.players[0]["cards"][1]["type"] = "2s"
    #table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("6d")
    table.addedMainCard("7d")
    
    assert Bot.getActionBasedOnCardsAndControls(table) == "clickFoldButton"
    
    
    table.players[0]["cards"][0]["type"] = "3h"
    table.players[0]["cards"][1]["type"] = "2s"
    table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("6d")
    table.addedMainCard("7d")
    
    table.setControlsButtons(["check", "fold", "bet"])
    
    assert Bot.getActionBasedOnCardsAndControls(table) == "clickCheckButton"
    
    
    table.players[0]["cards"][0]["type"] = "3h"
    table.players[0]["cards"][1]["type"] = "2s"
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("3d")
    table.addedMainCard("7d")
    table.setControlsButtons(["check", "fold", "bet"])
    assert Bot.getActionBasedOnCardsAndControls(table) == "clickBetButton"