# Python-Image-Repository

This is a simple python based image repository that accepts single or list of multiple image locations, their tags, and a description. 
Repository moves the files internally to for organizing and keeps track of all relevant information in a dataframe for easy retrieval. 
Images can be retrieved one or many at a time by their indexed number. 

**Instructions:**

Run the python file on terminal, you will be presented with 3 options: add, search, retrieve. Highlight the desired choice and press enter. 
Then enter the appropriate query and press enter. 

**For Adding**

Acceptable formats for query:
    
    /Directory/to/image.png [tag1,tag2,tag3] Description
    
    /Directory/to/images.txt
    
The text file must follow the same format as the single image upload line by line.


**For Searching**

Acceptable format for query:
    
    {'tags':'query','text':'query'}
    
Any combination of tags or text query can be used. The matching will be based on text containing, not an exact match. I.e "app" will match with "apple".

**For Retrieval**

Acceptable format for query:
    
    213 23 3 
    
Retrieval is based on indexed number for images found through search. One or many numbers can be specified. Relevant images will be copied to 'Output' folder in local directory.
Originals will be kept in repository. 


    
