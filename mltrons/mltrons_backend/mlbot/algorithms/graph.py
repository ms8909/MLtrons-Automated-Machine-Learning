from pyspark.mllib.stat import Statistics
import pandas as pd
import numpy as np
from pyspark.ml.feature import OneHotEncoder, StringIndexer
from pyspark.ml import Pipeline
import pyspark
from pyspark.sql import SparkSession
import time
class generate_graph():

    def __init__(self, ID, key):

        done= True
        while done:
            self.sc=pyspark.SparkContext.getOrCreate()
            if self.sc==None:
                print("something")
                time.sleep(3)
            else:
                done=False


        #configuration
        self.hadoop_conf=self.sc._jsc.hadoopConfiguration()
        self.hadoop_conf.set("fs.s3n.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
        self.hadoop_conf.set("fs.s3n.awsAccessKeyId", ID)
        self.hadoop_conf.set("fs.s3n.awsSecretAccessKey", key)
        # self.sql=pyspark.sql.SparkSession(self.sc)

    def correlation(self, d):
        remove_columns= ['timestamp']
        df= d.na.fill(0)
        df= df.replace('None',None)
        dtypes= df.dtypes
        for t in dtypes:
            if t[1]=='int' or t[1]=='bigint' or t[1]=='double' or t[1]=='float':
                pass
            elif t[1]=="string":
                stringIndexer = StringIndexer(inputCol=t[0], outputCol=t[0]+"_index")
                model = stringIndexer.fit(df)
                pipeline = Pipeline(stages= [stringIndexer])
                pipelineModel = pipeline.fit(df)
                df= pipelineModel.transform(df)
                df= df.drop(t[0])
            elif t[1] in remove_columns: # remove time for time being
                df= df.drop(t[0])
            else:
                pass
        pearson = self.pearson_correlation(df)
        spearman = self.spearman_correlation(df)
        return {"pearson": pearson, "spearman": spearman}

    def pearson_correlation(self, df):

        col_names = df.columns
        features = df.rdd.map(lambda row: row[0:])
        corr_mat = Statistics.corr(features, method="pearson")
        corr_df = pd.DataFrame(corr_mat).fillna(0)
        corr_df.index, corr_df.columns = col_names, col_names
        graph = {}
        graph["x"] = list(corr_df.columns)
        graph["y"] = list(corr_df.columns)
        array = []
        for a in np.array(corr_df):
            l = list(a)
            l2 = [float(i) for i in l]
            array.append(l2)
        graph["array"] = array
        return graph

    def spearman_correlation(self, df):
        col_names = df.columns
        features = df.rdd.map(lambda row: row[0:])
        corr_mat = Statistics.corr(features, method="spearman")
        corr_df = pd.DataFrame(corr_mat).fillna(0)
        corr_df.index, corr_df.columns = col_names, col_names
        graph = {}
        graph["x"] = list(corr_df.columns)
        graph["y"] = list(corr_df.columns)
        array = []
        for a in np.array(corr_df):
            l = list(a)
            l2 = [float(i) for i in l]
            array.append(l2)
        graph["array"] = array
        return graph

    def histogram_from_df(self, d):
        df= d.na.fill(0)
        df= df.replace('None',None)
        graph = {}
        for c in df.dtypes:

            count = df.select(c[0]).distinct().count()
            if c[1] == 'int' or c[1] == 'bigint' or c[1] == 'double' or c[1] == 'float':
                if count < 30:
                    s_df = df.select(c[0])

                    res = s_df.groupBy(c[0]).count()
                    arr = list(np.array(res.select([c[0], 'count']).toPandas()))

                    x = []
                    y = []
                    for a in arr:
                        if type(a[0]) == type("a"):
                            x.append(a[0])
                        else:
                            try:
                                x.append(float(a[0]))
                            except:
                                x.append(a[0])

                        y.append(int(a[1]))

                    graph[c[0]] = {"x": x, "y": y, "graph_type": "bar_chart"}
                else:
                    bins, counts = df.select(c[0]).rdd.flatMap(lambda x: x).histogram(30)
                    graph[c[0]] = {"x": bins, "y": counts, "graph_type": "histogram"}
            else:
                # categorical to int
                if count > 300:
                    pass
                else:
                    s_df = df.select(c[0])

                    res = s_df.groupBy(c[0]).count()
                    arr = list(np.array(res.select([c[0], 'count']).toPandas()))

                    x = []
                    y = []
                    for a in arr:
                        if type(a[0]) == type("a"):
                            x.append(a[0])
                        else:
                            try:
                                x.append(float(a[0]))
                            except:
                                x.append(a[0])

                        y.append(int(a[1]))

                    graph[c[0]] = {"x": x, "y": y, "graph_type": "bar_chart"}

        return graph
