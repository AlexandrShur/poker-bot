from PokerWindow import PokerWindow
import cv2
import configparser
import schedule 
from datetime import datetime
from SettingsUtils import SettingsUtils
from LoggerUtils import LoggerUtils

self = PokerWindow()

def getDataToDisplay():
    config = SettingsUtils.getConfig()
    
    players_data = []

    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_1').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_2').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_3').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_4').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_5').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_6').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'buttons').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_fold').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_check').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_raise').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_call').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_bet').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_allin').split()])
    
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'input').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'bank').split()])
    
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_1_r').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_1_s').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_2_r').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_2_s').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_3_r').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_3_s').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_4_r').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_4_s').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_5_r').split()])
    players_data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_5_s').split()])
    
    print (players_data)
    return players_data
    
    
#schedule.every(10).seconds.do(getDataToDisplay)
    
def drawData(rec_data, image):
        cv2.rectangle(image,
                         (rec_data[self.matrix_to_draw_x2], rec_data[self.matrix_to_draw_y2]),
                         (rec_data[self.matrix_to_draw_x1], rec_data[self.matrix_to_draw_y1]),
                         (0,255,0),
                         1)

def displayData(image):
        print("TableDataDisplay:displayData")

        current_data_type = None
        current_data_corner = None
        current_data_value = None
        is_latest_notification_dispalyed = True
        data = getDataToDisplay()
        lastT = 0
        
        quit = 0 # Loop control variable
        while quit == 0:
            #schedule.run_pending()
            imageToDraw = image.copy()
            for rec_data in data:
                drawData(rec_data, imageToDraw)
            cv2.imshow("Poker table data display(from image)", imageToDraw)
            
            dt = datetime.now()
            ts = int(datetime.timestamp(dt))
            if (ts - lastT) > 6:
                lastT = ts
                data = getDataToDisplay()
                print (ts)
                
            key = cv2.waitKey(3) & 0xFF
            if key == ord("q"):
                quit = 1
            elif key == ord("r"):
                data = getDataToDisplay()
            elif key == 27:
                current_data_type = None
                current_data_corner = None
                current_data_value = None
                is_latest_notification_dispalyed = True
            elif key >= 48 and key <= 57:
                num_to_set = key - 48
                if current_data_type != None and current_data_corner != None:
                    if current_data_value == None:
                        current_data_value = str(num_to_set)
                    else: 
                        current_data_value = str(current_data_value) + str(num_to_set)
                    is_latest_notification_dispalyed = False
                elif current_data_type != None:
                    current_data_corner = num_to_set
                    is_latest_notification_dispalyed = False
                elif current_data_type == None:
                    current_data_type = num_to_set
                    is_latest_notification_dispalyed = False
                
            if is_latest_notification_dispalyed == False:
                print("Current settings: ", current_data_type, current_data_corner, current_data_value)
                is_latest_notification_dispalyed = True
        cv2.destroyAllWindows()
    
def main():
    #displayData(cv2.imread('temp/pokershots/1668593213.089405.jpg'))
    #displayData(cv2.imread('temp/pokershots/2/1679174092.653809.jpg'))
    displayData(cv2.imread(SettingsUtils.getDisplayByKey("table_data_display_template")))
main()