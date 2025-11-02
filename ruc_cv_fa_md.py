import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time



# Load the labeled ratio dataset
ratio_df = pd.read_csv("Test_fuzzy_90.csv")

# Extract the index where the benign data ends
benign_end_index = ratio_df.loc[ratio_df['Label'] == 'attack'].index[0]


# Load the cross-validation dataset
#input_file = input("Enter CSV file for validation data: ")
validation_data = pd.read_csv("RUC_test_f7_k3_90.csv")


# Split the cross-validation dataset into benign and attack parts
benign_data = validation_data.iloc[:benign_end_index]
mask = np.isnan(benign_data )
benign_data  = benign_data [~mask]
attack_data = validation_data.iloc[benign_end_index:]


# Take input for optimal tao value
#opt_tao = float(input("Enter optimal tao value: "))

# Define the weight pairs for false alarm and miss detection
wfa_values = 0.9
wmd_values = 0.1

# Define the candidate tao values for each weight pair
tao_values = np.array([-0.166297651])


# Calculate the false alarm and miss detection rates for each weight pair and tao value
fa_rates = np.zeros_like(tao_values)
md_rates = np.zeros_like(tao_values)
md_values = np.zeros_like(tao_values)

for i in range(len(tao_values)):
  
    tao = tao_values[i]

    # Calculate false alarm rate
    false_alarms = np.sum(benign_data < tao)
    print("false alarm count", false_alarms)
    fa_rate = false_alarms / len(benign_data)
    #print("total benign data:",len(benign_data))
    fa_rates[i] = fa_rate
    print('fa_rates',fa_rates)
    
    # Calculate miss detection rate
    miss_detections = np.sum(attack_data >= tao)
    print('miss_detections count',miss_detections)
    md_rate = miss_detections / len(attack_data)
    #print("total attack data:",len(attack_data))
    md_rates[i] = md_rate
    print('md_rates',md_rates)
    print("\n")

window_length = ratio_df.loc[benign_end_index]['Window length']
fuzzy_raw_file = pd.read_csv('Fuzzy_attack_dataset.csv',names = ['Raw file'])


start_time = time.time()
start_timestamp = fuzzy_raw_file.loc[window_length-90][0]
start = start_timestamp.find(':') + 11  # find the index of the first colon and add 9 to skip over it and the space
end = start_timestamp.find(' ', start)  # find the index of the first space after the start index
start_value = float(start_timestamp[start:end])
#print('Start time:', start_value,'s')

# Find the row index of the first occurrence of the value < opt_tao
row_idx = np.where(attack_data < tao_values)[0][0]
first_attack_value = attack_data.iloc[row_idx]
#print('First attack value:', first_attack_value)
original_index = attack_data.index.copy()
pos = attack_data.index.get_loc(attack_data.index[row_idx])

#Get the original index value at that position
original_pos = original_index[pos]
#print('Original index value at position {}: {}'.format(pos, original_pos))
window_length1 = ratio_df.loc[original_pos, 'Window length']
#print('The last window range:', int(window_length1))
end_timestamp = fuzzy_raw_file.loc[window_length1][0]
start = end_timestamp.find(':') + 11 # find the index of the first colon and add 9 to skip over it and the space
end = end_timestamp.find(' ', start)  # find the index of the first space after the start index
end_value = float(end_timestamp[start:end])

end_time = time.time()

execution_time = end_time - start_time
print("Total execution time:", execution_time, "seconds")

#print('End time:', end_value,'s')

time_to_detection = end_value - start_value
print('Time to detection:', time_to_detection,'s')

