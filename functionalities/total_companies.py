import plotly.express as px
from dash import dcc, html
from data_processing import load_placement_data

def create_total_companies_graph(data_folder):
    """Creates a 3D-styled bar graph of the total companies visiting each year, within a styled frame."""

    # Load placement data
    company_counts = load_placement_data(data_folder)

    # Create the bar graph
    years = list(company_counts.keys())
    counts = list(company_counts.values())

    fig = px.bar(
        x=years,
        y=counts,
        labels={'x': 'Year', 'y': 'Number of Companies'},
        title='Number of Companies Visiting Each Year'
    )

    # Add 3D styling and visual effects
    fig.update_traces(
    marker=dict(
        color=['#446BAD' if count > 50 and count<100 else '#008ECC' if count >  100  else '#0147AB' for count in counts]  # Red for >50, Green otherwise
    )
)
    fig.update_layout(
        title=dict(
            font=dict(size=24, color='#333333'),
            x=0.5,  # Center align
            xanchor='center'
        ),
        plot_bgcolor='rgba(240, 240, 240, 1)',  # Light gray background
        paper_bgcolor='rgba(255, 255, 255, 1)',  # White frame
        font=dict(family='Arial, sans-serif', size=14, color='#444444'),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            title=dict(font=dict(size=18, color='#333333')),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.5)',
            zeroline=False,
            title=dict(font=dict(size=18, color='#333333')),
        ),
    )

    # Create a styled frame for the graph
    graph_layout = html.Div(
        children=[
            html.H2("Yearly Company Visits", style={
                'textAlign': 'center',
                'color': '#555555',
                'fontFamily': 'Arial, sans-serif',
                'marginBottom': '15px'
            }),
            dcc.Graph(figure=fig)
        ],
        style={
            'border': '3px solid #444444',
            'borderRadius': '10px',
            'padding': '15px',
            'boxShadow': '5px 5px 15px rgba(0, 0, 0, 0.3)',
            'backgroundColor': '#f9f9f9',
            'margin': '20px'
        }
    )

    return graph_layout
