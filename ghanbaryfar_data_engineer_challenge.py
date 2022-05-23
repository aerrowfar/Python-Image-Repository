#interactive shell that asks for functions: add, search
from ast import arguments
from asyncore import file_dispatcher
from lib2to3.pytree import Base
from PyInquirer import prompt
import os.path
from os import path
import shutil
import pandas as pd
import json

#workflow of PyInquirer in terminal
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

    #load dataframe of our repository if it previously exists
    df=pd.read_pickle('index')
    print(df)

    #prompt the choices defined above on command line
    choice = prompt(choices)
    arguement = choice.get("arguement")
    option = choice.get("option")

    #go to appropriate function
    if option == 'add':
        add(arguement,df)
    elif option== 'search':
        search(arguement,df)
    else: 
        retrieve(arguement, df)


# add function just moves pic into depository folder and renames it, accepts path. 
# can accept a single path on command line or path to text file with one path per line 

def add(arguement, df):
    #acceptable inputs: 
    #/Directory/to/image.png [tag1,tag2,tag3] Description
    #/Directory/to/images.txt 

    arguement = arguement.split()
    address = arguement[0]


    numeric = str(len(df.index)+1)

    #format includes tags and description.
    if len(arguement)>=3:
        description = arguement[2:]
        description = ' '.join([str(item) for item in description])
        tags=arguement[1]
        df = df.append({'index': numeric, 'tags':tags,'description':description}, ignore_index=True)

    #format only includes tags.
    if len(arguement)==2:
        tags=arguement[1]
        df = df.append({'index': numeric,'tags':tags}, ignore_index=True)

    #format does not include tags or description. 
    if len(arguement)==1:
        #checks to see if its a text file of multiple images.
        if arguement[0][-3:] == 'txt':
            print('recognized text file')
            with open(arguement[0]) as text:
                for line in text:
                    df=pd.read_pickle('index')
                    
                    add(line,df)
        else:
            df = df.append({'index': numeric}, ignore_index=True)
      


    shutil.move(address,'Repository/'+numeric+'.'+address.split('.')[1])

    df.to_pickle('index')

    print(df)
    print('Succesfully added to Repository!')
    

# search function: can search by tags or text. 
# returns a dataframe of image details that match.

def search(arguement,df):
    # acceptable format:
    # {'tags':'query','text':'query','similar':'query'}
    try:
        arguement = json.loads(arguement)
        if 'tag' in arguement:
            print('came here')
            print(arguement['tag'])
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




# Returns copies of all specified image numbers (space seperated) in a new folder 

def retrieve(arguement,df):
    #acceptable input format:
    #  213 23 23 
    arguement = arguement.split()
    print(arguement)
    for item in arguement:
 
        path='Repository/'+item+'.jpg'
        
        out = 'Output'
        
        shutil.copy(path,out)
        print('succesfully outputted image:', path)


if __name__ == "__main__":
    main()