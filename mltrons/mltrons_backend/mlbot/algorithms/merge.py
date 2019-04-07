from pyspark.sql.functions import *
import re
import pyspark
from pyspark.sql import SparkSession


class merge():
    def __init__(self, ID, key):
        self.param= {}
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

    #this method merges dataframes and returns the merged dataframe
    def merge(self, df1, df2, pairs):
        df1 = df1.drop('id')
        df2 = df2.drop('id')
        df1, df2, merge_columns, out_names = self.rename_columns(df1, df2, pairs)
        # merge both data frames
        df_final = df1.join(df2, merge_columns)
        if df_final.count() == 0:
            print("Merge not possible")
            return False, False
        print(merge_columns)
        # return dataframe
        return df_final, out_names

    def rename_columns(self, df1, df2, pairs):
        merge_columns = []
        # rename columns bases ona pairs
        out_names = []
        for p in pairs:
            c0 = re.sub('\W+', '', str(p[0]))
            c1 = re.sub('\W+', '', str(p[1]))
            if p[0] != p[1]:
                new_name = c0 + '_' + c1
            else:
                new_name = c0
            print(new_name)
            out_names.append([p[0], new_name])
            out_names.append([p[1], new_name])

            df1 = self.rename(df1, p[0], new_name)
            df2 = self.rename(df2, p[1], new_name)
            merge_columns.append(new_name)
        return df1, df2, merge_columns, out_names

    def rename(self, df, old_name, new_name):
        df = df.withColumnRenamed(old_name, new_name)
        return df
