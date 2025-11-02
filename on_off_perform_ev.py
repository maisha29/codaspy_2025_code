import numpy as np
import pandas as pd
import glob

# List of file paths for ratio files
ratio_files = glob.glob("Fuzzy new_test_90_on_off*.csv")


# Load the cross-validation dataset
# input_file = input("Enter CSV file for validation data: ")
validation_files = glob.glob("RUC_fuzzytest_f7_k3_90_on_off*.csv")

for file in ratio_files:
        #print(file)
        
        # Extract the common parameters from the ratio file name
        common_params = file.split("Fuzzy new_test_")[1].split(".csv")[0]
        
        # Find the corresponding validation file
        matching_validation_file = None #This variable will store the path of the matching validation file.
        for validation_file in validation_files:
            if common_params in validation_file:
                matching_validation_file = validation_file
                break
    
        if matching_validation_file is not None:
            print(matching_validation_file,":")
            validation_data = pd.read_csv(matching_validation_file)
            ratio_df = pd.read_csv(file)
            label = ratio_df["Label"]
            validation_data["Label"] = label
            
            # Modify labels based on fl value
            fl = 7
            try:
                for index, row in validation_data.iterrows():
                    if row["Label"] == "attack" and validation_data.loc[index + 1, "Label"] == "benign":
                        for i in range(index+1, index+ fl):  # Set label "attack" for the next 9 rows
                            validation_data.at[i, "Label"] = "attack"
            
            except:
                pass

            benign_data = validation_data[validation_data["Label"] == 'benign'].RUC
            mask = np.isnan(benign_data)
            benign_data = benign_data[~mask]
            attack_data = validation_data[validation_data["Label"] == 'attack'].RUC

            tao = -0.166297651
            
            # Calculate false alarm rate
            false_alarms = np.sum(benign_data < tao)
            print("false alarm count", false_alarms)
            fa_rate = false_alarms / len(benign_data)
            #print("total benign data:",len(benign_data))
            #fa_rates[i] = fa_rate
            print('fa_rates',fa_rate)
    
            # Calculate miss detection rate
            miss_detections = np.sum(attack_data >= tao)
            print('miss_detections count',miss_detections)
            md_rate = miss_detections / len(attack_data)
            #print("total attack data:",len(attack_data))
            #md_rates[i] = md_rate
            print('md_rates',md_rate)
            #print("\n")


            # Find the row index of the first occurrence of the value < opt_tao
            row_idx = np.where(attack_data < tao)[0][0]
            original_index = attack_data.index.copy()
            pos = attack_data.index.get_loc(attack_data.index[row_idx])
            #Get the original index value at that position
            original_pos = original_index[pos]
            #print("index of first detection:", original_pos)
            first_attack_value = attack_data.iloc[row_idx]
            #print('First attack value:', first_attack_value)

            raw_file = pd.read_csv('Fuzzy_attack_dataset.csv',names = ['Raw file'])

            #fecth the index of first attack value from the dataset
            initial_pos = ratio_df.loc[ratio_df['Label'] == 'attack'].index[0]
            window_length1 = ratio_df.loc[initial_pos, 'Window length']
            start_timestamp = raw_file.loc[window_length1-90][0]
            start = start_timestamp.find(':') + 11  # find the index of the first colon and add 9 to skip over it and the space
            end = start_timestamp.find(' ', start)  # find the index of the first space after the start index
            start_value = float(start_timestamp[start:end])
            #print('Start time:', start_value,'s')


            window_length = ratio_df.loc[original_pos]['Window length']
            #print('The attack window range:', int(window_length))

            end_timestamp = raw_file.loc[window_length][0]
            start = end_timestamp.find(':') + 11 # find the index of the first colon and add 9 to skip over it and the space
            end = end_timestamp.find(' ', start)  # find the index of the first space after the start index
            end_value = float(end_timestamp[start:end])
            #print('End time:', end_value,'s')

            time_to_detection = end_value - start_value
            print('Time to detection:', time_to_detection,'s')
            print("\n")

        else:
            print("No matching validation file found for", file)
