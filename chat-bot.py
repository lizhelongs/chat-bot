# -*- coding: utf-8 -*-
from helper import extractName, Interpreter

interpreter = Interpreter()
def intent(message):
    global interpreter
    data = interpreter.parse(message)
    return data["intent"]["name"]

print("BOT: Hi! I'm Albert, a chat-bot designed to help you search for real-time information. What Can I do for you today?")
# Define chitchat_response()
def chitchat_response(message):
    # Call match_rule()
    response, var = match_rule(rules, message)
    # Return none is response is "default"
    if response == "default":
        return None
    if '{0}' in response:
        # Replace the pronouns of phrase
        phrase = replace_pronouns(message)
        # Calculate the response
        response = response.format(phrase)
    return response

import re
import random

def match_rule(rules, message):
    for pattern, responses in rules.items():
        match = re.search(pattern, message)
        if match is not None:
            response = random.choice(responses)
            var = match.group(1) if '{0}' in response else None
            return response, var
    return "default", None

rules = {'if (.*)': ["Do you really think it's likely that {0}", 'Do you wish that {0}', 'What do you think about {0}', 'Really--if {0}'], 'do you think (.*)': ['if {0}? Absolutely.', 'No chance'], 'I want (.*)': ['What would it mean if you got {0}', 'Why do you want {0}', "What's stopping you from getting {0}"], 'do you remember (.*)': ['Did you think I would forget {0}', "Why haven't you been able to forget {0}", 'What about {0}', 'Yes .. and?']}

def replace_pronouns(message):

    message = message.lower()
    if 'me' in message:
        return re.sub('me', 'you', message)
    if 'i' in message:
        return re.sub('i', 'you', message)
    elif 'my' in message:
        return re.sub('my', 'your', message)
    elif 'your' in message:
        return re.sub('your', 'my', message)
    elif 'you' in message:
        return re.sub('you', 'me', message)

    return message

# Define the states
INIT=0
AUTHED=1
CHOOSE_STOCK=2
CHOOSE_ATTR=3
SEARCHED=4
END=5

# Define the policy rules
policy_rules = {
    (INIT, "check"): (INIT, "Sure, I'm good at searching stocks. You'll have to log in first before searching, what's your phone number?", AUTHED),
    (INIT, "number"): (AUTHED, "Perfect, welcome back!", None),
    (AUTHED, "check"): (CHOOSE_STOCK, "Which stock are you interested in?", None),
    (CHOOSE_STOCK, "specify_stock"): (CHOOSE_ATTR, "What kind of information are you interested with this stock?", None),     
    (CHOOSE_ATTR, "specify_attr"): (SEARCHED, "What else do you want to know about this stock?", None),
    (SEARCHED, "specify_attr"): (SEARCHED, "What else do you want to know about this stock?", None),
    (SEARCHED, "end"): (END, "Glad to help you, have a great day!", None)
}




import string

stock_name = ""
specify_attr = False

def interpret(state, message):
    msg = message.lower()
    if 'search' in msg or 'find' in msg or 'look' in msg:
        return 'check'
    if state == CHOOSE_ATTR or state == SEARCHED:
        global specify_attr
        if specify_attr == True:
            return 'specify_attr'
    #print(message)
    #print(extractName(message))
    if extractName(message) is not None:
        global stock_name
        stock_name = extractName(message)
        return "specify_stock"
    if any([d in msg for d in string.digits]):
        return 'number'
    if re.search(r'\bno\b',msg) or re.search(r'\bend\b',msg):
        return 'end'
    return 'none'

from iexfinance.stocks import Stock
def get_info(name, attr):
    stock = Stock(name, token = "pk_a8f5744d18b5476ebbdf61ea35762825")
    if attr is None:
        return stock.get_quote()
    #aapl.get_quote()
    return stock.get_quote()[attr]



def respond(name, message):
    match = re.search("its (.*)", message)
    if match is not None:
        # Choose a random response
        response = "Its "
        phrase = match.group(1)
    # Return the response and phrase
    attr = intent(phrase)
    info = str(get_info(str(name), str(attr)))
    return response + phrase + " is " + info

# Define send_message()
def send_message(state, pending, message):
    global stock_name, specify_attr
    print("USER : {}".format(message))
    response = chitchat_response(message)
    if response is not None:
        print("BOT : {}".format(response))
        return state, None
    if state == CHOOSE_ATTR or (state == SEARCHED and interpret(state, message) != 'end'):
        try: 
            response = respond(stock_name, message)
            print("BOT : {}".format(response))
            specify_attr = True
        except:
            print("Wrong stock name, make sure the name is correct beofre you enter and try again!")
            return state, None
    # Calculate the new_state, response, and pending_state
    if interpret(state, message) == 'none':
        print("BOT : Sorry, I can't understand you, please make sure you enter the right message!")
        return state, None
    new_state, response, pending_state = policy_rules[(state, interpret(state, message))]
    specify_attr = False
    print("BOT : {}".format(response))
    if pending is not None:
        new_state, response, pending_state = policy_rules[pending]
        pending = None
        print("BOT : {}".format(response))        
    if pending_state is not None:
        pending = (pending_state, interpret(state, message))
    return new_state, pending

# Define send_messages()
def send_messages(messages):
    state = INIT
    pending = None
    for msg in messages:
        state, pending = send_message(state, pending, msg)

# Send the messages
send_messages([
    "I'd like to search for some information about trade stocks",
    "555-12345",
    "do you remember when I SEARCHED 1000 kilos by accident?",
    "awdad",
    "TSLA, please",
    "I would like to know its highest daily price",
    "And its lowest price during the last 52 week",
    "No, thanks"
])