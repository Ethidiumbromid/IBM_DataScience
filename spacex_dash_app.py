# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = [{'label':i, 'value':i} for i in spacex_df['Launch Site'].unique()]
launch_sites.append({'label': 'ALL', 'value':'ALL'})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(id='site-dropdown', options=launch_sites,placeholder='Select Launch Site',searchable=True,value='ALL')),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))        
def update_graph(value):
    if value == 'ALL':
        df_tmp = spacex_df.groupby("Launch Site")["class"].sum().to_frame()
        df_tmp.reset_index(inplace=True)
        print(df_tmp.index)
        df_tmp.to_csv('test.csv')
        fig = px.pie(df_tmp, values='class', names="Launch Site", title="Successful  Launches by Site")
    else:
        df_tmp = spacex_df[spacex_df["Launch Site"] == value]
        df_tmp.to_csv('test.csv')
        df_tmpp = df_tmp.groupby(["class"]).size().reset_index(name="count")
        df_tmpp.to_csv("test_ls.csv")
        
        fig = px.pie(df_tmpp, values='count', names="class", title="Successful  Launches by Site")

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])


def pie(site_dropdown):
    title_pie = f"Success Launches for site {site_dropdown}" 
    
    if site_dropdown == 'ALL':      
        fig = px.pie(spacex_df, values='class', names='Launch Site', title=title_pie)

    else:
        filtered_DD= spacex_df[spacex_df['Launch Site'] == site_dropdown]
        filtered_LS = filtered_DD.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(filtered_LS, values='class count', names='class', title=title_pie)
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
