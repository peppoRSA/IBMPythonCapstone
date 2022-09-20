# Import required libraries
from gc import callbacks
import pandas as pd
import dash
import dash_html_components as html
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


siteNames = ["All Sites"]

for i in spacex_df["Launch Site"].unique():
    siteNames.append(i)

# siteNames = siteNames.append(spacex_df["Launch Site"].unique())

# python3 spacex_dash_app.py

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),


                                html.Div(
                                    dcc.Dropdown(id='site-dropdown',
                                                 options=[


                                                     {'label': x, 'value': x} for x in siteNames
                                                 ],
                                                 value='All Sites',
                                                 placeholder="Select a Launch Site",
                                                 searchable=True

                                                 ),
),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(0, 10000, 1000, marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}, value=[
                    min_payload, max_payload],  id='payload-slider'),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@ app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    # filtered_df = spacex_df.groupby(["Launch Site", "class"]).size()
    if site_dropdown == 'All Sites':
        # filtered_df = spacex_df.query("`class` == 1")
        fig = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='Launch Site Totals for ' + site_dropdown)
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == site_dropdown]
        filtered_df = filtered_df.groupby(
            ["Launch Site", "class"]).size().reset_index(name="classTotal")
        fig = px.pie(filtered_df,
                     values="classTotal",
                     names='class',
                     title='Launch Site Totals for ' + site_dropdown)

        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@ app.callback(
    Output(component_id='success-payload-scatter-chart',
           component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value'))
def get_pie_chart(site_dropdown, payload_slider):

    if site_dropdown == "All Sites":
        low, high = payload_slider
        mask = (spacex_df['Payload Mass (kg)'] > low) & (
            spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], x='Payload Mass (kg)',
                         y='class', color='Booster Version Category', title='Scatterplot for ' + site_dropdown)

        return fig
    else:
        fdf = spacex_df[spacex_df["Launch Site"] == site_dropdown]
        low, high = payload_slider
        mask = (fdf['Payload Mass (kg)'] > low) & (
            fdf['Payload Mass (kg)'] < high)
        fig = px.scatter(fdf[mask], x='Payload Mass (kg)',
                         y='class', color='Booster Version Category', title='Scatterplot for ' + site_dropdown)

        return fig

    # Run the app
if __name__ == '__main__':
    app.run_server()


# python3 spacex_dash_app.py
