import pandas as pd
import plotly.express as px
from dash import dcc, html
import os

def load_and_clean_csv(file_path):
    """Load and clean the placement CSV file."""
    try:
        # Read the CSV file and set the correct header row
        raw_df = pd.read_csv(file_path, header=0)  # Adjust `header` if necessary
        
        # Drop completely empty rows and columns
        raw_df.dropna(axis=0, how='all', inplace=True)
        raw_df.dropna(axis=1, how='all', inplace=True)
        
        # Normalize column names
        raw_df.columns = raw_df.columns.str.strip()

        # Print the column names for debugging
        print("Columns after cleaning:", raw_df.columns.tolist())

        # Validate the presence of the required columns
        required_columns = {'Company Visited', 'Total'}
        if not required_columns.issubset(set(raw_df.columns)):
            raise KeyError(f"Columns {required_columns} are missing in the cleaned data.")

        return raw_df
    except Exception as e:
        print(f"Error while processing {file_path}: {e}")
        raise


def load_yearly_data(data_folder, year):
    """Loads placement data for a specific year and normalizes column names."""
    csv_file = f"Placement-Record-{year}.csv"
    file_path = os.path.join(data_folder, csv_file)

    try:
        df = load_and_clean_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file for year {year} does not exist in the folder '{data_folder}'.")
    except KeyError as e:
        raise KeyError(f"Error in file for year {year}: {e}")

    return df


def create_yearly_comparison_graph(data_folder, year1, year2):
    """Creates a comparison line chart for two selected years with enhanced styling."""
    # Load data for both years
    df1 = load_yearly_data(data_folder, year1)
    df2 = load_yearly_data(data_folder, year2)

    # Validate required columns
    required_columns = {'Company Visited', 'Total'}
    for year, df in zip([year1, year2], [df1, df2]):
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise KeyError(f"Columns {missing_columns} are missing in Year {year}")

    # Filter and rename columns
    df1_filtered = df1[['Company Visited', 'Total']].rename(columns={'Total': f'Total {year1}'})
    df2_filtered = df2[['Company Visited', 'Total']].rename(columns={'Total': f'Total {year2}'})

    # Merge the two datasets
    merged_df = pd.merge(df1_filtered, df2_filtered, on='Company Visited', how='outer').fillna(0)

    # Create the line chart
    fig = px.line(
        merged_df,
        x='Company Visited',
        y=[f'Total {year1}', f'Total {year2}'],
        labels={'value': 'Total Students Placed', 'variable': 'Year'},
        title=f'Yearly Comparison: {year1} vs {year2}'
    )

    # Add styling to the chart
    fig.update_layout(
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#ffffff',
        title=dict(
            font=dict(size=20, color='#4A90E2'),
            x=0.5  # Center-align the title
        ),
        xaxis=dict(
            title=dict(font=dict(size=14, color='#333333')),
            tickfont=dict(size=12, color='#333333')
        ),
        yaxis=dict(
            title=dict(font=dict(size=14, color='#333333')),
            tickfont=dict(size=12, color='#333333')
        ),
        legend=dict(
            title=dict(font=dict(size=12)),
            font=dict(size=12)
        )
    )

    # Create a styled expandable frame for the graph
    graph_layout = html.Div(
        children=[
            html.Details(
                children=[
                    html.Summary(
                        f'Compare {year1} and {year2}',
                        style={
                            'cursor': 'pointer',
                            'fontWeight': 'bold',
                            'fontSize': '16px',
                            'color': '#4A90E2'
                        }
                    ),
                    dcc.Graph(figure=fig)
                ]
            )
        ],
        style={
            'border': '2px solid #4A90E2',
            'borderRadius': '10px',
            'padding': '20px',
            'boxShadow': '3px 3px 10px rgba(0, 0, 0, 0.1)',
            'backgroundColor': '#ffffff',
            'margin': '20px'
        }
    )

    return graph_layout
