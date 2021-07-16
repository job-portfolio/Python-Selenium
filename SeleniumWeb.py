import time, ctypes, threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Functions: Keyboard control
def PressKey(hexKeyCode):
    print('a')
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    print('b')
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def PressEnter():
    time.sleep(10)
    print('Running: Press Enter')
    PressKey(0x0D)      # Enter
    time.sleep(0.2)
    ReleaseKey(0x0D)    # Enter

def OpenPage_crtlP():
    print('Running: Open Page')
    browser.get('https://www.myglenigan.com/project_search_results.aspx?searchId='+ID)
    time.sleep(3)
    element=browser.find_element_by_xpath("//body")
    element.send_keys(Keys.CONTROL, 'p')

# Initialise the Firefox webdriver
browser = webdriver.Firefox()
time.sleep(3)

# Login to Glenigan
browser.get('https://www.myglenigan.com/default.aspx')
browser.find_element_by_xpath('//*[@id="Template_ctl22_ctl01_login_UserName"]').clear()
browser.find_element_by_xpath('//*[@id="Template_ctl22_ctl01_login_UserName"]').send_keys('')
browser.find_element_by_xpath('//*[@id="Template_ctl22_ctl01_login_Password"]').clear()
browser.find_element_by_xpath('//*[@id="Template_ctl22_ctl01_login_Password"]').send_keys('')
browser.find_element_by_xpath('//*[@id="Template_ctl22_ctl01_login_Login"]').click()

searchIDs = ['10001','10002','10003','10004','10005']

# For each search ID- 1. enter the search results page; 2. print that page
for ID in searchIDs:
    t1 = threading.Thread(target=OpenPage_crtlP)
    t2 = threading.Thread(target=PressEnter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    time.sleep(10)
