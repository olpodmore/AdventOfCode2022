#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 15:41:36 2022

@author: oliviapodmore
"""

# Setup
from os import chdir
wd = "/home/oliviapodmore/AdventOfCode2022"
chdir(wd)

with open("data/input06.txt", "r") as Data:
    DataLines = Data.readlines()

# PART ONE

# convert to a string for easier handling
DataStreamBuffer = "".join(DataLines)


# iteratively check each chunk of four for repeat characters

RepeatedCharacterCheck = True
x = 4
while RepeatedCharacterCheck:
    ChunkOfFour = DataStreamBuffer[(x-4):x]
    # check if all characters are unique
    RepeatedCharacterCheck = len(set(ChunkOfFour)) != len(ChunkOfFour)
    if not RepeatedCharacterCheck:
        print(x)
    x += 1
    
# PART TWO

# the same, but chunks are 14 characters long
    
RepeatedCharacterCheck = True
x = 14
while RepeatedCharacterCheck:
    ChunkOfFour = DataStreamBuffer[(x-14):x]
    # check if all characters are unique
    RepeatedCharacterCheck = len(set(ChunkOfFour)) != len(ChunkOfFour)
    if not RepeatedCharacterCheck:
        print(x)
    x += 1






