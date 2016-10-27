import csv
import sumy
import re
from nltk import ngrams
from nltk.corpus import stopwords


def group_by_clusters():
    '''Group courses by clusters'''
    clusters = {}
    cluster_descriptions = {}

    # Course Dept   Course #    Course Name Prerequisites   Units   Tools   Description Course Cluster  Foundational    Applied Meta
    with open('single_clustered_courses.txt', 'r') as readfile:
        cols = csv.reader(readfile, delimiter='\t')
        for col in cols:
            # course_name = col[0] + " " + col[1] + " - " + col[2][re.search("\d", col[2]):]
            course_name = col[0] + " " + col[1]

            description = [word for word in col[6].split() if word not in stopwords.words('english')]
            cluster = col[7].replace("/", " & ")
            if cluster == "nan":
                continue
            if cluster not in clusters:
                clusters[cluster] = [course_name]
                cluster_descriptions[cluster] = [description]
            else:
                clusters[cluster].append(course_name)
                cluster_descriptions[cluster].append(description)


    '''Write tokenized descriptions of each cluster'''
    with open('./clusters/all' + ".txt", "w") as writeall:
        for cluster_course in sorted(clusters.keys()):
            with open('./clusters/' + cluster_course + ".txt", "w") as writefile:
                writefile.write(cluster_course + "\n")
                writeall.write(cluster_course + "\n")
                for course in sorted(clusters[cluster_course]):
                    writefile.write("\t" + course + "\n")
                    writeall.write("\t" + course + "\n")

            with open("./tokenized_phrases/" + cluster_course + ".txt", "w") as write_description_file:
                all_tokenized_phrases = []
                for description in sorted(cluster_descriptions[cluster_course]):

                    all_tokenized_phrases.extend([x for x in ngrams(description, 1)])
                    all_tokenized_phrases.extend([x for x in ngrams(description, 2)])
                    all_tokenized_phrases.extend([x for x in ngrams(description, 3)])
                write_description_file.write(str(set(all_tokenized_phrases)))
    return clusters


def extract_prereq_info():
    courses = {}
    '''
    Extract prerequisite information from the .tsv.
    '''
    with open('courses.tsv', 'r') as csvfile:
        cols = csv.reader(csvfile, delimiter='\t')
        for col in cols:
            prereqs = col[3].split(",")
            # course_name = col[0] + " " + col[1] + " - " + col[2][re.search("\d", col[2]):]
            course_name = col[0] + " " + col[1]

            for prereq in prereqs:
                if prereq not in courses:
                    courses[prereq] = [course_name]
                elif course_name not in courses[prereq]:
                    courses[prereq].append(course_name)

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

    return courses

# Setup Extraction & Clusters
CLUSTERS_TO_COURSES = group_by_clusters()
PREREQS_TO_COURSES = extract_prereq_info()
COURSES_TO_PREREQS = {}
for prereq in PREREQS_TO_COURSES.keys():
    follow_ups = PREREQS_TO_COURSES[prereq]
    for follow_up in follow_ups:
        if follow_up in COURSES_TO_PREREQS:
            COURSES_TO_PREREQS[follow_up].append(prereq)
        else:
            COURSES_TO_PREREQS[follow_up] = [prereq]



def is_prereq(course_name):
    prereq_abbr = course_name.split("(")[1].split(")")[0] + " " + course_name.split()[-1]
    for prereq in PREREQS_TO_COURSES.keys():
        if prereq_abbr in prereq:
            return prereq
    return ""

def get_follow_up_courses(course_lst, depth=0):
    ret_string = ""
    for course_name in course_lst:
        if is_prereq(course_name):
            indents = "\t" * (depth+1)
            ret_string += "\t" * depth + course_name + "\n" + get_follow_up_courses(PREREQS_TO_COURSES[is_prereq(course_name)], depth + 1)
        else:
            ret_string += "\t" * depth + course_name + "\n"
    return ret_string


def has_prereq(course_name):
    prereq_abbr = course_name.split("(")[1].split(")")[0] + " " + course_name.split()[-1]
    for course in COURSES_TO_PREREQS.keys():
        if prereq_abbr in COURSES_TO_PREREQS[course]:
            return COURSES_TO_PREREQS[prereq_abbr]
    return []

def get_prereq_courses(course_name):
    if course_name not in COURSES_TO_PREREQS.keys():
        return ""
    prereqs = sorted(COURSES_TO_PREREQS[course_name])
    for prereq in prereqs:
        for course in COURSES_TO_PREREQS.keys():
            if prereq in course:
                prereqs.extend(get_prereq_courses(COURSES_TO_PREREQS[course]))

    return "" if prereqs == ["None"] else str(prereqs) + "\n\t"


with open("./cluster_paths/all.txt", "w") as write_all_paths:
    for cluster in CLUSTERS_TO_COURSES.keys():
        write_all_paths.write("\n" + cluster + "\n\n")
        cluster_write_string = ""

        for course in sorted(CLUSTERS_TO_COURSES[cluster]):
            cluster_write_string += get_prereq_courses(course) + get_follow_up_courses([course])
            print(get_prereq_courses(course))

        with open("./cluster_paths/" + cluster + ".txt", "w") as write_paths:
            write_paths.write(cluster_write_string)
            write_all_paths.write(cluster_write_string)



