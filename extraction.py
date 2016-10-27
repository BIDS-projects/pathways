import csv
import re
import sumy

courses = {}
course_summaries = {}
'''
Extract prerequisite information from the .tsv to identify {foundational, applied, meta} weights.
'''
foundational = []
applied = []
meta = []

with open('courses.tsv', 'r') as csvfile:
    cols = csv.reader(csvfile, delimiter='\t')
    for col in cols:
        prereqs = col[3].split(",")

        # Determine Relevance
        if col[8]:
            relevance = col[8]
            rel_lst = foundational
        elif col[9]:
            relevance = col[9]
            rel_lst = applied
        else:
            relevance = col[10]
            rel_lst = meta

        course_name = col[0] + " " + col[1] + " - " + col[2][re.search("\d", col[2]):] + " <" + relevance + ">"
        rel_lst.append(course_name)

        for prereq in prereqs:
            if prereq not in courses:
                courses[prereq] = [course_name]
            elif course_name not in courses[prereq]:
                courses[prereq].append(course_name)

        course_summaries[course_name] = col[4]

# Remove Duplicates
remove_courses = []
for prereq in courses:
    for prereq_string in courses:
        if prereq_string != prereq and prereq in prereq_string:
            for ele in courses[prereq_string]:
                if ele not in courses[prereq]:
                    courses[prereq].append(ele)
            remove_courses.append(prereq_string)

for course in remove_courses:
    if course in courses:
        courses.pop(course)
    if course in course_summaries:
        course_summaries.pop(course)


# Write Summaries
with open("course_summaries.txt", "w") as summaries:
    for key in sorted(course_summaries.keys()):
        summaries.write("\n" + str(key).strip(" ") + ":\n")
        summaries.write("\t" + str(course_summaries[key]) + "\n")

# Write Prereqs
with open('prereq_dictionary.txt', "w") as writefile:
    for key in sorted(courses.keys()):
        writefile.write("\n" + str(key).strip(" ") + ":\n")
        for value in courses[key]:
            writefile.write("\t" + str(value) + "\n")

# Write Relevance
with open("relevance.txt", "w") as relevance_file:
    relevance_file.write("Foundational\n")
    relevance_file.write(str(foundational) + "\n\n")
    relevance_file.write("Applied\n")
    relevance_file.write(str(applied) + "\n\n")
    relevance_file.write("Meta\n")
    relevance_file.write(str(meta) + "\n\n")

from nltk import ngrams
def summarize(name, text):
    unigrams = [x for x in ngrams(text.split(), 1)]
    bigrams = [x for x in ngrams(text.split(), 2)]
    trigrams = [x for x in ngrams(text.split(), 3)]
    quadgrams = [x for x in ngrams(text.split(), 4)]
    with open("tokenized_files/" + name + ".txt", "w") as tokenized_file:
        tokenized_file.write(unigrams + "\n\n" + bigrams + "\n\n" + trigrams + "\n\n" + quadgrams)
