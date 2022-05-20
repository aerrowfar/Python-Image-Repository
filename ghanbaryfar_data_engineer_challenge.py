#interactive shell that asks for functions: add, search
from ast import arguments
from asyncore import file_dispatcher
from lib2to3.pytree import Base
from PyInquirer import prompt
import os.path
from os import path
import shutil
import pandas as pd
#import pickle
import json
#import glob

choices = [
    {
        'type':'list',
        'name':'option',
        'message':'Python Image Repository',
        'choices':['add','search','retrieve']
    
    },
    {
        'type':'input',
        'name':'arguement',
        'message':'Type in path to image or list of images, query, or retrieval number(s):'
    
    }
]

def main():

    if not path.exists('Repository'):
        os.mkdir('Repository')
    
    if not path.exists('Output'):
        os.mkdir('Output')

    if not path.exists('index'):
        df=pd.DataFrame(columns=['index','tags','description','image_hash'])
        df.to_pickle('index')

    df=pd.read_pickle('index')
    print(df)

    choice = prompt(choices)
    arguement = choice.get("arguement")
    option = choice.get("option")

    if option == 'add':
        add(arguement,df)
    elif option== 'search':
        search(arguement,df)
    else: 
        retrieve(arguement, df)


# acceptable inputs:
# /Desktop/image.png [tag1,tag2,tag3] Description
# /Desktop/images.txt  #where each line follows the above format

# {'tags':'','text':'','similar':''}

#  213 23 23 


# add function just moves pic into depository folder and renames it, accepts path. 
# can accept a single path on command line or path to text file with one path per line 

def add(arguement, df):
    
    arguement = arguement.split()
    address = arguement[0]
    #print(address)

    numeric = str(len(df.index)+1)

    if len(arguement)>=3:
        description = arguement[2:]
        description = ' '.join([str(item) for item in description])
        tags=arguement[1]
        df = df.append({'index': numeric, 'tags':tags,'description':description}, ignore_index=True)
        #print(description)
        #print(df)

    
    if len(arguement)==2:
        tags=arguement[1]
        df = df.append({'index': numeric,'tags':tags}, ignore_index=True)
        #print(tags)
        #print(df)
    
    if len(arguement)==1:
        #print(arguement[0])
        #print(arguement[0][-3:])
        if arguement[0][-3:] == 'txt':
            print('recognized text file')
            with open(arguement[0]) as text:
                #print(arguement[0])
                for line in text:
                    #print(line)
                    df=pd.read_pickle('index')
                    
                    add(line,df)
        else:
            df = df.append({'index': numeric}, ignore_index=True)
        #print(df)


    shutil.move(address,'Repository/'+numeric+'.'+address.split('.')[1])

    df.to_pickle('index')

    print(df)
    print('Succesfully added to Repository!')
    

# search function: can search by tags, text, or another image path. 
# returns a dataframe of image details

def search(arguement,df):
    try:
        arguement = json.loads(arguement)
        if 'tag' in arguement:
            print('came here')
            print(arguement['tag'])
            #print(df.loc[df])
            df2= df.loc[df['tags'].str.contains(arguement['tag'], case=False)]
            print(df2)
        if 'description' in arguement:
            df3= df.loc[df['description'].str.contains(arguement['description'], case=False)]
            print(df3)
        if not 'tag' in arguement and (not 'description' in arguement):
            print('No valid search criteria provided.')
    
    except BaseException as err:
        print('Not a valid search query!')
        print(err)



# can choose which ones on command prompt, comma seperated
# returns copies of all relevant images in a new folder 

def retrieve(arguement,df):
    
    arguement = arguement.split()
    print(arguement)
    for item in arguement:
        '''
        print(item)
        path='/Repository/'+item+'.???'
        print(path)
        print(glob.glob(glob.escape(path)))
        print(glob.glob(path))
        for filename in glob.glob(path):
            print(filename)
            shutil.copy(filename,'/Output')
            print('succesfully outputted image:', filename)
        '''
        path='Repository/'+item+'.jpg'
        
        out = 'Output'
        
        shutil.copy(path,out)
        print('succesfully outputted image:', path)


if __name__ == "__main__":
    main()