from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

import dino

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('window-size=600x310')

class Agent:
    def __init__(self, number, debug = False):
        self.index = index
        self.debug = debug
        self.dino = Dino()
        self.alive_since = None
        self.died_at = None
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.get('file:///home/kocur4d/projects/dinotrainer/trex/index.html')
        self.document = self.driver.find_element(By.XPATH, '//html')
        sleep(2)

    def start(self):
        self.alive_since = dt.now()
        self.document.send_keys(Keys.SPACE)

        while self.isDead() == False:
            self.react()
            sleep(0.100)

        if(self.debug == True):
            print('Agent ', self.index, ' died, score: ', self.score())

        return {
            score: self.score(),
            index: self.index
        }

    def score(self):
        print(self.alive_since)
        print(self.died_at)
        return (self.died_at - self.alive_since).total_seconds()

    def isDead(self):
        if self.died_at == None:
            if self.driver.execute_script("return Runner.instance_.crashed") == True:
                self.died_at = dt.now()
                return True
            else:
                return False
        else:
            return True

    def react(self):
        X = self.get_data()
        action = self.dino.react(X)
        self.__react(action)

    def get_data(self):
        screenshot = self.__get_screenshot()
        rhdata = screenshot[60:, 45:450]
        rhdata = np.where(rhdata > 0, 1, 0)
        up = rhdata[:25]
        down = rhdata[25:]
        up_sum = np.sum(up,axis=0)
        down_sum = np.sum(down,axis=0)
        return np.append(up_sum, down_sum).reshape((1,810))

    def __react(self, action):
        actions = {
            'down': lambda: self.document.send_keys(Keys.ARROW_DOWN),
            'up': lambda: self.document.send_keys(Keys.SPACE),
        }
        print('action', action)
        callback = actions.get(action, lambda: None)
        callback()

    def __get_screenshot(self):
        data = self.driver.execute_script('return document.getElementsByClassName("runner-canvas")[1].getContext("2d").getImageData(0,0,600,150);')['data']
        a = np.array(data).reshape((90000, 4))
        a = a[:, 2]
        return a.reshape((150, 600))
