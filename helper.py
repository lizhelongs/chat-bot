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



import spacy
nlp = spacy.load("en")

def extractName(message):
    ents = {'ORG':None}
    # Create a spacy document
    doc = nlp(message)
    for ent in doc.ents:
        #if ents[ent.label_] is None:
            ents[ent.label_] = ent
        #else:
         #   temp = []
          #  temp.extend(ents[ent.label_])
           # temp.append(ent)
            #ents[ent.label_] = temp
    return ents['ORG']



#print(extractName("I want to search for TSLA instead of ISRG now"))
#print(type(extractName("I changed for searching about JD now")))

    

