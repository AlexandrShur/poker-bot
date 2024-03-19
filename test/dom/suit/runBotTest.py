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
    
    #table.clearPlayersCards()
    #table.addedPlayerCardByIndex(0, ["3h", "2s"])
    #assert Bot.getScore(table) == 8000
    
    #print("table123: " + str(table.cards))
    
    #table.players[0]["cards"].append({})
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["5s", "4s"])
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
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["5s", "4s"])
    table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("4d")
    table.addedMainCard("5h")
    table.addedMainCard("2h")
    table.addedMainCard("3h")
    
    assert Bot.getScore(table) == 284
    
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["5s", "4s"])
    table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("5c")
    table.addedMainCard("5h")
    table.addedMainCard("2h")
    table.addedMainCard("3h")
    
    
    assert Bot.getScore(table) == 128

def test_getScoreForHandOnly():
    LoggerUtils.logStartMethod("runBotTest:test_getScoreForHandOnly")
    table = Table()
    assert Bot.getScoreForHandOnly(table) == 8000
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    
    assert Bot.getScoreForHandOnly(table) == 5000
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "3s"])
    assert Bot.getScoreForHandOnly(table) == 4000
    
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["Kh", "Ts"])
    assert Bot.getScoreForHandOnly(table) == 4000
    
    
def test_getActionBasedOnCardsAndControls():
    LoggerUtils.logStartMethod("runBotTest:test_getActionBasedOnCardsAndControls")
    table = Table()
      
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    #table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("6d")
    table.addedMainCard("7d")
    
    assert Bot.getActionBasedOnCardsAndControls(table) == "clickFoldButton"
    
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    table.clearMainCards()
    table.addedMainCard("5d")
    table.addedMainCard("6d")
    table.addedMainCard("7d")
    
    table.setControlsButtons(["check", "fold", "bet"])
    
    assert Bot.getActionBasedOnCardsAndControls(table) == "clickCheckButton"
    
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("3d")
    table.addedMainCard("7d")
    table.setControlsButtons(["check", "fold", "bet"])
    assert Bot.getActionBasedOnCardsAndControls(table) == "clickBetButton"
    
def test_getHandsLocalRate():
    LoggerUtils.logStartMethod("runBotTest:test_getHandsLocalRate")
    table = Table()
      
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    table.addedMainCard("5d")
    table.addedMainCard("6d")
    table.addedMainCard("7d")
    
    assert Bot.getHandsLocalRate(table) == 0
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    table.clearMainCards()
    table.addedMainCard("4d")
    table.addedMainCard("3d")
    table.addedMainCard("7d")
    
    assert Bot.getHandsLocalRate(table) == 2
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("3d")
    table.addedMainCard("7d")
    
    assert Bot.getHandsLocalRate(table) == 3
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    table.clearMainCards()
    table.addedMainCard("3c")
    table.addedMainCard("3d")
    table.addedMainCard("7d")
    
    assert Bot.getHandsLocalRate(table) == 4
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["Th", "2s"])
    table.clearMainCards()
    table.addedMainCard("3c")
    table.addedMainCard("Jd")
    table.addedMainCard("Qd")
    table.addedMainCard("Kd")
    table.addedMainCard("Ad")
    
    assert Bot.getHandsLocalRate(table) == 5
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["Th", "2d"])
    table.clearMainCards()
    table.addedMainCard("3c")
    table.addedMainCard("Jd")
    table.addedMainCard("Qd")
    table.addedMainCard("Kd")
    table.addedMainCard("Ad")
    
    assert Bot.getHandsLocalRate(table) == 6
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["Th", "2d"])
    table.clearMainCards()
    table.addedMainCard("2c")
    table.addedMainCard("Jd")
    table.addedMainCard("Qd")
    table.addedMainCard("Qh")
    table.addedMainCard("Qs")
    
    assert Bot.getHandsLocalRate(table) == 7
    
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["Td", "Qc"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("Th")
    table.addedMainCard("Qd")
    table.addedMainCard("Qh")
    table.addedMainCard("Qs")
    
    assert Bot.getHandsLocalRate(table) == 8
    
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3d", "5d"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("4d")
    table.addedMainCard("6d")
    table.addedMainCard("Qh")
    table.addedMainCard("Qs")
    
    assert Bot.getHandsLocalRate(table) == 9
    
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["Ts", "5s"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("Ks")
    table.addedMainCard("Js")
    table.addedMainCard("As")
    table.addedMainCard("Qs")
    
    assert Bot.getHandsLocalRate(table) == 9
    
def test_getPossibleHands():
    LoggerUtils.logStartMethod("runBotTest:test_getPossibleHands")
    table = Table()
      
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["3h", "2s"])
    table.addedMainCard("5d")
    table.addedMainCard("6d")
    table.addedMainCard("7d")
    
    possibles = Bot.getPossibleHands(table)
    print(possibles)
    assert possibles["straight"] == 60
    assert possibles["flush"] == 60
    
    table.clearPlayersCards()
    table.addedPlayerCardByIndex(0, ["Td", "Qc"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("Th")
    table.addedMainCard("Qd")
    table.addedMainCard("Qh")
    table.addedMainCard("Qs")
    possibles = Bot.getPossibleHands(table)
    print(possibles)
    assert possibles["two_pair"] == 60
    assert possibles["three"] == 100
    assert possibles["four"] == 80
    
def test_isPossibleLose(): 
    LoggerUtils.logStartMethod("runBotTest:test_getPossibleHands")
    table = Table()
    table.clearPlayersCards()
    table.setControlsButtons(["call", "fold", "raise"])
    table.addedPlayerCardByIndex(0, ["Td", "Qc"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("Th")
    table.addedMainCard("Qd")
    table.addedMainCard("Qh")
    table.addedMainCard("Qs")

    assert Bot.isPossibleLose(table) == False
    
    table.clearPlayersCards()
    table.setControlsButtons(["call", "fold", "raise"])
    table.addedPlayerCardByIndex(0, ["Td", "3c"])
    table.clearMainCards()
    table.addedMainCard("2d")
    table.addedMainCard("Th")
    table.addedMainCard("Qd")
    table.addedMainCard("Qh")
    table.addedMainCard("Qs")

    assert Bot.isPossibleLose(table) == True