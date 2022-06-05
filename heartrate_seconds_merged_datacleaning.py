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

#Importing dailyActivity_merged CSV file as daily_activity
heartrate_seconds = pd.read_csv(r'heartrate_seconds_merged.csv')
print("The uploaded csv contains:",heartrate_seconds.shape[0],"Rows")
print(heartrate_seconds)
#2483658 rows


#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(heartrate_seconds['Id'], heartrate_seconds['Value'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Heart Rate Value')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------

#-----------------Redundency Analysis-----------------

#created a list to check if there are any duplicates

duplicates_heartrate_seconds = heartrate_seconds[heartrate_seconds.duplicated(keep = False, subset=['Id','Time'])]
print("Number of Duplicates:",duplicates_heartrate_seconds.shape[0])
print(duplicates_heartrate_seconds)
#No duplicates found


#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------
#Created list in order to find if any null values in the table
na_list = heartrate_seconds[heartrate_seconds.isna().any(axis=1)]
print("There are ",na_list.shape[0]," rows contains NA")
print(na_list)
#no missing values


#-----------------Zero Values----------------------

#To find out if any values in Calories column has zero values

rows_with_zeroes_heartrate = heartrate_seconds.loc[(heartrate_seconds['Value'] == 0)]
print(rows_with_zeroes_heartrate)
#77 rows found with zero values

#creating rows_without_zeroes to remove any zero values.
rows_without_zeros_heartrate = heartrate_seconds.loc[(heartrate_seconds['Value'] != 0)]
print("After Removing Rows with 0 Values, Entries count:",rows_without_zeros_heartrate.shape[0])
print(rows_without_zeros_heartrate)
#removed zero values
#2483658 rows remaining


#-----------------------------------------------------------


#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros_heartrate['Id'], rows_without_zeros_heartrate['Value'], color='orange')

# X axis label
ax.set_xlabel('User')

# Y axis label
ax.set_ylabel('Value')
plt.title("Data with outliers")
plt.show()

#----------------------Z-Score-----------------------

#Identifying and Eliminating Outliers using Z-Score
#Zscore = (data_point -mean) / std. deviation
#Outliers are defined as data points having Z-Score -/+3(Gaussian Distribution approach)

#upper_threshold = 3
#lower_threshold = -3

z = np.abs(stats.zscore(rows_without_zeros_heartrate['Value']))
print("Z-Scores for the data:")
print(z)


#View outlier Data to decide if outliers to be eliminated or not

outliers_heartrate = (rows_without_zeros_heartrate.iloc[np.where(z > 3) or np.where(z < -3)])
print("The data contains ",outliers_heartrate.shape[0]," outliers.")
#print(outliers_heartrate)
#found 40703 outliers

data_cleaned_heartrate = pd.concat([rows_without_zeros_heartrate, outliers_heartrate]).drop_duplicates(keep=False)
#print(data_cleaned_heartrate)
#856 rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_heartrate['Id'], data_cleaned_heartrate['Value'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Values')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------


#Save the final cleaned data on a new csv to take it to "Process" phase
data_cleaned_heartrate.to_csv(r'heartrate_datacleaned.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"heartrate_datacleaned.csv\"")
print("-------------------------------------------------------------------")
