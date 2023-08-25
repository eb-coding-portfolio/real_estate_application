Application Research 

**Examples from Online**  
* Meh: https://github.com/mbruns13/redfin_housing_data
* Good: https://python.plainenglish.io/the-state-of-the-housing-market-using-pandas-to-analyze-housing-prices-%EF%B8%8F-eaf93c98d35a 
* Great: ? 

**Summary**   
I researched the internet and tried to leverage ChatGPT as much as possible to find examples of what I might want to build in the market analysis application. I wasnt able to find any great examples of the type of analysis I want to produce. Most of the examples online are ML or Multiple Linear Regression models that are trying to predict prices for a specific metro, which is useful but not something I am interested in doing for this use case. I found one example that uses the data I want to use (redfin) but I would rate it as meh overall, the bubble chart and bar charts dont tell me much I didnt already know. The one key takeaway I had from this was that I think a map visual would be really useful in my application. The second link above is a more closely aligned with how I might want to use housing data because it has an investment focused view on the data. I particularly liked that they used CAGR to measure appreciation, thats something I have used before to measure appreciation in a housing market. I also like that they showed the top 5 metros in there analysis, thats something I have seen in finance (top 10 losers and winners of a portfolio is common). As I have hinted at above there was nothing I would consider great, no link included for that. 
  
**Key Takeaways**  
* Would like to incorporate CAGR as a metric to measure the market appreciation aspect of returns
  * Note: There are 4 main components to returns in real estate: loan paydown, appreciation (market and forced), tax benefits (depreciation etc.), and cashflow 
* Would like to have a map visual of the US that is shaded according to a metric
  * CAGR to start but would like this to eventually be togglable to other metrics
* Would also like drill down capability so that when you click on the state you can see the same metric shaded at the metro level
* Would also like to incorporate another bar chart similar to the one at the link below on the 'ZHVI' tab of the Tableau chart
  * https://www.zillow.com/research/data/ 
* Would also like to have a chart that plots multiple metrics over time that users can add metrics from a larger list of metrics to.For example a user could plot pending_sales, median_sale_price_yoy, and avg_sale_to_list on the chart. This would be a sandbox area for users to look at a whole host of metrics and it would be good it if it had its own date and metro filters but was filtered by the state that was already selected in one of the above charts.
* 

Columns to Focus on 
*Note can really focus on the none yoy metrics first

* median_sale_price
* median_sale_price_yoy
* median_list_price
* median_list_price_yoy
* homes_sold
* homes_sold_yoy
* pending_sales
* new_listings
* inventory
* median_dom
* median_dom_yoy
* avg_sale_to_list
* avg_sale_to_list_yoy