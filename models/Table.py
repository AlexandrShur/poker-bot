class Table:
    
    def __init__(self):
        self.name = ""
        self.type = ""
        self.players = [{}] * 6
        self.bank = 0
        self.set = ""
        self.cards = [{}] * 5
        self.bot = None
        self.controls = {}
        self.callMoney = 0
        self.isRequiredAction = False
    def init(self):
        print("Table:init")
        
    def clearPlayers(self):
        self.players = []
        
    def clearPlayersCards(self):
        for player in self.players:
            player["cards"] = []
      
    def addedPlayer(self, name):
        player = {}
        player["name"] = name
        self.players.append(player)
      
    def addedPlayerCard(self, playerName, cards):
        for player in self.players:
            if player["name"] == playerName:
                player["cards"] = [{}, {}]
                player["cards"][0]["type"] = cards[0]
                player["cards"][1]["type"] = cards[1]
                break;
                
    def addedPlayerCardByIndex(self, index, cards):
        self.players[index]["cards"] = [{}, {}]
        self.players[index]["cards"][0]["type"] = cards[0]
        self.players[index]["cards"][1]["type"] = cards[1]

      
    def clearMainCards(self):
        self.cards = []
    
    def addedMainCard(self, cardName):
        r = cardName[0:1]
        d = cardName[1:2]
        card = {}
        card["type"] = r + "_" + d
        self.cards.append(card)

    def getMainCardsAsStrList(self):
        board = []
        for i in range(0, len(self.cards)):
            if (self.cards[i] is not None and 'type' in self.cards[i] and self.cards[i]['type'] is not None):
                board.append(self.cards[i]['type'].replace("_", ""))
        return board

    def getPlayerCardsAsStrList(self):
        hand_cards = []
        hand = []
        for i in range(0, len(self.players)):
            if (self.players[i] is not None and 'cards' in self.players[i] and len(self.players[i]["cards"]) > 0):
                hand_cards = self.players[i]["cards"]
        for i in range(0, len(hand_cards)):
            hand.append(hand_cards[i]['type'].replace("_", ""))
        return hand
    
    def updatePlayersData(self):
        print("Table:updatePlayersData")
        
    def processTableImage(self, image):
        print("Table:processTableImage")
        y1=0
        y2=1
        x1=2
        x2=3

        players_data = []
        players_data.append([150,320,80,340])
        players_data.append([35,205,532,792])
        players_data.append([150,320,982,1242])

        players_data.append([430,600,68,328])
        players_data.append([585,755,532,792])
        players_data.append([430,600,994,1254])


        player_table_1 = ROI[150:320, 80:340]
        player_table_2 = ROI[35:205, 532:792]
        player_table_3 = ROI[150:320, 982:1242]


        player_table_4 = ROI[430:600, 68:328]
        player_table_5 = ROI[585:755, 532:792]
        player_table_6 = ROI[430:600, 994:1254]

        player_table_6 = ROI[430:600, 994:1254]

        cards_main = ROI[335:455, 438:886]

        #for rec in players_data:
        #    print(rec)
        #    cv2.rectangle(ROI,(rec[x2],rec[y2]),(rec[x1],rec[y1]),(0,255,0),3)

        #cam_quit = 0 # Loop control variable
        #while cam_quit == 0:
        #    cv2.imshow("Card Detector", cards_main)
        #    key = cv2.waitKey(1) & 0xFF
        #    if key == ord("q"):
        #        cam_quit = 1
                
        #cv2.destroyAllWindows()
        
    def isPlayerActionRequired(self, image):
        print("Table:isPlayerActionRequired")
        
        
    def confirmActionButtonTap(self, image):
        print("Table:confirmActionButtonTap")  

    def getCardsList(cards):
        result = []
        if cards == None:
            return result
        
        for i in range(0, len(cards)):
            if cards[i] != None:
                result.append(cards[i]["type"])
        return result
        
    def cardsInfo(self):
        return str(Table.getCardsList(self.cards))
        
    def controlsInfo(self):
        result = [""]
        #for i in range(0, len(self.controls)):
        #    result.append(self.cards[i].replace("_", ""))
        return str(self.controls)    
        #controlsInfo
        
    def playersInfo(self):
        result = []
        for i in range(0, len(self.players)):
            if self.players[i] != None:
                #class PlayerInfo: cards=[]; name=''
                #playerInfo = PlayerInfo()
                #playerInfo.cards = str(Table.getCardsList(self.players[i].cards))
                #playerInfo.name = players[i].name
                result.append(Table.getCardsList(self.players[i]["cards"]))
        return str(result)    

    def checkThatButtonExistInList(self, type):
        if self == None or self.controls == None or "buttons" not in self.controls or self.controls["buttons"] == None:
            return False
        for i in range(0, len(self.controls["buttons"])):
            if self.controls["buttons"][i]["type"] == type:
                return True
        return False
    
    def setControlsButtons(self, buttons):
        self.controls["buttons"] = []
        for i in range(0, len(buttons)): 
            self.controls["buttons"].append({"type": buttons[i]})
    
    def isActionRequired(self):
        if(
            self.isFoldButtonActive() or self.isCheckButtonActive() or 
            self.isCallButtonActive() or self.isRaiseButtonActive() or 
            self.isAllinButtonActive() or self.isBetButtonActive()
        ):
            return True
        else:
            return False        
    
    def isFoldButtonActive(self):
        return self.checkThatButtonExistInList("fold")
        
    def isCheckButtonActive(self):
        return self.checkThatButtonExistInList("check")
        
    def isCallButtonActive(self):
        return self.checkThatButtonExistInList("call")
        
    def isRaiseButtonActive(self):
        return self.checkThatButtonExistInList("raise")
        
    def isAllinButtonActive(self):
        return self.checkThatButtonExistInList("allin")
        
    def isBetButtonActive(self):
        return self.checkThatButtonExistInList("bet")
        
    def isNewgameButtonActive(self):
        return self.checkThatButtonExistInList("newgame")