#!/usr/bin/env python
# coding: utf-8

# In[1]:


# We've to load multiple packages to do the analysis


# In[2]:


import numpy as np
import pandas as pd
import datetime as dt


# In[ ]:





# In[3]:


# Step 1. Importing the data


# In[13]:


# Load airbnb_price.csv in prices

prices = pd.read_csv("prices.csv")


# In[6]:


# Load airbnb_room_type.xlsx in xls

xls = pd.ExcelFile("room_types.xlsx")


# In[11]:


# Parse the first sheet from xls, room_types

room_types = xls.parse(0)


# In[12]:


# Load airbnb_last_review.tsv, reviews

reviews = pd.read_csv("reviews.tsv",sep = "\t")


# In[32]:


# Display the first few rows


# In[33]:


prices.head()


# In[34]:


reviews.head()


# In[35]:


room_types.head()


# In[ ]:





# In[36]:


# Check the dimensions of the dataset


# In[37]:


prices.shape


# In[38]:


reviews.shape


# In[40]:


room_types.shape


# In[41]:


# Check the data types of columns


# In[92]:


prices.dtypes


# In[43]:


reviews.dtypes


# In[44]:


room_types.dtypes


# In[45]:


# Get summary statistics


# In[46]:


prices.describe()


# In[47]:


reviews.describe()


# In[48]:


room_types.describe()


# In[49]:


# Check for missing values


# In[50]:


prices.isnull().sum()


# In[51]:


reviews.isnull().sum()


# In[52]:


room_types.isnull().sum()


# In[14]:


# Step 2. Cleaning the price column


# In[16]:


# Remove whitespace and string characters from prices column

prices["price"] = prices["price"].str.replace(" dollars", "")


# In[17]:


# Convert prices column to numeric datatype

prices["price"] = pd.to_numeric(prices["price"])


# In[ ]:





# In[18]:


# Step 3. Calculating average price


# In[22]:


prices.describe()


# In[164]:


# To Remove Outliers: Calculate the first quartile (Q1) and third quartile (Q3)

Q1 = prices["price"].quantile(0.25)
Q3 = prices["price"].quantile(0.75)


# In[165]:


# Calculate the interquartile range (IQR)

IQR = Q3 - Q1


# In[166]:


# Define the upper and lower bounds to identify outliers

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR


# In[167]:


# Filter the DataFrame to remove outliers

filtered_prices = prices[(prices["price"] >= lower_bound) & (prices["price"] <= upper_bound)]


# In[168]:


#  Resulting DataFrame after removing the outliers

print(filtered_prices.head())  


# In[169]:


# Subset prices for listings costing $0, free_listings

free_listings = prices["price"] == 0


# In[170]:


# Update prices by removing all free listings from prices

prices = prices.loc[~free_listings]


# In[171]:


# Calculate the average price, avg_price

avg_price = round(prices["price"].mean(), 2)


# In[172]:


avg_price


# In[58]:


# Step 4. Comparing costs to the private rental market


# In[59]:


# Add a new column to the prices DataFrame, price_per_month

prices["price_per_month"] = prices["price"] * 365 / 12


# In[75]:


prices["price_per_month"]


# In[63]:


# Calculate average_price_per_month

average_price_per_month = round(prices["price_per_month"].mean(), 2)


# In[65]:


average_price_per_month


# In[173]:


# listing costs, on average, per nigh  in New York City costs, on average, $3,100 per month.  


# In[68]:


difference = round((average_price_per_month - 3100),2)


# In[69]:


difference


# In[ ]:





# In[80]:


# Step 5. Cleaning the room_type column


# In[87]:


# Convert the room_type column to lowercase

room_types["room_type"] = room_types["room_type"].str.lower()


# In[88]:


room_types["room_type"]


# In[93]:


# Update the room_type column to category data type

room_types["room_type"] = room_types["room_type"].astype("category")


# In[95]:


room_types["room_type"].dtype


# In[96]:


# Create the variable room_frequencies

room_frequencies = room_types["room_type"].value_counts()


# In[97]:


room_frequencies


# In[ ]:





# In[98]:


# Step 6. What timeframe are we working with?


# In[99]:


# Change the data type of the last_review column to datetime

reviews["last_review"] = pd.to_datetime(reviews["last_review"])


# In[105]:


reviews["last_review"].dtype


# In[106]:


# Create first_reviewed, the earliest review date

first_reviewed = reviews["last_review"].dt.date.min()


# In[107]:


first_reviewed


# In[108]:


# Create last_reviewed, the most recent review date

last_reviewed = reviews["last_review"].dt.date.max()


# In[109]:


last_reviewed


# In[ ]:





# In[110]:


# Step 7. Joining the DataFrames


# In[111]:


# Merge prices and room_types to create rooms_and_prices

rooms_and_prices = prices.merge(room_types, how="outer", on="listing_id")


# In[118]:


rooms_and_prices


# In[112]:


rooms_and_prices.shape


# In[113]:


rooms_and_prices.describe()


# In[116]:


# Merge rooms_and_prices with the reviews DataFrame to create airbnb_merged

airbnb_merged = rooms_and_prices.merge(reviews, how="outer", on="listing_id")


# In[119]:


airbnb_merged.shape


# In[120]:


airbnb_merged.describe()


# In[117]:


airbnb_merged


# In[121]:


# Drop missing values from airbnb_merged

airbnb_merged.dropna(inplace=True)


# In[174]:


airbnb_merged


# In[175]:


# check for duplicates.
duplicates = airbnb_merged[airbnb_merged.duplicated(keep=False)]


# In[176]:


print(duplicates)


# In[ ]:





# In[123]:


# Step 8. Analyzing listing prices by NYC borough


# In[131]:


# Extract information from the nbhood_full column and store as a new column, borough

airbnb_merged["borough"] = airbnb_merged["nbhood_full"].str.partition(",")[0]


# In[134]:


print(airbnb_merged["borough"])


# In[135]:


# Group by borough and calculate summary statistics

boroughs = airbnb_merged.groupby("borough")["price"].agg(["sum", "mean", "median", "count"])


# In[137]:


boroughs


# In[138]:


# Round boroughs to 2 decimal places, and sort by mean in descending order

boroughs = boroughs.round(2).sort_values("mean", ascending=False)


# In[139]:


boroughs


# In[ ]:





# In[140]:


# Step 9. Price range by borough


# In[141]:


# Create labels for the price range, label_names

label_names = ["Budget", "Average", "Expensive", "Extravagant"]


# In[142]:


label_names


# In[143]:


# Create the label ranges, ranges

ranges = [0, 69, 175, 350, np.inf]


# In[145]:


ranges


# In[146]:


# Insert new column, price_range, into DataFrame

airbnb_merged["price_range"] = pd.cut(airbnb_merged["price"], bins=ranges, labels=label_names)


# In[152]:


airbnb_merged


# In[153]:


# Calculate occurence frequencies for each label, prices_by_borough

prices_by_borough = airbnb_merged.groupby(["borough", "price_range"])["price_range"].count()


# In[157]:


prices_by_borough


# In[ ]:





# In[158]:


# Step 10. Storing the final result


# In[159]:


solution = {'avg_price':avg_price,
            'average_price_per_month': average_price_per_month,  
            'difference':difference,          
            'room_frequencies':room_frequencies, 
            'first_reviewed': first_reviewed,
            'last_reviewed': last_reviewed,
            'prices_by_borough':prices_by_borough}
print(solution)


# In[162]:


# Export the DataFrame to a CSV file

airbnb_merged.to_csv('cleaned_and_merged_data.csv', index=False)


# In[163]:


airbnb_merged.size


# In[ ]:




