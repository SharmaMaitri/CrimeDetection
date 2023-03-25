# Importing the pandas package.
import pandas as pd
def processdata():
    # Loading and reading the CSV file.
    df = pd.read_csv(f'C:\\Users\\Admin\\Downloads\\archive\\chipotle_stores.csv', delimiter = ',')
    # Converting the CSV data to a list.
    df = df.to_dict(orient = 'records')
    print(df)
    return df