import pandas as pd
import os

def convert_xlsx_to_csv(folder_path):
    """Converts all XLSX files in the given folder to CSV files, excluding 'Placement-Record-Overall.csv'."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx'):
            year = file_name.split('-')[-1].replace('.xlsx', '')
            # Exclude 'Placement-Record-Overall.xlsx' by checking its name
            if file_name == 'Placement-Record-Overall.xlsx':
                print(f"Skipping {file_name}")
                continue

            df = pd.read_excel(os.path.join(folder_path, file_name))
            df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names

            # Convert and save CSV file
            csv_file_name = f'Placement-Record-{year}.csv'
            df.to_csv(os.path.join(folder_path, csv_file_name), index=False)
            print(f"Converted {file_name} to {csv_file_name}")

def load_placement_data(folder_path):
    """Loads placement data from CSV files and aggregates company counts by year, excluding 'Placement-Record-Overall.csv'."""
    company_counts = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            # Exclude 'Placement-Record-Overall.csv' by checking its name
            if file_name == 'Placement-Record-Overall.csv':
                print(f"Skipping {file_name}")
                continue

            year = file_name.split('-')[-1].replace('.csv', '')
            df = pd.read_csv(os.path.join(folder_path, file_name))

            # Count the number of rows which should correspond to the number of companies
            company_count = len(df)
            company_counts[year] = company_count

    return company_counts
