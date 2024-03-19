from bot.holdem_calc import HoldemCalc 
from bot import holdem_functions
from treys import Card, Deck, Evaluator
from PokerWindow import PokerWindow
from LoggerUtils import LoggerUtils


#board = []
#board.append(holdem_functions.Card("Ah"))
#board.append(holdem_functions.Card("Kh"))
#player_cards = tuple([(holdem_functions.Card("As"),holdem_functions.Card("Ks")), (holdem_functions.Card("Kd"),holdem_functions.Card("Qs"))])
#player_cards = tuple([(holdem_functions.Card("As"),holdem_functions.Card("Ks"))])

#ss = HoldemCalc()
class Bot:
    def getScore(table):
        board = []
        hand = []
        mainCards = table.getMainCardsAsStrList()
        for i in range(0, len(mainCards)):
            board.append(Card.new(mainCards[i]))
        handCards = table.getPlayerCardsAsStrList()
        for i in range(0, len(handCards)):
            hand.append(Card.new(handCards[i]))
        
        if len(board) == 0 and len(hand) == 0:
            return 8000
        
        evaluator = Evaluator()
        score = evaluator.evaluate(hand, board)
        return score
    
    def getScoreForHandOnly(table):
        hand = []
        handCards = table.getPlayerCardsAsStrList()
        for i in range(0, len(handCards)):
            hand.append(Card.new(handCards[i]))
        if len(hand) < 2:
            print("ERROR: getScoreForHandOnly recieved less than 2 cards")
            return 8000
        if Bot.isPair(hand):
            return 4000
        if Bot.isHigherThanNine(hand):
            return 4000
        
        
        return 5000
        
    def isPair(hand):
        first = Card.int_to_str(hand[0])[0]
        second = Card.int_to_str(hand[1])[0]
        if first == second:
            return True
        return False
    
    def isHigherThanNine(hand):
        rf = Card.int_to_str(hand[0])[0]
        rs = Card.int_to_str(hand[1])[0]
        rnks = ['A','K','Q','J','T']
        if rf in rnks and rs in rnks:
            return True
        return False
        
    def getActionBasedOnCardsAndControls(table):
        
        if table.isNewgameButtonActive():
            LoggerUtils.info("Action: step 0")
            PokerWindow.clickNewgameButton()
            return "clickNewgameButton"
        
        
        #winRate = Bot.getWinRateFromTable(table)
        isFirstRound = len(table.getMainCardsAsStrList()) == 0
        if isFirstRound:
            score = Bot.getScoreForHandOnly(table)
        else: 
            score = Bot.getScore(table)

        if isFirstRound and table.isCheckButtonActive():
            LoggerUtils.info("Action: step 1")
            PokerWindow.clickCheckButton()
            return "clickCheckButton"
        if Bot.isWorthToPeek(table) and table.isCallButtonActive() and table.callMoney > 0 and not Bot.isPossibleLose(table):
            LoggerUtils.info("Action: step 2")
            print("Bot.isPossibleLose(table): " + str(Bot.isPossibleLose(table)))
            print("Bot.isWorthToPeek(table): " + str(Bot.isWorthToPeek(table)))
            PokerWindow.clickCallButton()
            return "clickCallButton"
        elif isFirstRound and table.isCallButtonActive() and table.callMoney < 7 and score <= 4000:
            LoggerUtils.info("Action: step 3")
            PokerWindow.clickCallButton()
            return "clickCallButton"
        elif isFirstRound and table.isCallButtonActive():
            LoggerUtils.info("Action: step 4")
            PokerWindow.clickFoldButton()
            return "clickFoldButton"
        elif Bot.isPossibleLose(table):
            LoggerUtils.info("Action: step 5")
            PokerWindow.clickFoldButton()
            return "clickFoldButton"
        elif score <= 4000 and table.isCallButtonActive():
            LoggerUtils.info("Action: step 6")
            PokerWindow.clickCallButton()
            return "clickCallButton"
        elif score <= 4000 and table.isBetButtonActive():
            LoggerUtils.info("Action: step 7")
            PokerWindow.clickBetButton()
            return "clickBetButton"
        elif score <= 4000 and table.isCallButtonActive():
            LoggerUtils.info("Action: step 8")
            PokerWindow.clickCallButton()
            return "clickCallButton"
        elif score <= 3000 and table.isRaiseButtonActive():
            LoggerUtils.info("Action: step 9")
            PokerWindow.clickRaiseButton()
            return "clickRaiseButton"
        elif score > 4000 and table.isCheckButtonActive():
            LoggerUtils.info("Action: step 10")
            PokerWindow.clickCheckButton()
            return "clickCheckButton"
        elif score < 1000 and table.isAllinButtonActive():
            LoggerUtils.info("Action: step 11")
            PokerWindow.clickAllinButton()
            return "clickAllinButton"
        else:
            LoggerUtils.info("Action: step default")
            PokerWindow.clickFoldButton()
            return "clickFoldButton"

            
    #def isPossibleLose(table):
    #    print("")
        #bet = getBet(table)
        #if  (possibleHighestHand(table) > currentHand(table) && isBetHighFor(possibleHighestHand(table))):
        #    return True
        #return False
        
    def currentHand():
        print("")
        
    def possibleHighestHand():
        print("")
    
    def isWorthToPeek(table):
        rate = Bot.getHandsLocalRate(table)
        LoggerUtils.info("isWorthToPeek: " + str(rate))
        if Bot.getHighCardRank(table) > 11 and table.callMoney <= 2:
            LoggerUtils.info("isWorthToPeek: HighCardRank")
            return True
        if Bot.isHandSameSuit(table) and table.callMoney <= 2:
            LoggerUtils.info("isWorthToPeek: HandSameSuit")
            return True
        if rate >= 2 and table.callMoney <= 5:
            LoggerUtils.info("isWorthToPeek: rate >= 2")
            return True
        if rate > 2 and table.callMoney <= 8:
            LoggerUtils.info("isWorthToPeek: rate > 2")
            return True
        if rate >= 5:
            LoggerUtils.info("isWorthToPeek: rate >= 5")
            return True
        return False
    
    def getHighCardRank(table):
        ranksNum = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }
        handCards = table.getPlayerCardsAsStrList()
        if len(handCards) == 2:
            rank = handCards[0][0]
            rank2 = handCards[1][0]
            if ranksNum[rank] > ranksNum[rank2]:
                return ranksNum[rank]
            return ranksNum[rank2]
        return 0
    
    def isHandSameSuit(table):
        handCards = table.getPlayerCardsAsStrList()
        if len(handCards) == 2:
            suit = handCards[0][1]
            suit2 = handCards[1][1]
            if suit == suit2:
                return True
        return False
        
    def getHandsLocalRate(table):
        rate = 0
        hCounter = 0
        dCounter = 0
        cCounter = 0
        sCounter = 0
        maxStraight = 0
        sameRanksCounter = 0
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        ranksNum = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }
        ranksCounter = {
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "T": 0,
            "J": 0,
            "Q": 0,
            "K": 0,
            "A": 0
        }
        ranksSuits = {
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
            "7": [],
            "8": [],
            "9": [],
            "T": [],
            "J": [],
            "Q": [],
            "K": [],
            "A": []
        }
        suits = ["d", "h", "s", "c"]
        suitsCounter = {"d": 0, "h": 0, "s": 0, "c": 0}
        
        
        cards = []
        mainCards = table.getMainCardsAsStrList()
        for i in range(0, len(mainCards)):
            cards.append(mainCards[i])
            rank = mainCards[i][0]
            suit = mainCards[i][1]
            ranksCounter[rank] += 1
            suitsCounter[suit] += 1
            ranksSuits[rank].append(suit)
        
        
        handCards = table.getPlayerCardsAsStrList()
        for i in range(0, len(handCards)):
            cards.append(handCards[i])
        #cards = board + hand
            rank = handCards[i][0]
            suit = handCards[i][1]
            ranksCounter[rank] += 1
            suitsCounter[suit] += 1
            ranksSuits[rank].append(suit)
            
        rate2 = 0
        rate22 = 0
        rate3 = 0
        rate4 = 0
        curStraight = 0
        highStraight = None
        flushSuit = None
        lastSuit = None
        curFlash = 0
        isZerroed = False
        for i in range(0, len(suits)):
            if suitsCounter[suits[i]] >= 5:
                curFlash = suitsCounter[suits[i]]
                flushSuit = suits[i]
        for i in range(0, len(ranks)):
            if ranksCounter[ranks[i]] > 0 and isZerroed == False:
                curStraight +=1
                highStraight = ranks[i]
            elif curStraight < 5:
                curStraight = 0
            elif curStraight >= 5 and ranksCounter[ranks[i]] == 0:
                isZerroed = True
            if ranksCounter[ranks[i]] == 2:
                if rate2 > 0:
                    rate22 = 2
                else:
                    rate2 = 2

            if ranksCounter[ranks[i]] == 3:
                rate3 = 3
            if ranksCounter[ranks[i]] == 4:
                rate4 = 4
        if rate2 > 0:
            rate = 2
        if rate22 > 0:
            rate = 3
        if rate3 > 0:
            rate = 4
        if curStraight >= 5:
            rate = 5
        if curFlash > 0:
            rate = 6
        if rate3 > 0 and rate2 > 0:
            rate = 7
        if rate4 > 0:
            rate = 8
        if curStraight >= 5 and curFlash >= 5:
            stflCounter = 0
            for i in range(ranksNum[highStraight] - 6, ranksNum[highStraight] - 1):
                for g in range (0, len(ranksSuits[ranks[i]])):
                    if flushSuit == ranksSuits[ranks[i]][g]:
                        stflCounter +=1
                        break;
            if stflCounter >= 5:
                rate = 9
        return rate
        
    def getPossibleHands(table):
        rate = 0
        hCounter = 0
        dCounter = 0
        cCounter = 0
        sCounter = 0
        maxStraight = 0
        sameRanksCounter = 0
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        ranksNum = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }
        ranksCounter = {
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "T": 0,
            "J": 0,
            "Q": 0,
            "K": 0,
            "A": 0
        }
        ratesResult = {
            "pair": 0,
            "two_pair": 0,
            "three": 0,
            "straight": 0,
            "flush": 0,
            "full_house": 0,
            "four": 0,
            "straight_flush": 0,
        }
        ranksSuits = {
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
            "7": [],
            "8": [],
            "9": [],
            "T": [],
            "J": [],
            "Q": [],
            "K": [],
            "A": []
        }
        suits = ["d", "h", "s", "c"]
        suitsCounter = {"d": 0, "h": 0, "s": 0, "c": 0}
        
        
        cards = []
        mainCards = table.getMainCardsAsStrList()
        for i in range(0, len(mainCards)):
            cards.append(mainCards[i])
            rank = mainCards[i][0]
            suit = mainCards[i][1]
            ranksCounter[rank] += 1
            suitsCounter[suit] += 1
            ranksSuits[rank].append(suit)
        
        
        #handCards = table.getPlayerCardsAsStrList()
        #for i in range(0, len(handCards)):
        #    cards.append(handCards[i])
        #    rank = handCards[i][0]
        #    suit = handCards[i][1]
        #    ranksCounter[rank] += 1
        #    suitsCounter[suit] += 1
        #    ranksSuits[rank].append(suit)
            
        rate2 = 0
        rate22 = 0
        rate3 = 0
        rate4 = 0
        curStraight = 0
        highStraight = None
        flushSuit = None
        lastSuit = None
        curFlash = 0
        isZerroed = False
        for i in range(0, len(suits)):
            if suitsCounter[suits[i]] >= 5:
                Bot.setPercentageRate(ratesResult, "flush", 100)
            if suitsCounter[suits[i]] == 4:
                Bot.setPercentageRate(ratesResult, "flush", 80)
            if suitsCounter[suits[i]] == 3:
                Bot.setPercentageRate(ratesResult, "flush", 60)
            
        for i in range(0, len(ranks)):
            if ranksCounter[ranks[i]] > 0 and isZerroed == False:
                curStraight +=1
                if curStraight >= 5:
                    Bot.setPercentageRate(ratesResult, "straight", 100)
                if curStraight == 4:
                    Bot.setPercentageRate(ratesResult, "straight", 80)
                if curStraight == 3:
                    Bot.setPercentageRate(ratesResult, "straight", 60)
                highStraight = ranks[i]
            elif curStraight < 5:
                curStraight = 0
            elif curStraight >= 5 and ranksCounter[ranks[i]] == 0:
                isZerroed = True
            if ranksCounter[ranks[i]] > 0 and rate2 > 0:
                Bot.setPercentageRate(ratesResult, "two_pair", 80)
            if ranksCounter[ranks[i]] == 1:
                Bot.setPercentageRate(ratesResult, "pair", 80)
            print ("ranksCounter[ranks[i]]: " + str(ranksCounter[ranks[i]]))
            if ranksCounter[ranks[i]] == 2:
                if rate2 > 0:
                    rate22 = 2
                    Bot.setPercentageRate(ratesResult, "two_pair", 100)
                    Bot.setPercentageRate(ratesResult, "full_house", 80)
                    Bot.setPercentageRate(ratesResult, "three", 80)
                    Bot.setPercentageRate(ratesResult, "four", 70)
                else:
                    rate2 = 2
                    Bot.setPercentageRate(ratesResult, "pair", 100)
                    Bot.setPercentageRate(ratesResult, "three", 80)
                    Bot.setPercentageRate(ratesResult, "four", 60)
                    Bot.setPercentageRate(ratesResult, "two_pair", 50)
                    Bot.setPercentageRate(ratesResult, "full_house", 50)

            if ranksCounter[ranks[i]] == 3:
                Bot.setPercentageRate(ratesResult, "three", 100)
                Bot.setPercentageRate(ratesResult, "four", 80)
                Bot.setPercentageRate(ratesResult, "full_house", 60)
                Bot.setPercentageRate(ratesResult, "two_pair", 60)
                rate3 = 3
            if ranksCounter[ranks[i]] == 4:
                Bot.setPercentageRate(ratesResult, "four", 100)
                Bot.setPercentageRate(ratesResult, "two_pair", 50)
                Bot.setPercentageRate(ratesResult, "full_house", 70)
                rate4 = 4
        if rate2 > 0:
            rate = 2
        if rate22 > 0:
            rate = 3
        if rate3 > 0:
            rate = 4
        if curStraight >= 5:
            rate = 5
        if curFlash > 0:
            rate = 6
        if rate3 > 0 and rate2 > 0:
            rate = 7
        if rate4 > 0:
            rate = 8
        if curStraight >= 5 and curFlash >= 5:
            stflCounter = 0
            for i in range(ranksNum[highStraight] - 6, ranksNum[highStraight] - 1):
                for g in range (0, len(ranksSuits[ranks[i]])):
                    if flushSuit == ranksSuits[ranks[i]][g]:
                        stflCounter +=1
                        break;
            if stflCounter >= 5:
                rate = 9
        return ratesResult    
    

    def setPercentageRate(rates, name, percentage):
        if rates[name] < percentage:
            rates[name] = percentage
      
    def isPossibleLose(table):
        if table.isAllinButtonActive() or table.isCallButtonActive():
            ratePos = {
                2 : "pair",
                3 : "two_pair",
                4 : "three",
                5 : "straight",
                6 : "flush",
                7 : "full_house",
                8 : "four",
                9 : "straight_flush"
            }
            rate = Bot.getHandsLocalRate(table)
            possibles = Bot.getPossibleHands(table)
            print("rate: " + str(rate))
            print("possibles: " + str(possibles))
            if rate > 2 and rate < 9:
                for i in range(rate+1, 9):
                    if possibles[ratePos[i]] > 70:
                        return True
                
        return False
        
    #def isFirstGo(table):
    #    if len(table.getMainCardsAsStrList()) == 0:
            
#print("===============" + str(suit_value_dict))
#print(str(getWinRate(["As","Ks"], ["Qh", "2h", "3h"])))
#run(hole_cards, num, exact, board, file_name, True)
