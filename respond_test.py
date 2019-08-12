# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 18:21:31 2019

@author: Administrator
"""
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

def Interpreter():
    # Create a trainer that uses this config
    trainer = Trainer(config.load("config_spacy.yml"))
    
    # Load the training data
    training_data = load_data('demo-stock.json')
    
    # Create an interpreter by training the model
    interpreter = trainer.train(training_data)
    return interpreter

def intent(message):
    interpreter = Interpreter()
    data = interpreter.parse(message)
    return data["intent"]["name"]

from iexfinance.stocks import Stock
def get_info(name, attr):
    stock = Stock(name, token = "pk_a8f5744d18b5476ebbdf61ea35762825")
    if attr is None:
        return stock.get_quote()
    #aapl.get_quote()
    return stock.get_quote()[attr]


import re
def respond(name, message):
    match = re.search("its (.*)", message)
    if match is not None:
        # Choose a random response
        response = "Its "
        phrase = match.group(1)
    # Return the response and phrase
    attr = intent(phrase)
    info = str(get_info(name,attr))
    return response + phrase + " is " + info
print("end" == 'end')
#print(respond("TSLA","And its lowest price during the last 52 week"))