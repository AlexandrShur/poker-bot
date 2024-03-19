from pprint import pprint
import cv2
import numpy as np
import configparser
from LoggerUtils import LoggerUtils

class SettingsUtils:

    @staticmethod
    def getRanksTemplates():
        LoggerUtils.logStartMethod("SettingsUtils.getRanksTemplates")
        config = SettingsUtils.getConfig()
        
        data = []
        data.append(config.get('cards', 'template_two').split())
        data.append(config.get('cards', 'template_three').split())
        data.append(config.get('cards', 'template_four').split())
        data.append(config.get('cards', 'template_five').split())
        data.append(config.get('cards', 'template_six').split())
        data.append(config.get('cards', 'template_seven').split())
        data.append(config.get('cards', 'template_eight').split())
        data.append(config.get('cards', 'template_nine').split())
        data.append(config.get('cards', 'template_ten').split())
        data.append(config.get('cards', 'template_jack').split())
        data.append(config.get('cards', 'template_queen').split())
        data.append(config.get('cards', 'template_king').split())
        data.append(config.get('cards', 'template_ace').split())

        LoggerUtils.debug(data)
        return data

    @staticmethod
    def getSuitsTemplates():
        LoggerUtils.logStartMethod("SettingsUtils.getSuitsTemplates")
        config = SettingsUtils.getConfig()
        
        data = []
        data.append(config.get('cards', 'template_hearts').split())
        data.append(config.get('cards', 'template_clubs').split())
        data.append(config.get('cards', 'template_diamonds').split())
        data.append(config.get('cards', 'template_spades').split())

        LoggerUtils.debug(data)
        return data
        
    @staticmethod
    def getRanksAndSuits():
        LoggerUtils.logStartMethod("SettingsUtils.getRanksAndSuits")
        config = SettingsUtils.getConfig()
        
        data = []
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_1_r').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_1_s').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_2_r').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_2_s').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_3_r').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_3_s').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_4_r').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_4_s').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_5_r').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_5_s').split()])
        
        LoggerUtils.debug(data)
        return data
        
    @staticmethod
    def getMainCardsXRanges():
        LoggerUtils.logStartMethod("SettingsUtils.getMainCardsXRanges")
        config = SettingsUtils.getConfig()
        
        data = []
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_1_pos').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_2_pos').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_3_pos').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_4_pos').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards_5_pos').split()])
        
        LoggerUtils.debug(data)
        return data
        
    @staticmethod
    def getMainCards():
        LoggerUtils.logStartMethod("SettingsUtils.getMainCards")
        config = SettingsUtils.getConfig()   
        #print(config)
        data = []
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'main_cards').split()])
        LoggerUtils.debug("getMainCards: " + str(data))
        return data
        
    @staticmethod
    def getPlayers():
        LoggerUtils.logStartMethod("SettingsUtils.getPlayers")
        config = SettingsUtils.getConfig()   
        #print(config)
        data = []
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_1').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_2').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_3').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_4').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_5').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'player_6').split()])
        
        LoggerUtils.debug("getPlayers: " + str(data))
        return data

    @staticmethod
    def getButtons():
        LoggerUtils.logStartMethod("SettingsUtils.getButtons")
        config = SettingsUtils.getConfig()
        data = []
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'buttons').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_fold').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_check').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_raise').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_call').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_bet').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_allin').split()])
        data.append([int(numeric_string) for numeric_string in config.get('draw', 'button_newgame').split()])
        LoggerUtils.debug("getButtons: " + str(data))
        return data
    
    @staticmethod
    def getButtonsTemplates():
        LoggerUtils.logStartMethod("SettingsUtils.getButtonsTemplates")
        config = SettingsUtils.getConfig()
        
        data = []
        data.append(config.get('buttons', 'template_fold').split())
        data.append(config.get('buttons', 'template_check').split())
        data.append(config.get('buttons', 'template_call').split())
        data.append(config.get('buttons', 'template_bet').split())
        data.append(config.get('buttons', 'template_raise').split())
        data.append(config.get('buttons', 'template_allin').split())
        data.append(config.get('buttons', 'template_newgame').split())

        LoggerUtils.debug(data)
        return data
        
    @staticmethod
    def getConfig(): 
        config = configparser.RawConfigParser()
        
        mainConfigFilePath = r'settings/settings.txt'
        config.read(mainConfigFilePath)
        confName = config.get('main', 'current_config_name')
        #configFilePath = r'display_conf.txt'
        config.read(confName, encoding='utf-8')
        return config
        
    @staticmethod
    def getDisplayByKey(key): 
        config = SettingsUtils.getConfig()
        return config.get('draw', key)