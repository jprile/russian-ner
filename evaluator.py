
import re
import numpy as np

### All Simon's work, just moving it into this class. ###

class Evaluator():

    def __init__ (self):
        #Calculate accuracy for 
        self.claim_2_total_correct = 0
        self.claim_2_total_possible = 0
        self.claim_2_total_retrieved = 0
        self.claim_2_total_rec = []
        self.claim_2_total_prec = []
        self.claim_2_total_fscore = []

    # If we ever need to get the stats per iteration and used them in main, we can call this.
    def claim_2_calc_stats(self, ann_people, err_people):
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

    # This will automatically update the totals when called each iteration from main.
    def claim_2_metric(self, ann_people, err_people):
        precision, recall, fscore, correct_ann, possible, retrieved = self.claim_2_calc_stats(ann_people, err_people)
        self.claim_2_total_rec.append(recall)
        self.claim_2_total_prec.append(precision)
        self.claim_2_total_fscore.append(fscore)
        self.claim_2_total_correct += correct_ann
        self.claim_2_total_possible += possible
        self.claim_2_total_retrieved += retrieved

    def claim_2_print(self):
        self.claim_2_total_recall = float(self.claim_2_total_correct / self.claim_2_total_possible)
        self.claim_2_total_precision = float(self.claim_2_total_correct / self.claim_2_total_retrieved)
        print("total Recall: " + str(self.claim_2_total_recall))
        self.claim_2_total_rec_arr = np.array(self.claim_2_total_rec)
        print("Mean Recall: " + str(np.mean(self.claim_2_total_rec_arr)))
        print("total Precision: " + str(self.claim_2_total_precision))
        self.claim_2_total_prec_arr = np.array(self.claim_2_total_prec)
        print("Mean Precision: " + str(np.mean(self.claim_2_total_prec_arr)))
        print("total F-Score: " + str(2 * (self.claim_2_total_recall * self.claim_2_total_precision) / (self.claim_2_total_recall + self.claim_2_total_precision)))
        self.claim_2_total_fscore_arr = np.array(self.claim_2_total_fscore)
        print("Mean F-Score: " + str(np.mean(self.claim_2_total_fscore_arr)))