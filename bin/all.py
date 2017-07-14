#!/usr/local/bin/python3

import time
datetime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
f = open (r'/a-fund/bin/autorun.log','a')
print (datetime+' autorun successful',file = f)
f.close()

import os
os.system("python3 /a-fund/fetch/fetch.py")
os.system("python3 /a-fund/process/process_db.py")