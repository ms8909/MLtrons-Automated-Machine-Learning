from django.apps import AppConfig
from django.conf import settings
import pyspark
import os
from pyspark import SparkConf, SparkContext

class ProjectConfig(AppConfig):
    name = 'project'
    verbose_name = "Project"

    def ready(self):
        pass
        # os.environ['PYSPARK_PYTHON'] = '/home/ubuntu/app/env/env/bin/python'
        # os.environ['PYSPARK_DRIVER_PYTHON'] = '/home/ubuntu/app/env/env/bin/python'
        # os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages=org.apache.hadoop:hadoop-aws:2.7.3 pyspark-shell"
        # sc=pyspark.SparkContext()
        # conf = SparkConf()
        # conf = (conf.setMaster('local[*]')
        # # #         .set('spark.executor.memory', '40G')
        # # #         .set('spark.driver.memory', '45G')
        # # #         .set('spark.driver.maxResultSize', '10G'))
        #conf = SparkConf().setMaster('local[*]')
        #conf.set('spark.scheduler.mode', 'FAIR')

        #sc=pyspark.SparkContext(conf=conf).getOrCreate()
        #hadoop_conf=sc._jsc.hadoopConfiguration()
        #hadoop_conf.set("fs.s3n.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
        #hadoop_conf.set("fs.s3n.awsAccessKeyId", settings.S3_CLIENT_ID)
        #hadoop_conf.set("fs.s3n.awsSecretAccessKey", settings.S3_CLIENT_SECRET)
