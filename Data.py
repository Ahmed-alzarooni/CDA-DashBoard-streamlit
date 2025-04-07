import pandas as pd
import numpy as np

# Load the dataset
file_path = 'Dataset/P_Data_Extract_From_World_Development_Indicators.xlsx'
xls = pd.ExcelFile(file_path)
data_df = pd.read_excel(xls, sheet_name='Data')

# Clean up the column names (removing spaces and brackets)
data_df.columns = data_df.columns.str.replace(r"\[|\]", "", regex=True)
data_df.columns = data_df.columns.str.strip()

# Replace '..' with NaN in the dataset
data_df.replace('..', np.nan, inplace=True)

# Optional: Save the cleaned dataset to a new file
output_path = 'Dataset/cleaned_dataset.xlsx'
data_df.to_excel(output_path, index=False)

# Print confirmation
print(f"Dataset cleaned and saved to {output_path}")
#weqwe
