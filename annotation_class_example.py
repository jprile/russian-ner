from descriptions import PROJECT_ROOT_DIR
from util.data_utils import load_data
from annotation import Annotation

train_path = PROJECT_ROOT_DIR + "/data/NEREL-v1.1/train"
test_path =  PROJECT_ROOT_DIR + "/data/NEREL-v1.1/test"

# Load training data
train_data = load_data(train_path)

# Pick the first sample from training data
train_data_sample = train_data[0]

# Unpack sample into the original text and annotation
text, ann = train_data_sample

### Create a new Annotation object by wrapping an annotation text file ###
annotation = Annotation(ann)

### You can now access all of the Name objects within that annotation object ###
for name in annotation.names:

    ### Name objects have a name field which is a list containing each part of the name
    print("name: " + str(name.name))

    ### Name objects also have starting and ending characters for each name ###
    print("position (start_char, end_char): " + name.start_char + "," + name.end_char)

    ### You can get the alternate names for any name by using 
    ### the Annotation classes' get_alt_names method
    alt_names = annotation.get_alt_names(name.name)
    print("alterante names: " + str(alt_names))

    print("----------------------------------------")
