from pyspark.ml.feature import OneHotEncoder, StringIndexer
from pyspark.sql import SQLContext as spark
from pyspark.sql.functions import isnan, when, count, col, from_unixtime
from pyspark.ml import Pipeline, Transformer
from pyspark.ml.feature import Imputer
from pyspark.sql.functions import year, month, dayofmonth
from pyspark.sql.functions import *
from pyspark.sql.types import DoubleType, TimestampType
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable, JavaMLReadable, JavaMLWritable
from datetime import datetime
from pyspark.sql.functions import udf
from pyspark.sql.types import DateType
from pyspark.ml.param.shared import *
import random
import string
import pyspark
from pyspark.sql import SparkSession
import time

class correct_day_format(Transformer,DefaultParamsReadable, DefaultParamsWritable):
    column = Param(Params._dummy(), "column", "column for transformation", typeConverter=TypeConverters.toString)
    formt = Param(Params._dummy(), "formt", "format", typeConverter=TypeConverters.toString)

    def __init__(self, column='', formt=''):
        super(correct_day_format, self).__init__()
        # lazy workaround - a transformer needs to have these attributes
#         self._defaultParamMap = dict()
#         self._paramMap = dict()
        self._setDefault(formt=formt, column= column)
        self.setColumn(column)
        self.setFormt(formt)


#         self.uid= str(uuid.uuid4())


    def getColumn(self):
        """
        Gets the value of withMean or its default value.
        """
        return self.getOrDefault(self.column)


    def setColumn(self, value):
        """
        Sets the value of :py:attr:`withStd`.
        """
        return self._set(column=value)

    def getFormt(self):
        """
        Gets the value of withMean or its default value.
        """
        return self.getOrDefault(self.formt)


    def setFormt(self, value):
        """
        Sets the value of :py:attr:`withStd`.
        """
        return self._set(formt=value)


    def _transform(self,df):
        df= df.withColumn(self.getColumn(), from_unixtime(unix_timestamp(self.getColumn(), self.getFormt())).cast(TimestampType()))

        df= df.withColumn('yearrr', year(self.getColumn()))
        df= df.withColumn('monthhh', month(self.getColumn()))
        df= df.withColumn('dayyy', dayofmonth(self.getColumn()))
        df= df.withColumn('dayofweekkk', dayofweek(self.getColumn()))
        df= df.withColumn('hourrr', hour(self.getColumn()))
        df= df.withColumn('minutesss', minute(self.getColumn()))
        df= df.withColumn('secondss', second(self.getColumn()))
        df= df.drop(self.getColumn())
        return df


class transform_pipeline():
    def __init__(self, ID, key):
        #variables
        self.pipeline=None
        self.stages=[]
        # selected_columns specifies the order of the columns
        self.param={'variables_updated':False, 'columns': [], 'y_variable': None, 'time_variable':[], 'selected_columns':[],  'correct_var_types':{}}

        done= True
        while done:
            self.sc=pyspark.SparkContext.getOrCreate()
            if self.sc==None:
                print("something")
                time.sleep(2)
            else:
                done=False
        #configuration
        self.hadoop_conf=self.sc._jsc.hadoopConfiguration()
        self.hadoop_conf.set("fs.s3n.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
        self.hadoop_conf.set("fs.s3n.awsAccessKeyId", ID)
        self.hadoop_conf.set("fs.s3n.awsSecretAccessKey", key)
        self.sql=pyspark.sql.SparkSession(self.sc)

    #methods
    def set_parameter(self, key, value):
        self.param[key]= value

    def get_parameter(self, key=None):
        if key==None:
            return self.param
        return self.param[key]


    #methods
    def save_pipeline(self, bucket= 'mltrons', path=None):
        if path==None:
            #generate own path
            path= ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

        self.pipeline.save('s3n://'+bucket+'/'+ path)
        return path

    def load_pipeline(self, df= None, bucket= 'mltrons', path=None):
        if df== None:
            print("PLease provide test df")
            return False
        pipeline = Pipeline.load('s3n://'+bucket+'/'+ path)
        self.pipeline= pipeline.fit(df)
        return self.pipeline

    def remove_y_from_variables(self, variables, y_var, training=True):
        new_variable = []
        if training == True:
            for v in variables:
                if y_var == v[0]:
                    pass
                else:
                    new_variable.append(v)
        return new_variable

    def convert_y_to_float(self, df, y_var):
        return df.withColumn(y_var, col(y_var).cast(DoubleType()))

    def transform(self, df=None):
        if df==None:
            print("Please provide dataframe to build")
            return False

        if self.pipeline==None:
            print("Please build or load the pipeline first.")
            return False
        df= self.pipeline.transform(df)
        return df

    def build_pipeline(self, df=None):
        # make sure all the variables are available
        if self.param['variables_updated']==False:
            print("Summary parameters are missing.")
            return False
        if df == None:
            print("Please provide dataframe to build a pipeline")
            return False


        # handle time
        try:
            self.split_change_time()
        except Exception as e:
            print(e, "in split time")
            return False

        # convert int to double
        try:
            self.int_to_double()
        except Exception as e:
            print(e, "int to double")
            return False

        # categories: string to integer
        try:
            self.categorical_to_float()
        except Exception as e:
            print(e, "categorical to float")
            return False

        # handle imputations
        try:
            self.handle_missing_values()
        except Exception as e:
            print(e, "handling missing values")
            return False


        pi= Pipeline(stages=self.stages)

        self.pipeline = pi.fit(df)
#         self.param['selected_columns'].remove(self.param['y_varaible'])
#         return self.param['selected_columns']
        return True


    def int_to_double(self):
        co= ['bigint', 'int', 'double', 'float']
        for colum in self.param["columns"]:
            if self.param['correct_var_types'][colum[0]] in co:
                # time to transform
                change = change_type(column=colum[0])
                self.stages+= [change]


    def categorical_to_float(self):

        for column in self.param["columns"]:
            if self.param['time_variable']!=[]:
                if column[0]== self.param['time_variable'][0]:
                    continue
            if column[1]=='string':
                # time to transform
                stringIndexer = StringIndexer(inputCol=column[0], outputCol=column[0] + "Index").setHandleInvalid("keep")
                self.param["selected_columns"].append(column[0] + "Index")
                self.stages+= [stringIndexer]
                d = drop(column[0])
                self.stages+= [d]
            else:
                self.param["selected_columns"].append(column[0])

    def handle_missing_values(self):

        imputer = Imputer(
                            inputCols=self.param["selected_columns"],
                            outputCols=self.param["selected_columns"]
                        )
        self.stages+= [imputer]


    def split_change_time(self):
        if self.param['time_variable'] != []:
            time= correct_day_format(self.param['time_variable'][0], self.param['time_variable'][1])
            self.stages+= [time]

    def drop_empty_columns(self):
        pass



class change_type(Transformer,DefaultParamsReadable, DefaultParamsWritable):

    column = Param(Params._dummy(), "column", "column for transformation", typeConverter=TypeConverters.toString)

    def __init__(self, column=''):
        super(change_type, self).__init__()

        self._setDefault(column= column)
        self.setColumn(column)

    def getColumn(self):
        """
        Gets the value of withMean or its default value.
        """
        return self.getOrDefault(self.column)


    def setColumn(self, value):
        """
        Sets the value of :py:attr:`withStd`.
        """
        return self._set(column=value)


    def _transform(self,df):
        return df.withColumn(self.getColumn(), col(self.getColumn()).cast(DoubleType()))


class drop(Transformer,DefaultParamsReadable, DefaultParamsWritable):

    column = Param(Params._dummy(), "column", "column for transformation", typeConverter=TypeConverters.toString)

    def __init__(self, column=''):
        super(drop, self).__init__()

        self._setDefault(column= column)
        self.setColumn(column)

    def getColumn(self):
        """
        Gets the value of withMean or its default value.
        """
        return self.getOrDefault(self.column)


    def setColumn(self, value):
        """
        Sets the value of :py:attr:`withStd`.
        """
        return self._set(column=value)


    def _transform(self,df):
        return df.drop(self.getColumn())
