import pandas as pd
import numpy as np
import pyspark as spark
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import isnan, when, count, col


class load_file():
    def __init__(self):

        # parameters
        self.spark = SparkSession.builder.appName("python SparkSQL basic example").getOrCreate()
        self.data_frame = None

        # variables

    # methods
    def set_data_frame(self, df):
        self.data_frame = df

    def get_data_frame(self):
        return self.data_frame

    def load_from_csv(self, path):
        try:
            self.data_frame = self.spark.read.csv(path, inferSchema=True, header=True)
            return 1
        except:
            return 0

    def load_from_json(self, path):
        return 1

    def load_from_sql(self, path):
        return 0

    def load_from_excel(self, path):
        return 0


class data_summary():

    def __init__(self):
        # parameters
        self.data_frame = None
        self.param = {"summary": None, "count": None, "distributions": None, "columns_types": [],
                      "num_missing_values": None, "columns": None}

        # variables

    # methods
    def set_parameter(self, key, value):
        self.param[key] = value

    def get_parameter(self, key=None):
        if key == None:
            return self.param
        return self.param[key]

        # methods

    def set_dataframe(self, df):
        self.data_frame = df

    def get_dataframe(self):
        return self.data_frame

    def calculate(self):
        # calculate types of each columns
        self.param["column_types"] = self.types()
        self.param["summary"] = self.summary()
        self.param["count"] = self.count()
        self.param["num_missing_values"] = self.num_missing_values()
        self.param["columns"] = self.columns()

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

# l= load_file()
# s= data_summary()
# l.load_from_csv('trainn.csv')
# s.set_dataframe(l.get_data_frame())
# s.calculate()
# b=s.get_parameter()

# import pyspark
# sc=pyspark.SparkContext()
# hadoop_conf=sc._jsc.hadoopConfiguration()
# hadoop_conf.set("fs.s3n.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
# hadoop_conf.set("fs.s3n.awsAccessKeyId", 'AKIAJFHAJ5DUZOUWMGPA')
# hadoop_conf.set("fs.s3n.awsSecretAccessKey", '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')
# sql=pyspark.sql.SparkSession(sc)
# df= sql.read.csv('', inferSchema = True, header = True)
# exprs = [col(column).alias(column.replace(' ', '_')) for column in df.columns]
# df = df.select(*exprs)
# df.write.save('s3n://mltrons/mydata.parquet', format="parquet")

