import os
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from data_processing import convert_xlsx_to_csv
from functionalities.total_companies import create_total_companies_graph
from functionalities.yearly_comparison import create_yearly_comparison_graph
from functionalities.department_yearly_comparison import department_yearly_comparison
from functionalities.placement_percentage import generate_placement_graphs

# Define paths
data_folder = 'data/'

# Convert all XLSX files to CSV
convert_xlsx_to_csv(data_folder)

# Initialize the Dash app
app = Dash(__name__)
app.title = "Campus Placement Dashboard"

# Suppress callback exceptions
app.config.suppress_callback_exceptions = True

# List of departments
departments = [
    'CST', 'ETC', 'EE', 'IT', 'ME', 'CE', 'MET', 'MIN', 'ARC', 'AERO',
    'VLSI', 'Mat Science', 'Mechatronics', 'Food Proc.', 'REST', 'Bio-Medical',
    'Safety', 'Physics', 'Maths', 'Chem', 'MBA', 'Earth Science'
]

# Uniform styling for sections
section_style = {
    'padding': '20px',
    'border': '2px solid #4A90E2',
    'borderRadius': '10px',
    'backgroundColor': '#f9f9f9',
    'boxShadow': '3px 3px 10px rgba(0, 0, 0, 0.1)',
    'margin': '20px'
}

# Layout of the app
app.layout = html.Div([
    # Header
    html.H1("Campus Placement Dashboard", style={'textAlign': 'center', 'color': '#4A90E2'}),

    # Total companies graph
    create_total_companies_graph(data_folder),

    # Yearly comparison section
    html.Div([
        html.H2("Yearly Comparison", style={'color': '#333333'}),
        html.Label("Select Year 1:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
        dcc.Dropdown(id='year1-dropdown',
                     options=[{'label': str(year), 'value': str(year)} for year in range(2015, 2025)],
                     value='2023'),
        html.Label("Select Year 2:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
        dcc.Dropdown(id='year2-dropdown',
                     options=[{'label': str(year), 'value': str(year)} for year in range(2015, 2025)],
                     value='2024'),
        html.Div(id='yearly-comparison-output')
    ], style=section_style),

    # Department-wise comparison section
    html.Div([
        html.H2("Department Yearly Comparison", style={'color': '#333333'}),
        html.Label("Select Department:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
        dcc.Dropdown(id='department-dropdown',
                     options=[{'label': dept, 'value': dept} for dept in departments],
                     value='CST'),
        html.Label("Select Years:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
        dcc.Dropdown(id='department-years-dropdown',
                     options=[{'label': str(year), 'value': str(year)} for year in range(2020, 2025)],
                     value=['2023', '2024'],
                     multi=True),
        html.Div(id='department-comparison-output')
    ], style=section_style),

    # Placement percentage section
    html.Div([
        html.H2("Placement Percentage Analysis", style={'color': '#333333'}),
        html.Label("Select Placement Year:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
        dcc.Dropdown(
            id='placement-year-dropdown',
            options=[{'label': str(year), 'value': str(year)} for year in range(2020, 2025)],
            value='2023'
        ),
        html.Label("Select Department (Optional):", style={'fontWeight': 'bold', 'fontSize': '14px'}),
        dcc.Dropdown(
            id='placement-department-dropdown',
            options=[{'label': dept, 'value': dept} for dept in departments] + [{'label': 'Overall', 'value': ''}],
            value=''
        ),
        html.Button(
            id='placement-plot-button',
            n_clicks=0,
            children='Plot Graph',
            style={
                'backgroundColor': '#4CAF50',
                'color': 'white',
                'padding': '10px 20px',
                'border': 'none',
                'cursor': 'pointer',
                'borderRadius': '10px',  # Rounded edges
                'marginTop': '20px'  # Padding above the button
            }
        ),
        html.Div(id='placement-percentage-output')
    ], style=section_style),


])

# Callbacks

# Yearly comparison callback
@app.callback(
    Output('yearly-comparison-output', 'children'),
    [Input('year1-dropdown', 'value'), Input('year2-dropdown', 'value')]
)
def update_yearly_comparison(year1, year2):
    return create_yearly_comparison_graph(data_folder, year1, year2)

# Department comparison callback
@app.callback(
    Output('department-comparison-output', 'children'),
    [Input('department-dropdown', 'value'), Input('department-years-dropdown', 'value')]
)
def update_department_comparison(department, years):
    return department_yearly_comparison(data_folder, department, years)

# Placement percentage callback
@app.callback(
    Output('placement-percentage-output', 'children'),
    [
        Input('placement-plot-button', 'n_clicks'),
        Input('placement-year-dropdown', 'value'),
        Input('placement-department-dropdown', 'value')
    ]
)
def update_placement_percentage(n_clicks, year, department):
    if n_clicks > 0:  # Ensure the graph is plotted only after the button is clicked
        file_path = "data/Placement-Record-Overall.csv"
        return generate_placement_graphs(file_path, year, department)
    return html.Div("Click the button to generate the graph.", style={'color': 'blue'})


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
