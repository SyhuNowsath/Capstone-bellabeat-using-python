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
sleep_day_merged = pd.read_csv(r'sleepDay_merged.csv')
print("The uploaded csv contains:",sleep_day_merged.shape[0],"Rows")
print(sleep_day_merged)
#413 rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(sleep_day_merged['Id'], sleep_day_merged['TotalMinutesAsleep'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Total Minutes Asleep')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------


#-----------------Redundency Analysis-----------------

#created a list to check if there are any duplicates

duplicates_sleep_day = sleep_day_merged.loc[sleep_day_merged.duplicated(keep = False, subset=['Id','SleepDay'])]
print("Number of Duplicates:", duplicates_sleep_day.shape[0])
print(duplicates_sleep_day)
#3 duplicates found

sleep_day_nodup = sleep_day_merged.drop_duplicates(keep = 'first', subset=['Id','SleepDay'])
print(sleep_day_nodup)
#410 rows remaining
#-----------------------------------------------------



#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------

#Created list in order to find if any null values in the table
na_list = sleep_day_nodup[sleep_day_nodup.isna().any(axis=1)]
print("There are ",na_list.shape[0]," rows contains NA")
print(na_list)
#no missing values

#-----------------Zero Values----------------------

#To find out if any values in Calories column has zero values

rows_with_zeroes_sleep_day = sleep_day_nodup.loc[(sleep_day_nodup['TotalMinutesAsleep'] == 0)]
print("There are ", rows_with_zeroes_sleep_day.shape[0]," number of entries containing Zero calories.")
print(rows_with_zeroes_sleep_day)
#NO rows found with zero values

#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(sleep_day_nodup['Id'], sleep_day_nodup['TotalMinutesAsleep'], color='orange')

# X axis label
ax.set_xlabel('User')

# Y axis label
ax.set_ylabel('Total Minutes Asleep')
plt.title("Data with outliers")
plt.show()

#----------------------Z-Score-----------------------

#Identifying and Eliminating Outliers using Z-Score
#Zscore = (data_point -mean) / std. deviation
#Outliers are defined as data points having Z-Score -/+3(Gaussian Distribution approach)

#upper_threshold = 3
#lower_threshold = -3

z = np.abs(stats.zscore(sleep_day_nodup['TotalMinutesAsleep']))
print("Z-Scores for the data:")
print(z)

#View outlier Data to decide if outliers to be eliminated or not
outliers_sleep_day = (sleep_day_nodup.iloc[np.where(z > 3)  or np.where(z < -3)])
print("The data contains ",outliers_sleep_day.shape[0]," outliers.")
print(outliers_sleep_day)
#found 6 outliers

#Final cleaned data after removing outliers
data_cleaned_sleep_day = pd.concat([sleep_day_nodup, outliers_sleep_day]).drop_duplicates(keep=False)
print("The final cleaned data:")
print(data_cleaned_sleep_day)
#404 rows remaining

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_sleep_day['Id'], data_cleaned_sleep_day['TotalMinutesAsleep'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Total Minutes Asleep')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------

#Save the final cleaned data on a new csv to take it to "Process" phase
data_cleaned_sleep_day.to_csv(r'sleep_day_datacleaned.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"sleep_day_datacleaned.csv\"")
print("-------------------------------------------------------------------")
