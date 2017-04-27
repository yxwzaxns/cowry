import subprocess

cmd = 'sleep 5;ls l'
completed = subprocess.Popen(cmd, shell=True)
print('returncode:', completed.returncode)
