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
weightLogInfo_merged = pd.read_csv(r'weightLogInfo_merged.csv')
print("The uploaded csv contains:",weightLogInfo_merged.shape[0],"Rows")
print(weightLogInfo_merged)
#67 rows

#Data Cleaning

#Redundency Analysis
#created a duplicated list to check if there are any duplicates
duplicates_weightlog = weightLogInfo_merged[weightLogInfo_merged.duplicated(keep = False, subset=['Id','Date'])]
print(duplicates_weightlog)
#No duplicates found

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(weightLogInfo_merged['Id'], weightLogInfo_merged['BMI'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('BMI')
plt.title("How does raw data look like")
plt.show()

#------------------------------------------------------

#-----------------Missing Values----------------------

#-----------------NA/Null Values----------------------

na_list = weightLogInfo_merged[weightLogInfo_merged.isna().any(axis=1)]
print("There are ",na_list.shape[0]," rows contains NA")
#print(na_list)
#no missing values

#-----------------Zero Values----------------------
#To find out if any values in Calories column has zero values
rows_with_zeroes_weightLogInfo = weightLogInfo_merged.loc[(weightLogInfo_merged['BMI'] == 0)]
print("There are ",rows_with_zeroes_weightLogInfo.shape[0]," number of entries containing Zero calories.")
print(rows_with_zeroes_weightLogInfo)
#No rows found with zero values



rows_without_zeros_weightLogInfo = weightLogInfo_merged.loc[(weightLogInfo_merged['BMI'] != 0)]
print("After Removing Rows with 0 Calories, Entries count:",rows_without_zeros_weightLogInfo.shape[0])
print(rows_without_zeros_weightLogInfo)
#no zero values, 67 rows

#-----------------------------------------------------------



#-----------------Outliers Analysis-------------------

#-------------------Scatter Plot------------------------


fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(rows_without_zeros_weightLogInfo['Id'], rows_without_zeros_weightLogInfo['BMI'], color='orange')

# X axis label
ax.set_xlabel('User')

# Y axis label
ax.set_ylabel('BMI')
plt.title("Data with outliers")
plt.show()

#----------------------Z-Score-----------------------

#Identifying and Eliminating Outliers using Z-Score
#Zscore = (data_point -mean) / std. deviation
#Outliers are defined as data points having Z-Score -/+3(Gaussian Distribution approach)

#upper_threshold = 3
#lower_threshold = -3

z = np.abs(stats.zscore(rows_without_zeros_weightLogInfo['BMI']))
print("Z-Scores for the data:")
print(z)



#View outlier Data to decide if outliers to be eliminated or not

outliers_weightLogInfo= (rows_without_zeros_weightLogInfo.iloc[np.where(z > 3) or np.where(z < -3)])
print("The data contains ",outliers_weightLogInfo.shape[0]," outliers.")
print(outliers_weightLogInfo)
#found 1 outliers

#Final cleaned data after removing outliers
data_cleaned_weightLogInfo = pd.concat([rows_without_zeros_weightLogInfo, outliers_weightLogInfo]).drop_duplicates(keep=False)
print("The final cleaned data:")
print(data_cleaned_weightLogInfo)
#66 rows

#-------------------Scatter Plot----------------------

#Creating a ScatterPlot to view Outliers
fig, ax = plt.subplots(figsize = (18,10))
ax.scatter(data_cleaned_weightLogInfo['Id'], data_cleaned_weightLogInfo['BMI'], color='orange')

# X axis label
ax.set_xlabel('User Id')

# Y axis label
ax.set_ylabel('BMI')
plt.title("How does cleaned data look like")
plt.show()

#------------------------------------------------------

#Save the final cleaned data on a new csv to take it to "Process" phase

data_cleaned_weightLogInfo.to_csv(r'weightLogInfo_datacleaned.csv')
print("---------------------Data Cleaned Successfully---------------------")
print("Final cleaned Data stored in: \"weightLogInfo_datacleaned.csv\"")
print("-------------------------------------------------------------------")

