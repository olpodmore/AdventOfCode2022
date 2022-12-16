#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:42:51 2022

@author: oliviapodmore
"""

# Setup
import pandas as pd
import numpy as np
import textwrap
import re

from os import chdir
wd = "/home/oliviapodmore/AdventOfCode2022"
chdir(wd)

with open("data/input05.txt", "r") as Data:
    DataLines = Data.readlines()

# PART ONE
# from visual inspection, know that the crates only take up first 8 lines
# so this is hardcoded, not ideal...
Crates = DataLines[0:8]

# from visual inspection, the length of each string is 36.
# from visual inspection, there are nine stacks
# therefore each stack takes up four characters
CleanCratesList = []
for x in range(8):
    CleanCratesList.append(textwrap.wrap(Crates[x], 4, drop_whitespace=False))

CratesDf = pd.DataFrame(CleanCratesList, columns=["Stack1", "Stack2", "Stack3", "Stack4", "Stack5", "Stack6", "Stack 7", "Stack8", "Stack9"])

# from visual inspection, know that the instructions start on line 10
Instructions = DataLines[10:]

NumberOfMovements = len(Instructions)

for x in range(NumberOfMovements):
    
    # Pull out instructions
    Movements = re.findall("[0-9]{1,2}", Instructions[x])
    NumberToMove = int(Movements[0])
    OriginalColumnNumber = int(Movements[1])
    DestinationColumnNumber = int(Movements[2])
    
    # replace blanks with NAs
    CratesDf = CratesDf.mask(CratesDf == "    ")

    OriginalColumn = CratesDf.copy()

    # selects column 4
    OriginalColumn = OriginalColumn.iloc[:, OriginalColumnNumber-1:OriginalColumnNumber]

    # remove rows with NAs
    OriginalColumnFiltered = OriginalColumn.dropna(axis=0)

    # then take the first NumberToMove rows
    ValuesToMove = OriginalColumnFiltered.iloc[0:NumberToMove, 0]

    # store what the remaining column looks like
    RemainingColumn = OriginalColumnFiltered.iloc[NumberToMove:, ]
    #RemainingColumn = RemainingColumn.reset_index(drop=True)

    # reverse the rows that are moving
    ReversedValues = ValuesToMove.sort_index(ascending=False)

    # select the destination column
    DestinationColumn = CratesDf.copy()

    DestinationColumn = DestinationColumn.iloc[:, DestinationColumnNumber-1:DestinationColumnNumber]

    # remove rows with NAs
    DestinationColumnFiltered = DestinationColumn.dropna(axis=0)

    # select the current destination values
    CurrentDestinationValues = DestinationColumnFiltered.iloc[:, 0]

    # create the new destination values after moving the crates
    NewDestinationValues = ReversedValues.append(CurrentDestinationValues)
    NewDestinationValuesDf = NewDestinationValues.to_frame()

    # have to reset index or I get an error when trying to add it in later
    NewDestinationValuesDf = NewDestinationValuesDf.reset_index(drop=True)

    # add the new original and destination column back into the df, overwriting the originals
    # remove original origin column
    CratesDf = CratesDf.drop(CratesDf.columns[OriginalColumnNumber-1], axis=1)

    # replace with new origin column
    CratesDf.insert(OriginalColumnNumber-1, "Stack"+str(OriginalColumnNumber), RemainingColumn)

    # remove original destination column
    CratesDf = CratesDf.drop(CratesDf.columns[DestinationColumnNumber-1], axis=1)

    # if new destination column is longer than the main df, make the main df bigger
    # otherwise python doesn't let me add the new destination column 
    Difference = len(NewDestinationValuesDf) - len(CratesDf)
    while Difference > 0:
        AdjustmentList = ["    ", "    ", "    ", "    ", "    ", "    ", "    ", "    "]
        CratesDf.loc[len(CratesDf)] = AdjustmentList
        Difference = Difference = len(NewDestinationValuesDf) - len(CratesDf)

    # replace with new destination column
    CratesDf.insert(DestinationColumnNumber-1, "Stack"+str(DestinationColumnNumber), NewDestinationValuesDf)
    
# Select the top crates on each column
TopCrates = CratesDf.copy()

TopCrates = TopCrates.apply(lambda x: pd.Series(x.dropna().to_numpy()))

#Solution part 1
print(TopCrates.iloc[0])

# PART TWO

# Same code as above, but values that are moving don't need to be reversed

CratesDf = pd.DataFrame(CleanCratesList, columns=["Stack1", "Stack2", "Stack3", "Stack4", "Stack5", "Stack6", "Stack 7", "Stack8", "Stack9"])

NumberOfMovements = len(Instructions)

for x in range(NumberOfMovements):
    
    # Pull out instructions
    Movements = re.findall("[0-9]{1,2}", Instructions[x])
    NumberToMove = int(Movements[0])
    OriginalColumnNumber = int(Movements[1])
    DestinationColumnNumber = int(Movements[2])
    
    # replace blanks with NAs
    CratesDf = CratesDf.mask(CratesDf == "    ")

    OriginalColumn = CratesDf.copy()

    # selects column 4
    OriginalColumn = OriginalColumn.iloc[:, OriginalColumnNumber-1:OriginalColumnNumber]

    # remove rows with NAs
    OriginalColumnFiltered = OriginalColumn.dropna(axis=0)

    # then take the first NumberToMove rows
    ValuesToMove = OriginalColumnFiltered.iloc[0:NumberToMove, 0]

    # store what the remaining column looks like
    RemainingColumn = OriginalColumnFiltered.iloc[NumberToMove:, ]
    #RemainingColumn = RemainingColumn.reset_index(drop=True)

    # select the destination column
    DestinationColumn = CratesDf.copy()

    DestinationColumn = DestinationColumn.iloc[:, DestinationColumnNumber-1:DestinationColumnNumber]

    # remove rows with NAs
    DestinationColumnFiltered = DestinationColumn.dropna(axis=0)

    # select the current destination values
    CurrentDestinationValues = DestinationColumnFiltered.iloc[:, 0]

    # create the new destination values after moving the crates
    NewDestinationValues = ValuesToMove.append(CurrentDestinationValues)
    NewDestinationValuesDf = NewDestinationValues.to_frame()

    # have to reset index or I get an error when trying to add it in later
    NewDestinationValuesDf = NewDestinationValuesDf.reset_index(drop=True)

    # add the new original and destination column back into the df, overwriting the originals
    # remove original origin column
    CratesDf = CratesDf.drop(CratesDf.columns[OriginalColumnNumber-1], axis=1)

    # replace with new origin column
    CratesDf.insert(OriginalColumnNumber-1, "Stack"+str(OriginalColumnNumber), RemainingColumn)

    # remove original destination column
    CratesDf = CratesDf.drop(CratesDf.columns[DestinationColumnNumber-1], axis=1)

    # if new destination column is longer than the main df, make the main df bigger
    # otherwise python doesn't let me add the new destination column 
    Difference = len(NewDestinationValuesDf) - len(CratesDf)
    while Difference > 0:
        AdjustmentList = ["    ", "    ", "    ", "    ", "    ", "    ", "    ", "    "]
        CratesDf.loc[len(CratesDf)] = AdjustmentList
        Difference = Difference = len(NewDestinationValuesDf) - len(CratesDf)

    # replace with new destination column
    CratesDf.insert(DestinationColumnNumber-1, "Stack"+str(DestinationColumnNumber), NewDestinationValuesDf)
    
# Select the top crates on each column
TopCrates = CratesDf.copy()

TopCrates = TopCrates.apply(lambda x: pd.Series(x.dropna().to_numpy()))

#Solution part 2
print(TopCrates.iloc[0])

    
    
    
    



