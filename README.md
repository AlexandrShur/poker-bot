# Bot which plays poker. 
Uses OpenCV to recognize cards, buttons and etc... on a screen.
Written on python.

# Tests
Added main cases tests
python -m pytest runTemplatesTest.py -s
python -m pytest tests

# Apps
runTableManager.py - main script which starts bot.
runTableDataDisplay.py - displays how detected elements.
runTemplatesGenerator.py - script to get cards and buttons templates from real screenshots.
runTableSaver.py - saves table screenshots

# Folders
/bot - bot models and logic.
/log - logs written here
/models - folder for common reused DTO's/Entities
/res - folder where stored cards and buttons templates
/settings - here stores settings for current poker platform
/test - tests with tes screenshots to check bot logic