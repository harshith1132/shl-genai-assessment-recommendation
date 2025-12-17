import pandas as pd

# Load Excel file
file_path = "datasets/Gen_AI Dataset.xlsx"

xls = pd.ExcelFile(file_path)

print("Sheets found:", xls.sheet_names)

# Load train and test sheets (adjust names if needed)
train_df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
test_df = pd.read_excel(xls, sheet_name=xls.sheet_names[1])

print("\nTrain data preview:")
print(train_df.head())

print("\nTest data preview:")
print(test_df.head())
