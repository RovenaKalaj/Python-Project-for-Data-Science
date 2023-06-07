#!/usr/bin/env python
# coding: utf-8

# # Extracting and Visualizing Stock Data

# ## Description
# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.
# 
# ## Table of Contents
# Define a Function that Makes a Graph
# Question 1: Use yfinance to Extract Stock Data
# Question 2: Use Webscraping to Extract Tesla Revenue Data
# Question 3: Use yfinance to Extract Stock Data
# Question 4: Use Webscraping to Extract GME Revenue Data
# Question 5: Plot Tesla Stock Graph
# Question 6: Plot GameStop Stock Graph
# 

# In[9]:


get_ipython().system('pip install yfinance bs4 nbformat')


# In[10]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# **Define Graphing Function
# In this section, we define the function make_graph. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.

# In[11]:


def make_graph(stock_data, revenue_data, stock):
    #stock_data is data frame that must contain Date and Close columns
    # revenue_data is data frame with revenue data must contain Date and Revenue cols
    # stock name, a string.
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ## Question 1: Use yfinance to Extract Stock Data
# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is TSLA.

# In[12]:


tsla_ticker = yf.Ticker("TSLA")


# Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to max so we get information for the maximum amount of time.

# In[13]:


tesla_data = tsla_ticker.history(period="max") 


# Reset the index using the reset_index(inplace=True) function on the tesla_data DataFrame and display the first five rows of the tesla_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.

# In[14]:


# type(tesla_data) # this is a pd Dataframe
# print(tesla_data.head())
tesla_data.reset_index(inplace=True)
print(tesla_data.head())


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data
# Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named html_data.

# In[15]:


url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data = requests.get(url, "html.parser").text
type(html_data)


# Parse the html data using beautiful_soup.

# In[17]:


soup = BeautifulSoup(html_data, 'html5lib')
type(soup)


# Using BeautifulSoup or the read_html function extract the table with Tesla Quarterly Revenue and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue.

# In[18]:


table_element = soup.find_all("table")[1]
tesla_revenue = pd.read_html(str(table_element))
tesla_revenue = tesla_revenue[0]
tesla_revenue.columns = ['Date', 'Revenue']
#print(tesla_revenue.head())


# In[ ]:


#Execute the following line to remove the comma and dollar sign from the Revenue column


# In[19]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
#print(tesla_revenue.head())


# In[20]:


#Execute the following lines to remove an null or empty strings in the Revenue column.


# In[21]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[22]:


tesla_revenue.tail()


# ## Question 3: Use yfinance to Extract Stock Data

# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.

# In[24]:


gme_ticker = yf.Ticker("GME")


# Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data. Set the period parameter to max so we get information for the maximum amount of time.

# In[25]:


gme_data = gme_ticker.history(period="max")
#print(gme_data)


# #Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.

# In[27]:


gme_data.reset_index(inplace=True)
gme_data.head()


# ## Question 4: Use Webscraping to Extract GME Revenue Data
# Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named html_data.

# In[28]:


url2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data = requests.get(url2).text


# In[29]:


#Parse the html data using beautiful_soup.


# In[30]:


soup = BeautifulSoup(html_data, "html5lib")


# Using BeautifulSoup or the read_html function extract the table with GameStop Quarterly Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns Date and Revenue. Make sure the comma and dollar sign is removed from the Revenue column using a method similar to what you did in Question 2.

# In[31]:


gme_revenue = pd.read_html(url)[1]
#print(gamestop_revenue.head())
gme_revenue.columns = ["Date", "Revenue"]
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(",|\$","")
#print(gamestop_revenue.head())


# In[33]:


gme_revenue.tail()


# ## Question 5: Plot Tesla Stock Graph
# Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the make_graph function is make_graph(tesla_data, tesla_revenue, 'Tesla'). Note the graph will only show data upto June 2021.

# In[35]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# ## Question 6: Plot GameStop Stock Graph
# Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the make_graph function is make_graph(gme_data, gme_revenue, 'GameStop'). Note the graph will only show data upto June 2021.

# In[37]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




