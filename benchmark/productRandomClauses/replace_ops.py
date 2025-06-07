"""
    A Simple Script for replacing Lukiesewitz operators for product ones
"""
import sys, os, subprocess, csv, re, signal

datasets = ["10vars","20vars","30vars","40vars"]

for datasets_dir in datasets :
    for filename in os.listdir(datasets_dir+"/") :
        with open(datasets_dir+"/"+filename, 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('TW', 'TP')
        filedata = filedata.replace('SW', 'SP')
        filedata = filedata.replace('IW', 'IP')
        filedata = filedata.replace('N', 'NP')
        filedata = filedata.replace('TM', 'TP')
        filedata = filedata.replace('SM', 'SP')
        filedata = filedata.replace('IM', 'IP')

        # Write the file out again
        with open(datasets_dir+"/"+filename, 'w') as file:
            file.write(filedata)