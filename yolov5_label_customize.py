import os 
import pandas as pd 

with os.scandir("/Users/halil/Desktop/final") as files:  # from this dir , labels getting
    counter = -1    #for naming txt files going  0 to n 
    for file in files:
        counter += 1
        xalil_name = "label" + str(counter)
        #if file.name.endswith("migros_005.txt" ):  #this line used for testing the scrip, can be removed 
        t = open(file,"r+")
        new_file = open(f"/Users/halil/Desktop/labels/{xalil_name}.txt", "w+")  #new labels writing on this dir 

        for line in t :                
            a = line.split(' ')   #line by line splitting each line elements by space 
            a[0] = "0"             #whatever label is replacing with 0 
            x = ""
            for i in a:
                x += i+" "
            new_file.write(x + '\n')  #writing lines 
        new_file.close()

        
        ////////////////////////////////////
import os
path = '/Users/halil/Desktop/dataset/images2'
files = os.listdir(path)


for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, 'object'.join([str(index), '.png'])))
