#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 19:40:59 2019

Ananda Chatbot

@author: lypzis
"""

#Imports
import time
import os

from selenium import webdriver #automation library
from selenium.webdriver.common.keys import Keys #keys duh
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

#Instantiate chatbot
chatbot = ChatBot("Ananda")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.portuguese")
trainerer = ListTrainer(chatbot)

#Folder to store 
dir_path = os.getcwd()

#Start Applications
driver = webdriver.Chrome(dir_path+'/chromedriver')
#driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(15)

#Basic communication function
def getTalk():
    try:
        post = driver.find_elements_by_class_name("_12pGw")
        last = len(post) - 1
        text = post[last].find_elements_by_css_selector("span.selectable-text").text
        return text
    except:
        pass
         
def sendMessage(message):
    text_box = driver.find_elements_by_class_name("_3u328") #hardcoded !
    value = "*Ananda:* "+str(message)
    
    for part in value.split("\n"): #at each new line '\n'
        text_box.send_keys(part)
        ActionChains(driver).key_down(keys.SHIFT).key_down(keys.ENTER).key_up(keys.SHIFT).perform()
        
    time.sleep(0.5) #waiting for next action
    button_send = driver.find_elements_by_class_name('_3M-N-')
    button_send.click()
    
# this should be disabled in production
def train(message):
    answer = 'Como respondo isso? me ensina por favor...? utilize ;"'+str(message)+'"'
    sendMessage(answer)
    new = []
    try:
        while True:
            last = getTalk()
            if last == "!": #break the loop
                sendMessage("Você desativou meu aprendizado.")
                break
            elif last.replace(';', '') != '' and last != message and last[0] == ';': #avoid taking useless information
                temp = last
                print(message.lower().strip())
                print(last.replace(';', '').lower().strip())
                new.append(message.lower().strip())
                new.append(last.replace(';','').lower().strip())
                trainerer.train(new)
                sendMessage("Pronto, aprendi! Obrigrada <3")
                break
    except:
        pass