# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:48:23 2017

@author: Muddassar Sharif
"""
import numpy as np
import pandas as pd
from sklearn import preprocessing
import pickle
import math
from sklearn.model_selection import train_test_split
import random as rd
#from multiple_files import *
import csv
import io
import datetime
class preprocess():

    def __init__(self):
        self.address= None
        self.list_variables=[]
        self.list_s_variables=[]
        self.y_var=None
        self.mean=[]
        self.st_dev=[]
        self.io_dim=[[],[]]
        self.data_array=[]

        self.data= 0
        self.y=None
        self.key={}
        self.convert=False
        self.train_x=[]
        self.train_x=[]
        self.train_y=[]
        self.test_y=[]
        self.time= None



    def file_address(self, address):
        self.address= address


    def save_data_and_y(self):
        basename = "preprocessing"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        file_name = "_".join([basename, suffix]) + ".pickle"  # e.g. 'mylogfile_120508_171442'
        self.preprocess_p_file = file_name
        self.data_array.append(self.preprocess_p_file)

        with open(self.data_array[-1], 'wb') as f:
            pickle.dump((self.data, self.y), f, protocol=pickle.HIGHEST_PROTOCOL)

        # time to empty the spaces
        self.data=0
        self.y= None
        self.train_x=[]
        self.train_x=[]
        self.train_y=[]
        self.test_y =[]


    def load_data_and_y(self, i):
        with open(self.data_array[i], 'rb') as f:
            self.data, self.y= pickle.load(f)



    def read_file(self, nrows, start):   # needs modification
        try:
            if start== 0:

                if nrows== None:
                    csv_file = self.address
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    #reader = csv.reader(io_string, delimiter=';', quotechar='|')
                    try:
                        self.data= pd.read_csv(io_string)
                    except:
                        self.data = pd.read_excel(io_string)
                    return len(self.data.index)
                else:
                    csv_file = self.address
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    # reader = csv.reader(io_string, delimiter=';', quotechar='|')
                    self.data = pd.read_csv(io_string, nrows= nrows)
                    return len(self.data.index)
            else:
                csv_file = self.address
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                # reader = csv.reader(io_string, delimiter=';', quotechar='|')
                self.data = pd.read_csv(io_string)
                index= len(self.data.index)
                self.data = self.data[start:]
                return index

        except Exception as e:
            print( str(e))
            print("File does not exist")
            return 0

    def pandas_data(self):
        return self.data

    def variables(self):
        self.list_variables= self.data.columns.values.tolist()
        self.list_s_variables= self.list_s_variables
        return self.list_variables

    def extract_variables(self, variables):
        if variables == None:
            if self.list_s_variables==[]:

                self.list_s_variables= np.array(self.list_variables)
        else:
            self.list_s_variables= np.array(variables)

        if self.convert== True:
            self.data=self.data[np.append(self.list_s_variables, self.y_var)]
        return self.list_s_variables

    def replace_nan(self, nan):
        try:

            self.data= self.data.fillna(nan)
            return " replace nan done!"
        except:
            print("sorry an error occured!" )
            return " Sorry replace nan not done"

    def split_time(self):
        self.time = None
        temp1 = []
        for col in self.list_s_variables:
            if self.data[col].dtype == 'object':
                try:
                    x = pd.to_datetime(self.data[col][:20])
                    temp1.append(col)
                except ValueError:
                    pass

        if temp1 == []:
            return "files does not have the time attribute"
        else:
            self.time = temp1[0]
            temp = pd.to_datetime(self.data[self.time])

            self.data[self.time + 'yearrr'] = temp.dt.year
            self.data[self.time + 'monthhh'] = temp.dt.month
            self.data[self.time + 'dayyy'] = temp.dt.day
            if self.convert == False:  # limit to running only the first time

                self.list_s_variables = np.append(self.list_s_variables, self.time + 'yearrr')
                self.list_s_variables = np.append(self.list_s_variables, self.time + 'monthhh')
                self.list_s_variables = np.append(self.list_s_variables, self.time + 'dayyy')
                self.list_variables = np.append(self.list_variables, self.time + 'yearrr')
                self.list_variables = np.append(self.list_variables, self.time + 'monthhh')
                self.list_variables = np.append(self.list_variables, self.time + 'dayyy')

                i = np.where(self.list_s_variables == self.time)
                self.list_s_variables = np.delete(self.list_s_variables, i[0][0], None)

            self.data = self.data.drop(self.time, axis=1)

            return "removed and splitted " + self.time + "!"


    def delete_row(self,row):
        try:
            self.data=self.data.drop(row, axis=1)
            i= np.where(self.list_s_variables==row)
            self.list_s_variables= np.delete(self.list_s_variables, i[0][0], None)
            return "row " +str(row) +" deleted"
        except:
            return "row " +str(row) + " does not exist"

    def Filterout(self, row, value):
        try:
            self.data = self.data.loc[self.data[row]!=value]
            return "data only contain rows with: " + str(row) +" != " + str(value)
        except:
            return "please check your inputs please. Filteration not done"

    def Filterin(self, row, value):
        try:
            self.data = self.data.loc[self.data[row]==value]
            return "data only contain rows with: " + str(row) +"==" + str(value)
        except:
            return "please check your inputs please. Filteration not done"

    def Binning(self, inp):# not tested yet
        try:

            if inp==None:
                for x in self.list_s_variables:
                    if (type(self.data[x][1])== np.int64 ) or (type(self.data[x][1])== np.float64 ):
        #                    #binning when required
                            if (self.data[[x]].max()-self.data[[x]].min()) > 40:
                                length= 20
                                group_names = [i for i in range(1,length+1)]
                                jump= (self.data[[x]].max()-self.data[[x]].min())/length+ (self.data[[x]].max()-self.data[[x]].min())%length
                                number=self.data[[x]].min()
                                bins=[]
                                for j in range(len(length)+1):
                                    bins.append(number)
                                    number= number+jump

                                bins[0]= bins[0]-10
                                bins[-1]= bins[-1] + 10
                                self.data[x] = pd.cut(self.data[x], bins, labels=group_names)
                    else:
                        pass

            else:
                if (self.data[[inp]].max()-self.data[[inp]].min()) > 40:
                    length= 20
                    group_names = [i for i in range(1,length+1)]
                    jump= (self.data[[x]].max()-self.data[[x]].min())/length+ (self.data[[x]].max()-self.data[[x]].min())%length
                    number=self.data[[x]].min()
                    bins=[]
                    for j in range(len(length)+1):
                        bins.append(number)
                        number= number+jump

                        bins[0]= bins[0]-10
                        bins[-1]= bins[-1] + 10
                        self.data[x] = pd.cut(self.data[x], bins, labels=group_names)
            return "Binning Done!"
        except:
            return "An error occured when Binning"


    def category_to_nominal(self):
        if self.convert==False:
            self.convert= self.make_key()

        for x in self.list_s_variables:

            if (type(np.array(self.data[x])[1])== np.int64 ) or (type(np.array(self.data[x])[1])== np.float64 ) or (type(np.array(self.data[x])[1])== long ):
#                    std= self.data[[x]].std()
#                    mean= self.data[[x]].mean()
#                    self.data[[x]]=np.tan(np.array(((self.data[[x]]-mean)/std)*.01 +1))
                pass
            else:
                self.data[[x]]=self.nom_convert_int(self.data[[x]],x)

        return "categoricol to nominal done!"

    def y_to_float(self, y):
        try:
            self.data[y]= np.array(self.data[y].str.replace(",", "").astype(float))
            return " y converted to float "

        except:
            return " Error while converting y to float"


    def choose_y(self, y):
        temp= self.y_to_float(y)
        self.y_var= y
        self.y= np.array(self.data[y])

        self.data=self.data.drop(y, axis=1)

        if self.convert== False:
            i= np.where(self.list_s_variables==y)

            self.list_s_variables= np.delete(self.list_s_variables, i[0][0], None)

        return "y choosen"

    def normalize(self):
#        self.mean
#        self.st_dev
        return True

    def calculate_dim(self):
        for x in self.list_s_variables:
            temp = (int(max(len(self.data[x].unique()), self.data[x].max())) + 5)
            self.io_dim[0].append(temp)
            if temp >= 8:
                self.io_dim[1].append(int(temp * .025 + 3))
            else:
                self.io_dim[1].append(temp - 1)

        return "dimensions calculated"

    def test_train_divide(self, l):
        self.train_x , self.test_x, self.train_y ,self.test_y= train_test_split(np.array(self.data),np.array(self.y), test_size=l)


    def get_train_x(self):
        return self.train_x
    def get_test_x(self):
        return self.test_x
    def get_train_y(self):
        return self.train_y
    def get_test_y(self):
        return self.test_y

    def get_x(self):
        return self.data

    def get_y(self):
        return self.y

    def get_y_var(self):
        return self.y_var

    def get_dim(self):
        return self.io_dim

    def get_key(self):
        return self.key

    def get_s_variables(self):
        return self.list_s_variables

    def get_time_var_name(self):
        return self.time

    def set_key(self, key):
        self.key= key
        self.convert=True


    def preprocess_data(self):

        return True

    def split_data(self, split_rate):
        return True
        #store split data somewhere

    def save_file(self, path):
        self.data.to_pickle(path, compression='infer')
        return path
        #mongodb vs pickle for now
        # how about saving pickle file in mongodb


    def nom_convert_int(self,df,x):
        import numpy as np
        counter=0
        x_c= np.array(df)
        dic=self.key[x]
        for i in x_c:
            if i[0] in dic:
                pass
            else:
                dic[i[0]]=counter
                counter=counter+1
        for j in range(len(x_c)):
             x_c[j][0]=dic[x_c[j][0]]

        self.key[x]=dic
        return x_c


    def make_key(self):
        for i in self.list_s_variables:
            self.key[i]={}

        self.convert= True
        return True


    def get_key_for_perdiction(self):

        return [self.list_s_variables, self.key]
