import pandas as pd


# Read the CSV file into a DataFrame with one column
df = pd.read_csv('Impersonation_attack_dataset.csv', header=None, names=['Raw'])

# Extract information using regular expressions
df = df['Raw'].str.extract(r'Timestamp:\s+([\d.]+)\s+ID:\s+(\S+)\s+(\S+)?\s+DLC:\s+(\d+)(?:\s+([\da-f\s]+))?')

# Rename columns
df.columns = ["Timestamp", "ID", "RTR", "DLC", "Payload"]

# Display the resulting DataFrame
#print(df)

# Calculate row count between occurrences of RTR = 100 and RTR = 000 for each unique ID

unique_ids = df["ID"].unique()
offset_data = []

for target_id in unique_ids:
    # Filter rows for the target ID
    #target_id = '0153'
    id_rows = df[df["ID"] == target_id]
    print(id_rows)

    # Find indices where RTR transitions from 100 to 000
    indices_100 = id_rows.index[id_rows["RTR"] == "100"]
    #print(indices_100)
    indices_000 = id_rows.index[id_rows["RTR"] == "000"]

    # Calculate the offset for each occurrence of RTR = 100
    for idx_100 in indices_100:
        # Find the nearest index where RTR = 000
        idx_000 = min(indices_000[indices_000 > idx_100], default=-1)
        #print(idx_000)
        # Calculate the offset
        if idx_000 != -1:
            #print("Valid Pair:")
            #print(id_rows.loc[idx_100:idx_000])
            offset = idx_000 - idx_100
            # Get the payload corresponding to RTR = 000
            payload_dataframe = id_rows.loc[idx_000, "Payload"] #if idx_000 < len(id_rows) else None
            offset_data.append((target_id, offset, payload_dataframe))

# Create a DataFrame from the collected data
offset_df = pd.DataFrame(offset_data, columns=["ID", "Imp Offset", "Dataframe_Payload"])

# Save the DataFrame to a CSV file
offset_df.to_csv('imp_offset_results.csv', index=False)

