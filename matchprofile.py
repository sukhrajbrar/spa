import string
import secrets
from struct import *
import os
import time
print(os.getcwd())
f=open('knockknock/servertimefile.txt', 'w')
f.write(str(time.time_ns()))
f.close()
