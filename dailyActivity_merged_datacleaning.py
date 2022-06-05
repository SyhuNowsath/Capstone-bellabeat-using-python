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
daily_activity = pd.read_csv(r'dailyActivity_merged.csv')
print("The uploaded csv contains:",daily_activity.shape[0],"Rows")
#print(daily_activity)

#Data Cleaning


#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(daily_activity['Id'], daily_activity['TotalSteps'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('TotalSteps')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------


#------------------------------------------------------



#-----------------Redundency Analysis-----------------

#created a list to check if there are any duplicates
duplicates_list = daily_activity[daily_activity.duplicated(keep = False, subset=['Id','ActivityDate'])]
print("Number of Duplicates:",duplicates_list.shape[0])
print(duplicates_list)

#---------OR---------

#Return Data frame removing all duplicates occurrences
data_without_duplicates = daily_activity.drop_duplicates(subset=['Id', 'ActivityDate'], keep=False)
print(data_without_duplicates)
#-----------------------------------------------------



#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------

#Created list in order to find if any null values in the table
na_list = daily_activity[daily_activity.isna().any(axis=1)]
print("There are ",na_list.shape[0]," rows contains NA")
print(na_list)

#-----------------Zero Values----------------------

#To find out if any values in TotalSteps column has zero values(Its impossible to have a person taking 0 steps a day)

rows_with_zeroes = daily_activity.loc[(daily_activity['TotalSteps'] == 0)]
print("There are ",rows_with_zeroes.shape[0]," number of entries containing Zero steps.")
print(rows_with_zeroes)

#creating rows_without_zeroes to remove any zero values in Total steps.
rows_without_zeros = daily_activity.loc[(daily_activity['TotalSteps'] != 0)]
print("After Removing Rows with 0 Calories, Entries count:",rows_without_zeros.shape[0])
print(rows_without_zeros)

#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

#Creating a ScatterPlot to view Outliers

fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros['Id'], rows_without_zeros['TotalSteps'], color='orange')

# X axis label
ax.set_xlabel('User')

# Y axis label
ax.set_ylabel('Total Steps')
plt.title("Data with outliers")
plt.show()

#----------------------Z-Score-----------------------
#Identifying and Eliminating Outliers using Z-Score
#Zscore = (data_point -mean) / std. deviation
#Outliers are defined as data points having Z-Score -/+3(Gaussian Distribution approach)

#upper_threshold = 3
#lower_threshold = -3

z = np.abs(stats.zscore(rows_without_zeros['TotalSteps']))
print("Z-Scores for the data:")
print(z)

#View outlier Data to decide if outliers to be eliminated or not

outliers = (rows_without_zeros.iloc[np.where(z> 3) or np.where(z < -3)])
print("The data contains ",outliers.shape[0]," outliers.")
print(outliers)

#Final cleaned data after removing outliers
data_cleaned_daily_activity = pd.concat([rows_without_zeros, outliers]).drop_duplicates(keep=False)
print("The final cleaned data:")
print(data_cleaned_daily_activity)

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_daily_activity['Id'], data_cleaned_daily_activity['TotalSteps'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('TotalSteps')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------


#Save the final cleaned data on a new csv to take it to "Process" phase

data_cleaned_daily_activity.to_csv(r'dailyactivity_merged_datacleaned.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"dailyactivity_merged_datacleaned.csv\"")
print("-------------------------------------------------------------------")


