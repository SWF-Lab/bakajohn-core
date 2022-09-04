from os import listdir
from os.path import isfile, join
import os
import json

onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]

print(onlyfiles)

for file in onlyfiles:
    if(file[-3:] == '.py'):
        continue
    print(file)
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        num = data['name'][-3:]
        data['image'] = "https://ipfs.io/ipfs/QmS83ES9NEpqsAQxx6cAA1VK4JeLEmTndHs49sCy3bu1i2/BAKAJOHN#" + num + "A.png"
        print(data['image'])

    with open(file, 'w') as json_file:
        json.dump(data, json_file)