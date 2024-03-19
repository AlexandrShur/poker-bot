from pprint import pprint
import logging
from colorama import init, Fore, Back, Style, just_fix_windows_console

class ColorLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.INFO)
        #color_formatter = ColorFormatter("%(name)-10s %(levelname)-18s : %(message)s")
        color_formatter = ColorFormatter("%(asctime)s %(levelname)-18s : %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)
        
        fileHandler = logging.FileHandler("N:\\train\\open_cv_card\\log\\main.log")
        fileHandler.setFormatter(color_formatter)
        self.addHandler(fileHandler)

class ColorFormatter(logging.Formatter):
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "WARNING": Fore.RED,
        "ERROR": Fore.RED + Back.WHITE,
        "DEBUG": Style.DIM,
        "INFO": Fore.GREEN,
        "INFO2": Fore.MAGENTA,
        "INFO3": Fore.CYAN,
        "INFO4": Fore.YELLOW,
        "CRITICAL": Fore.RED + Back.WHITE
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:
            record.name = color + record.name
            record.levelname = color + record.levelname
            record.msg = color + str(record.msg)
        return logging.Formatter.format(self, record)
        
class LoggerUtils:
    #print(Fore.RED + Back.WHITE + "Init LoggerUtils.")
    init(autoreset=True)
    logging.setLoggerClass(ColorLogger)
    #logging.basicConfig(filename='C:\var\log\example.log', encoding='utf-8', level=logging.DEBUG)
    #logging.basicConfig(filename='N:\train\open_cv_card\log\', encoding='utf-8', level=logging.DEBUG)
    
    logger = logging.getLogger(__name__)
    
    
    
    #logger.info("This is an info message")
    #logger.warning("This is a warning message")
    #logger.debug("This is a debug message")
    #logger.error("This is an error message")

    #just_fix_windows_console()
    #init(autoreset=True)
    #level = logging.DEBUG
    #logging.basicConfig(filename='C:\var\log\example.log', encoding='utf-8', level=logging.DEBUG)


    @staticmethod
    def logStartMethod(name):
        #print(Fore.RED + 'some red text')
        LoggerUtils.logger.debug("===================" + "Started `" + name + "` execution" + "===================")
        #print("===================" + "Started `" + name + "` execution" + "===================")
        
        
    @staticmethod
    def logEndMethod(name):
        #print(Fore.RED + 'some red text')
        LoggerUtils.logger.debug("===================" + "Finished `" + name + "` execution" + "===================")
        #print("===================" + "Finished `" + name + "` execution" + "===================")
     
    @staticmethod
    def debug(text):
        LoggerUtils.logger.debug(text)
        
    @staticmethod
    def error(text):
        LoggerUtils.logger.error(text)
        
    @staticmethod
    def info(text):
        LoggerUtils.logger.info(text)
        
    @staticmethod
    def info2(text):
        LoggerUtils.logger.info(text)
        
    @staticmethod
    def info3(text):
        print(Fore.YELLOW + str(text))
        
    @staticmethod
    def info4(text):
        LoggerUtils.logger.info(text)
        
    @staticmethod
    def warning(text):
        LoggerUtils.logger.warning(text)
        
    @staticmethod
    def critical(text):
        LoggerUtils.logger.critical(text)
    