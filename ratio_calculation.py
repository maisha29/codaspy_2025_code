import pandas as pd
import numpy as np


dosoff1 = pd.read_csv('Attack_free_all_IDs.csv')

#fetch the last value of the column
last_value = dosoff1.iloc[-1]['data_counter']

bins = []
for i in range(0,last_value,155):
    if i>0:
        n = i+1
    else: 
        n = i
    bins.append(n)
#print(bins)

#grouping of counter
for i in range(0,len(bins)-1):
    lowervalue = bins[i]
    uppervalue = bins[i+1]
    dosoff1.loc[(dosoff1['data_counter'] >= lowervalue) & (dosoff1['data_counter'] < uppervalue), 'Window length'] = uppervalue
      
    

#calculating ratio for each group
grouped = dosoff1.groupby("Window length")
hmean = grouped["time_interval"].apply(lambda x: 1 / np.mean(1 / x[x > 0]) if x[x > 0].size > 1 else np.nan)
mean = grouped["time_interval"].mean()
ratio = hmean / mean
ratio = ratio.apply(lambda x: 'null' if np.isnan(x) else x)
last_timestamps = grouped['data_frame_timestamp'].last()

# creating a new Dataframe with the ratio and last timestamp columns
combined_df = pd.DataFrame({'Ratio': ratio, 'data_frame_timestamp': last_timestamps})

file_to_save = 'AF_all_ID_grouped155.csv'
combined_df.to_csv(file_to_save)


filename = pd.read_csv('AF_all_ID_grouped155.csv')

filename.dropna(inplace=True)

window = []

for i in range(0,len(filename)):
    if i>=0:
        n = i+1
    else: 
        n = i
    window.append(n) 
filename['Window']= window

filename.to_csv("AF_all_ID_grouped155.csv", index=False)
print('Finished')
