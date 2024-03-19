import cv2
import configparser
from datetime import datetime
from os import listdir
from os.path import isfile, join
from SettingsUtils import SettingsUtils

def getDataToProcess():
    
    data = []
    data.extend(SettingsUtils.getRanksAndSuits())
    data.extend(SettingsUtils.getButtons())
    print (data)
    return data
    

def saveTableImage(image, iter):    
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        #cv2.imwrite("N:\\train\\open_cv_card\\temp\\templates\\" + str(iter) + str(ts) + ".jpg", image)    
        cv2.imwrite(SettingsUtils.getDisplayByKey("save_generated_templates_path") + str(iter) + str(ts) + ".jpg", image)    
   

def generateTemplates(sourceDir):
        print("TableDataDisplay:generateTemplates")
        
        files = [f for f in listdir(sourceDir) if isfile(join(sourceDir, f))]
        print(files)
        data = getDataToProcess()
        iter = 0
        for fileName in files:
            
            image = cv2.imread(sourceDir + fileName)
            for templateData in data:
                iter = iter + 1
                saveTableImage(image[templateData[0]:templateData[1], templateData[2]:templateData[3]], iter)
        
        print("generation finished")
        
def main():
    generateTemplates(SettingsUtils.getDisplayByKey("read_genarated_templates_path"))
main()