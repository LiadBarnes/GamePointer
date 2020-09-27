import time

from classes import Myjson, tennis_game, stick_game, check_mouse
import pyautogui
#check_mouse()
# line_up = 'Volley'
# tennis_Player = tennis_game(line_up)
#
# tennis_Player.listener()


# stick_fight_Player = stick_game()
# Keyboard = Myjson('jsons/StickFight/Keyboard.json').get()
#
# stick_fight_Player.listener(Keyboard)

def bug_exploiter():
    while True:
        # 140 540 enter game
        pyautogui.moveTo(140, 540)
        pyautogui.click()
        time.sleep(10)

        # 510 365 Play game
        pyautogui.moveTo(510, 365)
        pyautogui.click()
        time.sleep(3)

        # 980 80 enter mailbox
        pyautogui.moveTo(980, 80)
        pyautogui.click()
        time.sleep(2)

        # 510 360 Claim
        pyautogui.moveTo(510, 360)
        pyautogui.click()
        time.sleep(1)

        # 575 555 screens
        pyautogui.moveTo(575, 555)
        pyautogui.click()
        time.sleep(2)

        # 650 165 close
        pyautogui.moveTo(650, 165)
        pyautogui.click()
        time.sleep(2)

