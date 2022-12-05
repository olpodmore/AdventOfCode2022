# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Setup
import pandas as pd
import numpy as np
import string

from os import chdir
wd = "/home/oliviapodmore/AdventOfCode2022"
chdir(wd)


Rucksacks = pd.read_csv("data/input03.txt", header=None, names=["Items"])

# PART ONE

# split the rucksacks into the two compartments
Rucksacks["NumberOfItems"] = Rucksacks["Items"].str.len()
Rucksacks["HalfDelimiter"] = Rucksacks["NumberOfItems"]/2
Rucksacks["HalfDelimiter"] = Rucksacks["HalfDelimiter"].astype("int")

# for learning: apply applies a function along the axis of the dataframe
# everything from lambda up until axis is the function I am applying
# axis = 1 means applying the function to each row
# lambda is an anonymous function that can take any number of arguments
# I think the r: is designating what it will return
# the function takes the row (stored as r)
# and slices each row according to the HalfDelimiter
# the "r" could have been any character
Rucksacks["FirstCompartment"] = Rucksacks.apply(
    lambda r: r.Items[:r.HalfDelimiter], axis=1)
Rucksacks["SecondCompartment"] = Rucksacks.apply(
    lambda r: r.Items[r.HalfDelimiter:], axis=1)

# check which (case-specific) character appears in both compartments
Rucksacks["CommonItem"] = [set(a).intersection(b)
                           for a, b in zip(Rucksacks.FirstCompartment,
                                           Rucksacks.SecondCompartment)]
# need to change the column type from sets to strings so that the
# (future) join works
Rucksacks["CommonItem"] = Rucksacks["CommonItem"].str.join("")

# create priority lookup
Lowercase = list(string.ascii_lowercase[:])
Uppercase = list(string.ascii_uppercase[:])
Allcases = Lowercase+Uppercase
LowercasePriorities = list(range(1, 27))
UppercasePriorities = list(range(27, 53))
AllPriorities = LowercasePriorities+UppercasePriorities
PriorityLookup = pd.DataFrame(list(zip(Allcases, AllPriorities)),
                              columns=["Character", "Priority"])

# match priority values with the common item
RucksacksWithPriorities = Rucksacks.merge(PriorityLookup,
                                          left_on="CommonItem",
                                          right_on="Character", how="left")

# sum up the total priority score
Solution1 = RucksacksWithPriorities["Priority"].sum()

# PART TWO

Rucksacks2 = Rucksacks.copy()

# removing unnecessary columns for clarity
Rucksacks2 = Rucksacks2[["Items"]]

# how many groups of three elves are there?
NumberOfGroups = int(len(Rucksacks2.index)/3)

# create an ID for each group
GroupIDs = np.repeat(np.arange(1, NumberOfGroups+1), 3)

# assign the IDs
Rucksacks2["GroupID"] = GroupIDs

# merge into one group
RucksacksGrouped = Rucksacks2[["GroupID", "Items"]].groupby(
    "GroupID", as_index=False).agg("_".join)

# split back into the three parts of each group - but now each
# group has its own column
RucksacksGrouped[["Elf1", "Elf2", "Elf3"]] = RucksacksGrouped["Items"].str.split("_", 2, expand=True)

# check which (case-specific) character appears in both compartments
RucksacksGrouped["CommonItem"] = [set(a).intersection(b, c)
                                  for a, b, c in zip(RucksacksGrouped.Elf1,
                                                     RucksacksGrouped.Elf2,
                                                     RucksacksGrouped.Elf3)]
# need to change the column type from sets to strings so that
# the (future) join works
RucksacksGrouped["CommonItem"] = RucksacksGrouped["CommonItem"].str.join("")

# match priority values with the common item
RucksacksGroupedWithPriorities = RucksacksGrouped.merge(PriorityLookup,
                                                        left_on="CommonItem",
                                                        right_on="Character",
                                                        how="left")

# sum up the total priority score
Solution2 = RucksacksGroupedWithPriorities["Priority"].sum()



## questions to think about later why all of this didn't work

#Rucksacks["CommonItem"] = list(set(Rucksacks["FirstCompartment"])&set(Rucksacks["SecondCompartment"]))


# but want to iterate this over all the columns
#list(set(Rucksacks["FirstCompartment"][0])&set(Rucksacks["SecondCompartment"][0]))

#s1="test"
#s2="brE"
#a=list(set(s1)&set(s2))

#test = np.intersect1d(Rucksacks["FirstCompartment"][0], Rucksacks["SecondCompartment"][0])

#np.intersect1d(["h", "i", "j", "k"], ["H", "i","l", "m"])
#np.intersect1d([Rucksacks["FirstCompartment"]], [Rucksacks["SecondCompartment"]])



#test = Rucksacks["HalfDelimiter"][0]
#test2 = 5

#Rucksacks["FirstCompartment"] = Rucksacks["Items"].str[:test]




