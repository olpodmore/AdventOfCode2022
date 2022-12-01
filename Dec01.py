# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# PART ONE

import pandas as pd
import numpy as np

with open("data/input01.txt", "r") as calories:
    CaloriesLines = calories.readlines()

CaloriesDf = pd.DataFrame(CaloriesLines, columns=["Calories"])

# create a waiting ID column
CaloriesDf["ID"] = ""

# convert the blanks to NaN
CaloriesDfClean = CaloriesDf.mask(CaloriesDf == "\n")

# find the NAs in the calories column
NALocations = np.where(pd.isnull(CaloriesDfClean))

# how many NAs are there in the Calories column?
NACount = CaloriesDfClean["Calories"].isna().sum()

# create IDs for each elf
IDs = list(range(1, NACount+1))

# add an ID for the start of each elf
CaloriesDfClean["ID"].iloc[NALocations[0]] = IDs

# manual fix for the first elf since no blank above her
CaloriesDfClean["ID"].iloc[0] = 0

# convert the blanks in ID to NaN
# NB this actually does it over the whole df, which works in this case
# but would be better if it only did the ID colummn
CaloriesDfCleanID = CaloriesDfClean.mask(CaloriesDfClean == "")


# now fill IDs downwards until hit another ID
cols = ['ID']
CaloriesDfCleanID.loc[:, cols] = CaloriesDfCleanID.loc[:, cols].ffill()

# remove the NA in Calories rows
CaloriesFinal = CaloriesDfCleanID.dropna()

# change calories column to numeric
CaloriesFinal["Calories"] = CaloriesFinal["Calories"].apply(pd.to_numeric)

# group by elf (ID) and sum their calories
CaloriesCounted = CaloriesFinal.groupby("ID").sum()
Solution = CaloriesCounted.max()

# PART TWO
# find the calories for top three elves
Solution2 = CaloriesCounted.Calories.nlargest(3).sum()
