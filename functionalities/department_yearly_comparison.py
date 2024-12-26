import pandas as pd
import os
from dash import dcc, html
import plotly.express as px

def load_yearly_data(data_folder, year):
    """Loads and cleans placement data for a specific year."""
    csv_file = f'Placement-Record-{year}.csv'
    file_path = os.path.join(data_folder, csv_file)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if file not found

    df = pd.read_csv(file_path)
    # Normalize column names
    df.columns = df.columns.str.replace(r'\s+', ' ', regex=True).str.strip()
    return df
    
def department_yearly_comparison(data_folder, department, years):
    """
    Compares placement data for a specific department across multiple years.

    Parameters:
        data_folder (str): Folder containing placement data CSV files.
        department (str): Department to analyze.
        years (list): List of years for comparison.

    Returns:
        dash.html.Details: Expandable layout with a line chart comparison.
    """
    department_column_map = {
        'CST': ['CST', 'CST.1'], 'ETC': ['ETC', 'ETC.1'], 'EE': ['EE', 'EE.1'],
        'IT': ['IT', 'IT.1'], 'ME': ['ME', 'ME.1'], 'CE': ['CE', 'CE.1','CE.2'], 'MET': ['MET','MET.1','MET.2'], 'MIN':['MIN','MIN.1'] , 'ARC':['ARC','ARC.1'], 'AERO':['AERO','AERO.1'], 'Geo Informatics':['Geo Informatics'],'VLSI':['VLSI'],'Mat Science':['Mat Science'],'Mechatronics':['Mechatronics'],'Food Proc.':['Food Proc.'],'REST':['REST'],'Bio-MedIcal':['Bio-MedIcal'],'Safety':['Safety'],'Phys':['Phys'],'Mths':['Mths'],'Chem':['Chem'],'MBA':['MBA'],'Earth Science':['Earth Science']
        # Add other departments as needed...
    }
    
    department_columns = department_column_map.get(department)
    if not department_columns:
        raise ValueError(f"Department '{department}' not found in the dataset.")

    comparison_data = []

    for year in years:
        df = load_yearly_data(data_folder, year)
        if df.empty:
            print(f"No data found for year {year}. Skipping...")
            continue

        # Debug: Check available columns
        print(f"Columns in {year}: {list(df.columns)}")

        annual_ctc_col = 'Annual CTC Offered'
        company_name_col = 'Company Visited'

        if all(col in df.columns for col in department_columns + [annual_ctc_col, company_name_col]):
            # Convert relevant columns to numeric
            for col in department_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            df[annual_ctc_col] = pd.to_numeric(df[annual_ctc_col], errors='coerce')

            # Find the highest package and the corresponding company
            highest_package = 0
            company_name = None
            for _, row in df.iterrows():
                if any(row[dept_col] > 0 for dept_col in department_columns):
                    if row[annual_ctc_col] > highest_package:
                        highest_package = row[annual_ctc_col]
                        company_name = row[company_name_col]

            comparison_data.append({
                'Year': year,
                'Highest Package (LPA)': highest_package,
                'Company': company_name or "Unknown"
            })
        else:
            print(f"Required columns missing for department '{department}' in year '{year}'. Skipping...")

    if not comparison_data:
        print("No valid data found for the selected department and years.")
        return html.Div("No data available for the selected department and years.")

    # Create DataFrame for comparison data
    comparison_df = pd.DataFrame(comparison_data)
    print("Comparison DataFrame:", comparison_df)

    # Create a line chart
    # Create a bar chart
    fig = px.bar(
        comparison_df,
        x='Year',
        y='Highest Package (LPA)',
        color='Company',  # Add color to distinguish companies
        text='Company',   # Show company names as text on the bars
        labels={'Highest Package (LPA)': 'Highest Placement Package (LPA)'},
        title=f'{department} Department Placement Comparison'
    )

    # Position the text above the bars for better readability
    fig.update_traces(textposition='outside')

    # Return the bar chart inside the expandable layout
    graph_layout = html.Details([
        html.Summary(f'Yearly Comparison for {department} Department'),
        dcc.Graph(figure=fig)
    ], style={'margin': '20px'})

    return graph_layout
