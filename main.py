### This is a demo ###
import numpy as np
import spacy
import re
from tqdm import tqdm
from annotation import Annotation
from evaluator import Evaluator
from spacy.lang.ru.examples import sentences 
from descriptions import PROJECT_ROOT_DIR
from util.data_utils import load_data, people_from_annotation, calculate_stats, IGNORE

train_path = PROJECT_ROOT_DIR + "/data/NEREL-v1.1/train"
test_path =  PROJECT_ROOT_DIR + "/data/NEREL-v1.1/test"

nlp = spacy.load("ru_core_news_sm")

# Load training data
train_data = load_data(train_path)

# Pick the first sample from training data
train_data_sample = train_data[0]

### Performance Metrics ###
eval = Evaluator()

for train_data_sample in tqdm(train_data, desc="Analyzing"):
    # Unpack sample into the original text and annotation
    text, ann = train_data_sample

    # Wrap text with nlp instance
    doc = nlp(text)

    # Create annoation instance from this annoataion
    annotation = Annotation(ann)

    # Get a list of all of the people from this document's annotation
    ann_people = []
    for name in annotation.names:
        ann_people.append(name[0])

    people = []
    err_people = []
    name_list = []

    alternate_names = []
    # This loops greedily tries to build the longest @name and adds it to @people. 
    for token in doc:
        if (token.ent_type_ == "PER"):
            name_list.append(token)
            
        else:
            # This wasn't a name, so add the current name and then flush.
            if (len(name_list) > 0):

                ### Alternate name identification ###

                # TODO: modify name

                people.append(name_list)
                err_people.append(str(name_list))
                name_list = []

    # print (annotation.org_alt_name_pairs)
    # exit()

    eval.claim_2_metric(ann_people, err_people)

eval.claim_2_print()
