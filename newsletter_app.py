# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


app = Dash(__name__)


newsletter_counts_df = pd.read_csv('src/assets/newsletter_counts.csv')
newsletter_counts_df = newsletter_counts_df[newsletter_counts_df.columns[1:]]

active_counts_by_proj_type_df = pd.read_csv('src/assets/newsletter_active_counts_by_proj_type.csv')

newsletter_housed_counts_by_destination_df = pd.read_csv('src/assets/newsletter_housed_counts_by_destination_by_race.csv')



newsletter_counts_by_race_df1 = pd.read_csv('src/assets/newsletter_counts_by_race.csv')

old_cols = [x for x in newsletter_counts_by_race_df1.columns if 'by Race' in x]
new_cols = [x.split(" by ")[0] for x in newsletter_counts_by_race_df1 if 'by Race' in x]

newsletter_counts_by_race_df1 = newsletter_counts_by_race_df1.rename(columns=dict(zip(old_cols, new_cols)))

newsletter_active_counts_by_proj_type_by_race = pd.read_csv('src/assets/newsletter_active_counts_by_proj_type_by_race.csv')

race_picklist = sorted(list(newsletter_counts_by_race_df1['static_demographics.race_text'].unique()))



app.layout = html.Div(
    children=[
        html.H1(children='HMIS Data Newsletter'),
        html.Div(
            className="filter_section",
            children=[
                html.P("Select Reporting Month", className='filter_titles'),
                dcc.Dropdown(
                    options=['Jan-2023', 'Dec-2022', 'Nov-2022', 'Oct-2022', 'Sep-2022'],#newsletter_counts_df["Reporting Month"].unique(),
                    value='Jan-2023',
                    id='year-slider'
                ),
                html.P("Select Reporting Window", className='filter_titles'),
                dcc.RadioItems(newsletter_counts_df["Reporting Window"].unique(), 'Monthly', id="report-window", className = "radio_button",),
                html.P("Race Filter", className='filter_titles'),
                dcc.Checklist(options=race_picklist, value=race_picklist,labelStyle={"display": "flex", "align-items": "center"}, id="race_option")
            ]
        ),
        html.Div(
            className="container",
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="block-1",
                            children=[
                                html.Div(
                                    className="title-section-1",
                                    children=[html.H2(children="What's new?")]
                                ),
                                html.Div(
                                    className="body-section-1",
                                    children=[
                                        html.Div(
                                            id='first_card',
                                            className="card",
                                            children=[
                                                html.H3(id="fth_count", className="metric"),
                                                html.H3(children="First Time Homeless"),
                                                html.Div(className="plots", children=[dcc.Graph(id='fth_race_plot', className='race_plot')]),
                                            ]
                                        ),
                                        html.Div(
                                            className="card",
                                            children=[
                                                html.H3(id="housed_count", className="metric"),
                                                html.H3(children="Persons Housed"),
                                                html.Div(className="plots", children=[dcc.Graph(id='housed_race_plot', className='race_plot')]),
                                            ]
                                        ),
                                        html.Div(
                                            className="card",
                                            children=[
                                                html.H3(id="new_entries_count",className="metric"),
                                                html.H3(children="New Program Entries"),
                                                html.Div(className="plots", children=[dcc.Graph(id='new_entries_race_plot', className='race_plot')]),
                                            ]
                                        ),
                                        html.Div(
                                            className="card",
                                            children=[
                                                html.H3(id="new_referrals_count", className="metric"),
                                                html.H3(children="New Referrals to Housing Queue"),
                                                html.Div(className="plots", children=[dcc.Graph(id='new_referrals_race_plot', className='race_plot')]),
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            className="block-2",
                            children=[
                                html.Div(
                                    className="title-section-2",
                                    children=[html.H2(children="Who's active")]
                                ),
                                html.Div(
                                    className="body-section-2",
                                    children=[
                                        html.Div(
                                            className="body-section-2-subsection-1",
                                            children=[
                                                html.Div(
                                                    className='top',
                                                    children=[
                                                        html.Div(
                                                            className="active-bottom-right",
                                                            children=[
                                                                html.H3(id="seniors_active_count",className="metric"),
                                                                html.H3(children="Seniors (55+) Served"),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='senior_active_race_plot'),
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className="active-bottom",
                                                            children=[
                                                                html.H3(id="families_active_count", className="metric"),
                                                                html.H3(children="Families Served"),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='families_active_race_plot'),
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    className='bottom',
                                                    children=[    
                                                        html.Div(
                                                            className="active-right",
                                                            children=[
                                                                html.H3(id="tay_active_count", className="metric"),
                                                                html.H3(children="TAY (18-24) Served"),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='tay_active_race_plot'),
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className="active",
                                                            children=[
                                                                html.H3(id="veterans_active_count", className="metric"),
                                                                html.H3(children="Veterans Served"),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='veteran_active_race_plot'),
                                                                ),
                                                            ]
                                                        )
                                                    ]
                                                ),                                        
                                            ]
                                        ), 
                                        html.Div(
                                            className="body-section-2-subsection-2",
                                            children = [
                                                dcc.Graph(
                                                    id='active_counts_pie'
                                                ),
                                                html.Div(
                                                    className='active-card',
                                                    children=[
                                                        html.Div(
                                                            className='active-card-top',
                                                            children=[
                                                                html.Div(id="active_count", className="active-metric-1"),
                                                                html.Div(className="active-text-1",children="Active Clients"),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='active-card-bottom',
                                                            children=[
                                                                html.Div(className="arrow-up-1", children=""),
                                                                html.Div(className="active-metric-2", children="4% Last Month"),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),                             
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            className="block-3",
                            children=[
                                html.Div(
                                    className="title-section-3",
                                    children=[html.H2(children="Who found housing?")]
                                ),
                                html.Div(
                                    className="body-section-3",
                                    children=[
                                        html.Div(
                                            className="body-section-3-subsection-1",
                                            children=[
                                                html.Div(
                                                    className="card",
                                                    children=[
                                                        html.H3(id='housed_count_1',className="metric"),
                                                        html.H3(children="Persons Housed"),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className="body-section-3-subsection-2",
                                            children=[
                                                html.Div(
                                                    className='section-3-subsection-2-top',
                                                    children=[
                                                        html.Div(
                                                            className="house-card",
                                                            children=[
                                                                html.Div(
                                                                    className="arrow-up",
                                                                    children=""
                                                                ),
                                                                html.Div(
                                                                    className="housed-metrics",
                                                                    children=[
                                                                        html.H4(id="senior_housed_count"),
                                                                        html.H4(className="bar",children="|"),
                                                                        html.H4(children="Seniors"),   
                                                                    ]
                                                                ),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='senior_housed_race_plot'),
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className="house-card",
                                                            children=[
                                                                html.Div(
                                                                    className="arrow-up",
                                                                    children=""
                                                                ),
                                                                html.Div(
                                                                    className="housed-metrics",
                                                                    children=[
                                                                        html.H4(id="tay_housed_count"),
                                                                        html.H4(className="bar",children="|"),
                                                                        html.H4(children="Families"),
                                                                    ]
                                                                ),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='families_housed_race_plot'),
                                                                    ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                                html.Div(
                                                    className='section-3-subsection-2-bottom',
                                                    children=[
                                                        html.Div(
                                                            className="house-card",
                                                            children=[
                                                                html.Div(
                                                                    className="arrow-up",
                                                                    children=""
                                                                ),
                                                                html.Div(
                                                                    className="housed-metrics",
                                                                    children=[
                                                                        html.H4(id="families_housed_count"),
                                                                        html.H4(className="bar",children="|"),
                                                                        html.H4(children="TAY 18-24"),
                                                                    ]
                                                                ),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='tay_housed_race_plot', style={'width': 'auto', 'height': '10vh'}),
                                                                ),
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className="house-card",
                                                            children=[
                                                                html.Div(
                                                                    className="arrow-up",
                                                                    children=""
                                                                ),
                                                                html.Div(
                                                                    className="housed-metrics",
                                                                    children=[
                                                                        html.H4(id="veterans_housed_count"),
                                                                        html.H4(className="bar",children="|"),
                                                                        html.H4(children="Veterans"),
                                                                    ]
                                                                ),
                                                                html.Div(
                                                                    className='housed_plots',
                                                                    children=dcc.Graph(id='veteran_housed_race_plot'),
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                )                                                                                                                        
                                            ]
                                        ),
                                        html.Div(
                                            className="body-section-3-subsection-2",
                                            children=[
                                                dcc.Graph(id='graph-with-slider'),
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)



@app.callback(
    Output('active_counts_pie', 'figure'),
    Input('year-slider', 'value'),
    Input('report-window', 'value'),
    Input('race_option', 'value'),)
def update_figure(selected_year, report_window, race_option):
    filtered_df = newsletter_active_counts_by_proj_type_by_race[(newsletter_active_counts_by_proj_type_by_race['Reporting Month'] == selected_year) & (newsletter_active_counts_by_proj_type_by_race['Reporting Window'] == report_window) & (newsletter_active_counts_by_proj_type_by_race['static_demographics.race_text'].isin(race_option))].reset_index(drop=True)

    fig = px.pie(filtered_df, names="Project Type", values="Active Clients Count", labels='abbrev', hole=.7)
    fig.update_layout({
        "margin_r":120,
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'legend_font': {"color":"rgba(255,255,255,0.95)"},
        "legend_title_text":"HMIS Project Types",
        "legend_title_side":"top",
        "legend_yanchor":"top",
        "legend_y":.85,
        "legend_xanchor":"right",
        "legend_x":2.1
    })
    fig.update_traces(
        textposition="auto",
        insidetextorientation="horizontal", 
        insidetextfont_color="white",#"rgba(255,255,255,1)",
        outsidetextfont_color="white"#"rgba(255,255,255,1)"
        )

    return fig

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('report-window', 'value'),
    Input('race_option', 'value'),)
def update_figure(selected_year, report_window, race_option):
    filtered_df = newsletter_housed_counts_by_destination_df[(newsletter_housed_counts_by_destination_df['Reporting Month'] == selected_year) & (newsletter_housed_counts_by_destination_df['Reporting Window'] == report_window) & (newsletter_housed_counts_by_destination_df['static_demographics.race_text'].isin(race_option))].reset_index(drop=True)
    
    fig = px.bar(filtered_df, y='Permanent Destination', x='clients.unique_identifier', orientation='h', color='static_demographics.race_text', text_auto=True)
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'legend_bgcolor': "rgba(1,1,1,1)",
    "showlegend":False,
    'yaxis_title':""
    })
    # fig.update_traces(
    #     insidetextanchor="end",
    #     textposition="inside",
    #     insidetextfont_color="white",#"rgba(255,255,255,1)",
    #     outsidetextfont_color="white"#"rgba(255,255,255,1)"
    #     )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(
        tickmode="array",
        categoryorder="total ascending",
        ticklabelposition="outside",
        tickfont=dict(color="white"), matches=None, showticklabels=True, visible=True
    )
    

    # fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output(component_id='fth_count', component_property='children'),
    Output(component_id='housed_count', component_property='children'),
    Output(component_id='new_entries_count', component_property='children'),
    Output(component_id='new_referrals_count', component_property='children'),
    Output(component_id='seniors_active_count', component_property='children'),
    Output(component_id='tay_active_count', component_property='children'),
    Output(component_id='families_active_count', component_property='children'),
    Output(component_id='veterans_active_count', component_property='children'),
    Output(component_id='housed_count_1', component_property='children'),
    Output(component_id='senior_housed_count', component_property='children'),
    Output(component_id='tay_housed_count', component_property='children'),
    Output(component_id='families_housed_count', component_property='children'),
    Output(component_id='veterans_housed_count', component_property='children'),
    Output(component_id='active_count', component_property='children'),
    Input('year-slider', 'value'),
    Input('report-window', 'value'),
    Input('race_option', 'value'),)
def update_metrics(selected_year, report_window, race_option):
    temp_df = newsletter_counts_by_race_df1[(newsletter_counts_by_race_df1['Reporting Month']==selected_year) & (newsletter_counts_by_race_df1['Reporting Window']==report_window) & (newsletter_counts_by_race_df1['static_demographics.race_text'].isin(race_option))]
    d = {col: temp_df[col].sum() for col in temp_df if 'Count' in col}
    return (
        d['FTH Count'], 
        d['Housed Count'], 
        d['New Program Entries Count'], 
        d['New Referrals Count'],
        d['Active Seniors Count'], 
        d['Active TAY Count'],
        d['Active Families Count'],
        d['Active Veterans Count'],
        d['Housed Count'], 
        d['Housed Seniors Count'],
        d['Housed TAY Count'],
        d['Housed Families Count'],
        d['Housed Veterans Count'],
        d['Active Count'],
        )


@app.callback(
    Output('fth_race_plot', 'figure'),
    Output('housed_race_plot', 'figure'),
    Output('new_entries_race_plot', 'figure'),
    Output('new_referrals_race_plot', 'figure'),
    Input('year-slider', 'value'),
    Input('report-window', 'value'),
    Input('race_option', 'value'),
)
def update_(selected_year, report_window, race_option):
    temp_df = newsletter_counts_by_race_df1[(newsletter_counts_by_race_df1['Reporting Month']==selected_year) & (newsletter_counts_by_race_df1['Reporting Window']==report_window) & (newsletter_counts_by_race_df1['static_demographics.race_text'].isin(race_option))].reset_index(drop=True)

    donut_plot_d = {}
    for col in [x for x in temp_df.columns if 'Count' in x]:
        count_by_race_df = temp_df[['static_demographics.race_text',col]].copy()
        fig = px.pie(count_by_race_df, names='static_demographics.race_text', values=col, hole=0.7)
        fig.update_layout({
            'showlegend':False,
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'margin_b':0,
            'margin_l':0,
            'margin_t':0,
            'margin_r':0
        })
        donut_plot_d[col] = fig
    return donut_plot_d['FTH Count'], donut_plot_d['Housed Count'], donut_plot_d['New Program Entries Count'], donut_plot_d['New Referrals Count']

@app.callback(
    Output('senior_active_race_plot', 'figure'),
    Output('veteran_active_race_plot', 'figure'),
    Output('families_active_race_plot', 'figure'),
    Output('tay_active_race_plot', 'figure'),
    Output('senior_housed_race_plot', 'figure'),
    Output('veteran_housed_race_plot', 'figure'),
    Output('tay_housed_race_plot', 'figure'),
    Output('families_housed_race_plot', 'figure'),
    Input('year-slider', 'value'),
    Input('report-window', 'value'),
    Input('race_option', 'value'),
)
def update_housed_race_plots(selected_year, report_window, race_option):
    temp_df = newsletter_counts_by_race_df1[(newsletter_counts_by_race_df1['Reporting Month']==selected_year) & (newsletter_counts_by_race_df1['Reporting Window']==report_window) & (newsletter_counts_by_race_df1['static_demographics.race_text'].isin(race_option))].reset_index(drop=True)
    

    bar_plot_d = {}
    for col in  [x for x in temp_df.columns if ('Housed' in x or 'Active' in x) and x!='Housed Count' and x!='Active Count']:
        count_by_race_df = temp_df[['Reporting Month', 'static_demographics.race_text', col]].copy()
        fig = px.bar(count_by_race_df, x=col, y='Reporting Month', orientation='h', color='static_demographics.race_text', text_auto=True)
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'margin_b':0,
            'margin_l':0,
            'margin_t':0,
            'margin_r':0,
            'xaxis': {
            #     'range': [0, 1],
                'showgrid': False, # thin lines in the background
                'zeroline': False, # thick line at x=0
                'visible': False,  # numbers below
            }, # the same for yaxis
            'yaxis': {
            #     'range': [0, 1],
                'showgrid': False, # thin lines in the background
                'zeroline': False, # thick line at x=0
                'visible': False,  # numbers below
            }, # the same for yaxis
            'barmode':'stack',
            # 'barnorm':'percent',
            'showlegend':False,
            'uniformtext_minsize':16, 
            "uniformtext_mode":'hide', 
            "autosize":False
        })

        bar_plot_d[col] = fig
    return (
        bar_plot_d['Active Seniors Count'], 
        bar_plot_d['Active Veterans Count'], 
        bar_plot_d['Active TAY Count'], 
        bar_plot_d['Active Families Count'],
        bar_plot_d['Housed Seniors Count'], 
        bar_plot_d['Housed Veterans Count'], 
        bar_plot_d['Housed TAY Count'], 
        bar_plot_d['Housed Families Count'])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)