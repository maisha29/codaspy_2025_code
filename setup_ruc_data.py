import pandas as pd
import numpy as np
import glob

def calculate_std(column):
    std = column.std()
    return std

def calculate_safe_margins(column, kappa):
    mean = column.mean()
    std = calculate_std(column)
    upper = mean + kappa * std
    lower = mean - kappa * std
    return upper, lower

def calculate_stateless_residuals(column, upper_margin, lower_margin):
    residuals = []
    for i in range(len(column)):
        if column[i] > upper_margin:
            residuals.append(column[i] - upper_margin)
        elif column[i] < lower_margin:
            residuals.append(column[i] - lower_margin)
        else:
            residuals.append(0)
    return residuals


def calculate_RUC(stateless_residuals, F):
    RUC = np.zeros(len(stateless_residuals))
    for i in range(len(stateless_residuals)):
        if i < F-1:
            RUC[i] = 'Nan'
        else:
            RUC[i] = np.sum(stateless_residuals[i-F+1:i+1])
    return RUC

file_list = glob.glob('Test_imp_155*.csv')
frame_lengths = [5,7,9]
kappas = [4,4.3,4.5,4.7,5]

for file in file_list:
    # Load the dataset for the current window length Imp new_test_200_on8_off8
    
    common_params = file.split("Test_imp")[1].split(".csv")[0]
    #filename = f'Imp new_test_{window_length}_{*}.csv'
    df = pd.read_csv(file)
    
    for frame_length in frame_lengths:
        for kappa in kappas:
            
            # Calculate RUC values
            qr = df['Ratio'].values
            upper_margin, lower_margin = calculate_safe_margins(qr, kappa)
            stateless_residuals = calculate_stateless_residuals(qr, upper_margin, lower_margin)
            ruc = calculate_RUC(stateless_residuals, frame_length)
            
            # Save RUC values to file
            RUC = pd.DataFrame({'RUC': ruc})
            
            # Generate output file name
            output_filename = f'RUC_test_imp_f{frame_length}_k{kappa}_155.csv'
            RUC.to_csv(output_filename, index=False)