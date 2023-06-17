import subprocess

iterate = subprocess.run('for file in *.csv;do python plot.py $file; done', shell=True)
