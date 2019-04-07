# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 00:20:11 2017

@author: Muddassar Sharif
"""

from .models import *
from .preprocess  import *
from .graph import *
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import sys
sys.setrecursionlimit(10000)
import random as rd
import datetime
import pickle
class Dashboard():

    def __init__(self, address, y_var):
        self.data_address= address
#        self.models={'LinearModel':[LinearModel() for i in range(3)],'RF':[RF() for i in range(3)], 'SVM': [SVM() for i in range(3)], 'XGBoost':[XGBoost() for i in range(3)], 'HistricalMedian':[HistricalMedian() for i in range(3)], 'KNN':[KNN() for i in range(3)], 'NN_with_EntityEmbedding': [NN_with_EntityEmbedding() for i in range(3)], 'NN2_with_EntityEmbedding': [NN2_with_EntityEmbedding() for i in range(3)], 'NN': [NN() for i in range(3)] }
        self.models={'NN_with_EntityEmbedding': [NN_with_EntityEmbedding() for i in range(1)]}
        self.best_model={}
        self.y_variable=y_var
        basename = "preprocessing_object"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        file_name = "_".join([basename, suffix]) + ".pickle"  # e.g. 'mylogfile_120508_171442'
        self.preprocess_p_file = file_name
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        file_name = "_".join(['best_model', suffix]) + ".pickle"  # e.g. 'mylogfile_120508_171442'
        self.best_model_file = file_name
        self.preprocess_object= preprocess()
        self.preprocess_object.file_address(address)
        self.mode= "train"
        self.rows_info= {"start":0, "end":0}
        self.graph_objects=[]


    #save and load preprocess object
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)


    def check_for_new_data(self):

#        try:
            if len(pd.read_csv(self.data_address).index)== self.rows_info["end"]:
                print("No New Data added to the file")

            else:
            # time to train this baby : incremental learning
                print(len(pd.read_csv(self.data_address).index), self.rows_info["end"])
                print("file has new data")
                self.new_data_transformation()
#        except:
#            print("some error with the file so retraining can not be done")


    def test_train_switch(self, mde):
        self.mode= mde

    def more_data(self, address):
        self.data_address.append(address)

    def file_transformation(self):

        print("reading file")

        temp= self.preprocess_object.read_file(None, self.rows_info["start"])  # just reading 10000 rows for testing right now
        self.rows_info["end"]= temp

        var= self.preprocess_object.variables()
        print(var)

        sel_var= self.preprocess_object.extract_variables(None)
        print(sel_var)

        ans= self.preprocess_object.replace_nan(0)
        print(ans)

        ans= self.preprocess_object.split_time()  # automate this process finding the data using
        print(ans)




        if self.mode == "train":
            ans= self.preprocess_object.Filterout(self.y_variable, 0)
            ans= self.preprocess_object.choose_y(self.y_variable)

            print(ans)




        ans1= self.preprocess_object.category_to_nominal()
        print(ans1)
        dim= self.preprocess_object.calculate_dim()
        print(dim)
        self.preprocess_object.test_train_divide(.2)



    # function to take care of training when new data comes in
    def new_data_transformation(self):

        self.load_preprocess_object()
        print("reading file")
        self.preprocess_object.save_data_and_y()    # this will backup previous data and y
        temp= self.preprocess_object.read_file(None, self.rows_info["end"])    # reading new data



        ans= self.preprocess_object.split_time()  # time variable taken care of
        print(ans)

        sel_var= self.preprocess_object.extract_variables(self.preprocess_object.get_s_variables())  # this will give an errot right now
        print(sel_var)

        ans= self.preprocess_object.replace_nan(0)
        print(ans)



        if self.mode == "train":
            ans= self.preprocess_object.Filterout(self.y_variable, 0)
            ans= self.preprocess_object.choose_y(self.y_variable)

            print(ans)

            # preprocess function to divide the time between test and train


        ans1= self.preprocess_object.category_to_nominal()                               # checked for errors and is working properly.
        print(ans1)

        self.preprocess_object.test_train_divide(.01)                                    # no need for this step as we are just training
        self.save_preprocess_object()
        self.train_best_model()

        self.rows_info["end"] = temp


    def train_best_model(self):
        for model_name in self.best_model.keys():
                self.best_model[model_name][0].train()    # make a traiining function to just train the file




    def finding_best_model(self):
        self.save_preprocess_object()
        if self.best_model.keys()!=[]:
            for model in self.best_model.keys():
                print('fitting'+ str(model))
                for i in range(len(self.best_model[model])):
                    self.best_model[model][i].input(self.preprocess_p_file)

        else:
            for model in self.models.keys():
                for i in range(len(self.models[model])):
                    print('fitting'+ str(model))
                    self.models[model][i].input(self.preprocess_p_file)

            self.update_best_model()


    def update_best_model(self):
        temp= [None,None, 0]
        for i in self.models.keys():
            for model in self.models[i]:
                if model.get_results()>temp[1]:
                    temp=[i, model, model.get_results]
        self.best_model[temp[0]]=[temp[1]]


    # def prediction_key(self):
    #     self.load_preprocess_object()
    #     key= self.preprocess_object.get_key_for_perdiction()
    #     graph1= graph()
    #     self.graph_objects.append(graph1)
    #     self.graph_objects[-1].key_from_user(key)
    #     return [self.graph_objects.index(self.graph_objects[-1]), key[0], key[1]]

    def get_prediction_key(self):
            # self.load_preprocess_object()
        self.key= self.preprocess_object.get_key_for_perdiction()
        return [-1, list(self.key[0]), self.key[1]]
            #        graph1= graph()
            #        self.graph_objects.append(graph1)
            #        self.graph_objects[-1].key_from_user(key)
            #        return [self.graph_objects.index(self.graph_objects[-1]), key[0], key[1]]

    def make_graph_object(self):
            #        self.load_preprocess_object()
        #key= self.preprocess_object.get_key_for_perdiction()
        graph1 = graph()
        self.graph_objects.append(graph1)
        self.graph_objects[-1].key_from_user(self.key)
        return self.graph_objects.index(self.graph_objects[-1])

    def make_graph(self, k, user_in):
        if user_in != None:
            self.graph_objects[k].user_input(user_in)
            # return self.graph_objects[k].get_df_for_per()
        y = self.best_model[self.best_model.keys()[0]][0].guess(np.array(self.graph_objects[k].get_df_for_per()))
        self.graph_objects[k].set_per_y(y)

        return [self.graph_objects.index(self.graph_objects[k]), self.graph_objects[k].get_plot_data()]


    def get_best_model(self):
        return self.best_model

    def get_trained_models(self):
        return self.models

    def get_preporcessed_file(self):
        return self.preprocess_object

    def save(self):
        #save the best model

        with open(self.best_model_file, 'wb') as f:
            pickle.dump((self.best_model), f, protocol=pickle.HIGHEST_PROTOCOL)

        return self.best_model_file






    #implement changes on other models after one model is finalized.



def main(args):
    file_object= Dashboard(args[0], args[1])
    file_object.file_transformation()
    file_object.finding_best_model()
    file_object.update_best_model()
    file_name= file_object.save()

    return file_object, file_name

#x, file_name = main(['t.csv', 'Sales'])






#
#for tomorrow:
#        modify the model.py file
#        modify the preprocess file to handle new data scenerios
#        test
#        come up with the way to run the code using command line
#
# try to store the inner the preprocess also in a pickle file so you can remove the burden of the the main pickle file
