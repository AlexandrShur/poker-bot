import pygetwindow
import time
import os
import pyautogui
import PIL
import cv2
import numpy as np
from datetime import datetime
from SettingsUtils import SettingsUtils
import pyautogui
import random
from LoggerUtils import LoggerUtils

class PokerWindow:

    matrix_to_draw_y1=0
    matrix_to_draw_y2=1
    matrix_to_draw_x1=2
    matrix_to_draw_x2=3
    x3 = int(SettingsUtils.getDisplayByKey("window_width"))
    #x3 = 1117
    y3 = int(SettingsUtils.getDisplayByKey("window_height"))
        
    #y3 = 843
    isMock = False
    mockIterator = 0
    mockFrames = []

    def getWindowByName(self, windowName):
        LoggerUtils.debug("PokerWindow.getWindowByName")
        titles = pygetwindow.getAllTitles()
        win = None
        for title in titles:
            if (title.find(windowName) >= 0):
                win = pygetwindow.getWindowsWithTitle(title)[0]
                break
        LoggerUtils.debug(win.title)
        return win

    
    def prepareWindow(self):
        LoggerUtils.debug("PokerWindow.prepareWindow")
        if (self is not None and self.isMock == True):
            return
        titles = pygetwindow.getAllTitles()
        #windows = pygetwindow.getAllWindows()
        #print(titles)
        win = None
        #windowName = 'Лобби'
        windowName = SettingsUtils.getDisplayByKey("window_name")
        for title in titles:
            if (title.find(windowName) >= 0):
                #print(title)
                win = pygetwindow.getWindowsWithTitle(title)[0]
                break
        LoggerUtils.debug(win.title)

        #       imageObj = pyautogui.screenshot() cv_imageObj = cv2.cvtColor(numpy.array(imageObj),                      cv2.COLOR_RGB2BGR)
        #win.resizeTo(1024, 768)

        # get screensize
        x,y = pyautogui.size()
        LoggerUtils.debug(f"width={x}\theight={y}")

        x2,y2 = pyautogui.size()
        x2,y2=int(str(x2)),int(str(y2))
        LoggerUtils.debug(x2//2)
        LoggerUtils.debug(y2//2)


        #x3 = x2 // 2
        #y3 = y2 // 2
        #x3 = 1024
        #y3 = 768
        time.sleep(3)
        win.resizeTo(self.x3, self.y3)
        time.sleep(3)
        # top-left
        win.moveTo(0, 0)
        time.sleep(3)
        #time.sleep(3)
        win.activate()
        #time.sleep(1)
        time.sleep(6)
        #p = pyautogui.screenshot()
        #===========================
        #imageObj = pyautogui.screenshot() 
        #cv_imageObj = cv2.cvtColor(np.array(imageObj), cv2.COLOR_RGB2BGR)

        #header_offest = 87
        #left_border_offset = 9
        ##y_offset = 135
        ##x_offset = -167
        #y_offset = 162
        #x_offset = 102


        #ROI = cv_imageObj[header_offest:y3 + y_offset, left_border_offset:x3 + x_offset]
        #print(ROI.shape) # (843, 1117, 3)

        #================================


        #cam_quit = 0 # Loop control variable
        #while cam_quit == 0:
        #    cv2.imshow("Card Detector", ROI)
        #    key = cv2.waitKey(1) & 0xFF
        #    if key == ord("q"):
        #        cam_quit = 1
                
        #cv2.destroyAllWindows()
        
        #return ROI
        
    def getTableImage(self):
        if (self is not None and self.isMock == True):
            ROI = cv2.imread(self.mockFrames[self.mockIterator], cv2.COLOR_RGB2BGR)
            LoggerUtils.warning(self.mockFrames[self.mockIterator])
            self.mockIterator += 1
            return ROI
            
        imageObj = pyautogui.screenshot() 
        cv_imageObj = cv2.cvtColor(np.array(imageObj), cv2.COLOR_RGB2BGR)


        header_offest = int(SettingsUtils.getDisplayByKey("header_offest"))
        left_border_offset = int(SettingsUtils.getDisplayByKey("left_border_offset"))
        y_offset = int(SettingsUtils.getDisplayByKey("bottom_border_offset"))
        x_offset = int(SettingsUtils.getDisplayByKey("right_border_offset"))
        

        ROI = cv_imageObj[header_offest:self.y3 + y_offset, left_border_offset:self.x3 + x_offset]
        LoggerUtils.debug(ROI.shape)
        
        return ROI
    
    def getPlayersData(self):
        players_data = []
        players_data.append([150,320,80,340])
        players_data.append([35,205,532,792])
        players_data.append([150,320,982,1242])
        players_data.append([430,600,68,328])
        players_data.append([585,755,532,792])
        players_data.append([430,600,994,1254])

        #player_table_1 = image[150:320, 80:340]
        #player_table_2 = image[35:205, 532:792]
        #player_table_3 = image[150:320, 982:1242]
        #player_table_4 = image[430:600, 68:328]
        #player_table_5 = image[585:755, 532:792]
        #player_table_6 = image[430:600, 994:1254]
        
        return players_data
        
    def getMainCardsData(self, image):
        #return image[335:455, 438:886]
        return [150,320,80,340]
        
    def showAllImportantPartsOnline(self):
        LoggerUtils.debug("Table:showAllImportantPartsOnline")
        image = self.getTableImage()
        players_data = self.getPlayersData(image)
        cards_main_data = self.getMainCardsData(image)
        #buttons_data = getButtonsData(image)
        #bank_data = getBankData(image)
        #cards_main_details_data = getMainCardsDetailsData(image)
        
        for rec in players_data:
            LoggerUtils.debug(rec)
            cv2.rectangle(image,
                         (rec[self.matrix_to_draw_x2], rec[self.matrix_to_draw_y2]),
                         (rec[self.matrix_to_draw_x1], rec[self.matrix_to_draw_y1]),
                         (0,255,0),
                         3)
        cv2.rectangle(image,
                         (cards_main_data[self.matrix_to_draw_x2], cards_main_data[self.matrix_to_draw_y2]),
                         (cards_main_data[self.matrix_to_draw_x1], cards_main_data[self.matrix_to_draw_y1]),
                         (0,255,0),
                         3)
        cam_quit = 0 # Loop control variable
        while cam_quit == 0:
            cv2.imshow("Poker table data display(from image)", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cam_quit = 1
                
        cv2.destroyAllWindows()
    
    def saveTableImage(self, image):    
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        #cv2.imwrite("N:\\train\\open_cv_card\\temp\\pokershots\\2\\" + str(ts) + ".jpg", image)
        cv2.imwrite(SettingsUtils.getDisplayByKey("save_shots_path") + str(ts) + ".jpg", image)
        
    def saveTableImageBugs(self, image):    
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        print("saveTableImageBugs:  " + SettingsUtils.getDisplayByKey("save_bugs_path"))
        #cv2.imwrite("N:\\train\\open_cv_card\\temp\\pokershots\\2\\" + str(ts) + ".jpg", image)
        cv2.imwrite(SettingsUtils.getDisplayByKey("save_bugs_path") + str(ts) + ".jpg", image)
    
    def saveTableImageInALoop(self):
        LoggerUtils.debug("Table:saveTableImageInALoop")
        
        cam_quit = 0 # Loop control variable
        while cam_quit == 0:
            windowName = "Poker table save image"
            cv2.imshow(windowName, np.ones((100,100,1),np.uint8)*255 )
            #time.sleep(1)
            #win = self.getWindowByName(windowName)
            #win.moveTo(1000, 0)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cam_quit = 1
            if key == ord("s"):
                LoggerUtils.info("Table:saveTableImageInALoop:saved")
                self.saveTableImage(self.getTableImage())
        cv2.destroyAllWindows()
        
    def getClickPosition(x1, x2):
        return random.randrange(x1 + 5, x2 - 5)

    def doClickInAnArea(mcd):
        pyautogui.click(PokerWindow.getClickPosition(mcd[2], mcd[3]), PokerWindow.getClickPosition(mcd[0], mcd[1]) + int(SettingsUtils.getDisplayByKey("header_offest")))
        
       
    def clickFoldButton():
        LoggerUtils.info("clickFoldButton")
        buttonsSettings = SettingsUtils.getButtons()
        mcd = buttonsSettings[1]
        PokerWindow.doClickInAnArea(mcd)
    
    def clickCheckButton():
        LoggerUtils.info("clickCheckButton")
        buttonsSettings = SettingsUtils.getButtons()
        mcd = buttonsSettings[2]
        PokerWindow.doClickInAnArea(mcd)
        
    def clickRaiseButton():
        LoggerUtils.info("clickRaiseButton")
        buttonsSettings = SettingsUtils.getButtons()
        mcd = buttonsSettings[3]
        PokerWindow.doClickInAnArea(mcd)
    
    def clickCallButton():
        LoggerUtils.info("clickCallButton")
        buttonsSettings = SettingsUtils.getButtons()
        mcd = buttonsSettings[4]
        PokerWindow.doClickInAnArea(mcd)
    
    def clickBetButton():
        LoggerUtils.info("clickBetButton")
        buttonsSettings = SettingsUtils.getButtons()
        mcd = buttonsSettings[5]
        PokerWindow.doClickInAnArea(mcd)
  
    def clickAllinButton():
        LoggerUtils.info("clickAllinButton")
        buttonsSettings = SettingsUtils.getButtons()
        mcd = buttonsSettings[6]
        PokerWindow.doClickInAnArea(mcd)
        
    def clickNewgameButton():
        LoggerUtils.info("clickNewgameButton")
        buttonsSettings = SettingsUtils.getButtons()
        mcd = buttonsSettings[7]
        PokerWindow.doClickInAnArea(mcd)
  