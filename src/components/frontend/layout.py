import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
from src.components.frontend import ui_ids
from config import metric_list, table_columns


def create_tab_1_content(data: pd.DataFrame, prop_type_options: list):
    return [
        html.Div(
            className=ui_ids.TAB_DIVS,
            children=[
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
                        html.Div([
                            dcc.Graph(id=ui_ids.US_MAP),
                            html.P("Data provided by Redfin, a national real estate brokerage.",
                                   className='caption-text')
                        ], className='chart-container'),
                    ],
                ),
                html.Div(
                    className='heat-map-container-components',
                    children=[
                        html.H6('Compare Metro Metric To:'),
                        dcc.RadioItems(
                            id=ui_ids.SELECT_COMP,
                            options=[
                                {'label': 'State', 'value': 'state'},
                                {'label': 'National', 'value': 'national'}
                            ],
                            value='state',
                            labelStyle={'display': 'block'}
                        ),
                        html.Button('Previous',
                                    id=ui_ids.BTN_PREV,
                                    n_clicks=0,
                                    ),
                        html.Button('Next',
                                    id=ui_ids.BTN_NXT,
                                    n_clicks=0,
                                    ),
                        html.Div(id=ui_ids.DIV_PGNUM, style={'display': 'none'}, children=1),
                    ]
                ),
                html.Div(
                    className='heat-map-container',
                    children=[
                        dcc.Graph(id=ui_ids.HOUSING_TABLE_ID, style={"height": "70vh"}),
                        html.P("Data provided by Redfin, a national real estate brokerage.",
                               className='caption-text')
                    ], style={"display": "flex", "flexDirection": "column", "height": "80vh"}
                )
                # Existing content ends here
            ]  # Children of the new outer Div end here
        )  # New outer Div ends here
    ]


def create_tab_2_content():
    return html.Div(
        className=ui_ids.TAB_DIVS,
        children=[
            html.H3('Market Selection Content Coming Soon!')
        ]
    )


def create_layout(app: Dash):
    return html.Div(
        className=ui_ids.TAB_DIVS,
        children=[
            html.Div(
                className='title-container',
                children=[
                    html.H1(app.title),
                    html.Img(
                        src='assets/map_Marker.png',
                        className='logo-img'
                    ),
                    html.Hr(),
                ],
            ),
            dcc.Tabs(
                id=ui_ids.TABS,
                value='tab1',
                children=[
                    dcc.Tab(
                        id=ui_ids.TAB_1,
                        label='Market Overview',
                        value='tab1'
                    ),
                    dcc.Tab(
                        id=ui_ids.TAB_2,
                        label='Market Selection',
                        value='tab2'
                    ),
                ]
            ),
            html.Div(id=ui_ids.TABS_CONTENT)
        ])
