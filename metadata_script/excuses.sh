#!/usr/bin/env python

import random; 

list = open("excuses.txt", "r")
excuses = list.readlines()
excuses = [x.strip() for x in excuses]
list.close()
print(random.choice(excuses));