# -*- coding: utf-8 -*-    
from cv2 import cv2

from captcha.solveCaptcha import solveCaptcha

from os import listdir
from src.logger import logger, loggerMapClicked
from random import randint
from random import random
import pygetwindow
import numpy as np
import mss
import pyautogui
import time
import sys

import yaml


msg = """
                                                _

>>---> Bot começou a rodar!

>>---> Acesse: https://github.com/sCryptoHelp/spacecrypto-bot

>>---> Pressione ctrl + c para parar o bot.

"""


print(msg)
time.sleep(2)


if __name__ == '__main__':
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

ct = c['threshold']
ch = c['home']

pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause

pyautogui.FAILSAFE = False
hero_clicks = 0
login_attempts = 0
last_log_is_progress = False



def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)

    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images():
    file_names = listdir('./targets/')
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

images = load_images()

def show(rectangles, img = None):

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    cv2.imshow('img',img)
    cv2.waitKey(0)





def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass

    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass

                return False
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2

        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))

        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll(clickAndDragAmount):

    flagScroll = positions(images['spg-flag-scrool'], threshold = ct['commom'])
    
    if (len(flagScroll) == 0):
        return
    x,y,w,h = flagScroll[len(flagScroll)-1]

    moveToWithRandomness(x,y,1)

    pyautogui.dragRel(0,clickAndDragAmount,duration=1, button='left')


def refreshPage():
    # refresh Page
    clickBtn(images['refresh-page'])

def login():
    global login_attempts
    logger('😿 Checking if game has disconnected')

    if login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing')
        login_attempts = 0
        processLogin()
        return

    if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        logger('🎉 Connect wallet button detected, logging in!')
        login_attempts = login_attempts + 1
        

    if clickBtn(images['select-wallet-2'], name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1

        if len(positions(images['spg-home'], threshold=ct['base_position']))  > 0:
           login_attempts = 0
           refreshSpaceships()
        return

    if not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = ct['select_wallet_buttons'] ):
            pass
            
    else:
        pass
        
    if clickBtn(images['select-wallet-2'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
        
    checkClose()

def goToSpaceShips():
    if clickBtn(images['spg-spaceships-ico']):
        global login_attempts
        login_attempts = 0

def loginSPG():
    global login_attempts
    
    if login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing')
        login_attempts = 0
        processLogin()
        return

    if clickBtn(images['spg-connect-wallet'], name='connectWalletBtn', timeout = 10):
        logger('🎉 Connect wallet button detected, logging in!')
        login_attempts = login_attempts + 1
        

    if clickBtn(images['select-wallet-2'], name='sign button', timeout=8):
        # sometimes the sign popup appears imediately
        login_attempts = login_attempts + 1
        return
        # click ok button

    if not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = ct['select_wallet_buttons'] ):
            pass
    else:
        pass

    if clickBtn(images['select-wallet-2'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
                
def playSPG():
    if clickBtn(images['spg-play'], name='okPlay', timeout=5):
            logger('played SPG')

def removeSpaceships():
    time.sleep(2)   

    while True: 
        buttons = positions(images['spg-x'], threshold=ct['remove_to_work_btn'])
       
        for (x, y, w, h) in buttons:
            moveToWithRandomness(x+(w/2),y+(h/2),1)
            pyautogui.click()

        if len(buttons) == 0:
            break
       
def clickButtonsFight():
    buttons = positions(images['spg-go-fight'], threshold=ct['go_to_work_btn'])
    qtd_send_spaceships = ct['qtd_send_spaceships']
    
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        
        if hero_clicks >= qtd_send_spaceships:
            logger('Finish Click Hero')
            return -1
    return len(buttons)

def refreshSpaceships():

    logger('Refresh Spaceship to Fight')

    buttonsClicked = 1
    empty_qtd_spaceships = ct['qtd_spaceships']
    qtd_send_spaceships = ct['qtd_send_spaceships']

    cda =  c['click_and_drag_amount']
    
    global hero_clicks
    hero_clicks = 0

    # c['scroll_attemps']
    empty_scrolls_attempts = qtd_send_spaceships 
      
    checkClose()

    while(empty_scrolls_attempts >0):
        buttonsClicked = clickButtonsFight()
        
        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
            scroll(-cda)
        else:
            if buttonsClicked == -1:
                empty_scrolls_attempts = 0   
            else:
                if buttonsClicked > 0:
                    empty_scrolls_attempts = empty_scrolls_attempts + 1

        time.sleep(2)
        logger('💪 {} Spaceships sent to Fight'.format(hero_clicks))

    if hero_clicks == qtd_send_spaceships:
        goToFight()
    else:
        goToFight()
        time.sleep(3)
        returnBase()
        time.sleep(2)
        refreshSpaceships()

def goToFight():
    clickBtn(images['spg-go-to-boss'])
    time.sleep(1)
    clickBtn(images['spg-confirm'])

def endFight():
    logger("End fight")
    time.sleep(3) 
    returnBase()
    time.sleep(15) 

    if len(positions(images['spg-processing'], threshold=ct['commom_position'])) > 0:
        time.sleep(ct['check_processing_time']) 

    if len(positions(images['spg-home'], threshold=ct['base_position']))  > 0:
        removeSpaceships()
        time.sleep(1) 
        refreshSpaceships()
    else:
        refreshPage()


def returnBase():
    goToSpaceShips()

def lifeBoss():
    lessPosition = positions(images['spg-life-boss-1'], threshold=ct['end_boss'])

    if len(lessPosition) == 0:
        lessPosition = positions(images['spg-life-boss-2'], threshold=ct['end_boss'])
                    
    if len(lessPosition) == 0:
        lessPosition = positions(images['spg-life-boss-3'], threshold=ct['end_boss'])

    return lessPosition

def processLogin():
    logger('Starting Login')
    sys.stdout.flush()
    loginSPG()
    time.sleep(3)
    playSPG()

def checkClose():
    if clickBtn(images['spg-close'], name='closeBtn', timeout=1):
        processLogin()


def main():
    time.sleep(5)
    t = c['time_intervals']
    

    windows = []

    for w in pygetwindow.getWindowsWithTitle('spacecrypto'):
        windows.append({
            "window": w,
            "lessPosition":[],
            "CheckInitialPage":0,
            
            })

    while True:
        now = time.time()
        
        for last in windows:
            if clickBtn(images['spg-connect-wallet'], name='conectBtn', timeout=1):
                time.sleep(2) 
                processLogin() 
            else:
                if len(positions(images['spg-home'], threshold=ct['base_position']))  > 0:
                    removeSpaceships()
                    refreshSpaceships()

            if clickBtn(images['spg-confirm'], name='okBtn', timeout=1):
                time.sleep(2) 
                endFight()

            if clickBtn(images['spg-confirm-victory'], name='okVicBtn', timeout=1):
               pass

            if len(positions(images['spg-processing'], threshold=ct['commom_position'])) > 0:
                time.sleep(ct['check_processing_time']) 
                if len(positions(images['spg-processing'], threshold=ct['commom_position'])) > 0:
                    refreshPage()
                    processLogin()
                

            if len(positions(images['spg-initial-pg'], threshold=ct['commom_position'])) > 0:
                if now - last["CheckInitialPage"] > addRandomness(ct['check_initial_page']):
                    refreshPage()
                    time.sleep(3) 
                    processLogin()
                else:
                    last["CheckInitialPage"] = now
                    pass
        
            checkClose()

             spg_surrender =  positions(images['spg-surrender'], threshold=ct['end_boss'])  
            if len(spg_surrender) > 0:

                cont = ct['check_boss']
                while(cont >0):
                    cont = cont-1
                    nowPosition = lifeBoss()
                    
                    if len(last["lessPosition"]) == 0:
                        if len(nowPosition) > 0:
                            last["lessPosition"] = nowPosition
                            logger("Starting position")
                                                        
                    else:
                        if np.array_equal(nowPosition,last["lessPosition"]) == False:
                            last["lessPosition"] = nowPosition
                            logger("Updating position")
                            break
                        else:
                            if clickBtn(images['spg-confirm'], name='okBtn', timeout=3):
                                time.sleep(2) 
                                endFight()
                                break
                            else:
                                if cont == 0:
                                    logger("End time wait")
                                    endFight()
                                    break
                                else:
                                    logger("Waiting")
                                    last["lessPosition"] = nowPosition
                                    time.sleep(5) 
                            

                    if len(nowPosition) == 0:
                        last["checkBossTime"] = now
                        
            
main()



