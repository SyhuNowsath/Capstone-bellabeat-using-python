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
daily_intensities = pd.read_csv(r'dailyIntensities_merged.csv')
print("The uploaded csv contains:",daily_intensities.shape[0],"Rows")
print(daily_intensities)

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(daily_intensities['Id'], daily_intensities['SedentaryMinutes'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('SedentaryMinutes')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------


#-----------------Redundency Analysis-----------------
#created a list to check if there are any duplicates
duplicates_intensities_list = daily_intensities[daily_intensities.duplicated(keep = False, subset=['Id','ActivityDay'])]
#print(duplicates_intensities_list)
#No duplicates
#-----------------------------------------------------



#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------

#Created list in order to find if any null values in the table

#created na_list in order to find any null values in the table
na_list = daily_intensities[daily_intensities.isna().any(axis=1)]
#print(na_list)
##No null values

#-----------------Zero Values----------------------
#To find out if any values in Sedentary minutes column has zero values
rows_with_zeroes2 = daily_intensities.loc[(daily_intensities['SedentaryMinutes'] == 0)]
print("There are ",rows_with_zeroes2.shape[0]," number of entries containing Zero calories.")
#print(rows_with_zeroes2)
# 1 rows found

#creating rows_without_zeroes to remove any zero values in Total steps and calories.
rows_without_zeros2 = daily_intensities.loc[(daily_intensities['SedentaryMinutes'] != 0)]
print("After Removing Rows with 0 Calories, Entries count:",rows_without_zeros2.shape[0])
#print(rows_without_zeros)

#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros2['Id'], rows_without_zeros2['SedentaryMinutes'], color='orange')

# X axis label
ax.set_xlabel('User')

# Y axis label
ax.set_ylabel('SedentaryMinutes')
plt.title("Data with outliers")
plt.show()

#----------------------Z-Score-----------------------

#Identifying and Eliminating Outliers using Z-Score
#Zscore = (data_point -mean) / std. deviation
#Outliers are defined as data points having Z-Score -/+3(Gaussian Distribution approach)

#upper_threshold = 3
#lower_threshold = -3

z = np.abs(stats.zscore(rows_without_zeros2['SedentaryMinutes']))
print("Z-Scores for the data:")
#print(z)
#print(np.abs(stats.zscore(rows_without_zeros['Calories'])))

#View outlier Data to decide if outliers to be eliminated or not
outliers_intensities = (rows_without_zeros2.iloc[np.where(z > 3)])
#print(outliers_intensities)
#3 outliers

#Final cleaned data after removing outliers

data_cleaned_intensities = pd.concat([rows_without_zeros2, outliers_intensities]).drop_duplicates(keep=False)
print("The final cleaned data:")
#print(data_cleaned_intensities)

#-------------------Scatter Plot----------------------
#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_intensities['Id'], data_cleaned_intensities['SedentaryMinutes'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('SedentaryMinutes')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------
#Save the final cleaned data on a new csv to take it to "Process" phase
data_cleaned_intensities.to_csv(r'data_cleaned_dailyCalories_merged.csv')
print("---------------------Data Cleaned Successfully---------------------")
data_cleaned_intensities.to_csv(r'dailyintensities_datacleaned.csv')
print("-------------------------------------------------------------------")