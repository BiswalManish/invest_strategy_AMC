# INVESTMENT_ASSIGNMENT_AMC

THIS is an assignment I did as part of my DS coursework.

# Data
This repository includes data directory that has raw and clean data. Follow the notebooks to use the data accordingly.
The raw_data consists of 3 files.
companies.csv
rounds2.csv
mapping.csv
The clean_data dir consists of
companies_clean.csv
rounds2_clean.csv
master_clean.csv
Instructions to when to use the data files are mentioned in the notebooks as comments


# Notebooks
# Data_cleaning 1 
is the first notebook.
Here we set path for our dataframes.
Copy your own path of the raw_data files

This notebook mainly resolves some encoding issues and case correction.
Go through the comments for details.

run the note book and check the results.
if you have some issues while running the .ipynb file.
Set the python environment according to that in the requirements.txt file


The last cell here contains the code to create clean csv files.
But those have been done and kept in the clean_data directory.
You can run these codes to copy clean the csv files if you want.


# Data_cleaning_2 
file takes the path from the clean_data file for
companies and rounds2 files

This notebook mainly deals with missing values and merges the above two files.
It finally stores the clean master file as .csv.
This task is already done.
If you want to do the same you can run the code in the last cell.

# Analysis 
This is the final analysis file.
Here we get funding_wise, country_wise and sector-wise analysis.

# Reports 
Reports directory has all the reports from the above three notebooks.
The plots dir contains some figures. You can create your own figures by runnning the .py in the src directory.

