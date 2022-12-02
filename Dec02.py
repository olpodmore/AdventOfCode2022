# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np

ResultsRaw = pd.read_csv("data/input02.txt", sep=" ", header=None,
                         names=["OpponentShape", "MyShape"])

# PART ONE

ResultsPartOne = ResultsRaw.copy()

# create a list of score conditions for MyShape
ConditionsShape = [
    (ResultsPartOne["MyShape"] == "X"),  # rock
    (ResultsPartOne["MyShape"] == "Y"),  # paper
    (ResultsPartOne["MyShape"] == "Z")  # scissors
    ]

# create a list of the values we want to assign for each condition
ValuesShape = [1, 2, 3]  # rock scores 1, paper scores 2, scissors scores 3

# create a new column and use np.select to assign values to it
# using our lists as arguments
ResultsPartOne["ShapeScore"] = np.select(ConditionsShape, ValuesShape)

# now similarly for score conditions for the result
ConditionsResult = [
    (ResultsPartOne["MyShape"] == "X") &
    (ResultsPartOne["OpponentShape"] == "A"),  # tie: your rock vs rock
    (ResultsPartOne["MyShape"] == "X") &
    (ResultsPartOne["OpponentShape"] == "B"),  # loss: your rock vs paper
    (ResultsPartOne["MyShape"] == "X") &
    (ResultsPartOne["OpponentShape"] == "C"),  # win: your rock vs scissors
    (ResultsPartOne["MyShape"] == "Y") &
    (ResultsPartOne["OpponentShape"] == "A"),  # win: your paper vs rock
    (ResultsPartOne["MyShape"] == "Y") &
    (ResultsPartOne["OpponentShape"] == "B"),  # tie: your paper vs paper
    (ResultsPartOne["MyShape"] == "Y") &
    (ResultsPartOne["OpponentShape"] == "C"),  # loss: your paper vs scissors
    (ResultsPartOne["MyShape"] == "Z") &
    (ResultsPartOne["OpponentShape"] == "A"),  # loss: your scissors vs rock
    (ResultsPartOne["MyShape"] == "Z") &
    (ResultsPartOne["OpponentShape"] == "B"),  # win: your scissors vs paper
    (ResultsPartOne["MyShape"] == "Z") &
    (ResultsPartOne["OpponentShape"] == "C")  # tie: your scissors vs scissors
    ]

# create a list of the values we want to assign for each condition
# win = 6, tie = 3, loss = 0
ValuesResult = [3, 0, 6, 6, 3, 0, 0, 6, 3]

# create a new column and use np.select to assign values to it
# using our lists as arguments
ResultsPartOne["ResultsScore"] = np.select(ConditionsResult, ValuesResult)

# Total score
ResultsPartOne["TotalScore"] = ResultsPartOne["ShapeScore"]+ResultsPartOne["ResultsScore"]

Solution1 = ResultsPartOne["TotalScore"].sum()

# PART TWO

# need to recalculate shape score

ResultsPartTwo = ResultsRaw.copy()

# rename column for clarity
ResultsPartTwo.rename(columns={"MyShape": "Result"}, inplace=True)

# conditions and values again
# create a list of score conditions for MyShape
ConditionsDesiredResult = [
    (ResultsPartTwo["Result"] == "X"),  # lose
    (ResultsPartTwo["Result"] == "Y"),  # tie
    (ResultsPartTwo["Result"] == "Z")  # win
    ]

# create a list of the values we want to assign for each condition
# win = 6, tie = 3, loss = 0
ValuesDesiredResult = [0, 3, 6]

# create a new column and use np.select to assign values to it
# using our lists as arguments
ResultsPartTwo["ResultsScore"] = np.select(ConditionsDesiredResult,
                                           ValuesDesiredResult)

# create a list of shape conditions to get to the desired result
ConditionsRequiredShape = [
    (ResultsPartTwo["Result"] == "X") &
    (ResultsPartTwo["OpponentShape"] == "A"),  # lose against rock = scissors
    (ResultsPartTwo["Result"] == "X") &
    (ResultsPartTwo["OpponentShape"] == "B"),  # lose against paper = rock
    (ResultsPartTwo["Result"] == "X") &
    (ResultsPartTwo["OpponentShape"] == "C"),  # lose against scissors = paper
    (ResultsPartTwo["Result"] == "Y") &
    (ResultsPartTwo["OpponentShape"] == "A"),  # tie against rock = rock
    (ResultsPartTwo["Result"] == "Y") &
    (ResultsPartTwo["OpponentShape"] == "B"),  # tie against paper = paper
    (ResultsPartTwo["Result"] == "Y") &
    (ResultsPartTwo["OpponentShape"] == "C"),  # tie against scissors =scissors
    (ResultsPartTwo["Result"] == "Z") &
    (ResultsPartTwo["OpponentShape"] == "A"),  # win against rock = paper
    (ResultsPartTwo["Result"] == "Z") &
    (ResultsPartTwo["OpponentShape"] == "B"),  # win against paper = scissors
    (ResultsPartTwo["Result"] == "Z") &
    (ResultsPartTwo["OpponentShape"] == "C")  # win against scissors = rock
    ]

# create a list of the values we want to assign for each condition
# rock scores 1, paper scores 2, scissors scores 3
ValuesRequiredShape = [3, 1, 2, 1, 2, 3, 2, 3, 1]

# create a new column and use np.select to assign values to it
# using our lists as arguments
ResultsPartTwo["ShapeScore"] = np.select(ConditionsRequiredShape,
                                         ValuesRequiredShape)

# Total score
ResultsPartTwo["TotalScore"] = ResultsPartTwo["ShapeScore"] + ResultsPartTwo["ResultsScore"]

Solution2 = ResultsPartTwo["TotalScore"].sum()
