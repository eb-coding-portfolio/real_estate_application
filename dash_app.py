from dash import Dash, callback_context, no_update
import pandas as pd
from src.components.frontend.layout import create_layout, create_tab_1_content, create_tab_2_content
from dash.dependencies import Input, Output, State
import plotly.express as px
from utils import calculate_differences, add_heatmap_annotations, line_chart_predict
from src.components.frontend import ui_ids
from config import percentage_metric_list, table_columns
import numpy as np
import os
import plotly.graph_objs as go
# import psutil

from sqlalchemy import create_engine

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    DATABASE_URL = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
    engine = create_engine(DATABASE_URL)

    state_filter = 'state'

    data = pd.read_sql(f"SELECT * FROM market_tracker where region_type = '{state_filter}'", engine)
    global_max_date = pd.read_sql('select MAX(period_end) as max_date from market_tracker', engine)

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

        max_date = global_max_date.iloc[0, 0]

        map_df = map_input_df[(map_input_df['period_end'] == max_date) &
                              (map_input_df['region_type'] == 'state') &
                              (map_input_df['property_type'] == selected_property_type)][
            ['state_code', selected_metric]]

        # Calculate the 5th, 25th, 50th, and 75th percentiles for the selected metric
        p5 = np.percentile(map_df[selected_metric], 5)
        p25 = np.percentile(map_df[selected_metric], 25)
        p50 = np.percentile(map_df[selected_metric], 50)
        p75 = np.percentile(map_df[selected_metric], 75)

        if selected_metric in percentage_metric_list:
            hover_data = {selected_metric: ':.1%'}
            tickformat = '.1%'
        else:
            hover_data = None
            tickformat = None
        fig = px.choropleth(map_df, locations='state_code',  # DataFrame column with locations
                            color=selected_metric,  # DataFrame column with color values
                            locationmode="USA-states",  # built-in location mode for U.S. states
                            scope="usa",
                            color_continuous_scale='haline',
                            hover_data=hover_data,
                            range_color=(p5, p75),
                            )
        fig.update_coloraxes(colorbar_tickformat=tickformat, colorbar=dict(x=0.85, y=0.7))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            autosize=True
        )

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
        if clickData is None:
            # If no state has been clicked, don't update the table.
            state_code = 'CA'
        else:
            state_code = clickData['points'][0]['location']

        heat_map_data = calculate_differences(state_code, heat_map_prop_type, compare_to, engine)

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

        paginated_differences_filtered = paginated_differences[metric_list]

        paginated_differences_filtered_percentile = paginated_differences_filtered.fillna(0)

        # Extract the desired percentiles
        desired_percentiles = [5, 25, 50, 75]
        percentiles = [np.percentile(paginated_differences_filtered_percentile.values, p) for p in desired_percentiles]

        fig = px.imshow(
            paginated_differences_filtered,
            labels=dict(x="Metrics", y="Metros", color="Difference"),
            x=metric_list,
            y=paginated_differences['region'].tolist(),
            color_continuous_scale='haline',
            range_color=[percentiles[0], percentiles[-1]]
        )

        fig_metrics_added = add_heatmap_annotations(fig, paginated_differences_filtered)

        fig_metrics_added.update_layout(coloraxis_colorbar=dict(
            tickvals=percentiles,
            ticktext=[f"{p * 100:.1f}%" for p in percentiles]
        ))
        fig_metrics_added.update_coloraxes(colorbar=dict(x=0.9, y=0.7))
        fig_metrics_added.update_layout(
            height=675,
            width=900
        )

        return fig_metrics_added, new_page


    @app.callback(
        Output(ui_ids.LINE_CHART_ID, 'figure'),
        Input(ui_ids.HOUSING_TABLE_ID, 'clickData'),
        Input(ui_ids.PROPERTY_TYPE_DROP, 'value'),
    )
    def update_line_graph(clickData, line_prop_type):

        if clickData:
            # Safely extract the relevant data from clickData
            try:
                # Extract row and column indices from clickData
                metro = clickData['points'][0]['y']
                metric = clickData['points'][0]['x'].replace("_yoy", "")

                print(clickData)
            except (TypeError, KeyError, IndexError):
                print("Error extracting data from clickData:", clickData)
        else:
            metro = 'Anaheim, CA metro area'
            metric = 'median_sale_price'

        line_chart_df = line_chart_predict(metric, metro, line_prop_type, engine)
        line_chart_df['period_end'] = pd.to_datetime(line_chart_df['period_end'])  # Convert the date column to datetime
        line_chart_df = line_chart_df.sort_values(by='period_end')

        # Extract rows where lower and upper bounds are available
        predictions = line_chart_df.dropna()
        predictions.to_csv(r'C:\Users\Eric C. Balduf\Documents\pred_plot.csv')

        # Create an empty figure
        fig = go.Figure()

        # Add the confidence interval as a shaded area
        fig.add_trace(go.Scatter(
            x=predictions['period_end'].tolist() + predictions['period_end'].tolist()[::-1],
            y=predictions['lower bound'].tolist() + predictions['upper bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            name='Prediction Interval',
        ))

        # add plot line to graph
        fig.add_trace(go.Scatter(
            x=line_chart_df['period_end'],
            y=line_chart_df[metric],
            line=dict(color='rgba(0,0,255,0.5)'),
            mode='lines',
            name=metric,
            showlegend=False
        ))

        # Update layout options if needed
        fig.update_layout(
            yaxis_title=metric,
            xaxis_title='Date',
            title=f'{line_prop_type} property type for {metro} with 12 month prediction',
            height=675,
            width=900
        )

        return fig  # Return an empty string since we're not updating any visible component


    # Callback to switch tabs
    @app.callback(
        Output('tabs-content', 'children'),
        [Input('tabs', 'value')]
    )
    def update_tab(tab_name):
        if tab_name == 'tab1':
            return create_tab_1_content(prop_type_options, global_max_date)
        elif tab_name == 'tab2':
            return create_tab_2_content()


    @app.callback(
        [
            Output('markdown-modal', 'style'),
            Output('markdown-userguide', 'children')
        ],
        [
            Input('start-button', 'n_clicks'),
            Input('close-modal', 'n_clicks')
        ],
        [State('markdown-modal', 'style')]
    )
    def toggle_modal(start_btn, close_btn, modal_style):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'start-button' and start_btn:
            with open('assets/user_guide.md', 'r') as file:
                markdown_content = file.read()
            return {"display": "block"}, markdown_content
        elif button_id == 'close-modal' and close_btn:
            return {"display": "none"}, no_update
        else:
            return no_update, no_update

    # process = psutil.Process(os.getpid())
    # print("Memory Usage Before UI Startup:", process.memory_info().rss / 1024 / 1024, "MB")

    app.title = "Realty.Wise"
    app.layout = create_layout(app)
    # app.layout = create_layout(app, data, prop_type_options, active_tab='tab1')
    app.run(host='0.0.0.0', port=port)
