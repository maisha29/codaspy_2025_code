import pandas as pd

# Read the CSV file
df = pd.read_csv("Test_Imp_200.csv")

# Separate benign and attack data
benign = df[df["Label"] == 'benign']
attack = df[df["Label"] == 'attack']

# Define the sequences
sequences = [70]

for sequence in sequences:
    test1 = pd.DataFrame()  # Initialize test1 within the loop
   
    # Add the required number of pattern repetitions to the test set
    for i in range(len(df)):
        test1 = pd.concat([test1, benign[:sequence], attack[:sequence]])
        benign = benign[sequence:]
        attack = attack[sequence:]

    # Add the remaining samples to the test set without maintaining the pattern
    remaining_samples = len(df) - len(test1)
    test1 = pd.concat([test1, benign[:remaining_samples], attack[:remaining_samples]])

    # Reset the index of the test set
    test1 = test1.reset_index(drop=True)
    test1.to_csv(f'Imp_new_test_200_on_off_{sequence}.csv', index=False)