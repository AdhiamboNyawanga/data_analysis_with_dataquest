#!/usr/bin/env python
# coding: utf-8

# This project explores eBay Car Sales Data
# It aims at cleaning the data and analyzing the included used car listings
# The data dictionary provided with data is as follows:
# 
# 1. dateCrawled - When this ad was first crawled. All field-values are taken from this date.
# 2.  - Name of the car.
# 3. seller - Whether the seller is private or a dealer.
# 4. offerType - The type of listing
# 5. price - The price on the ad to sell the car.
# 6. abtest - Whether the listing is included in an A/B test.
# 7. vehicleType - The vehicle Type.
# 8. yearOfRegistration - The year in which the car was first registered.
# 9. gearbox - The transmission type.
# 10. powerPS - The power of the car in PS.
# 11. model - The car model name.
# 12. kilometer - How many kilometers the car has driven.
# 13. monthOfRegistration - The month in which the car was first registered.
# 14. fuelType - What type of fuel the car uses.
# 15. brand - The brand of the car.
# 16. notRepairedDamage - If the car has a damage which is not yet repaired.
# 17. dateCreated - The date on which the eBay listing was created.
# 18. nrOfPictures - The number of pictures in the ad.
# 19. postalCode - The postal code for the location of the vehicle.
# 20. lastSeenOnline - When the crawler saw this ad last online.

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


autos = pd.read_csv("autos.csv", encoding='Latin-1')


# In[3]:


autos


# In[4]:


autos.info()
autos.head()


# From the information above; there are 20 columns and none of them has null value. Also, only 5 columns have integer values the rest are objects.
# The column names use camelcase instead of Python's preferred snakecase, which means we can't just replace spaces with underscores.

# First step, we'll rename the column names from camelcase to snakecase. To do this, we series.map()method which will require us to first create a dictionary, with the current names as the keys and the modified names as the values as shown below.

# In[5]:


corrections = {
    "dateCrawled" : "date_crawled",
    "name" : "name",
    "seller" : "seller",
    "offerType" : "offer_type",
    "price" : "price",
    "abtest" : "abtest",
    "vehicleType": "vehicle_type",
    "yearOfRegistration": "registration_year",
    "gearbox": "gearbox",
    "powerPS" :"power_ps",
    "model": "model",
    "odometer" : "odometer",
    "monthOfRegistration" : "registration_month",
    "fuelType": "fuel_type",
    "brand": "brand",
    "notRepairedDamage": "unrepaired_damage",
    "dateCreated" : "ad_created",
    "nrOfPictures" : "nr_of_pictures",
    "postalCode" : "postal_code",
    "lastSeen": "last_seen"    
}


# Assign the dataframe.columns to a variable, map them then assign the modified column names back to the dataframe.columns.

# In[6]:


s = autos.columns


# In[7]:


s = s.map(corrections)
autos.columns= s


# In[8]:


autos.head()


# In[9]:


autos.describe(include='all')


# From the data above, the price and odometer columns are numeric values stored as text. For each column. 
# We therefore will 
# 1.Remove any non-numeric characters.
# 2.Convert the column to a numeric dtype.
# 3.Use DataFrame.rename() to rename the column to odometer_km

# In[10]:


autos["price"] = autos["price"].str.replace("$", "")
autos["price"] = autos["price"].str.replace(",", "")
autos["odometer"] = autos["odometer"].str.replace("km", "")
autos["odometer"] = autos["odometer"].str.replace(",", "")


# 2. Convert the column to a numeric dtype.

# In[11]:


autos["price"] = autos["price"].astype(float)
autos["odometer"] = autos["odometer"].astype(float)


# Use DataFrame.rename() to rename the column to odometer_km

# In[12]:


autos.rename({"odometer":"odometer_km"}, axis = 1, inplace = True)


# In[13]:


autos.head()


# In[14]:


autos["price"].unique().shape


# In[15]:


autos["price"].describe()


# In[16]:


autos["price"].value_counts().sort_index(ascending= False).head()


# In[17]:


autos["price"].value_counts().sort_index(ascending= True).head()


# In[18]:


autos.loc[autos["price"] > 1000000].sort_values("price").shape


# Below, we'll remove cars whose prices don't fall between the range of 1100(the minimum) and 1000000 dollars. Because it is unlickely to get second hand cars that go above 1000000 dollars.

# In[19]:


autos[autos["price"].between(1100, 1000000)]


# In[20]:


autos = autos[autos["price"].between(100, 10000000)]


# We'll annalyse the odomere_km column the same way we did the price column.

# In[21]:


autos["odometer_km"].unique()
autos["odometer_km"].unique().shape


# In[22]:


autos["odometer_km"].describe()


# In[23]:


autos["odometer_km"].value_counts().sort_index(ascending= False).head()


# In[24]:


autos["odometer_km"].value_counts().sort_index(ascending= True).head()


# In[25]:


print(autos[["date_crawled","ad_created", "last_seen"]])


# In[26]:


print("Distribution of values in the date_crawled column as percentages.")
autos['date_crawled'].str[:10].value_counts(normalize=True, dropna=False).sort_index()*100
#autos = autos['ad_created'].str[:10]
#autos = autos['last_seen'].str[:10]


# In[27]:


print("Distribution of values in the ad_created column as percentages.")
autos['ad_created'].str[:10].value_counts(normalize=True, dropna=False).sort_index()*100


# From the information above, the ad_created column was eddited from 11th June 2015 to 7th April 2016; approximately 10 months or 300 days. However, there are only 76 entry days recorded

# In[28]:


print("Distribution of values in the last_seen column as percentages.")
autos['last_seen'].str[:10].value_counts(normalize=True, dropna=False).sort_index()*100


# The last_seen_online column values were populated from 7th Mar 2016 to 4th Apr 2016 on a regular basis everyday varying in between 0.5 percent to 2.5 percent. However, in the last 3 days the numbers are above 10 perecent which are unusually high and seems like the data listings were taken down by the management just before closing the business operations

# In[29]:


autos["registration_year"].describe()


# One thing that stands out from the exploration we did in the last screen is that the registration_year column contains some odd values:
# 
# The minimum value is 1000, before cars were invented
# The maximum value is 9999, many years into the future
# Because a car can't be first registered after the listing was seen, any vehicle with a registration year above 2016 is definitely inaccurate. Determining the earliest valid year is more difficult. Realistically, it could be somewhere in the first few decades of the 1900s.
# 
# Let's count the number of listings with cars that fall outside the 1900 - 2016 interval and see if it's safe to remove those rows entirely, or if we need more custom logic.

# In[30]:


reg_years = autos[autos["registration_year"].between(1900, 2016)] ["registration_year"].value_counts(normalize = True).sort_index() * 100


# In[31]:


reg_yr_70pc = reg_years[reg_years.index > 1999].sum()
print("percentage of car registered since 2000: ", reg_yr_70pc)
reg_yr_90pc = reg_years[reg_years.index > 1995].sum()
print("percentage of car registered since 1996: ", reg_yr_90pc)
reg_yr_99pc = reg_years[reg_years.index > 1978].sum()
print("percentage of car registered since 1980: ", reg_yr_99pc)


# In[32]:


autos["brand"].unique()
autos["brand"].unique().shape


# In[33]:


autos["brand"].value_counts()


# From the data above, we have 40 unique brand names. We'll agregate half of the list ie cars with counts above 400.

# In[34]:


selected_data= autos["brand"].value_counts().head(20)


# In[35]:


aggregate_data = {}
for x in selected_data.index:
    price1 = autos[autos["brand"] == x]["price"]
    avg_price = price1.mean()
    aggregate_data[x] = avg_price
sorted_brand_price = dict(sorted(aggregate_data.items(), key = lambda item : item[1], reverse = True))
sorted_brand_price


# In[36]:


top_6_brands = autos["brand"].value_counts().index[:6]
mean_mileage = {}
mean_price = {}

for brand in top_6_brands:
    mileage_col = autos[autos["brand"] == brand]["odometer_km"]
    avg_mileage = mileage_col.mean()
    mean_mileage[brand] = avg_mileage
    
for brand in top_6_brands:
    price_col = autos[autos["brand"] == brand]["price"]
    avg_price = price_col.mean()
    mean_price[brand] = avg_price

mileage_series = pd.Series(mean_mileage)
price_series = pd.Series(mean_price)

mileage_df = pd.DataFrame(mileage_series, columns = ["mileage"])
mileage_df["price"] = price_series
mileage_df.sort_values("price", inplace = True, ascending = False)
print(selected_data[:6])
mileage_df


# From our above analysis, we can observe that Audi is the most highly priced car and Opel is the least priced car and both of them have similar mileages.
# 
# Ford has on the average the least mileage among all the brands which is one of the less expensive brands. But, Opel is more than 1000 USD less expensive then Ford but has as good mileage as the most expensive brand Audi.
# 
# So, it is not clear that there is any direct correation in betwwn the price of the car and their mileage.

# Identify categorical data that uses german words, translate them and map the values to their english counterparts.

# In[37]:


# Creating the mapping dictionary from 'German' to 'english' for all the columns reqired 
map_seller = {"privat":"private"}
map_offer_type = {"Angebot":"offer"}
map_vehicle_type = {
                        "kleinwagen": "small_cars",
                        "kombi": "station_wagon",
                        "cabrio": "convertible",
                        "andere": "other_types"
                    }
map_gearbox = {
                   "manuell": "manual",
                   "automatik": "automatic"
              }
map_fuel_type = {
                    "benzin": "petrol",
                    "electro": "electric"
                }

map_unrepaired_damage = {
                    "nein": "no",
                    "ja": "yes"
                }

#autos.loc[:,"seller"].replace(map_seller, inplace = True)
#autos.loc[:,"offer_type"].replace(map_offer_type, inplace = True)
#autos.loc[:,"vehicle_type"].replace(map_vehicle_type, inplace = True)
#autos.loc[:,"gearbox"].replace(map_gearbox, inplace = True)
#autos.loc[:,"fuel_type"].replace(map_fuel_type, inplace = True)
#autos.loc[:,"unrepaired_damage"].replace(map_unrepaired_damage, inplace = True)

autos.loc[:,"seller"] = autos.loc[:,"seller"].map(map_seller).copy()
autos.loc[:,"offer_type"] = autos.loc[:,"offer_type"].map(map_offer_type).copy()
autos.loc[:,"vehicle_type"] = autos.loc[:,"vehicle_type"].map(map_vehicle_type).copy()
autos.loc[:,"gearbox"] = autos.loc[:,"gearbox"].map(map_gearbox).copy()
autos.loc[:,"fuel_type"] = autos.loc[:,"fuel_type"].map(map_fuel_type).copy()
autos.loc[:,"unrepaired_damage"] = autos.loc[:,"unrepaired_damage"].map(map_unrepaired_damage).copy()
autos


# Convert the dates to be uniform numeric data, so "2016-03-21" becomes the integer 20160321
# The columns to be changed are as follows:
# 1. date_crawled
# 2. ad_created
# 3. last_seen_online

# In[38]:


#date_str = autos.loc[:,"date_crawled"].str[:10]
#date_str = date_str.str.replace("-","")
#print(autos.loc[:,"date_crawled"].dtype)
#print(autos.loc[:,"date_crawled"])



autos.loc[:,"date_crawled"] = autos.loc[:,"date_crawled"].str[:10].str.replace("-","").astype(int)
autos.loc[:,"ad_created"] = autos.loc[:,"ad_created"].str[:10].str.replace("-","").astype(int)
autos.loc[:,"last_seen"] = autos.loc[:,"last_seen"].str[:10].str.replace("-","").astype(int)
print(autos.loc[:,"last_seen"].dtype)
autos


# See if there are particular keywords in the name column that you can extract as new columns

# In[39]:


sport_utility = autos[autos["name"].str.contains("Sport", case= False)]
sport_utility


# There are 2593 rows in the name column with the keyword "sport". We can create a separate column named "sport_utility" and assign 'yes' or 'no'

# In[40]:


autos.loc[:,"sport_utility"] = "no"
autos.loc[autos["name"].str.contains("sport", case= False),"sport_utility"] = "Yes"
autos


# Find the most common brand/model combinations

# In[41]:


brand_model = autos["brand"] + "_" + autos["model"]
brand_model.describe()


# The data above shows that volkswagen_golf is the most common brand_model with 3876 counts.

# Split the odometer_km into groups, and use aggregation to see if average prices follows any patterns based on the mileage.

# In[43]:


autos["odometer_km"].unique()


# There are 13 unique values for mileage with the lowest being 5,000 and the highest is 150,000.
# 
# We can divide them into 3 groups:
# 

# In[44]:


low_mile_avg_price = autos.loc[autos["odometer_km"] <= 50000, "price" ].mean()
mid_mile_avg_price = autos.loc[autos["odometer_km"].between(50001,100000), "price"].mean()
high_mile_avg_price = autos.loc[autos["odometer_km"] > 100000, "price"].mean()

print("Mileage <= 50,000 : ", low_mile_avg_price, "\n")
print("50,000 < Mileage <= 100,000 : ", mid_mile_avg_price, "\n")
print("Mileage > 100,000 : ", high_mile_avg_price, "\n")


# From the data above, we can conclude that the higher the mileage, the cheaper the vehicle.
# 

# Finding out how much cheaper cars with damage are as compared to their non-damaged counterparts

# In[46]:


# Avg. Price of damaged cars
damaged_cars_prc = autos.loc[autos["unrepaired_damage"] == "yes","price"].mean()
# Avg. Price of non-damaged cars
undamaged_cars_prc = autos.loc[autos["unrepaired_damage"] == "no","price"].mean()

print("On average, damaged cars are cheaper than non-damaged cars by:")
print(undamaged_cars_prc - damaged_cars_prc)

