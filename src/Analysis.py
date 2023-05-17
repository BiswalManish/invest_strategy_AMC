#!/usr/bin/env python
# coding: utf-8

# # Part 3: Analysis
#     
#     In this notebook we will do funding_type, country analysis, and sector-wise analysis.
#     The sector-wise analysis will require us to merge the mapping file with the master. 
#     Hence we will do it at last.
#     Lets start with funding type analysis

# ## 1. Funding analysis
# 
#     In this we will look at the funding type and funding amount for each of the companies
#     We will also have a constraint of investment amount of 5-15 million USD.
#     So will look at the funding type with average amount in this range
# 

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')


# In[2]:


path = '/Users/manish/Documents/Projects/data_science/investment_strategy/data/clean_data/master_clean.csv'


# In[3]:


master = pd.read_csv(path)


#making a copy of the master file to work on
df = master.copy()
df.head()


# In[4]:


#top investing types
print(df.funding_round_type.value_counts())
print('--'*20)
print(round(100*df.funding_round_type.value_counts()/len(df.index), 2))


#     Types of funding-
# 
#     venture - a sum of money investors commit for investment in early-stage companies. 
#               The investors who supply the fund with money are designated as limited partners.
#     
#     seed - is the first official equity funding stage.
#     
#     debt_financing - loan
#     
#     angel - one-time/ongoing investment in return for equity
#     
#     grant - usually from a non-profit
#     
#     private_equity - investment on a private company in return for equity
#     
#     convertible_notes- investor would be loaning money to a startup and instead of a return in 
#                        the form of principal plus interest, the investor would receive equity in the company.
#     
#     equity_crowdfunding -  Equity crowdfunding is the online offering of private company securities 
#                            to a group of  people for investment
#     
#     post_ipo_equity- equity based investment is done after the company has gone public.
#     
#     product_crowd_funding - it seems it is another form of crowd funding but based on product.
#                             We have to look further
#     
#     post_ipo_debt - debt based investment is done after the company has gone public.
#     
#     non_equity_assistance - funding without getting equity on the company, 
#                             these can be futures contract or any other OTC tools
#     
#     secondary_market- buying and selling securities already owned.
#     

#     Sparks Fund wants to invest in the funding type as invested by other companies.
#     THis seems to be pattern for a firm that is trying to invest in startups or are 
#     in early phase of business.
#     
#     
#     Keeping this in mind following are the appropriate investment statergies - 
#     1. venture
#     2. seed
#     3. angel
#     4. private_equity
#     5. convertible_notes
#     6. equity_crowdfunding
#     7. debt_financing
#     8. non_equity_assistance
#     
#     We can further drop non_equity_assistance as it has only `60` investors 
#     which is the least popular funding type.

# In[5]:


#lets look at the funding_round_type categories
df.funding_round_type.unique()


# In[6]:


# keeping the necessary funding types in the data frame and removing the rest
funding_types = ['venture', 'seed', 'convertible_note',
                'private_equity', 'angel', 'equity_crowdfunding',
                'debt_financing']
df = df[df['funding_round_type'].isin(funding_types)]


# In[7]:


#checking the funding round type column
df.funding_round_type.value_counts()


# We will investigate each type of funding type and match the based on the
# raised amount as our constraint is `5-15 million USD`
# 

# In[8]:


#box plots to check the raised amounts stats
plt.figure(figsize = (10,6))
plt.grid()
sns.boxplot(y = df.raised_amount_usd)
plt.title("Raised_amount_USD")
plt.yscale('log')
plt.show()


# In[9]:


#common stats of raised amount
df.describe()


# The mean amount is about `9.8 million USD` and the median amount is `1.9 million USD`

# In[10]:


#checking the summary stats for various investment types
plt.figure(figsize = (10,6))
plt.grid()
sns.boxplot(y = df.raised_amount_usd, x = df.funding_round_type)
plt.yscale('log')
plt.title('Raised_amount_USD vs funding_type')
plt.xticks(rotation = 45)
plt.show()


# In[11]:


#checking the summary stats
pd.pivot_table(data = df, values = 'raised_amount_usd', columns = 'funding_round_type',
              aggfunc = np.mean)


# In[12]:


pd.pivot_table(data = df, values = 'raised_amount_usd', columns = 'funding_round_type',
              aggfunc = np.median)


# We see the average and median funding amount have huge differences. This is because of outliers in 
# the data. So its more appropriate to choose the `median` value to get the basic stat
# of each funding_type

# In[13]:


#checking the median values in order
print(df.groupby('funding_round_type')['raised_amount_usd'].median().sort_values(ascending = False))


# The private_equity type funding has a median funding type of about `20 MM USD`
# this is beyond the range of Sparks Fund.
# 
# The most suitable is venture type funding which has a median amount of `5 MM USD`
# 
# The rest all are less than the amount Sparks Funds are looking to invest.

# In[14]:


# reducing the data frame to only contain venture type funds
df = df[df['funding_round_type'] == 'venture']

#checking 
df.funding_round_type.value_counts()


# We have successfully deleted other funding types

# ## 2. Country Analysis
#         
#        This analysis requires those countries where english is the official language or 
#        common speaking language
#        

# In[15]:


#checking the dataframe
df.shape


# In[16]:


country_wise_investments = df.groupby('country_code')['raised_amount_usd'].sum().sort_values(ascending = False)


# In[17]:


#Lets check where the most investments are occuring
country_wise_investments[:10]


# Out of the top ten companies `USA`, `GBR`, `IND`, `CAN` are the top english speaking countries
# or countries with official language as english.

# In[18]:


top_4 = ['USA', 'GBR', 'IND', 'CAN']


# In[19]:


#reducing the data frame to include only these companies
df = df[df['country_code'].isin(top_4)]
df.shape


# The reduction leaves us with `40049` companies out of `47809`

# In[20]:


#checking median investment amount of the countries
pd.pivot_table(data = df, values = 'raised_amount_usd', columns = 'country_code',
              aggfunc = np.median)


# In[21]:


#checking investments in various comapanies by country and status of the company
pd.pivot_table(data = df, values = 'raised_amount_usd', columns = ['country_code', 'status'],
              aggfunc = np.median)


# In[22]:


#checking some plots
plt.figure(figsize = (10,6))
plt.grid()
sns.boxplot(y = df['raised_amount_usd'],  x = df['country_code'])
plt.title("Raised_amount_USD vs top_4 countries")
plt.yscale('log')
plt.show()


# In[23]:


#checking investments in companies according to status of the company
plt.figure(figsize = (10,6))
plt.grid()
sns.boxplot(y = df['raised_amount_usd'],  x = df['country_code'], hue = df['status'])
plt.title("Raised_amount_USD vs top_4 countries according to status")
plt.yscale('log')
plt.show()


# It shows `IND` has the highest median investments among all countries with `7.5 MM USD`.
# This is followed by `USA`, `GBR` and `CAN`
# 
# We also plotted a graph for the companies with present status. 
# Although we are not needed to know the status but we should be able to check which are operating and those that 
# are closed.
# 
# We will check on this after checking the sectorwise analysis

# ## 3. Sector-wise Analysis
# 
#        There is a mapping file for mapping the sectors into some categories.
#        But first lets check the category_list of the dataframe 

# In[24]:


df.category_list.value_counts()


# There are some entries where we have multiple categories. Where some have sub_categories.
# The `first` name must be the `main category` and this must be used to merge with mapping file

# In[25]:


#getting the first name of the multiple category entries
df['category_list'].apply(lambda x : x.split('|')[0]).value_counts()


# It seems to be working

# In[26]:


#replacing the category list columns
df['category_list'] = df['category_list'].apply(lambda x : x.split('|')[0])


# In[27]:


#checking
df['category_list'].value_counts()


# In[28]:


#checking everything else is intact
df.head()


# In[29]:


#lets for the sake of not messing with case errors convert the category_list to lower case
df['category_list'] = df['category_list'].apply(lambda x : x.lower())


# In[30]:


#checking everything else is intact
df.head()


# In[31]:


#now lets check the mapping file.
mapping_path = '/Users/manish/Documents/Projects/data_science/investment_strategy/data/raw_data/mapping.csv'

mapping  = pd.read_csv(mapping_path)


# In[32]:


#checking for null values
mapping.info()


# Mapping file has `10` columns for various categories, where `category_list` columnn has `1 missing value`
# Lets check that entry

# In[33]:


mapping[mapping['category_list'].isnull()]


# In[34]:


#dropping the null column
mapping = mapping[~mapping['category_list'].isnull()]


# In[35]:


mapping.info()


# Now mapping file has 9 column with no null values

# In[36]:


#converting category_list to lower case
mapping.category_list = mapping.category_list.apply(lambda x : x.lower())


# ### Checking the mapping file with df

# In[37]:


#lets check whether each category in df is present in mapping file
df[~df['category_list'].isin(mapping.category_list)]['category_list'].value_counts()


# It seems those that have management, analytics, finance are mostly not present in mapping file
# This seems odd as these are valid categories.
# Lets check the mapping file category list that are not present in df.

# In[38]:


#checking category list in mapping that are not present in df
mapping[~mapping.category_list.isin(df.category_list)].category_list.value_counts()[:20]


# We see a pattern here that `0` are present within strings which seems to be in place of `na`

# In[39]:


#lets rectify this
mapping.category_list = mapping.category_list.apply(lambda x : x.replace('0', 'na'))


# In[40]:


#checking category list in mapping that are not present in df
mapping[~mapping.category_list.isin(df.category_list)].category_list.value_counts()


# In[41]:


#lets check whether each category in df is now present in mapping file
df[~df['category_list'].isin(mapping.category_list)]


# In[42]:


#lets check these index in the original master file
index_to_check = df[~df['category_list'].isin(mapping.category_list)].index


# In[43]:


len(index_to_check)


# In[44]:


#checking the data against the status and name
pd.pivot_table(data = master.iloc[index_to_check,:],
              columns = ['status', 'name', 'category_list'])


# We see there are 15 companies which do not have categories in the mapping file we can either impute them 
# or delete them.
# 
# The raised amount in Velocomp, Sense, Onspring Technologies, Healthtell, Consensus Point, ShantiNiketan Inc. 
# have investments in the SFs range.
# 
# Lets work on these entries

# In[45]:


#companies to work on
list_companies =['Velocomp', 'Sense', 'Onspring Technologies', 'HealthTell', 
                 'Consensus Point']


# In[46]:


df[df.name.isin(list_companies)]


# THe enterprise 2.0 category is present in the csv file but not in the data frame meaning 
# this means when we converte 0's to na it became enterprise 2.na
# 
#     We have to convert it to enterprise 2.0
#     
#     Also the greentech can be converted to green as it is a software company/clean tech as can be 
#     seen from the master file.
#     
#     Adaptive equipment can be change to sporting goods as sporting goods is present in mapping file
#     
#     We can convert biotechnology and semiconductors to biotechnology
#     

# In[47]:


#checking our first assumption
mapping.loc[mapping.category_list == 'enterprise 2.na']


# In[48]:


#replacing it
mapping.category_list = mapping.category_list.apply(lambda x : x.replace('enterprise 2.na' ,
                                                                         'enterprise 2.0'))
mapping.loc[mapping.category_list == 'enterprise 2.0']


#     Now lets convert rest of the categories in df

# In[49]:


#checking greentech loc
df.loc[df.category_list == 'greentech']


# In[50]:


#replace greentech to green
df.category_list = df.category_list.apply(lambda x : x.replace('greentech' ,
                                                                         'green'))
df.loc[df.category_list == 'green']


# In[51]:


#replacing adaptive equipment by sports good
df.loc[df.category_list == 'adaptive equipment']


# In[52]:


#here is an issue as adaptive technology is present in dolores speech products and velocomp
#but since we have only chosen velocomp we drop dolores speech
df = df.loc[df.name != 'Dolores Speech Products']


# In[53]:


#checking
df.loc[df.name == 'Dolores Speech Products']


# In[54]:


#replacing adaptive equipment by sports good
df.loc[df.category_list == 'adaptive equipment']


# In[55]:


df.category_list = df.category_list.apply(lambda x : x.replace('adaptive equipment',
                                                               'sporting goods'))


# In[56]:


#checking
df.loc[df.category_list == 'sporting goods']


# In[57]:


#replacing biotechnolgy and semiconductors
df.loc[df.category_list == 'biotechnology and semiconductor']


# In[58]:


df.category_list = df.category_list.apply(lambda x : x.replace('biotechnology and semiconductor',
                                                               'biotechnology'))

df.loc[df.name == 'HealthTell']


#     Now lets check the df file again
#     

# In[59]:


#lets check whether each category in df is now present in mapping file
df[~df['category_list'].isin(mapping.category_list)]


# In[60]:


df[~df['category_list'].isin(mapping.category_list)].shape


# In[61]:


df.shape


# In[62]:


#dropping these columns
df = df[df['category_list'].isin(mapping.category_list)]
df.shape


# In[63]:


#lets check again
df[~df['category_list'].isin(mapping.category_list)]


# In[64]:


#also dropping those categories in mapping file which are not in the df file 
mapping.shape


# In[65]:


mapping[~mapping.category_list.isin(df.category_list)].shape


# In[66]:


mapping = mapping[mapping.category_list.isin(df.category_list)]

print(mapping.shape)
mapping[~mapping.category_list.isin(df.category_list)].shape


#     so we have succesfully cleaned all the columns and now we can do the merge

# ### Merging the mapping and df files on category_list

# In[67]:


df = pd.merge(df, mapping, on = 'category_list')
df.info()


# In[68]:


df.head()


#     The merging resulted in a wide format for the sectors
#     
#     We can use pd.melt function to convert them into long format  
#     Now for that we need the sectors from the mapping file as value_vars
#     and rest of the columns as id_vars
#     
#     Keep the values column obtained thus, where values are 1
#     Convert the variable column to sector
#     check the shape of the dataframe again

# In[69]:


#setting value vars and id_vars
value_vars = list(mapping.drop(columns = ['category_list'], axis =1).columns)
id_vars = list(df.drop(columns = value_vars, axis = 1).columns)
print(value_vars)
print('--'*20)
print(id_vars)


# In[70]:


long_df = pd.melt(frame = df, id_vars = id_vars, value_vars = value_vars)


# In[71]:


long_df.head()


# In[72]:


long_df.shape


# In[73]:


#dropping where values are 0 and dropping the value column
long_df = long_df[long_df.value == 1]
long_df = long_df.drop(columns = ['value'], axis =1)
long_df.shape


# In[74]:


#renaming the variable column to sector
long_df = long_df.rename(columns = {'variable' : 'sector'})


#     We have succesfully managed to convert to long format as the shape is same as our original df.
#     We also have set a new column called sector where we can do our final analysis.
#     
#     Now our only job left is to find the companies where the range of investment is in the range of 
#     5 - 15 MM USD

# In[75]:


#changing the final df
df = long_df[(long_df.raised_amount_usd >= 5000000) & (long_df.raised_amount_usd <= 15000000)]
df.head()


# ### Some final statistical analysis
# 

# In[76]:


sector_wise_df = df.groupby(['country_code', 'sector']).raised_amount_usd.agg(['sum', 'mean', 
                                                                              'median', 'count'])


# In[77]:


sector_wise_df


# In[78]:


#sector_wise_df.to_csv('final_report.csv', index = True)


# In[79]:


plt.figure(figsize = (10,8))
sns.barplot(x='sector', y='raised_amount_usd', hue='country_code', data=df, estimator=np.sum)
plt.yscale('log')
plt.xticks(rotation = 90)
plt.grid()
plt.title('Total Invested Amount (USD)')


# In[80]:


plt.figure(figsize = (10,8))
sns.countplot(x='sector', hue='country_code', data=df)
plt.xticks(rotation = 90)
plt.yscale('log')
plt.grid()
plt.title('Number of Investments')


# In[81]:


plt.figure(figsize = (10,8))
sns.barplot(x='sector', y='raised_amount_usd', hue='country_code', data=df, estimator=np.median)
plt.xticks(rotation = 90)
plt.grid()
plt.title('Median investment')
plt.show()


#     1. In CAN highest amount is invested in cleantech/semiconductores followed by others.
#        With median investment of 9.07 MM USD and 8.5 MM USD respectively.
#        Total companies are 112 and 109 respectively
#        
#     2. In GBR highest amount invested is in others followed by cleantech/semiconductors.
#        Median investment is about 8.73 and 8.95 MM USD respectively.
#        Total companies are 147 and 130 respectively.
#     
#     3. In IND most investments are in others category followed by Social, Finance, Analytics, Advertising.
#        Median investment of 9.21 and 9.18 MM USD respectively.
#        Total companies are 110 and 60 respectively.
#     
#     4. USA is the leading hub for companies and investments. 
#        With Others leading followed by Social, Finance, Analytics, Advertising.
#        Median investment are 8.92 and 8.77 MM USD respectively.
#        Total companies count is also very high with 2950 and 2714 respectively
#     
# #### Note. All these investments are of English speaking countries with venture type funding between 5 to 15 MM USD of investments each.
#     
#     
#   
#        
