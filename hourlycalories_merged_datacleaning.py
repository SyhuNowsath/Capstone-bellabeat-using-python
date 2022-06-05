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
hourly_calories = pd.read_csv(r'hourlyCalories_merged.csv')
print("The uploaded csv contains:",hourly_calories.shape[0],"Rows")
print(hourly_calories)
#22099 rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(hourly_calories['Id'], hourly_calories['Calories'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Calories')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------


#-----------------Redundency Analysis-----------------

#created a list to check if there are any duplicates

duplicates_hourly_calories = hourly_calories[hourly_calories.duplicated(keep = False, subset=['Id','ActivityHour'])]
print("Number of Duplicates:",duplicates_hourly_calories.shape[0])
print(duplicates_hourly_calories)
#No duplicates found

#-----------------------------------------------------



#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------

#created na_list in order to find any null values in the table
na_list = hourly_calories[hourly_calories.isna().any(axis=1)]
print("There are ",na_list.shape[0]," rows contains NA")
print(na_list)
#no missing values

#-----------------Zero Values----------------------
#to find out if any values in totalsteps column has zero values
rows_with_zeroes_hourly_calories = hourly_calories.loc[(hourly_calories['Calories'] == 0)]
print("There are ",rows_with_zeroes_hourly_calories.shape[0]," number of entries containing Zero calories.")
#print(rows_with_zeroes_hourly_calories)
#NOfound with zero values

#creating rows_without_zeroes to remove any zero values in Total steps and calories.
rows_without_zeros_hourly_calories = hourly_calories.loc[(hourly_calories['Calories'] != 0)]
print("After Removing Rows with 0 Calories, Entries count:",rows_without_zeros_hourly_calories.shape[0])
#print(rows_without_zeros_hourly_calories)
#22099 rows remaining

#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros_hourly_calories['Id'], rows_without_zeros_hourly_calories['Calories'], color='orange')

# X axis label
ax.set_xlabel('User')

# Y axis label
ax.set_ylabel('Calories')
plt.title("Data with outliers")
plt.show()

#----------------------Z-Score-----------------------
#Identifying and Eliminating Outliers using Z-Score
#Zscore = (data_point -mean) / std. deviation
#Outliers are defined as data points having Z-Score -/+3(Gaussian Distribution approach)

#upper_threshold = 3
#lower_threshold = -3

z = np.abs(stats.zscore(rows_without_zeros_hourly_calories['Calories']))
print("Z-Scores for the data:")
print(z)

#View outlier Data to decide if outliers to be eliminated or not
outliers_hourly_calories = (rows_without_zeros_hourly_calories.iloc[np.where(z > 3) or np.where(z < -3)])
print("The data contains ",outliers_hourly_calories.shape[0]," outliers.")
print(outliers_hourly_calories)
#found 449 outliers

#Final cleaned data after removing outliers
data_cleaned_hourly_calories = pd.concat([rows_without_zeros_hourly_calories,outliers_hourly_calories]).drop_duplicates(keep=False)
print("The final cleaned data:")
print(data_cleaned_hourly_calories)
#21650 rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_hourly_calories['Id'], data_cleaned_hourly_calories['Calories'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Calories')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------


#Save the final cleaned data on a new csv to take it to "Process" phase
data_cleaned_hourly_calories.to_csv(r'hourly_calories_datacleaned.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"data_cleaned_hourlycalories_merged.csv\"")
print("-------------------------------------------------------------------")

