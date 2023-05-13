#!/usr/bin/env python
# coding: utf-8

# # Part 1: Data cleaning

# In[1]:


import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')


# In[2]:


#creating path name var for the raw csv files

rounds2_path    = '/Users/manish/Documents/Projects/data_science/investment_strategy/data/raw_data/rounds2.csv'
companies_path = '/Users/manish/Documents/Projects/data_science/investment_strategy/data/raw_data/companies.csv'
mapping_path   = '/Users/manish/Documents/Projects/data_science/investment_strategy/data/raw_data/mapping.csv'


# # Initial Analysis

# ## 1. Companies

# In[3]:


#creating dataframes
companies = pd.read_csv(companies_path, encoding = 'ISO-8859-1')
companies.head()


# In[4]:


#basic info of companies file
companies.info()


# In[5]:


#checking unique & top values and frequencies of the top values in all the columns
companies.describe()


# In[6]:


#checking the missing values
companies.isnull().sum()


# ### Companies file analysis -
#     
#     Companies file has 66368 entries and 10 columns with various features
# 
#     1. permalink, home_url and name are three company specific identifiers and name column 
#         has 1 missing value, with home_url with 5038 missing values.
#     
#     2. category_list gives the industry category the company belongs to.
#     
#     3. country_code, state_code, region_code and city are geography specific identifiers 
#         and have some missing values.
#     
#     4. status has also some missing values along with founded_at.
#     
#     5. We will deal with each column one-by-one
#     
#     6. Lets get some initial analysis of rounds file.

# ## 2. Rounds

# In[7]:


#creating dataframe
rounds2 = pd.read_csv(rounds2_path, encoding = 'ISO-8859-1')
rounds2.head()


# In[8]:


#basic info
rounds2.info()


# In[9]:


# general analysis of  numerical columns
rounds2.describe()


# In[10]:


#getting data for rest of the columns
rounds2.drop(columns = ['raised_amount_usd']).describe()


# In[11]:


rounds2.isnull().sum()


# ### Rounds file analysis
# 
#     Rounds file has 114949 entries and 6 columns with various features
#     
#     1. company_permalink seems to be similar to that of the permalink column
#     in companies file
#     
#     2. fundaing_round_permalink is another name identifier for the funding round
#     
#     3. funding round type gives us the idea of the type of funding done.
#     
#     4. funding_round_code is another feature with codes about the funding round. 
#         1. It has 83809 missing values
#     
#     5. Raised_amount_usd gives the funding in USD.
#         1. Max amount raised is 21.27 billion USD
#         2. Min is 0 and average funding is 10 million USD
#         3. The average is inflated due the high outliers.

# ## 3. Checking the common permalink column in both companies and rounds2 file

#     * rounds2 has 90247 unique permalink 
#     * companies has 66368 unique permalink entries
#     * let us try to convert them to lower case and check

# In[12]:


#this function returns converted column to lower case
def convert_to_lower(df):
    
    print("column to convert to lower case:\n")
    column = input('> ').strip().lower()
    
    df[column] = df[column].apply(lambda x: x.lower())

    return df
    


# In[13]:

print("\n Convert rounds file's company_permalink column to lower case: \n")
rounds2 = convert_to_lower(rounds2)


# In[14]:

print("\nConvert companies file's permalink column to lower case:\n")
companies = convert_to_lower(companies)


# In[15]:


#checking the unique entries in both the data frame

print('rounds', len(rounds2.company_permalink.unique()))
print('companies', len(companies.permalink.unique()))


#     * This seems reasonable. BUt still there are two more unique entries in rounds2 df that 
#       is not present in companies df

# In[16]:


#Lets investigate further
rounds2.loc[~rounds2.company_permalink.isin(companies.permalink), :]['company_permalink']


#     * There seems to be some weird characters in the company_permalink in rounds file.
#     * Lets check the csv file to see if these entries are actually the same as in dataframe
#     * The csv file seems to have the above 7 entries in correct format.
#     * This means there is an issue in decoding the file in python
#     * The main reason that python is not able to decode is beacause of various languages this data 
#       is collected from various countries. 
#     * By searching some errors online, the following hack can be used

# In[17]:


rounds2['company_permalink'] = rounds2.company_permalink.str.encode('utf-8').str.decode('ascii', 'ignore')
companies['permalink']       = companies.permalink.str.encode('utf-8').str.decode('ascii', 'ignore')


# In[18]:


#lets if the hack worked
print('Uncommon permalink in rounds to that in companies:',
      rounds2.loc[~rounds2.company_permalink.isin(companies.permalink), :]['company_permalink'])

print('rounds', len(rounds2.company_permalink.unique()))
print('companies', len(companies.permalink.unique()))


#     * It seems the hack has worked.
#     * We can put these clean files separately and not bother about encoding

# In[19]:


#writing to clean csv files
#rounds2.to_csv("rounds2_clean.csv", index = False)
#companies.to_csv("companies_clean.csv", index = False)


# ### Lets move to data cleaning 2 notebook
