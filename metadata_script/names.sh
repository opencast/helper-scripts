#!/usr/bin/env python

import random; 

list = open("names.txt", "r")
names = list.readlines()
names = [x.strip() for x in names]
list.close()
print(random.choice(names));