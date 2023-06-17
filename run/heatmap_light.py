import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import subprocess
import shlex
import csv
import os
from time import sleep


def run(min_freq, max_freq,time):
    date = str(time)
    datetime = date.replace(" ", "_")
    
    filename = str(datetime+"_"+min_freq+"Mhz-"+max_freq+"Mhz.csv")
    filename = filename.replace(":","_")
    sweep = subprocess.call(["./sweep.sh", min_freq, max_freq,filename])
    mv = subprocess.call(["mv",filename, "data/"])



if __name__ == '__main__':
    GNNS_frequencies = {"L1": ("1550","1600"), "L2": ("1210", "1240"), "L5":("1150","1200"), "GL1": ("1580","1620"), "GL2":("1230","1260"), "GL3": ("1190","1220")}
    while True:
        for v in GNNS_frequencies.values():
        	print("scanning from" + v[0] + " MHz to " + v[1] +" MHz ")
        	run(min_freq=v[0], max_freq=v[1],time=datetime.now())
        #print("wainting for next sweep")
        #sleep(600)
