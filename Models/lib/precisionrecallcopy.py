import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
#from sklearn import cross_validation, linear_model
from sklearn.model_selection import cross_validate
from sklearn.cluster import KMeans
from sklearn import datasets
import random
import time
import pylab as pl

# Method to return random percentage of values from a list
def remove_percentage(list_a, percentage):
    k = int(len(list_a) * percentage)
    random.seed(0)
    indicies = random.sample(range(len(list_a)), k)
    new_list = [list_a[i] for i in indicies]

    return new_list

def precision_recall_calculator(test_data, train_data, model2, percentage):
    
    user_test_sample = None
    ism_training_dict = dict()
    test_dict = dict()
    
    #Create a test sample of users for use in calculating precision
    #and recall
    #Find users common between training and test set
    users_test_and_training = list(set(test_data['user_id'].unique()).intersection(set(train_data['user_id'].unique())))
    print("Length of user_test_and_training:%d" % len(users_test_and_training))

    #Take only random user_sample of users for evaluations
    users_test_sample = remove_percentage(users_test_and_training, percentage)

    print("Length of user sample:%d" % len(users_test_sample))
        
    #Generate recommendations for users in the user test sample
    #For these test_sample users, get top 10 recommendations from training set
    #self.ism_training_dict = {}
    #self.pm_training_dict = {}

    #self.test_dict = {}

    for user_id in users_test_sample:
        #Get items for user_id from item similarity model
        print("Getting recommendations for user:%s" % user_id)
        user_sim_items = model2.recommend(user_id)
        ism_training_dict[user_id] = list(user_sim_items["song_id"])

        #Get items for user_id from test_data
        test_data_user = test_data[test_data['user_id'] == user_id]
        test_dict[user_id] = set(test_data_user['song_id'].unique() )
    
    #Calculate the precision and recall measures
    #Create cutoff list for precision and recall calculation
    cutoff_list = list(range(1,11))


    #For each distinct cutoff:
    #    1. For each distinct user, calculate precision and recall.
    #    2. Calculate average precision and recall.

    ism_avg_precision_list = []
    ism_avg_recall_list = []


    num_users_sample = len(users_test_sample)
    for N in cutoff_list:
        ism_sum_precision = 0
        ism_sum_recall = 0
        ism_avg_precision = 0
        ism_avg_recall = 0

        for user_id in users_test_sample:
            ism_hitset = test_dict[user_id].intersection(set(ism_training_dict[user_id][0:N]))
            testset = test_dict[user_id]
    
            ism_sum_precision += float(len(ism_hitset))/float(len(testset))
            ism_sum_recall += float(len(ism_hitset))/float(N)
    

        ism_avg_precision = ism_sum_precision/float(num_users_sample)
        ism_avg_recall = ism_sum_recall/float(num_users_sample)

        ism_avg_precision_list.append(ism_avg_precision)
        ism_avg_recall_list.append(ism_avg_recall)

        
    return (ism_avg_precision_list, ism_avg_recall_list)

#Method to generate precision and recall curve
def plot_precision_recall(m2_precision_list, m2_recall_list, m2_label):
    pl.clf()    
    pl.plot(m2_recall_list, m2_precision_list, label=m2_label)
    pl.xlabel('Recall')
    pl.ylabel('Precision')
    pl.ylim([0.0, 0.20])
    pl.xlim([0.0, 0.20])
    pl.title('Precision-Recall curve')
    #pl.legend(loc="upper right")
    pl.legend(loc=9, bbox_to_anchor=(0.5, -0.2))
    pl.show()