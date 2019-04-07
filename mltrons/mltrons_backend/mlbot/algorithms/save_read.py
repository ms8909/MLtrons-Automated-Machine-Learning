import os
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import isnan, when, count, col
from pyspark.sql.functions import monotonically_increasing_id
from datetime import datetime
import boto3
from pyspark.sql import SQLContext
from django.conf import settings
import re
from pyspark.sql.types import DoubleType, StringType
from pyspark.sql import functions as F
from pyspark.sql.window import Window as W
from pyspark import SparkConf, SparkContext
import time

class save_read():
    def __init__(self, ID, key):

        # make sure all libraries are installed
        #initialize context


# make sure pyspark tells workers to use python3 not 2 if both are installed
        #os.environ['PYSPARK_PYTHON'] = '/home/ubuntu/app/env/env/bin/python'
        #os.environ['PYSPARK_DRIVER_PYTHON'] = '/home/ubuntu/app/env/env/bin/python'
        #os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'
        os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages=org.apache.hadoop:hadoop-aws:2.7.3 pyspark-shell"

        done= True
        while done:
            self.sc=pyspark.SparkContext.getOrCreate()
            if self.sc==None:
                print("something")
                time.sleep(2)
            else:
                done=False

        #configuration

        ### try miltiple times
        self.hadoop_conf=self.sc._jsc.hadoopConfiguration()
        self.hadoop_conf.set("fs.s3n.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
        self.hadoop_conf.set("fs.s3n.awsAccessKeyId", ID)
        self.hadoop_conf.set("fs.s3n.awsSecretAccessKey", key)
        self.sql=pyspark.sql.SparkSession(self.sc)

                ## config changed
                # conf = SparkConf()
                # conf = (conf.setMaster('local[*]')
                #         .set('spark.executor.memory', '40G')
                #         .set('spark.driver.memory', '45G')
                #         .set('spark.driver.maxResultSize', '10G'))
                # try:
                #     self.sc=pyspark.SparkContext(conf=conf).getOrCreate()
                #     print("new context")
                # except:
                #     self.sc=pyspark.SparkContext.getOrCreate()
                ## ends


        #parameters
        self.data_frame=None

        # session usinf boto
        self.session = boto3.Session(
                        aws_access_key_id=ID,
                        aws_secret_access_key=key,
                    )
        self.s3 = self.session.client('s3')


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

    def save_on_local_machine(self, df=None, path=None):
        # calculate types of each columns
        if path!=None:
            self.path= path
        else:
            self.path= "example_file.parquet"
        if df!=None:
            self.data_frame= df

        self.data_frame.write.save(self.path, format="parquet")


    def read_as_df(self, bucket=settings.S3_BUCKET, path=None):
        if path==None:
            print("path not given.")
            return False
        try:
            self.data_frame= self.sql.read.parquet('s3n://'+bucket+'/'+ path)
            return self.data_frame
        except Exception as e:
            print("path doesnot exist.", e)
            return False


    def save_df_on_s3(self, df=None, bucket=settings.S3_BUCKET, path=None):
        if df==None:
            print("data frame not given.")
            return None
        if path==None:
            path= datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3].replace(" ","")

        try:
            exprs = [col(column).alias(column.replace(' ', '_')) for column in df.columns]
            df = df.select(*exprs)

        except:
            pass
        try:
            windowSpec = W.orderBy(df.columns[0])
            df= df.withColumn("id", F.row_number().over(windowSpec))
            for t in df.dtypes:
                if t[1]== 'timestamp':
                    df= df.withColumn(t[0], col(t[0]).cast(StringType()))
            df.coalesce(1).write.save('s3n://'+bucket+'/'+path, format="parquet")


            print("Data frame saved on s3")
            bucket = 'mltrons'

            # returns file name
            files = self.s3.list_objects(Bucket=bucket, Prefix=path+'/', Delimiter='/')
            file_address= files['Contents'][1]['Key']
            return file_address
        except Exception as e:
            print(e)
            return False

    def save_df_on_s3_test(self, df=None, bucket=settings.S3_BUCKET, path=None):
        if df==None:
            print("data frame not given.")
            return None
        if path==None:
            path= datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3].replace(" ","")

        try:
            exprs = [col(column).alias(column.replace(' ', '_')) for column in df.columns]
            df = df.select(*exprs)

        except:
            pass
        try:
            df = df.select("*").withColumn("id", monotonically_increasing_id())


            sqlContext = SQLContext(self.sc)

            columns = ['id', 'dogs', 'cats']
            vals = [
                 (1, 2, 0),
                 (2, 0, 1)
            ]

            df2 = sqlContext.createDataFrame(vals, columns)
            df2= df
            df2.coalesce(1).write.save('s3n://'+bucket+'/'+path, format="parquet")
            print("Data frame saved on s3")
            bucket = 'mltrons'

            # returns file name
            files = self.s3.list_objects(Bucket=bucket, Prefix=path+'/', Delimiter='/')
            file_address= files['Contents'][1]['Key']
            return file_address
        except Exception as e:
            print(e)
            return False

    def read_as_df_local(self, path=None, ID=1):
        if path == None:
            print("path not given.")
            return False
        try:
            self.data_frame = self.sql.read.csv(path, inferSchema=True, header=True)
            columns = self.data_frame.columns
            for c in columns:
                c_new= re.sub('[^A-Za-z0-9]+', '', c) + '_'+str(ID)
                self.data_frame = self.data_frame.withColumnRenamed(c, c_new)

            return self.data_frame
        except Exception as e:
            print("path doesnot exist.", e)
            return False

    def read_parquet_as_json(self, bucket='mltrons', path=None, offset=None, limit= None):
        if path==None:
            print("path not given.")
            return False

        if offset==None or limit==None:
            expression= "select * from s3object"
        else:

            # use offset and limit
            frm= offset-1
            to= frm + limit
            expression= "select * from s3object where id>="+ str(frm)+" and id<"+ str(to)

        try:
            r1 = self.s3.select_object_content(
                Bucket=bucket,
                Key=path,
                ExpressionType='SQL',
                Expression=expression,
                InputSerialization={'Parquet': {}},
                OutputSerialization={'JSON': {}},
            )
        except Exception as e:
            print("path doesnot exist.",e)
            return False

        # make a json and send

        array = []
        for event in r1['Payload']:
            if 'Records' in event:
                records = event['Records']['Payload'].decode('utf-8')
                array = records.split('\n')
        return_array = []
        import json
        for i in range(len(array)):
            try:
                return_array.append(json.loads(array[i]))
            except:
                pass
        return return_array
