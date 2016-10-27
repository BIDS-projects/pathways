import csv
import re

with open('prereq_dictionary.txt', "r") as prereqs_file:


clusters = {}
with open('all', "r") as all_clusters_file:
	for line in all_clusters_file:
