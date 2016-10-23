import csv
import sumy
from nltk import ngrams
# Course Dept   Course #    Course Name Prerequisites   Units   Tools   Description Course Cluster  Foundational    Applied Meta

clusters = {}
cluster_descriptions = {}

with open('single_clustered_courses.txt', 'r') as readfile:
    cols = csv.reader(readfile, delimiter='\t')
    for col in cols:
        name = col[0] + " " + col[1]
        description = col[6]
        cluster = col[7].replace("/", " & ")
        if cluster == "nan":
            continue
        if cluster not in clusters:
            clusters[cluster] = [name]
            cluster_descriptions[cluster] = [description]
        else:
            clusters[cluster].append(name)
            cluster_descriptions[cluster].append(description)


with open('./clusters/all', "w") as writeall:
    for cluster_name in clusters:
        with open('./clusters/' + cluster_name, "w") as writefile:

            writefile.write(cluster_name + "\n")
            writeall.write(cluster_name + "\n")
            for course in clusters[cluster_name]:
                writefile.write("\t" + course + "\n")
                writeall.write("\t" + course + "\n")

        with open("./tokenized_phrases/" + cluster_name, "w") as write_description_file:
            all_tokenized_phrases = []
            for description in cluster_descriptions[cluster_name]:
                all_tokenized_phrases.extend([x for x in ngrams(description.split(), 1)])
                all_tokenized_phrases.extend([x for x in ngrams(description.split(), 2)])
                all_tokenized_phrases.extend([x for x in ngrams(description.split(), 3)])
            write_description_file.write(str(all_tokenized_phrases))



