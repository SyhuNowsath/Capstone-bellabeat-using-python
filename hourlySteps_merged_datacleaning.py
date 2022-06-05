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
hourly_Steps = pd.read_csv(r'hourlySteps_merged.csv')
print("The uploaded csv contains:",hourly_Steps.shape[0],"Rows")
print(hourly_Steps)
#22099  rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(hourly_Steps['Id'], hourly_Steps['StepTotal'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('Step Total')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------

#-----------------Redundency Analysis-----------------

#created a list to check if there are any duplicates

duplicates_hourly_Steps = hourly_Steps[hourly_Steps.duplicated(keep = False, subset=['Id','ActivityHour','StepTotal'])]
print("After removing Duplicates:",duplicates_hourly_Steps.shape[0])
print(duplicates_hourly_Steps)
#No duplicates found


#-----------------------------------------------------



#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------

#created na_list in order to find any null values in the table
na_list = hourly_Steps[hourly_Steps.isna().any(axis=1)]
print("There are ",na_list.shape[0]," rows contains NA")
print(na_list)
#no missing values


#-----------------Zero Values----------------------
#to find out if any values in totalsteps column has zero values
rows_with_zeroes_hourly_Steps = hourly_Steps.loc[(hourly_Steps['StepTotal'] == 0)]
print("There are ",rows_with_zeroes_hourly_Steps.shape[0]," number of entries containing Zero calories.")
print(rows_with_zeroes_hourly_Steps)
#9297 rows found with zero values

#creating rows_without_zeroes to remove any zero values in Total steps and calories.
rows_without_zeros_hourly_Steps = hourly_Steps.loc[(hourly_Steps['StepTotal'] != 0)]
print("After Removing Rows with 0 Calories, Entries count:", rows_without_zeros_hourly_Steps.shape[0])
print(rows_without_zeros_hourly_Steps)
#removed zero values
#12802 rows remaining


#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------

fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros_hourly_Steps['Id'], rows_without_zeros_hourly_Steps['StepTotal'], color='orange')

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

z = np.abs(stats.zscore(rows_without_zeros_hourly_Steps['StepTotal']))
print("Z-Scores for the data:")
print(z)

#View outlier Data to decide if outliers to be eliminated or not

outliers_hourly_steps = (rows_without_zeros_hourly_Steps.iloc[np.where(z > 3) or np.where(z < -3)])
print("The data contains ",outliers_hourly_steps.shape[0]," outliers.")
print(outliers_hourly_steps)
#found 319 outliers

#Final cleaned data after removing outliers
data_cleaned_hourly_steps = pd.concat([rows_without_zeros_hourly_Steps, outliers_hourly_steps]).drop_duplicates(keep=False)
print("The final cleaned data:")
print(data_cleaned_hourly_steps)
#12483 rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_hourly_steps['Id'], data_cleaned_hourly_steps['StepTotal'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('StepTotal')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------

#Save the final cleaned data on a new csv to take it to "Process" phase
data_cleaned_hourly_steps.to_csv(r'hourlysteps_datacleaned.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"hourlysteps_datacleaned.csv\"")
print("-------------------------------------------------------------------")

