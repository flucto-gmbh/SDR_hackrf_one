import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import subprocess
import shlex
import csv
import os
from time import sleep
import sys

filename = sys.argv[1]
print(filename)
print(type(filename))
df = pd.read_csv(filename)
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

new_df = pd.DataFrame({'timestamp': list_timestamp,'frequency': list_frequency, 'val': list_val})
plot = pd.pivot_table(new_df, index ='timestamp', columns = 'frequency', values = 'val')
fig, ax = plt.subplots(figsize =(20,8))
sns.set(font_scale =1.3)
filename = filename.replace(".csv","")
main_title = filename + "Frequency Sweep"
sns.heatmap(plot,cmap ='Spectral_r', vmin = -100, vmax = -40, cbar_kws={'label':'Dezibel'}).set(title = main_title)
plt.xlabel ("Frequency [MHz]")
plt.ylabel ("Timestamp")
plt.tight_layout()
main_title = main_title.replace(" ","_")
plt.savefig(main_title, format = 'png')
plt.close(main_title)
