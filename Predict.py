# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 18:44:12 2019

@author: admin
"""

def outputJson(input_file_path, output_file_path):
# ## Using the model
# ### STEP1: Reading a json file
    print("yoyo")
    import json
    import spacy
    with open(input_file_path,"r") as read_file:
        data = json.load(read_file)
    
    # ### STEP2: Processing the json to get csv
    myData=[]
    for document in data:
        text=document['text']
        H0=document['H0']
        H1=document['H1']
        i=0
        sentence=""
        categ="None"
        entities=[]
        while(i<len(text)):
            if(len(sentence)==0):
                start_index=0
            else:
                start_index=len(sentence)
            if(H0[i]==1):
                entities.append([start_index,start_index+len(text[i])-1,"H0"])
                if(categ!="H0"):
                    #categ='Priv'
                    categ='H0'
            if(H1[i]==1 and H0[i]==0):
                entities.append([start_index,start_index+len(text[i]),"H1"])
                if(categ!="H1" and categ!="H0"):
                    #categ='Priv'
                    categ='H1'
            sentence=sentence+text[i]+" "
            if('.' in text[i]):
                myData.append([sentence,categ,entities])
                sentence=""
                categ="None"
                entities=[]
            i+=1


    # ### STEP3: Writing into a csv file
    import pandas as pd
    my_df = pd.DataFrame(myData)
    my_df.columns=['Sentence', 'Category', 'Spacy']
    my_df.to_csv('Test/test.csv', index=False)


    # ## Using Spacy to find entities
    #Loading Spacy inbuilt model and our model
    
    output_dir="Spacy_Model"
    print(output_dir)
    nlp2 = spacy.load(output_dir)
    nlp = spacy.load("en_core_web_sm")
    import string
    table = str.maketrans(dict.fromkeys(string.punctuation)) #Used to remove the punctuations

    # Spacy prebuilt model's entities
    #NORP: Nationalities or religious or political groups. ---- H1
    #PERSON: People, including fictional ------ H0
    
    #Read the csv file
    data = pd.read_csv("Test/test.csv", index_col=False)

    #Predicting Output and storing in json format
    #final_output=[]
    dictText={}
    dictText['text']=[]
    dictText['H0']=[]
    dictText['H1']=[]
    for index, row in data.iterrows():
        sent_mymodel = nlp2(row['Sentence'])
        sent_inbuilt=nlp(row['Sentence'])
        entities=[]
        for ent in sent_inbuilt.ents:
            if(ent.label_=='PERSON'):
                #print(ent.text, ent.start_char, ent.end_char, ent.label_)
                entities.append([ent,'H0'])
            elif( ent.label_=='NORP'):
                entities.append([ent,'H1'])
                #print([ent,'H1'])
        for ent in sent_mymodel.ents:
            #print(ent.text, ent.start_char, ent.end_char, ent.label_)
            entities.append([ent,ent.label_])
        #print(row['Sentence'])
        words= row['Sentence'].split(" ")
        for word in words:
            dictText['text'].append(word)
            entity_name=None
            #count=0
            for entity in entities:
                #print(word.translate(table))
                #print(entity[0])
                #print(word.translate(table) in str(entity[0]))
                #print("For word:{0}, check entity:{1}, status:{2}".format(word, entity[0], word.translate(table) in str(entity[0])))
                if(word.translate(table) in str(entity[0])):
                    entity_name=str(entity[1])
                    #print("Word:{0}, EntityName:{1}".format(word,entity[1])) 
                    break
                    
            if(entity_name!=None):
                if(entity_name=='H0'):
                    dictText['H0'].append(1)
                else:
                    dictText['H0'].append(0)
                dictText['H1'].append(1)
            else:
                dictText['H0'].append(0)
                dictText['H1'].append(0)

    #Writing json
    import json
    with open(output_file_path, 'w') as outfile:
        json.dump(dictText, outfile)
        
        
        
        
        
        
        
outputJson("D:/Berkeley/1stSem/290/Project/Privacy_redaction/Test/Doc4.json","D:/Berkeley/1stSem/290/Project/Privacy_redaction/Test/Doc4_output.json")