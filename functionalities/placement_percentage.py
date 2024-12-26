import pandas as pd
import re
from dash import dcc, html
import plotly.express as px

def generate_placement_graphs(file_path, year, department=None):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path, header=0)
        print("CSV File Loaded Successfully")
        
        # Debugging: Print CSV Head
        print("CSV Head:")
        print(df.head())
        
        # Clean the Year column
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').dropna().astype(int)
        print("Unique Years in DataFrame after Conversion to Integer:")
        print(df['Year'].unique())

        # Filter the data for the selected year
        year_filter = df['Year'] == int(year)  # Ensure both are integers
        print("Filter Match Count after Fix:")
        print(year_filter.sum())

        if year_filter.sum() == 0:
            return html.Div(f"No data found for year {year}.", style={'color': 'red'})
        
        # Get the row that contains 'DEPARTMENT PLACEMENT' and its corresponding values
        overall_row = df[(year_filter) & (df.iloc[:, 1].str.contains('DEPARTMENT PLACEMENT', na=False, case=False))]
        if overall_row.empty:
            return html.Div(f"No 'DEPARTMENT PLACEMENT' row found for year {year}.", style={'color': 'red'})

        overall_percentage = float(overall_row.iloc[0, 2])
        print(f"Overall Placement Percentage: {overall_percentage}")

        # Generate Pie Chart for Overall Placement
        fig_overall = px.pie(
            names=['Placed', 'Not Placed'],
            values=[overall_percentage, 100 - overall_percentage],
            title=f"Overall Placement Percentage ({year})"
        )
        # Add a 3D-like effect
        fig_overall.update_traces(
            textinfo='percent+label',
            textfont_size=15,
            pull=[0.1, 0],  # Slightly pull the "Placed" slice
            marker=dict(
                colors=['#63cdda', '#f3a683'],  # Gradient-like colors
                line=dict(color='#000000', width=1.5),  # Border for the 3D look
            )
        )
        fig_overall.update_layout(
            title_font=dict(size=22, family='Arial Black', color='black'),
            title_x=0.5,
            title_y=0.9,
        )

        # Extract department information (from 4th column onwards in the row)
        department_dict = {}
        dep_info_row = overall_row.iloc[0, 3:]  # Start from the 4th column onward
        print(f"Processing department data in row: {dep_info_row}")

        for dep_data in dep_info_row:
            if isinstance(dep_data, str):
                # Clean the department data string
                dep_data_clean = dep_data.strip('[]').strip()
                
                # Match both ":" and "," format (e.g., "CST:91.5" or "CST,91.5")
                dep_match = re.split(r'[:,]', dep_data_clean)
                if len(dep_match) == 2:
                    dep_name = dep_match[0].strip().lower()  # Clean department name
                    try:
                        dep_percentage = float(dep_match[1])  # Parse percentage value
                        department_dict[dep_name] = dep_percentage
                        print(f"Extracted Department: {dep_name}, Percentage: {dep_percentage}")
                    except ValueError:
                        print(f"Error parsing percentage for {dep_name}. Value: {dep_match[1]}")

        print(f"Department Dictionary: {department_dict}")

        # Check if the department is in the dictionary (case insensitive match)
        if department:
            # Clean the department name for matching
            department_clean = department.strip().lower()
            print(f"Searching for department: {department_clean}")

            if department_clean not in department_dict:
                available_departments = ", ".join(department_dict.keys())
                print(f"Department not found. Available departments: {available_departments}")
                return html.Div(f"Department {department} not found in data. Available departments: {available_departments}", style={'color': 'red'})

            dep_percentage = department_dict[department_clean]
            print(f"{department} Placement Percentage: {dep_percentage}")

            # Ensure both names and values have the same length
            dep_pie_names = [department, 'Not Placed']
            dep_pie_values = [dep_percentage, 100 - dep_percentage]

            # Generate Pie Chart for the selected department
            fig_department = px.pie(
                names=dep_pie_names,
                values=dep_pie_values,
                title=f"Placement Percentage for {department} ({year})"
            )
            # Add a 3D-like effect
            fig_department.update_traces(
                textinfo='percent+label',
                textfont_size=15,
                pull=[0.1, 0],
                marker=dict(
                    colors=['#f8a5c2', '#3dc1d3'],
                    line=dict(color='#000000', width=1.5),
                )
            )
            fig_department.update_layout(
                title_font=dict(size=22, family='Arial Black', color='black'),
                title_x=0.5,
                title_y=0.9,
            )
            
            return html.Div([
                html.H4(f"Year: {year}"),
                html.P(f"Overall Placement Percentage: {overall_percentage}%"),
                dcc.Graph(figure=fig_overall),
                html.P(f"{department} Placement Percentage: {dep_percentage}%"),
                dcc.Graph(figure=fig_department)
            ])
        
        # If no department is specified, show only the overall placement pie chart
        return html.Div([
            html.H4(f"Year: {year}"),
            html.P(f"Overall Placement Percentage: {overall_percentage}%"),
            dcc.Graph(figure=fig_overall)
        ])
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return html.Div(f"An error occurred: {str(e)}", style={'color': 'red'})
