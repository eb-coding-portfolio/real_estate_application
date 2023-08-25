import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src.components.frontend import ui_ids


def state_code_render(app: Dash, data: pd.DataFrame):
    all_state_codes = data['state_code'].tolist()
    unique_state_codes = sorted(set(all_state_codes))

    @app.callback(
        Output(ui_ids.STATE_CODE_DROP, 'value'),
        Input(ui_ids.STATE_CODE_INPUT, 'value')

    )
    def select_state_code(state_code: str):
        callback_all_state_codes = data[state_code].tolist()
        callback_unique_state_codes = sorted(set(all_state_codes))
        return callback_unique_state_codes

    return html.Div(
        children=[
            html.H6('State Code'),
            dcc.Dropdown(
                id=ui_ids.STATE_CODE_DROP,
                options=[
                    {"label": state_code, "value": state_code}
                    for state_code in unique_state_codes
                ],
                style={"width": "300px", "font-size": "16px"},
                value=unique_state_codes,
                multi=False,
                placeholder='Select a two digit state code',
            ),
        ],
    )

# WORK IN PROGRESS
# @app.callback(
#     Input(ui_ids.STATE_CODE_INPUT, 'value')
#
# )
# def metro_render(app: Dash, data: pd.DataFrame, state_code_metro: str):
#     filter_by_state = data['stat_code' == state_code_metro]
#     unique_state_codes = sorted(set(data_state_filter[metro].tolist()))
#
#     def select_metro(state_code: str, metro: str):
#         data_state_filter = data['stat_code' == state_code]
#         callback_unique_metro = sorted(set(data_state_filter[metro].tolist()))
#         return callback_unique_metro
#
#     return html.Div(
#         children=[
#             html.H6('Metro'),
#             dcc.Dropdown(
#                 id=ui_ids.METRO_DROP,
#                 options=[
#                     {"label": metro, "value": metro}
#                     for metro in callback_unique_metro
#                 ],
#                 style={"width": "300px", "font-size": "16px"},
#                 value=unique_state_codes,
#                 multi=False,
#                 placeholder='Select a metro',
#             ),
#         ],
#     )