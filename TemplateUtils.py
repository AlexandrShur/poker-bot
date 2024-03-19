from pprint import pprint
import cv2
import numpy as np
from SettingsUtils import SettingsUtils
from LoggerUtils import LoggerUtils
import pytesseract

class TemplateUtils:

    @staticmethod
    def find_similar_by_template(source_img, template_img, threshold = 0.9):
        
        w, h = template_img.shape[::-1]
        result = []
        res = cv2.matchTemplate(source_img, template_img, cv2.TM_CCOEFF_NORMED)

        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            
            found_sample = {}
            found_sample["x"] = pt[0]
            found_sample["y"] = pt[1]
            found_sample["height"] = w
            found_sample["width"] = h
            found_sample["pt"] = pt
            
            result.append(found_sample)
            LoggerUtils.debug(found_sample)     
        return result
        
    @staticmethod
    def find_similar_main_cards_by_template(source_img, template_img, threshold = 0.9):
        cardsPositionsRanges = SettingsUtils.getMainCardsXRanges()
        found = TemplateUtils.find_similar_by_template(source_img, template_img, threshold)
        results = set([])
        for f in found:
            fx = int(f["x"])
            iter = 0
            for pos in cardsPositionsRanges:
                if fx >= int(pos[0]) and fx <= int(pos[1]):
                    results.add(iter)
                iter+=1
            
        return results
                    
    @staticmethod
    def main_cards_list_similar_templates(source_img, templates, threshold = 0.9):
        storedFound = []
        for template in templates:
            template_img = cv2.imread(template[1], 0) 
            found = TemplateUtils.find_similar_by_template(source_img, template_img, threshold)
            for f in found:
                fx = int(f["x"])
                is_already_stored = False
                for stored in storedFound:
                    if abs(stored['posx'] - fx) <= 10 and stored['type'] == template[0]:
                        is_already_stored = True
                        break
                
                if is_already_stored == False:
                    storedFoundDTO = {}
                    storedFoundDTO['posx'] = fx
                    storedFoundDTO['type'] = template[0]
                    storedFound.append(storedFoundDTO)
        LoggerUtils.debug("storedFound")
        LoggerUtils.debug(storedFound)
        return storedFound  
                    
    @staticmethod
    def find_cards(source_img):
        threshold = float(SettingsUtils.getDisplayByKey("template_threshold"))
        suitsTemplates = SettingsUtils.getSuitsTemplates()
        foundSuits = TemplateUtils.main_cards_list_similar_templates(source_img, suitsTemplates, threshold)        
        ranksTemplates = SettingsUtils.getRanksTemplates()
        foundRanks = TemplateUtils.main_cards_list_similar_templates(source_img, ranksTemplates, threshold)
        result = []
        if len(foundSuits) != len(foundRanks):
            PokerWindow.saveTableImageBugs(source_img)
            raise Exception('WrongCondition', 'Count of the founded suits and ranks are different')
        
        for suit in foundSuits:
            for rank in foundRanks:
                if abs(rank['posx'] - suit['posx']) <= 10:
                    resultDTO = {}
                    resultDTO['type'] = rank['type'] + "_" + suit['type']
                    resultDTO['posx'] = rank['posx']
                    resultDTO['rank'] = rank['type']
                    resultDTO['suit'] = suit['type']
                    result.append(resultDTO)
        
        result = sorted(result, key=lambda res: res['posx'])
        return result

    @staticmethod
    def find_text(source_img):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Alex\AppData\Local\Tesseract-OCR\tesseract.exe"
        #hsv = cv2.cvtColor(source_img, cv2.COLOR_BGR2HSV)
        #hsv = source_img
        
        #lower = np.array([0, 0, 218])
        #upper = np.array([157, 54, 255])
        #mask = cv2.inRange(hsv, lower, upper)
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3))
        #dilate = cv2.dilate(mask, kernel, iterations=1)
        #result = 255 - cv2.bitwise_and(dilate, mask)
        data = pytesseract.image_to_string(source_img, lang='rus',config='--psm 6')
        LoggerUtils.debug(data)
        return data  

    @staticmethod
    def find_number(source_img):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Alex\AppData\Local\Tesseract-OCR\tesseract.exe"
        data = pytesseract.image_to_string(source_img, lang='rus',config='--psm 6')
        if data is not None and isinstance(data, str):
            lines = data.splitlines()
            for line in lines:
                if line is not None:
                    processedLine = line.replace("р", "").replace(".", "").replace(",",".")
                    if TemplateUtils.is_number(processedLine):
                        try:
                            return int(processedLine)
                        except ValueError:
                            return int(float(processedLine))
        return None      
    
    @staticmethod
    def is_number(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def get_middle_color(source_img):
        data = np.reshape(source_img, (-1,3))
        LoggerUtils.debug(data.shape)
        data = np.float32(data)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)

        LoggerUtils.debug('Dominant color is: bgr({})'.format(centers[0].astype(np.int32)))
        return centers[0].astype(np.int32)

    @staticmethod
    def get_controls_data(sourceOriginal, buttonsSettings, buttonsTemplatesSettings):
        buttonTemplatesImage = cv2.cvtColor(sourceOriginal.copy(), cv2.COLOR_BGR2GRAY)
        image = sourceOriginal
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

        # Define lower and uppper limits of what we call "brown"
        brown_lo=np.array([0,0,0]) 
        brown_hi=np.array([254,254,254])

        # Mask image to only select browns
        mask=cv2.inRange(hsv,brown_lo,brown_hi)

        # Change image to red where we found brown
        image[mask>0]=(0,0,0)
        
        sourceOriginal = cv2.bitwise_not(image)
        mcd = buttonsSettings[1]
        fold_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
        mcd = buttonsSettings[2]
        check_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
        mcd = buttonsSettings[3]
        raise_source = sourceOriginal[mcd[0]:mcd[1], mcd[2]:mcd[3]]
        

        #cv2.imwrite("test/result.png",cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        cv2.imwrite("test/result.png", sourceOriginal)

        #TemplateUtils.find_text(sourceOriginal)
        fold_text = TemplateUtils.find_text(fold_source)
        check_text = TemplateUtils.find_text(check_source)
        raise_text = TemplateUtils.find_text(raise_source)
        
        #if "чек" in check_text.casefold():
        #    LoggerUtils.info ("check_text " + check_text)
        #if "поставить" in raise_text.casefold():
        #    LoggerUtils.info ("raise_text " + raise_text)
        #if "фолд" in fold_text.casefold():
        #    LoggerUtils.info ("fold_text " + fold_text)
        
        result = {}
        result["is_control_panel_active"] = False
        result["is_common_buttons"] = False
        result["buttons"] = TemplateUtils.get_buttons(buttonTemplatesImage, buttonsTemplatesSettings)
        if "чек" in check_text.casefold() and "фолд" in fold_text.casefold() and "поставить" in raise_text.casefold(): 
            LoggerUtils.debug ("Standard control found")
            result["is_control_panel_active"] = True
            result["is_common_buttons"] = True
        return result
        
    @staticmethod
    def get_buttons(sourceOriginal, buttonsSettings):    
        found_buttons = TemplateUtils.main_cards_list_similar_templates(sourceOriginal, buttonsSettings)
        return found_buttons
        