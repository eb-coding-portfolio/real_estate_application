import pandas as pd
from dash import Dash, html, dcc, dash_table
from src.components.frontend import ui_ids
from config import metric_list, table_columns


def create_layout(app: Dash, data: pd.DataFrame, prop_type_options: list):
    return html.Div(
        className='app-Div',
        children=[
            html.Div(
                className='title-container',  # Add custom class to this container
                children=[
                    html.H1(app.title),
                    html.Img(
                        src='assets/map_Marker.png',  # Replace with the image file name
                        className='logo-img'  # Add custom class for the image
                    ),
                    html.Hr(),
                ],
            ),
            html.Div(
                className='dropdown-container',
                children=[
                    html.H6('Property Type'),
                    dcc.Dropdown(
                        id=ui_ids.PROPERTY_TYPE_DROP,
                        options=prop_type_options,
                        style={"width": "300px", "font-size": "16px"},
                        value='All Residential',
                        multi=False,
                        placeholder='Select a property type',
                        className='custom-dropdown'
                    ),
                    html.H6('Metric'),
                    dcc.Dropdown(
                        id=ui_ids.METRIC_DROP,
                        options=[
                            {"label": metric, "value": metric}
                            for metric in metric_list
                        ],
                        style={"width": "300px", "font-size": "16px"},
                        value='median_sale_price_yoy',
                        multi=False,
                        placeholder='Select a metric',
                        className='custom-dropdown'
                    )
                ],
            ),
            html.Div(
                className='bar-chart-container',
                children=[
                    # Wrap the plot and the caption in a new html.Div
                    html.Div([
                        dcc.Graph(id=ui_ids.US_MAP),
                        html.P("Data provided by Redfin, a national real estate brokerage.", className='caption-text')
                    ], className='chart-container'),
                ],
            ),
            html.Div(
                className='heat-map-container-components',
                children=[
                    dcc.RadioItems(
                        id=ui_ids.SELECT_COMP,
                        options=[
                            {'label': 'State', 'value': 'state'},
                            {'label': 'National', 'value': 'national'}
                        ],
                        value='state',
                        labelStyle={'display': 'block'}
                    ),
                    html.Button('Previous', id=ui_ids.BTN_PREV, n_clicks=0),
                    html.Button('Next', id=ui_ids.BTN_NXT, n_clicks=0),
                    html.Div(id=ui_ids.DIV_PGNUM, style={'display': 'none'}, children=1),

                ]

            ),
            html.Div(
                className='heat-map-container',
                children=[
                    dcc.Graph(id=ui_ids.HOUSING_TABLE_ID, style={"height": "70vh"})
                ], style={"display": "flex", "flexDirection": "column", "height": "80vh"}
            )
        ],
    )
