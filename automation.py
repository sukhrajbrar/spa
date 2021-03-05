import sys, time
import subprocess

for i in range(30):
    command = 'sudo knockknock -p 34 spaserver'
    subprocess.run(command.split(), shell=false)
    time.sleep(30)

print("30 iterations done")    
