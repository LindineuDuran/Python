# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:42:21 2020

@author: lindineu.duran
"""

import csv
import os

app_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(app_path, 'protagonist.csv')

row_list = [["SN", "Name", "Contribution"],
             [1, "Linus Torvalds", "Linux Kernel"],
             [2, "Tim Berners-Lee", "World Wide Web"],
             [3, "Guido van Rossum", "Python Programming"]]

with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list)
