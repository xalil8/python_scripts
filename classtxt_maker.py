import os
#file path
dir = r'C:/Users/halil\Desktop/dataset_v1.3_v3'
m = [i for i in os.walk(dir)]
files = m[0][1]

#txt path to save 
txt_dir = "C:/Users/halil\Desktop/xalil.txt"
with open(txt_dir, 'w') as f:
    for line in files:
        f.write(f"{line}\n")
