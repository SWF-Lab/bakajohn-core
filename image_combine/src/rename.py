from os import listdir
from os.path import isfile, join
import os

onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]

count = 0
for file in onlyfiles:
    if(file[-4:] == '.png'):
        count += 1
        if(file[-5] == 'A'):
            new_name = 'John'
        elif(file[-5] == 'B'):
            new_name = 'Mad John'
        elif(file[-5] == 'C'):
            new_name = 'BAKAJOHN'
        
        num = int(file[:-5])
        num = format(num, '03d')
        new_name = new_name + ' #' + num + '.png'
        os.rename(file, new_name)

print(count)
