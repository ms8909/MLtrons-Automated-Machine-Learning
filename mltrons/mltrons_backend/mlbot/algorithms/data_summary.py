from pyspark.sql.functions import isnan, when, count, col
from pyspark.sql.types import DoubleType, StringType
import pandas as pd
import pyspark
from pyspark.sql import SparkSession

class data_summary():
    def __init__(self,ID, key):
        #parameters
        self.data_frame=None
        self.param={"summary":None, "count": None, "distributions": None, "columns_types": [], "num_missing_values":None, "columns":None }


        self.sc=pyspark.SparkContext.getOrCreate()
        #configuration
        self.hadoop_conf=self.sc._jsc.hadoopConfiguration()
        self.hadoop_conf.set("fs.s3n.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
        self.hadoop_conf.set("fs.s3n.awsAccessKeyId", ID)
        self.hadoop_conf.set("fs.s3n.awsSecretAccessKey", key)
        # self.sql=pyspark.sql.SparkSession(self.sc)
    #methods
    def set_parameter(self, key, value):
        self.param[key]= value

    def get_parameter(self, key=None):
        if key==None:
            return self.param
        return self.param[key]

    #methods
    def set_dataframe(self, df):
        self.data_frame= df

    def get_dataframe(self):
        return self.data_frame

    def calculate(self):
        # calculate types of each columns
        self.param["column_types"]= self.types()

        # change time to other type
        self.tem_change_type()

        self.param["summary"]= self.summary()
        self.param["count"] = self.count()
        self.param["num_missing_values"]= self.num_missing_values()
        self.param["columns"]= self.columns()

    def tem_change_type(self):
        con_types= ['timestamp']
        f1= self.data_frame
        for c in f1.dtypes:
            if c[1] in con_types:
                f1= f1.withColumn(c[0], col(c[0]).cast(StringType()))
        self.data_frame= f1

    def types(self):
        return self.data_frame.dtypes

    def summary(self):
        return self.data_frame.describe().toPandas()

    def count(self):
        return self.data_frame.count()

    def num_missing_values(self):
        return self.data_frame.select([count(when(isnan(c), c)).alias(c) for c in self.data_frame.columns]).toPandas()

    def columns(self):
        return self.data_frame.columns

    def distributions(self):
        return None
