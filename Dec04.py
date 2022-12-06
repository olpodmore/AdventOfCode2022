#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 16:36:12 2022

@author: oliviapodmore
"""

# Setup
import pandas as pd
import numpy as np

from os import chdir
wd = "/home/oliviapodmore/AdventOfCode2022"
chdir(wd)

Cleaning = pd.read_csv("data/input04.txt", sep=",", header=None, 
                       names=["Section1", "Section2"])

# PART ONE

#  split out the start and end sections for each elf
Cleaning[["StartSection1",
          "EndSection1"]] = Cleaning["Section1"].str.split("-", 1, expand=True)
Cleaning[["StartSection2",
          "EndSection2"]] = Cleaning["Section2"].str.split("-", 1, expand=True)
Cleaning[["StartSection1",
          "EndSection1", "StartSection2", "EndSection2"]] = Cleaning[["StartSection1", "EndSection1", "StartSection2", "EndSection2"]].apply(pd.to_numeric)

# conditions for section 1 in section 2 or vice versa
OverlapConditions = [
    (Cleaning["StartSection1"] >= Cleaning["StartSection2"]) &
    (Cleaning["EndSection1"] <= Cleaning["EndSection2"]),
    (Cleaning["StartSection2"] >= Cleaning["StartSection1"]) &
    (Cleaning["EndSection2"] <= Cleaning["EndSection1"])
    ]

# labels if the overlaps exist
OverlapLabels = ["Section1InSection2", "Section2InSection1"]

# execute and store the results of the overlap condition checks
Cleaning["OverlapCheck"] = np.select(OverlapConditions, OverlapLabels)

# how many of each condition occurred?
Results = Cleaning["OverlapCheck"].value_counts()

Solution1 = Results["Section1InSection2"]+Results["Section2InSection1"]

# PART TWO
Cleaning2 = Cleaning.copy()

# remove column for clarity
Cleaning2 = Cleaning2.drop(columns=["OverlapCheck"])

# check for overlap
# don't know why I can't do Cleaning2.StartSection2 <= Cleaning2.StartSection1 <= Cleaning2.EndSection2 
# it throws an error 'truth value of a series is amibguous'
Cleaning2["OverlapCheck"] = np.where(((Cleaning2.StartSection2 <= Cleaning2.StartSection1) &
                                      (Cleaning2.StartSection1 <= Cleaning2.EndSection2)) |
                                     ((Cleaning2.StartSection1 <= Cleaning2.StartSection2) &
                                      (Cleaning2.StartSection2 <= Cleaning2.EndSection1)) |
                                     ((Cleaning2.StartSection1 <= Cleaning2.EndSection2) &
                                      (Cleaning2.EndSection2 <= Cleaning2.EndSection1)) |
                                     ((Cleaning2.StartSection2 <= Cleaning2.EndSection1) &
                                      (Cleaning2.EndSection1 <= Cleaning2.EndSection2)),
                                     True, False)

Solution2 = Cleaning2["OverlapCheck"].sum()
