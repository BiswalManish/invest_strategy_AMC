#!/usr/bin/env python
# coding: utf-8

# # Part 2: Data cleaning
# 
#     > We have cleaned the files now we have to treat the missing values we found in rest of the columns.
#     > This time we will import from the cleaned csv files

# In[1]:


import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')


# In[2]:


#creating paths

rounds_path = '/Users/manish/Documents/Projects/data_science/investment_strategy/data/clean_data/rounds2_clean.csv' 
companies_path = '/Users/manish/Documents/Projects/data_science/investment_strategy/data/clean_data/companies_clean.csv'


# In[3]:


#creating dataframes
rounds = pd.read_csv(rounds_path)
companies = pd.read_csv(companies_path)


# In[4]:


#verifying the permalink columns unique entries in both the columns

print('rounds', len(rounds.company_permalink.unique()))
print('companies', len(companies.permalink.unique()))


#     > It seems to be working correctly.
#     > Now our job is missing value treatments 

# # Missing value treatment

# In[5]:


#checking missing values in bothe dataframes

print(rounds.isnull().sum())
print('--'*20)
print(companies.isnull().sum())


#     > lets create a master data frame for ease of analysis
#     > we can use pd.merge to merge on company_permalink column
#     > after merging we can drop any one of the permalink column as they are redundant

# In[6]:


#merging the two files
master = pd.merge(companies, rounds, how = 'inner',
                  left_on = 'permalink', right_on = 'company_permalink')
master = master.drop(columns = ['company_permalink'])
master.head()


# In[7]:


master.info()


#     > there we go we have succesfully merged the dataframes
#     > Also the company_permalink column has been dropped

# In[8]:


#missing entries in master df
print(master.isnull().sum())


# In[9]:


#percent of missing in each columns
print(100*master.isnull().sum()/len(master.index))


# Clearly, the column ```funding_round_code``` is useless (with about 73% missing values). Also, for the business objectives given, the columns ```homepage_url```, ```founded_at```, ```state_code```, ```region``` and ```city``` need not be used.

# In[10]:


#dropping the unnecessary columns
master = master.drop(columns = ['funding_round_code', 'homepage_url',
                                'founded_at', 'state_code', 'region', 
                                'city'])
master.head()


# In[11]:


#percent of missing in each columns
print(round(100*master.isnull().sum()/len(master.index),2))


# Missing columns include ```category_list```, ```country_code``` and ```raised_amount_usd```. 
# 
# We can not simply delete these columns as ```category_list``` will be used for merging with the mapping file.
# 
# ```country_code``` and ```raised_amount_usd``` are useful from business perspective.
# 
# We have to carefully tread through the ```raised_amount_usd``` column as it has about ```17%``` missing values
# 
# 

# In[12]:


#some stats of the raised amount column
master.raised_amount_usd.describe()


# The `mean` amount of funding is `10 million USD`.
# The `median` is about `1.7 million USD`.
# The highest amount invested is about `21.7 billion USD`
# The data is highly skewed and has very large outliers. This clearly inflate the mean.
# 
# This suggests we have no other option but to delete the missing values in `raised_amount_usd`
# as we can not impute them with mean or median

# In[13]:


#dropping the missing values 
master = master[~np.isnan(master.raised_amount_usd)]


# In[14]:


print(master.isnull().sum())
print('--'*20)
print(round(100*master.isnull().sum()/len(master.index),2))


# In[15]:


master.info()


# We can see the only `country_code` and `category_list` have missing values left 
# along with one entry in the `name` column. 
# 
# Lets check the country_code

# In[16]:


round(100*master.country_code.value_counts()/master.country_code.count(), 2)


# It looks like `USA` is the country with most companies around ``69.63%`` 
# of the non null values.Followed by `GBR`, `CAN`, `CHN` and `IND` with 
# `5.63%`, `2.94%`, `2.16%` and `1.85%` of the total countries.
# 
# Either we can delete the missing values or impute them with USA. 
# But since the % missing values in country_code is `~6%` we can del them as we have 
# enough data to carry on the analysis
# 
# Also since the missing category_list is about `0.65%` we can drop those entries as well.

# In[17]:


#deleting the entries with missing country_code
master = master[~pd.isnull(master.country_code)]
master.info()


# In[18]:


#printing the misising value after deleting the missing country_code entries
print(round(100*master.isnull().sum()/len(master.index),2))


# In[19]:


#deleting rows with missing category_list
master = master[~pd.isnull(master.category_list)]
master.info()


# In[20]:


#printing the misising value after deleting the missing category_list entries
print(round(100*master.isnull().sum()/len(master.index),2))


# In[21]:


#we can see only one entry without name. 
#lets have a look
master.loc[master.name.isnull(),:]


# In[22]:


#changing the name at the above loc to Tell_it_in
master.loc[98692,'name'] = 'Tell_it_in'


# In[23]:


#checking if it worked
master.loc[master.name.isnull(),:]


# In[24]:


#checking the name at the changed location
master.loc[98692,'name']


# In[25]:


#checking for missing values
print(master.isnull().sum())


# In[26]:


#checking the cleaned data
master.info()


# We have treated all the missing values.
# Now we have `88529` out of `114948` entries left after clean-up.
# We have about `78%` of our initial data. Which is low but as the data has `~89K` 
# entries, we can do some solid analysis to them.
# 
# Now we can put the cleaned master data to a csv file 

# In[27]:


#creating clean master csv file
#master.to_csv("master_clean.csv", index = False)


# ### Lets move to the Analysis notebook
