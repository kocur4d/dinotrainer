import os
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep
from datetime import datetime as dt

from dino import Dino

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1200x630')

class Agent:
    def __init__(self, index, debug = False):
        self.index = index
        self.debug = debug
        self.alive_since = None
        self.died_at = None
        self.dino = Dino()

    def setup(self):
        self.dino.setup()
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.get('file:///Users/lukaszskrzeszewski/projects/venv3.7/dinotrainer/trex/index.html')
        self.document = self.driver.find_element(By.XPATH, '//html')

    def start(self):
        self.setup()
        self.alive_since = dt.now()
        #self.document.send_keys(Keys.SPACE)

        while self.isDead() == False:
            self.react()
            sleep(0.1)

        if(self.debug == True):
            print('Agent ', self.index, ' died, score: ', self.score())

        return {
            'score': self.score(),
            'index': self.index
        }

    def score(self):
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
        self.document.send_keys(Keys.SPACE)
        screenshot = self.get_screenshot()
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

    def get_screenshot(self):
        data = self.driver.execute_script('return Runner.instance_.canvasCtx.getImageData(0,0,150,600)')['data']
        #data = self.driver.execute_script('return document.getElementsByClassName("runner-canvas")[0].getContext("2d").getImageData(0,0,600,150);')['data']
        #a = np.array(data).reshape((90000, 4))
        #a = a[:, 2]
        a = data[0::4]
        b = np.reshape(a, (150, 600))
        #self.driver.save_screenshot(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.', 'screenshot.png'))
        save_file = os.path.join(os.getcwd(), "data.png")
        fig = plt.figure(figsize=(4, 5))
        plt.imshow(b, interpolation='nearest')
        plt.savefig(save_file)
        plt.close(fig)
        return b

    def test(self):
        data = self.driver.execute_script('return document.getElementsByClassName("runner-canvas")[0].getContext("2d").getImageData(0,0,600,150);')['data']
        a = np.array(data).reshape((90000, 4))
        a = a[:, 0]
        b = a.reshape((150, 600))
        fig = plt.figure(figsize=(4, 5))
        plt.imshow(b, interpolation='nearest')
        plt.savefig(save_file)
        plt.close(fig)
        self.driver.save_screenshot(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.', 'ss.png'))
        data = self.driver.execute_script('return document.getElementsByClassName("runner-canvas")[0].toDataURL("image/png");')
        print('Canvas length: ', data)
        return b

if __name__ == "__main__":
    agent = Agent(1)
    agent.setup()
    agent.get_screenshot()
