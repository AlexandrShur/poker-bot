from models.Table import Table
from PokerWindow import PokerWindow
from SettingsUtils import SettingsUtils
from TemplateUtils import TemplateUtils
from treys import Card, Deck, Evaluator
import time
import cv2
from LoggerUtils import LoggerUtils
from bot.Bot import Bot

class TableManager:
    money = 0
    
    table = None
    isPlaying = False
    isMock = False
    prepareWindow = None
    def __init__(self):
        LoggerUtils.debug("TableManager:__init__")
        
    def initTable(self):
        self.prepareWindow()
        self.initTableData()
        self.initBot()
        
    def play(self):
        LoggerUtils.debug("TableManager:play")
        iter = 0
        self.isPlaying = True
        oldImage = None
        while self.isPlaying:
            LoggerUtils.debug("TableManager:isPlaying")
            
            currentTableImage = PokerWindow.getTableImage()
            if (oldImage != currentTableImage):
                table.processTableImage(currentTableImage)
            
            oldImage = currentTableImage
            
            iter +=1
            if iter > 3:
                self.isPlaying = False
            
            
    def prepareWindow(self):
        LoggerUtils.debug("TableManager:prepareWindow")
        self.pokerWindow = PokerWindow()
        if (self is not None):
            self.pokerWindow.isMock = self.isMock
        self.pokerWindow.prepareWindow()
        
        
    def initTableData(self):
        LoggerUtils.debug("TableManager:initTableData")
        self.table = Table()
        self.table.init()
        
    def initBot(self):
        LoggerUtils.debug("TableManager:initBot")
    
    def makeActionBasedOnTableData(self, controls):
        board = []
        hand = []
        for i in range(0, len(self.table.cards)):
            board.append(Card.new(self.table.cards[i].replace("_", "")))
        hand_cards = []
        for i in range(0, len(self.table.players)):
            if (len(self.table.players[i]['cards']) > 0):
                hand_cards = self.table.players[i]['cards']
        for i in range(0, len(hand_cards)):
            print("card: " + hand_cards[i]['type'].replace("_", ""))
            hand.append(Card.new(hand_cards[i]['type'].replace("_", "")))
        evaluator = Evaluator()
        score = evaluator.evaluate(hand, board)
        #posibleActions = {}
        #if controls["is_common_buttons"] == True:
        #    posibleActions.fold = True
        #    posibleActions.check = True
        #    posibleActions.call = True
        #    posibleActions.rise = None
        #    posibleActions.allin = None
        #else:
        #    posibleActions.fold = True
        #    posibleActions.check = None
        #    posibleActions.call = None
        #    posibleActions.rise = None
        #    posibleActions.allin = None
        
        
        #for i in range(0, len(controls["buttons"])):
            
        #    isFoldable = controls["buttons"] != None
        #    isChekable = posibleActions.check != None
        #    isCallable = posibleActions.call != None
        #    isRaisable = posibleActions.rise != None
        #    isAllinable = posibleActions.allin != None
            
        isFirstRound = len(board) == 0
        
        if isFirstRound and table.isCheckButtonActive():
            PokerWindow.clickCheckButton()
        elif isFirstRound and table.isCallButtonActive():
            PokerWindow.clickCallButton()
        elif score >= 3000 and table.isBetButtonActive():
            PokerWindow.clickBetButton()
        elif score >= 3000 and table.isCallButtonActive():
            PokerWindow.clickCallButton()
        elif score >= 3000 and table.isRaiseButtonActive():
            PokerWindow.clickRaiseButton()
        elif score < 3000 and table.isCheckButtonActive():
            PokerWindow.clickCheckButton()
        elif score > 5000 and table.isAllinButtonActive():
            PokerWindow.clickAllinButton()
        else:
            PokerWindow.clickFoldButton()
            
    def updateTableData(self, image):
        LoggerUtils.debug("TableManager:updateTableData")
        initialImage = image.copy()
        im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        playersSettings = SettingsUtils.getPlayers()
        for i in range(0, len(playersSettings)):
            ps = playersSettings[i]
            pSource = im_gray[ps[0]:ps[1], ps[2]:ps[3]]
            self.table.players[i] = {}
            try:
                self.table.players[i]['cards'] = TemplateUtils.find_cards(pSource)
            except:
                self.table.players[i]['cards'] = []
                LoggerUtils.error("Error aquired during players cards reading")
        mcs = SettingsUtils.getMainCards()[0]
        mcSource = im_gray[mcs[0]:mcs[1], mcs[2]:mcs[3]]
        
        try:
            self.table.cards = TemplateUtils.find_cards(mcSource)
        except:
            self.table.cards = []
            LoggerUtils.error("Error aquired during table cards reading")
        bs = SettingsUtils.getButtons()
        bts = SettingsUtils.getButtonsTemplates()
        self.table.controls = TemplateUtils.get_controls_data(image, bs, bts)
        
        mcd = bs[4]
        call_source = initialImage[mcd[0]:mcd[1], mcd[2]:mcd[3]]
        callMoney = TemplateUtils.find_number(call_source)
        LoggerUtils.info(TemplateUtils.find_text(call_source).splitlines())
        if callMoney is not None:
            self.table.callMoney = callMoney
        else:
            self.table.callMoney = 0
        
    def showTableData(self):
        LoggerUtils.info("============ Current table data: ===================")
        LoggerUtils.info("table cards: " + self.table.cardsInfo())
        LoggerUtils.info("controls: " + self.table.controlsInfo()) 
        LoggerUtils.info("players: " + self.table.playersInfo())
        LoggerUtils.error("callMoney: " + str(self.table.callMoney))
    
    def play2(self):
        LoggerUtils.debug("TableManager:play2")
        iter = 0
        self.isPlaying = True
        processed = False
        isRequiredAction = False
        while self.isPlaying:
            #if (self.pokerWindow.mockIterator + 1) >= len(self.pokerWindow.mockFrames):
                #self.isPlaying = False
                #break
            time.sleep(0.7)
            makeImage = self.pokerWindow.getTableImage()
            #displayFoundData(makeImage)
            
            self.updateTableData(makeImage)
            
            #LoggerUtils.info("isActionRequired: " + str(self.table.isFoldButtonActive()))
            if self.table.isActionRequired() == True and processed == False: 
                LoggerUtils.info("Making action on the table.")
                self.showTableData()
                #self.makeActionBasedOnTableData(self.table.controls)
                Bot.getActionBasedOnCardsAndControls(self.table)
                processed == True
            elif processed == True:
                processed = False
            #    processed = True
            #elif isRequiredAction == False and processed == True: 
            #    processed = False