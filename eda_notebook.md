Exploratory Analysis - HW 1  
  
Notes  
Dataset Selected: redfin_metro_market_tracker.tsv000  

**min/25/50/75th/max for all numeric variables**  
* -1 seems to be a min in a lot of the numerical columns, is this perhaps suppose to signify something else? Doesnt seem like a real value. Also some of the values seems unrealistically low, there is a value of 400 for a min median sales price which seems inaccurate.  
* 
**for each categorical variable that isn't a unique identifier, get value counts**  
* region type - There is only one value for which is 'metro' which makes sense because I am using the metro file from redfin
* is_seasonally_adjusted - There is only one value for which is 'f'
  * Does that mean seasonally adjust or not seasonally adjusted? ~Question to answer  
* region - I see some of the regions have a count of 680 which makes sense given the time series is a little over 11 years. The periodicity is 1 month and there are 5 property types for each month. 
  * Some are shorter than 680, why is that and how do I ensure everything is the same length? Does it need to be the same length? ~Question to answer
* state_code - looks good, 50 states + 1 for Washington DC
* property_type - 5 values: All Residential, Single Family Residential, Multi-Family (2-4 Unit), & Townhouse. Seems like there are a lot more single family residential records. 
* parent_metro_region - N/A

**number of null / na values in each column**  
city, state, price_drops_yoy, price_drops_mom, & price_drops are all over 50% null/NA with city and state being completely empty

  
**for all numeric variables, plot a single correlation matrix**  

![Correlation Matrix.png](..%2F..%2F..%2FPictures%2FReal%20Estate%20Results%2FCorrelation%20Matrix.png)  
  
**for all categorical variables, plot a bar chart**  
  
![is_seasonally_adjusted_bar.png](..%2F..%2F..%2FPictures%2FReal%20Estate%20Results%2Fis_seasonally_adjusted_bar.png)  
![property_type_bar.png](..%2F..%2F..%2FPictures%2FReal%20Estate%20Results%2Fproperty_type_bar.png)  
![region_type_bar.png](..%2F..%2F..%2FPictures%2FReal%20Estate%20Results%2Fregion_type_bar.png)  
![stat_code_bar.png](..%2F..%2F..%2FPictures%2FReal%20Estate%20Results%2Fstat_code_bar.png)  
  
**for a pair of numeric variables, plot a scatter plot.**  
![mediansaleprice_inventory_scatter.png](..%2F..%2F..%2FPictures%2FReal%20Estate%20Results%2Fmediansaleprice_inventory_scatter.png)
It seems as though supply is concentrated in the single family and condo property types. There also seems to be very little supply in the multi-family property type but they typically have a higher median sales price. The s