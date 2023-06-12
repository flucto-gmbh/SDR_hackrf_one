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

    
    folder = datetime.replace(":", "_") + "-" + min_freq + "MHz-" + max_freq + "MHz"
    filename = str(datetime+".csv")

    dir = subprocess.call(["mkdir","data/"+ folder])
    sweep = subprocess.call(["./sweep.sh", min_freq, max_freq,filename])
    mv = subprocess.call(["mv",filename, "data/" + folder + "/"])

    df = pd.read_csv("data/" + folder+ "/"+ filename)


    first_row = ["timestamp","time", "min","max", "width","num"]
    i = 1
    while i <= len (df.columns) - 6:
        first_row.append("dB" + str(i))
        i += 1

    df.columns  = first_row

    df["timestamp"] = df ["timestamp"] + df["time"]
    del df ["time"]

    list_timestamp = []
    list_frequency = []
    list_val  = []

    i = 0
    while i < df.shape[0]:
        j = 5
        row = list(df.iloc[i])
        current_frequency = round((row[1]/1000000),2) 

        while j < len(df.columns):
            timestamp = row[0]

            list_timestamp.append(timestamp)
            list_frequency.append(current_frequency)
            list_val.append(row[j])
            current_frequency = round(current_frequency + (row[3]/1000000),2)
            j += 1 
        i += 1

    min_freq = str(min(list_frequency))
    max_freq = str((list_frequency[len(list_frequency) -1]))
    new_df = pd.DataFrame({'timestamp': list_timestamp,'frequency': list_frequency, 'val': list_val})
    plot = pd.pivot_table(new_df, index ='timestamp', columns = 'frequency', values = 'val')
    fig, ax = plt.subplots(figsize =(20,8))
    sns.set(font_scale =1.3)
    main_title = 'Frequency Sweep Min' + min_freq + "MHz Max" + max_freq + "MHz"
    sns.heatmap(plot,cmap ='Spectral_r', vmin = -100, vmax = -40, cbar_kws={'label':'Dezibel'}).set(title = main_title)
    plt.xlabel ("Frequency [MHz]")
    plt.ylabel ("Timestamp")
    plt.tight_layout()
    main_title = main_title.replace(" ","_")
    plt.savefig(main_title, format = 'png')
    plt.close(main_title)
    mv = subprocess.call(["mv",main_title,"data/"+ folder + "/"])



if __name__ == '__main__':
    GNNS_frequencies = {"L1": ("1550","1600"), "L2": ("1210", "1240"), "L5":("1150","1200"), "E1": ("1560","1590"), "E5":("1160","1200"), "E6": ("1260","1300")}
    while True:
        for v in GNNS_frequencies.values():
        	print("scanning from" + v[0] + " MHz to " + v[1] +" MHz ")
        	run(min_freq=v[0], max_freq=v[1],time=datetime.now())
        print("wainting for next sweep")
        sleep(600)
