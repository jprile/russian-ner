import re
from os import walk
from unicodedata import normalize

IGNORE = ['\xa0', ' ', '  ']

def load_data(data_path: str, clean_data = True):
    """
    Returns a list of tuples of (text, annotation) pairs.
    """
    filenames = []
    for (_, _, filenames) in walk(data_path):
        filenames = filenames
        break

    data = []
    for file in filenames:
        if (file.endswith('.txt')):
            sample_name = data_path+ "/" + file[:len(file)-4]

            sample_txt = open(sample_name + ".txt",encoding='utf-8').read()
            sample_ann = open(sample_name + ".ann",encoding='utf-8').read()

            if (clean_data == True):
                sample_txt = sample_txt.replace('\xa0', ' ')
                sample_ann = sample_ann.replace('\xa0', ' ')

            data.append((sample_txt, sample_ann))

    return data


def people_from_annotation(ann: str)-> []:
    ann_people = []
    lines = ann.split('\n')
    for line in lines:
        if(line != ""):
            cols = re.split(r"[ \t]+", line)

            name = []
            type = cols[1]
            if(type == "PERSON"):
                # Get the full name
                for i in range (4, len(cols)):
                    name.append(cols[i])
        if (name != []):
            ann_people.append(name)

    return ann_people

def calculate_stats(ann_people: str,err_people: str):
    all_retrieved = len(err_people)
    correct_ann = 0
    for i in range(len(ann_people)):
        #Convert annotation into same format as model output
        ann_person = str(re.sub('[\']','',str(ann_people[i])))
        if ann_person in err_people:
            err_people.remove(ann_person)
            correct_ann = correct_ann + 1
    recall = float(correct_ann / len(ann_people))
    precision = float(correct_ann / all_retrieved)
    if recall > 0 and precision > 0:
        fscore = 2 * recall * precision / (recall + precision)
    else:
        fscore = 0
    # print("Correct Annotation: " + str(correct_ann), "Precision: " + str(precision), "Recall: " + str(recall))
    return precision,recall, fscore, correct_ann, len(ann_people), all_retrieved
