from dash import Dash, callback_context
import pandas as pd
from src.components.frontend.layout import create_layout
from dash.dependencies import Input, Output, State
import plotly.express as px
from utils import get_stat_val, calculate_differences, add_heatmap_annotations
from src.components.frontend import ui_ids
from config import percentage_metric_list, table_columns
import numpy as np
import os

from sqlalchemy import create_engine

if __name__ == "__main__":
    DATABASE_URL = os.environ.get('DATABASE_URL')
    engine = create_engine(DATABASE_URL)

    data = pd.read_sql('SELECT * FROM market_tracker', engine)

    external_stylesheets = ['https://bootswatch.com/5/litera/bootstrap.css', 'custom.css']
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    data_filters_prop_type = data['property_type'].unique()
    prop_type_options = [{'label': prop_type, 'value': prop_type} for prop_type in data_filters_prop_type]

    @app.callback(
        Output(ui_ids.US_MAP, 'figure'),
        Input(ui_ids.METRIC_DROP, 'value'),
        Input(ui_ids.PROPERTY_TYPE_DROP, 'value'),
    )
    def update_us_map(selected_metric, selected_property_type):
        map_input_df = pd.DataFrame(data)

        max_date = get_stat_val(map_input_df, 'period_end', 'max')

        map_df = map_input_df[(map_input_df['period_end'] == max_date) &
                              (map_input_df['region_type'] == 'state') &
                              (map_input_df['property_type'] == selected_property_type)][
            ['state_code', selected_metric]]

        if selected_metric in percentage_metric_list:
            hover_data = {selected_metric: ':.2%'}
            tickformat = '.2%'
        else:
            hover_data = None
            tickformat = None
        fig = px.choropleth(map_df, locations='state_code',  # DataFrame column with locations
                            color=selected_metric,  # DataFrame column with color values
                            locationmode="USA-states",  # built-in location mode for U.S. states
                            scope="usa",
                            color_continuous_scale='deep',
                            hover_data=hover_data,
                            )
        fig.update_coloraxes(colorbar_tickformat=tickformat)
        return fig


    @app.callback(
        Output(ui_ids.HOUSING_TABLE_ID, 'figure'),
        Output(ui_ids.DIV_PGNUM, 'children'),
        Input(ui_ids.SELECT_COMP, 'value'),
        Input(ui_ids.BTN_PREV, 'n_clicks'),
        Input(ui_ids.BTN_NXT, 'n_clicks'),
        Input(ui_ids.PROPERTY_TYPE_DROP, 'value'),
        Input(ui_ids.US_MAP, 'clickData'),
        State(ui_ids.DIV_PGNUM, 'children')
    )
    def update_heatmap(compare_to, prev_clicks, next_clicks, heat_map_prop_type, clickData, current_page):
        metric_list = [column for column in table_columns if 'yoy' in column]
        print(clickData)
        if clickData is None:
            # If no state has been clicked, don't update the table.
            state_code = 'CA'
        else:
            state_code = clickData['points'][0]['location']

        heat_map_data = calculate_differences(data, state_code, heat_map_prop_type, compare_to)
        heat_map_data.to_csv(r'C:\Users\Eric C. Balduf\Documents\heat_map_data.csv')

        ctx = callback_context
        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == ui_ids.BTN_NXT:
            new_page = current_page + 1
        elif button_id == ui_ids.BTN_PREV:
            new_page = current_page - 1
        else:
            new_page = current_page
        total_pages = -(-len(heat_map_data) // 10)  # Ceiling division

        if new_page > total_pages:
            new_page = total_pages
        elif new_page < 1:
            new_page = 1

        # Paginate the data
        start_idx = (new_page - 1) * 10
        end_idx = start_idx + 10
        paginated_differences = heat_map_data[start_idx:end_idx]

        paginated_differences.to_csv(r'C:\Users\Eric C. Balduf\Documents\paginated_differences.csv')
        paginated_differences_filtered = paginated_differences[metric_list]
        paginated_differences_filtered.to_csv(r'C:\Users\Eric C. Balduf\Documents\paginated_differences_filtered.csv')

        paginated_differences_filtered_percentile = paginated_differences_filtered.fillna(0)

        # Extract the desired percentiles
        desired_percentiles = [5, 25, 50, 75]
        percentiles = [np.percentile(paginated_differences_filtered_percentile.values, p) for p in desired_percentiles]

        fig = px.imshow(
            paginated_differences_filtered,
            labels=dict(x="Metrics", y="Metros", color="Difference"),
            x=metric_list,
            y=paginated_differences['region'].tolist(),
            color_continuous_scale='deep',
            range_color=[percentiles[0], percentiles[-1]]
        )

        fig_metrics_added = add_heatmap_annotations(fig, paginated_differences_filtered)

        fig_metrics_added.update_layout(width=2000, height=800)
        fig_metrics_added.update_layout(coloraxis_colorbar=dict(
            tickvals=percentiles,
            ticktext=[f"{p * 100:.2f}%" for p in percentiles]
        ))
        return fig_metrics_added, new_page


    app.title = "purlieu"
    app.layout = create_layout(app, data, prop_type_options)
    app.run()
    conn.close()
