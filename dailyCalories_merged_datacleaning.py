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
input_csv_as_dataframe = pd.read_csv(r'dailyCalories_merged.csv')

print("The uploaded csv contains:",input_csv_as_dataframe.shape[0],"Rows")
print(input_csv_as_dataframe)

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(input_csv_as_dataframe['Id'], input_csv_as_dataframe['Calories'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Calories')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------



#-----------------Redundency Analysis-----------------

#created a list to check if there are any duplicates
duplicates_list = input_csv_as_dataframe[input_csv_as_dataframe.duplicated(keep = False, subset=['Id','ActivityDay'])]
print("Number of Duplicates:",duplicates_list.shape[0])
print(duplicates_list)


#Return Data frame keeping one copy and removing other duplicates
data_without_duplicates = input_csv_as_dataframe.drop_duplicates(subset=['Id', 'ActivityDay'], keep='first')
print("After removing Duplicates:",data_without_duplicates.shape[0])
print(data_without_duplicates)

#---------OR---------

#Return Data frame removing all duplicates occurrences
data_without_duplicates = input_csv_as_dataframe.drop_duplicates(subset=['Id', 'ActivityDay'], keep=False)
print(data_without_duplicates)
#-----------------------------------------------------



#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------

#Created list in order to find if any null values in the table
na_rows = data_without_duplicates[data_without_duplicates.isna().any(axis=1)]
print("There are ",na_rows.shape[0]," rows contains NA")
print(na_rows)


#To remove rows containing NA values
data_without_NA = data_without_duplicates.dropna()

#---------OR---------

#To fill NA will Linear Progression
#data_without_NA = data_without_duplicates.interpolate(method='linear', limit_direction='forward', axis=0)


print("After removing NA Values:",data_without_NA.shape[0])
print(data_without_NA)


#-----------------Zero Values----------------------

#To find out if any values in Calories column has zero values(Its impossible to have a person buring 0 calories a day)
rows_with_zeroes = data_without_NA.loc[(data_without_NA['Calories'] == 0)]
print("There are ",rows_with_zeroes.shape[0]," number of entries containing Zero calories.")
print(rows_with_zeroes)

#creating rows_without_zeroes to remove any zero values in Total steps and calories.
rows_without_zeros = data_without_NA.loc[(data_without_NA['Calories'] != 0)]
print("After Removing Rows with 0 Calories, Entries count:",rows_without_zeros.shape[0])
print(rows_without_zeros)

#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros['Id'], rows_without_zeros['Calories'], color='orange')

# X axis label
ax.set_xlabel('User Id')

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
z_scores = np.abs(stats.zscore(rows_without_zeros['Calories']))
print("Z-Scores for the data:")
print(z_scores)


#View outlier Data to decide if outliers to be eliminated or not
outliers = (rows_without_zeros.iloc[np.where(z_scores > 3) or np.where(z_scores < -3)])
print("The data contains ",outliers.shape[0]," outliers.")
print(outliers)

#Final cleaned data after removing outliers
data_cleaned = pd.concat([rows_without_zeros, outliers]).drop_duplicates(keep=False)
print("The final cleaned data:")
print(data_cleaned)

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned['Id'], data_cleaned['Calories'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Calories')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------


#Save the final cleaned data on a new csv to take it to "Process" phase
data_cleaned.to_csv(r'data_cleaned_dailyCalories_merged.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"data_cleaned_dailyCalories_merged.csv\"")
print("-------------------------------------------------------------------")