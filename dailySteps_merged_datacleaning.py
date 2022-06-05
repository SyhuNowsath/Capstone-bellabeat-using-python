#-----------------------------------------------------
#-----------------Data Cleaning-----------------------
#-----------------------------------------------------

#File Name:dailyCalories_merged.csv
#--------------------Authors--------------------------
#Syhu Nowsath Ali  syhu91@gmail.com
#Sathyanarayanan S narayanansathya2108@gmail.com
#-----------------------------------------------------

#-----------------------------------------------------
#We considered three process of Data Cleaning:
#    1.Eliminating Redundancy/Duplicates
#    2.Eliminating Missing Values
#    3.Outliers Analysis
#-----------------------------------------------------


#Importing Necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

#Importing CSV file as Pandas Dataframe
daily_steps = pd.read_csv(r'dailySteps_merged.csv')
print("The uploaded csv contains:",daily_steps.shape[0],"Rows")
print(daily_steps)
#940 rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(daily_steps['Id'], daily_steps['StepTotal'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Steps Taken')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------


#-----------------Redundency Analysis-----------------

#created a list to check if there are any duplicates

duplicates_steps_list = daily_steps[daily_steps.duplicated(keep = False, subset=['Id','ActivityDay'])]
print("Number of Duplicates:",duplicates_steps_list.shape[0])
print(duplicates_steps_list)
#No duplicates found
#-----------------------------------------------------



#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------
#Created list in order to find if any null values in the table

na_list = daily_steps[daily_steps.isna().any(axis=1)]
print("After removing NA Values:",na_list.shape[0])
print(na_list)
#no missing values

#-----------------Zero Values----------------------
#To find out if any values in steps column has zero values(Its impossible to have a person taking 0 steps a day)
rows_with_zeroes_steps = daily_steps.loc[(daily_steps['StepTotal'] == 0)]
#print(rows_with_zeroes_steps)
#77 rows found with zero values

#To remove rows containing NA values
rows_without_zeros_steps = daily_steps.loc[(daily_steps['StepTotal'] != 0)]
print("There are ",rows_with_zeroes_steps.shape[0]," number of entries containing Zero steps.")
print(rows_without_zeros_steps)
#removed zero values
#863 rows remaining

#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros_steps['Id'], rows_without_zeros_steps['StepTotal'], color='orange')

# X axis label
ax.set_xlabel('User')

# Y axis label
ax.set_ylabel('StepTotal')
plt.title("Data with outliers")
plt.show()

#----------------------Z-Score-----------------------

#Identifying and Eliminating Outliers using Z-Score
#Zscore = (data_point -mean) / std. deviation
#Outliers are defined as data points having Z-Score -/+3(Gaussian Distribution approach)

#upper_threshold = 3
#lower_threshold = -3


z = np.abs(stats.zscore(rows_without_zeros_steps['StepTotal']))
print("Z-Scores for the data:")
print(z)

#View outlier Data to decide if outliers to be eliminated or not

outliers_steps = (rows_without_zeros_steps.iloc[np.where(z > 3) or np.where(z < -3)])
print("The data contains ",outliers_steps.shape[0]," outliers.")
print(outliers_steps)
#found 7 outliers

#Final cleaned data after removing outliers
data_cleaned_daily_steps = pd.concat([rows_without_zeros_steps, outliers_steps]).drop_duplicates(keep=False)
print("The final cleaned data:")
print(data_cleaned_daily_steps)
#856 rows
#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_daily_steps['Id'], data_cleaned_daily_steps['StepTotal'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Step Total')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------


#Save the final cleaned data on a new csv to take it to "Process" phase


data_cleaned_daily_steps.to_csv(r'daily_steps_datacleaned.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"daily_steps_datacleaned.csv\"")
print("-------------------------------------------------------------------")
