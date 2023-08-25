import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore


file_path = r'C:\Users\Eric C. Balduf\OneDrive\Documents\my-local-repo\python-fundamentals\Data\Redfin\redfin_metro_market_tracker.tsv000'
second_file_path = r'C:\Users\Eric C. Balduf\OneDrive\Documents\my-local-repo\python-fundamentals\Data\Population\cbsa-est2022.csv'
excel_path = r'C:\Users\Eric C. Balduf\OneDrive\Documents\\'

#changing the encoding of the file so I can read it into pandas
with open(second_file_path, 'r', encoding='cp1252') as file:
    content = file.read()

with open(second_file_path, 'w', encoding='utf-8') as file:
    file.write(content)


df_metro = pd.read_csv(file_path, delimiter='\t')
df_pop_2022 = pd.read_csv(second_file_path)
df_pop_2022_filtered = df_pop_2022.copy()
df_pop_2022_filtered = df_pop_2022_filtered[df_pop_2022_filtered['LSAD'] == 'Metropolitan Statistical Area']
print(len(df_pop_2022_filtered))


df_metro_ex_all_res = df_metro[df_metro['property_type'] != 'All Residential']


#get a summarization of all of the data columns. Be sure to include:

summary_stats = df_metro.describe().round(2)


desired_stats = summary_stats.loc[['min', '25%', '50%', '75%', 'max']]

columns_to_drop = ['period_duration', 'region_type_id', 'table_id', 'city', 'state', 'property_type_id', 'parent_metro_region_metro_code']

#min/25/50/75th/max for all numeric variables
desired_stats_final = desired_stats.drop(columns=columns_to_drop)

column_types = df_metro.dtypes

date_columns = ['period_begin', 'period_end', 'last_updated']

df_metro[date_columns] = df_metro[date_columns].apply(pd.to_datetime)

column_types = df_metro.dtypes


excel_writer = pd.ExcelWriter(f'{excel_path}eda_results.xlsx', engine='openpyxl')

desired_stats_final.to_excel(excel_writer, sheet_name="desired_stats_final", index=True)

#for each categorical variable that isn't a unique identifier,get value counts
for column in df_metro.columns:
    if pd.api.types.is_object_dtype(column_types[column]) or pd.api.types.is_categorical_dtype(column_types[column]):
        value_counts = df_metro[column].value_counts().reset_index()
        sheet_name = f"{column}_val_cnt"
        value_counts.to_excel(excel_writer, sheet_name=sheet_name, index=False)

excel_writer._save()

#number of null / na values in each column
null_counts = df_metro.isnull().sum()
null_counts = null_counts.reset_index()
null_counts.columns = ['Column', 'Count']

null_counts.to_excel(excel_writer, sheet_name="null_counts", index=False)


null_counts_pct = (df_metro.isnull().sum() / len(df_metro)) * 100
null_counts_pct = null_counts_pct.reset_index()
null_counts_pct.columns = ['Column', 'Percent of Total Rows']
null_counts_pct = null_counts_pct.sort_values(ascending=False, by='Percent of Total Rows')

null_counts_pct.to_excel(excel_writer, sheet_name="null_counts_pct", index=False)

excel_writer._save()

#for all numeric variables, plot a single correlation matrix
num_list = []
for col in df_metro_ex_all_res.columns:

    if pd.api.types.is_numeric_dtype(df_metro_ex_all_res[col]):
        num_list.append(col)

subset_corr_df = df_metro_ex_all_res[num_list].drop(columns=columns_to_drop)

exclude_columns = [col for col in subset_corr_df.columns if 'mom' in col or 'yoy' in col]

subset_corr_df_filtered = subset_corr_df.loc[:, ~subset_corr_df.columns.isin(exclude_columns)]


correlation_matrix = subset_corr_df_filtered.corr()

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()
plt.title('Correlation Matrix')

#for all categorical variables, plot a bar chart

for column in df_metro_ex_all_res.columns:
    if df_metro_ex_all_res[column].dtype != 'float64' and  df_metro_ex_all_res[column].dtype != 'int64':
        plt.figure()
        df_metro_ex_all_res[column].value_counts().plot(kind='bar')
        plt.title(column)
        plt.show()



#Plot a scatter plot
sns.scatterplot(df_metro_ex_all_res, x='inventory', y='median_sale_price', hue="property_type")
plt.ticklabel_format(style='plain', axis='y')
plt.title('Scatter Plot Inventory vs. Median Sale Price')
plt.show()




#normalize a variable
df_metro_ex_all_res_copy = df_metro_ex_all_res.copy()

df_metro_ex_all_res_copy['inventory_normalized'] = zscore(df_metro_ex_all_res_copy['inventory'].dropna())
df_metro_ex_all_res_copy['median_sale_price_normalized'] = zscore(df_metro_ex_all_res_copy['median_sale_price'].dropna())

#If there are any free text fields, note them for future exploration

#load a second data set and find a way to join it to another dataset

merged_df = pd.merge(df_metro, df_pop_2022_filtered, left_on='parent_metro_region_metro_code', right_on='CBSA', how='left')

print(merged_df[['parent_metro_region_metro_code', 'CBSA']])







