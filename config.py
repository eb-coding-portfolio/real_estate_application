metric_list = [
    'median_sale_price',
    'median_sale_price_yoy',
    'median_list_price',
    'median_list_price_yoy',
    'homes_sold',
    'homes_sold_yoy',
    'pending_sales',
    'new_listings',
    'inventory',
    'inventory_yoy',
    'median_dom',
    'median_dom_yoy',
    'avg_sale_to_list',
    'avg_sale_to_list_yoy'
]

percentage_metric_list = [
    'median_sale_price_yoy',
    'median_list_price_yoy',
    'homes_sold_yoy',
    'inventory_yoy',
    'avg_sale_to_list_yoy'
]

# Define the list of table columns including region, property_type, period_end and the metrics
table_columns = [
    'region',
    'region_type',
    'property_type',
    'period_end',
    'median_sale_price_yoy',
    'median_list_price_yoy',
    'homes_sold_yoy',
    'inventory_yoy',
    'avg_sale_to_list_yoy'
]


column_definitions = {
    'period_begin': 'TEXT',
    'period_end': 'TEXT',
    'period_duration': 'INTEGER',
    'region_type': 'TEXT',
    'region_type_id': 'INTEGER',
    'table_id': 'INTEGER',
    'is_seasonally_adjusted': 'TEXT',
    'region': 'TEXT',
    'city': 'TEXT',
    'state': 'TEXT',
    'state_code': 'TEXT',
    'property_type': 'TEXT',
    'property_type_id': 'INTEGER',
    'median_sale_price': 'REAL',
    'median_sale_price_mom': 'REAL',
    'median_sale_price_yoy': 'REAL',
    'median_list_price': 'REAL',
    'median_list_price_mom': 'REAL',
    'median_list_price_yoy': 'REAL',
    'median_ppsf': 'REAL',
    'median_ppsf_mom': 'REAL',
    'median_ppsf_yoy': 'REAL',
    'median_list_ppsf': 'REAL',
    'median_list_ppsf_mom': 'REAL',
    'median_list_ppsf_yoy': 'REAL',
    'homes_sold': 'REAL',
    'homes_sold_mom': 'REAL',
    'homes_sold_yoy': 'REAL',
    'pending_sales': 'REAL',
    'pending_sales_mom': 'REAL',
    'pending_sales_yoy': 'REAL',
    'new_listings': 'REAL',
    'new_listings_mom': 'REAL',
    'new_listings_yoy': 'REAL',
    'inventory': 'REAL',
    'inventory_mom': 'REAL',
    'inventory_yoy': 'REAL',
    'months_of_supply': 'REAL',
    'months_of_supply_mom': 'REAL',
    'months_of_supply_yoy': 'REAL',
    'median_dom': 'REAL',
    'median_dom_mom': 'REAL',
    'median_dom_yoy': 'REAL',
    'avg_sale_to_list': 'REAL',
    'avg_sale_to_list_mom': 'REAL',
    'avg_sale_to_list_yoy': 'REAL',
    'sold_above_list': 'REAL',
    'sold_above_list_mom': 'REAL',
    'sold_above_list_yoy': 'REAL',
    'price_drops': 'REAL',
    'price_drops_mom': 'REAL',
    'price_drops_yoy': 'REAL',
    'off_market_in_two_weeks': 'REAL',
    'off_market_in_two_weeks_mom': 'REAL',
    'off_market_in_two_weeks_yoy': 'REAL',
    'parent_metro_region': 'TEXT',
    'parent_metro_region_metro_code': 'INTEGER',
    'last_updated': 'TEXT'
}

column_definitions_pg = {'period_begin': 'String', 'period_end': 'String', 'period_duration': 'Integer', 'region_type': 'String', 'region_type_id': 'Integer', 'table_id': 'Integer', 'is_seasonally_adjusted': 'String', 'region': 'String', 'city': 'String', 'state': 'String', 'state_code': 'String', 'property_type': 'String', 'property_type_id': 'Integer', 'median_sale_price': 'Float', 'median_sale_price_mom': 'Float', 'median_sale_price_yoy': 'Float', 'median_list_price': 'Float', 'median_list_price_mom': 'Float', 'median_list_price_yoy': 'Float', 'median_ppsf': 'Float', 'median_ppsf_mom': 'Float', 'median_ppsf_yoy': 'Float', 'median_list_ppsf': 'Float', 'median_list_ppsf_mom': 'Float', 'median_list_ppsf_yoy': 'Float', 'homes_sold': 'Float', 'homes_sold_mom': 'Float', 'homes_sold_yoy': 'Float', 'pending_sales': 'Float', 'pending_sales_mom': 'Float', 'pending_sales_yoy': 'Float', 'new_listings': 'Float', 'new_listings_mom': 'Float', 'new_listings_yoy': 'Float', 'inventory': 'Float', 'inventory_mom': 'Float', 'inventory_yoy': 'Float', 'months_of_supply': 'Float', 'months_of_supply_mom': 'Float', 'months_of_supply_yoy': 'Float', 'median_dom': 'Float', 'median_dom_mom': 'Float', 'median_dom_yoy': 'Float', 'avg_sale_to_list': 'Float', 'avg_sale_to_list_mom': 'Float', 'avg_sale_to_list_yoy': 'Float', 'sold_above_list': 'Float', 'sold_above_list_mom': 'Float', 'sold_above_list_yoy': 'Float', 'price_drops': 'Float', 'price_drops_mom': 'Float', 'price_drops_yoy': 'Float', 'off_market_in_two_weeks': 'Float', 'off_market_in_two_weeks_mom': 'Float', 'off_market_in_two_weeks_yoy': 'Float', 'parent_metro_region': 'String', 'parent_metro_region_metro_code': 'Integer', 'last_updated': 'String'}