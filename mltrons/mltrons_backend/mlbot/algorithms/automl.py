# from pysparkling.ml import H2OAutoML
from pyspark.ml import Pipeline
from pyspark.ml.feature import SQLTransformer
import numpy as np
import h2o
import boto3
import os
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.estimators.deeplearning import H2ODeepLearningEstimator
from h2o.estimators.random_forest import H2ORandomForestEstimator
from datetime import datetime
import random
import string
import os
import pyspark
from pysparkling import *
import time
#
# class train_test():
#
#     def __init__(self):
#
#         # create context
#         os.environ['PYSPARK_PYTHON'] = '/home/ubuntu/app/env/env/bin/python'
#         os.environ['PYSPARK_DRIVER_PYTHON'] = '/home/ubuntu/app/env/env/bin/python'
#         self.os= os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages=org.apache.hadoop:hadoop-aws:2.7.3 pyspark-shell"
#         self.sc=pyspark.SparkContext.getOrCreate()
#         self.hc = H2OContext.getOrCreate(self.sc) # Start the H2OContext
#
#
#
#         self.df=None
#         self.selected_columns= None
#         self.y_variable= None
#
#
#         #initialize context
#         self.param= None
#         self.automlEstimator= None
#         self.seed=1
#         self.project_name= 'mltrons'
#         self.trained_models=[]
#         self.c=0
#
#
#
#     #methods
#     def set_parameter(self, key, value):
#         self.param[key]= value
#
#     def get_parameter(self, key=None):
#         if key==None:
#             return self.param
#         return self.param[key]
#
#
#     #methods
#     def run_automl(self, df=None, prediction_col=None, max_models=1, project_name= 'mltrons'):
#         if df==None or prediction_col==None:
#             print("df or perdiction_co is set to None.")
#             return False
#
#         # update variables
#         self.df= df
#         self.selected_columns= 'None'
#         self.y_variable= prediction_col
#
#         self.automlEstimator= H2OAutoML(maxModels=max_models, predictionCol=self.y_variable, ratio=0.99, seed=self.seed+2,projectName= project_name)
#         self.model = self.automlEstimator.fit(df)
#
#
#         return True
#
#     def get_details(self):
#         details=[]
#         mod=[]
#         models= np.array(self.automlEstimator.leaderboard().toPandas()['model_id'])
#         for m_id in models:
#             m=h2o.get_model(m_id)
#             if m_id in self.trained_models:
#                 pass
#             else:
#                 self.c +=1
#                 if 'DRF' in m_id:
#                     x=self.get_details_DRF(m)
#                     x['name']= 'Distributed Random Forest'+ '_'+str(self.c)
#                     x['model']= m
#                     details.append(x)
#                     mod.append(m_id)
#                 if 'GBM' in m_id:
#                     x=self.get_details_GBM(m)
#                     x['name']= 'Gradient Boosting Machine'+ '_'+str(self.c)
#                     x['model']= m
#                     details.append(x)
#                     mod.append(m_id)
#                 if 'GLM' in m_id:
#                     x=self.get_details_GLM(m)
#                     x['name']= 'Generalized Linear Modeling'+ '_'+str(self.c)
#                     x['model']= m
#                     details.append(x)
#                     mod.append(m_id)
#                 if 'XGBoost' in m_id:
#                     x=self.get_details_XGB(m)
#                     x['name']= 'XGBoost'+ '_'+str(self.c)
#                     x['model']= m
#                     details.append(x)
#                     mod.append(m_id)
#
#                 if 'Stacked' in m_id:
#                     x=self.get_details_ST(m)
#                     x['name']= 'Stacked Ensemble'+ '_'+str(self.c)
#                     x['model']= m
#                     details.append(x)
#                     mod.append(m_id)
#                 if 'Deep' in m_id:
#                     x=self.get_details_DL(m)
#                     x['name']= 'Deep Learning'+ '_'+str(self.c)
#                     x['model']= m
#                     details.append(x)
#                     mod.append(m_id)
#
#
#         for i in mod:
#             self.trained_models.append(i)
#         return details
#
#
#     def get_details_DRF(self, model):
#         return self.get_details_GBM(model)
#
#     def get_details_XGB(self, model):
#         return self.get_details_GBM(model)
#
#     def get_details_GLM(self, model):
#         metric={}
#         loss_iter={}
#         act_vs_pre={}
#
#
#         metric=self.calculate_metric(model.model_performance())
#         loss_iter= self.calculate_loss_vs_time(model.score_history())
#         act_vs_pre= self.calculate_act_vs_pre( model, self.df, self.y_variable)
#
#         model_details={}
#         graph={}
#         model_details['Metric']= metric
#         graph['Loss vs Iterations']= loss_iter
#         graph['Actual vs Predictions']= act_vs_pre
#         model_details['graph']= graph
#
#         return model_details
#
#
#     def get_details_DL(self, model):
#         model_details= self.get_details_ST(model)
#
#         loss_iter= self.calculate_loss_vs_time(model.score_history())
#         model_details['graph']['Loss vs Iterations']= loss_iter
#
#         return model_details
#
#
#     def get_details_ST(self, model):
#         metric={}
#         loss_iter={}
#         act_vs_pre={}
#
#
#         metric=self.calculate_metric(model.model_performance())
#         act_vs_pre= self.calculate_act_vs_pre( model, self.df, self.y_variable)
#
#         model_details={}
#         graph={}
#         model_details['Metric']= metric
#         graph['Actual vs Predictions']= act_vs_pre
#         model_details['graph']= graph
#
#         return model_details
#
#     def get_details_GBM(self, model):
#         metric={}
#         variable_importance={}
#         loss_iter={}
#         act_vs_pre={}
#
#
#         metric=self.calculate_metric(model.model_performance())
#         variable_importance= self.calculate_var_imp(model.varimp())
#         loss_iter= self.calculate_loss_vs_time(model.score_history())
#         act_vs_pre= self.calculate_act_vs_pre( model, self.df, self.y_variable)
#
#         model_details={}
#         graph={}
#         model_details['Metric']= metric
#         graph['Variable Importance']= variable_importance
#         graph['Loss vs Iterations']= loss_iter
#         graph['Actual vs Predictions']= act_vs_pre
#         model_details['graph']= graph
#
#         return model_details
#
#
#
#
#     def calculate_metric(self, metrics):
#         metric={}
#         metric['Mean Square Error']= metrics.mse()
#         metric['Root Mean Square Error']= metrics.rmse()
#         metric['Mean Absolute Error']= metrics.mae()
#         metric['Root Mean Square Algorithm Error']= metrics.rmsle()
#         metric['Mean Residual Deviance']= metrics.mean_residual_deviance()
#
#         return metric
#
#     def calculate_var_imp(self, vimp):
#         variable_importance={}
#         k=[]
#         v=[]
#         for v in vimp:
#             variable_importance[v[0]]= v[2]
#         variable_importance = {k: v for k, v in sorted(variable_importance.items(), key=lambda x: x[1])}
#         #     print(v[0])
#         #     print(v[2])
#         #     k.append(v[0])
#         #     v.append(v[2])
#         #
#         # list1 = np.array(v)
#         # list2 = np.array(k)
#         # idx   = np.argsort(list1)
#         #
#         # v = np.array(list1)[idx]
#         # k = np.array(list2)[idx]
#         #
#         # for i in range(len(k)):
#         #     variable_importance[k[i]]= float(v[i])
#
#         variable_importance['graph_type']= 'bar_chart'
#         return variable_importance
#
#     def calculate_loss_vs_time(self, scor_his):
#         loss_vs_iter={}
#         loss_vs_iter['y_training']= list(np.array(scor_his['training_rmse'])[1:])
#         loss_vs_iter['y_validation']= list(np.array(scor_his['validation_rmse'])[1:])
#         loss_vs_iter['x'] =[i for i in range(len(loss_vs_iter['y_validation']))]
#         loss_vs_iter['graph_type']= "line"
#         return loss_vs_iter
#
#     def calculate_act_vs_pre(self, model, df, y_variable):
#         done= False
#         i=250
#         while(not done):
#             try:
#                 fp= df.limit(i).toPandas()
#                 done= True
#             except:
#                 i= int(i/2)
#
#         act = np.array(fp[y_variable])
#         act= np.nan_to_num(act)
#         hf = h2o.H2OFrame(fp)
#         p=model.predict(hf)
#         pre= np.array(p.as_data_frame()['predict'])
#
#         act_vs_pre={}
#         # actual= list(act)
#         # new_actual= []
#         # for a in actual:
#         #     if a=="Nan":
#         #         new_actual.append(float(0))
#         #     else:
#         #         new_actual.append(float(a))
#         #
#         # act_vs_pre['y_actual']= new_actual
#         act_vs_pre['y_actual']= list(act)
#         act_vs_pre['y_prediction']= list(pre)
#         act_vs_pre['x']= [i for i in range(len(act_vs_pre['y_prediction']))]
#         act_vs_pre['graph_type']= "line"
#         return act_vs_pre
#
#     def predict(self, model, df, df_before=None, time=None):
#         df2 = df.toPandas()
#         hf = h2o.H2OFrame(df2)
#         p = model.predict(hf)
#         lst = list(np.array(p.as_data_frame()['predict']))
#         new_lst = []
#         for l in lst:
#             new_lst.append(float(l))
#         return new_lst
#
#     def get_x_from_frame(self, df, time_var=None):
#         if time_var == None:
#             x = []
#             for i in range(df.count()):
#                 x.append(i)
#             return x
#         else:
#             lst = list(np.array(df.select(time_var).toPandas()))
#             new_lst = []
#             for l in lst:
#                 new_lst.append(str(l))
#             return new_lst
#
#     def x_and_y_graph(self, x, y):
#         return {"x": x, "y": y}
#
#
#     def save_model(self, ID=None, key=None, model=None, bucket='mltrons', local=False):
#         if model==None:
#             print("Model not given")
#             return False
#
#         if ID==None or key == None:
#             print("ID and key not given")
#             return False
#
#         path= 'model/'+datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3].replace(" ","")
#
#         # save the model
#         try:
#             model_path = h2o.save_model(model= model, path='/tmp/'+path, force=True)
#
#             session = boto3.Session(
#                     aws_access_key_id=ID,
#                     aws_secret_access_key=key,
#                 )
#
#             s3 = session.client('s3')
#             res= s3.upload_file(model_path, bucket, path)
#             print(res)
#             os.remove(model_path)
#             return path
#         except Exception as e:
#             print(e)
#             return False
#
#     def load_model(self, ID=None, key=None,  bucket='mltrons', path=None):
#         if path==None:
#             print("Path not given")
#             return False
#
#         if ID==None or key == None:
#             print("ID and key not given")
#             return False
#
#         try:
#
#             session = boto3.Session(
#                     aws_access_key_id=ID,
#                     aws_secret_access_key=key,
#                 )
#
#             s3 = session.resource('s3')
#             local_path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
#             res= s3.Bucket(bucket).download_file(path, '/tmp/'+local_path)
#             print(res)
#             h2o.init()
#             model= h2o.load_model('/tmp/'+local_path)
#             os.remove('/tmp/'+local_path)
#             return model
#         except Exception as e:
#             print(e)
#             return False
#
#
#     def retrain(self, model=None, model_name=None, df=None, variables=None, y_variable=None):
#
#
#         from h2o.estimators.gbm import H2OGradientBoostingEstimator
#         from h2o.estimators.deeplearning import H2ODeepLearningEstimator
#         from h2o.estimators.random_forest import H2ORandomForestEstimator
#
#
#         if model_name==None:
#             print("Please provide model_name.")
#             return False
#
#         predictors=[]
#         for v in variables:
#             predictors.append(v[0])
#
#
#         if model_name== 'Gradient Boosting Machine':
#
#
#             # build and train model with 5 additional trees:
#             model_continued = H2OGradientBoostingEstimator(checkpoint= model.model_id, ntrees = model.ntrees+5)
#
#             df2= df.toPandas()
#             train = h2o.H2OFrame(df2)
#             model_continued.train(x = predictors, y = y_variable, training_frame = train, validation_frame = valid)
#
#             return model_continued
#
#         elif model_name== 'Distributed Random Forest':
#
#
#             # build and train model with 5 additional trees:
#             model_continued = H2ORandomForestEstimator(checkpoint= model.model_id, ntrees = model.ntrees+5)
#
#             df2= df.toPandas()
#             train = h2o.H2OFrame(df2)
#             model_continued.train(x = predictors, y = y_variable, training_frame = train, validation_frame = valid)
#
#             return model_continued
#
#         elif model_name== 'Deep Learning':
#
#
#             # build and train model with 5 additional trees:
#             model_continued = H2ODeepLearningEstimator(checkpoint= model.model_id, epochs = model.epochs+15)
#
#             df2= df.toPandas()
#             train = h2o.H2OFrame(df2)
#             model_continued.train(x = predictors, y = y_variable, training_frame = train, validation_frame = valid)
#
#
#             return model_continued
#
#         else:
#             print("Retraing not possible. Please run automl again.")
#             return False

from pyspark.ml import Pipeline
from pyspark.ml.feature import SQLTransformer
import numpy as np
import h2o
import boto3
import os
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.estimators.deeplearning import H2ODeepLearningEstimator
from h2o.estimators.random_forest import H2ORandomForestEstimator
from random import randint
from h2o.automl import H2OAutoML
import string
import pyspark
from pyspark.sql import SparkSession

class train_test():

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
        self.sql=pyspark.sql.SparkSession(self.sc)


        self.selected_columns= None
        self.y_variable= None
        h2o.init(max_mem_size = "6g")


        #initialize context
        self.param= None
        self.automlEstimator= None
        self.project_name= 'mltrons'
        self.trained_models=[]
        self.seed=randint(1, 99)
        self.c=1

        self.automl= None
        self.h2otrain=None
        self.h2otest=None



    #methods
    def set_parameter(self, key, value):
        self.param[key]= value

    def get_parameter(self, key=None):
        if key==None:
            return self.param
        return self.param[key]


    #methods
    def run_automl(self, df=None, prediction_col=None, max_models=5, project_name= 'mltrons',problem_type=None):
        if df==None or prediction_col==None:
            print("df or perdiction_co is set to None.")
            return False

        # update variables
        if self.h2otrain==None:
            # convert spark frame into h2o frame
            df2= df.toPandas()
            hf = h2o.H2OFrame(df2)

            # split the frame and run and make variables
            splits = hf.split_frame(ratios = [0.95], seed = self.seed)
            self.h2otrain = splits[0]
            self.h2otest = splits[1]

            ## conver the column here based on the type
            if problem_type=='Classification':
                #change the type of y column in both test and train dataset
                self.h2otrain[prediction_col]= self.h2otrain[prediction_col].asfactor()
                self.h2otest[prediction_col]= self.h2otest[prediction_col].asfactor()

        self.y_variable= prediction_col

        self.seed= randint(1, 99)
        print(self.seed)

        self.automlEstimator= H2OAutoML(max_models=max_models, seed = self.seed, project_name = project_name)
        self.automlEstimator.train(y = self.y_variable, training_frame = self.h2otrain,  validation_frame= self.h2otrain, leaderboard_frame = self.h2otrain)


        return True

    def get_details(self):
        details=[]
        mod=[]
        models= np.array(self.automlEstimator.leaderboard.as_data_frame()['model_id'])
        for m_id in models:
            m=h2o.get_model(m_id)
            if m_id in self.trained_models:
                pass
            else:
                self.c +=1
                if 'DRF' in m_id:
                    x=self.get_details_DRF(m)
                    x['name']= 'Distributed Random Forest'+ '_'+str(self.c)
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)
                if 'GBM' in m_id:
                    x=self.get_details_GBM(m)
                    x['name']= 'Gradient Boosting Machine'+ '_'+str(self.c)
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)
                if 'GLM' in m_id:
                    x=self.get_details_GLM(m)
                    x['name']= 'Generalized Linear Modeling'+ '_'+str(self.c)
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)
                if 'XGBoost' in m_id:
                    x=self.get_details_XGB(m)
                    x['name']= 'XGBoost'+ '_'+str(self.c)
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)

                if 'Stacked' in m_id:
                    x=self.get_details_ST(m)
                    x['name']= 'Stacked Ensemble'+ '_'+str(self.c)
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)
                if 'Deep' in m_id:
                    x=self.get_details_DL(m)
                    x['name']= 'Deep Learning'+ '_'+str(self.c)
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)


        for i in mod:
            self.trained_models.append(i)
        return details

    def get_details_classification(self):
        details=[]
        mod=[]
        models= np.array(self.automlEstimator.leaderboard.as_data_frame()['model_id'])
        for m_id in models:
            m=h2o.get_model(m_id)
            if m_id in self.trained_models:
                pass
            else:
                self.c +=1
                if 'GLM' in m_id:
                    print("model id is: "+ str(m_id))
                    x=self.get_details_GLM_classification(m)
                    x['name']= m_id
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)
                elif 'Stacked' in m_id:
                    print("model id is: "+ str(m_id))
                    x=self.get_details_ST_classification(m)
                    x['name']= m_id
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)
                else:
                    print("model id is: "+ str(m_id))
                    x=self.get_details_other_classification(m)
                    x['name']= m_id
                    x['model']= m
                    details.append(x)
                    mod.append(m_id)


        for i in mod:
            self.trained_models.append(i)
        return details


    # details for classification

    def get_details_GLM_classification(self, model):
        metric={}
        deviance_iter={}
        lift_gain={}
        confusion_matrix={}


        try:
            metric=self.calculate_metrics_classification(model)
        except:
            metric= None
        deviance_iter= self.calculate_deviance_iteration_classification(model)
        lift_gain= self.calculate_lift_gain(model)
        confusion_matrix= self.calculate_confusion_matrix( model)



        model_details={}
        graph={}
        model_details['Metric']= metric
        graph['Deviance vs Iter']= deviance_iter
        graph['lift_gain']= lift_gain
        graph['confusion_matrix']= confusion_matrix
        model_details['graph']= graph

        return model_details

    def get_details_other_classification(self, model):
        metric={}
        loss_trees={}
        lift_gain={}
        confusion_matrix={}
        variable_importance={}

        try:
            metric=self.calculate_metrics_classification(model)
        except:
            metric= None
        loss_trees= self.calculate_vali_loss_classification(model)
        lift_gain= self.calculate_lift_gain( model)
        confusion_matrix= self.calculate_confusion_matrix( model)
        variable_importance= self.calculate_variable_importance_class( model)



        model_details={}
        graph={}
        model_details['Metric']= metric
        graph['Loss vs trees']= loss_trees
        graph['lift_gain']= lift_gain
        graph['confusion_matrix']= confusion_matrix
        graph['variable_importance']= variable_importance
        model_details['graph']= graph

        return model_details


    def get_details_ST_classification(self, model):
        metric={}
        lift_gain={}
        confusion_matrix={}

        try:
            metric=self.calculate_metrics_classification(model)
        except:
            metric= None
        lift_gain= self.calculate_lift_gain( model)
        confusion_matrix= self.calculate_confusion_matrix( model)



        model_details={}
        graph={}
        model_details['Metric']= metric
        graph['lift_gain']= lift_gain
        graph['confusion_matrix']= confusion_matrix
        model_details['graph']= graph

        return model_details


    def calculate_confusion_matrix(self, model):
        c= model.confusion_matrix()
        d= c.table.as_data_frame()
        dic= d.to_dict()
        return dic

    def calculate_lift_gain(self, model):
        result= {}
        lg= model.gains_lift().as_data_frame()
        result['group']= list(lg['group'])
        result['cumulative_lift']= list(lg['cumulative_lift'])
        result['cumulative_gain']= list(lg['cumulative_gain'])
        return result


    def calculate_vali_loss_classification(self, model):
        result= {}
        result['Training Log Loss']= list(model.scoring_history()['training_logloss'])
        result['Validation Log Loss']= list(model.scoring_history()['validation_logloss'])
        result['Number of Trees']= list(model.scoring_history()['number_of_trees'])
        return result

    def calculate_deviance_iteration_classification(self, model):
        result= {}
        result['Deviance Train']= list(m.scoring_history()['deviance_train'])
        result['Deviance Test']= list(m.scoring_history()['deviance_test'])
        result['Iteration']= list(m.scoring_history()['iteration'])
        return result

    def calculate_variable_importance_class(self,model):
        result= {}
        variable_names= []
        importance=[]
        for every in model.varimp():
            variable_names.append(every[0])
            importance.append(every[1])

        result["variables"]= variable_names
        result["importance"]= importance
        return result

    def calculate_metrics_classification(self, model):
        result= {}
        metric=[]
        value= []
        cv_array=np.array(cv)
        for i in cv_array:
            metric.append(i[0])
            value.append(float(i[1]))
        result['name']= metric
        result['value']= value
        return result







    # model details for regression and time series

    def get_details_DRF(self, model):
        return self.get_details_GBM(model)


    def get_details_XGB(self, model):
        return self.get_details_GBM(model)

    def get_details_GLM(self, model):
        metric={}
        loss_iter={}
        act_vs_pre={}


        metric=self.calculate_metric(model.model_performance())
        loss_iter= self.calculate_loss_vs_time_glm(model.score_history())
        act_vs_pre= self.calculate_act_vs_pre( model, self.h2otest, self.y_variable)

        model_details={}
        graph={}
        model_details['Metric']= metric
        graph['Loss vs Iterations']= loss_iter
        graph['Actual vs Predictions']= act_vs_pre
        model_details['graph']= graph

        return model_details


    def get_details_DL(self, model):
        model_details= self.get_details_ST(model)

        loss_iter= self.calculate_loss_vs_time(model.score_history())
        model_details['graph']['Loss vs Iterations']= loss_iter

        return model_details


    def get_details_ST(self, model):
        metric={}
        loss_iter={}
        act_vs_pre={}


        metric=self.calculate_metric(model.model_performance())
        act_vs_pre= self.calculate_act_vs_pre( model, self.h2otest, self.y_variable)

        model_details={}
        graph={}
        model_details['Metric']= metric
        graph['Actual vs Predictions']= act_vs_pre
        model_details['graph']= graph

        return model_details

    def get_details_GBM(self, model):
        metric={}
        variable_importance={}
        loss_iter={}
        act_vs_pre={}


        metric=self.calculate_metric(model.model_performance())
        variable_importance= self.calculate_var_imp(model.varimp())
        loss_iter= self.calculate_loss_vs_time(model.score_history())
        act_vs_pre= self.calculate_act_vs_pre( model, self.h2otest, self.y_variable)

        model_details={}
        graph={}
        model_details['Metric']= metric
        graph['Variable Importance']= variable_importance
        graph['Loss vs Iterations']= loss_iter
        graph['Actual vs Predictions']= act_vs_pre
        model_details['graph']= graph

        return model_details




    def calculate_metric(self, metrics):
        metric={}
        metric['Mean Square Error']= metrics.mse()
        metric['Root Mean Square Error']= metrics.rmse()
        metric['Mean Absolute Error']= metrics.mae()
        metric['Root Mean Square Algorithm Error']= metrics.rmsle()
        metric['Mean Residual Deviance']= metrics.mean_residual_deviance()

        return metric

    def calculate_var_imp(self, vimp):
        variable_importance={}
        k=[]
        v=[]
        for v in vimp:
            variable_importance[v[0]]= v[2]
        variable_importance = {k: v for k, v in sorted(variable_importance.items(), key=lambda x: x[1])}
        #     print(v[0])
        #     print(v[2])
        #     k.append(v[0])
        #     v.append(v[2])
        #
        # list1 = np.array(v)
        # list2 = np.array(k)
        # idx   = np.argsort(list1)
        #
        # v = np.array(list1)[idx]
        # k = np.array(list2)[idx]
        #
        # for i in range(len(k)):
        #     variable_importance[k[i]]= float(v[i])

        variable_importance['graph_type']= 'bar_chart'
        return variable_importance

    def calculate_loss_vs_time(self, scor_his):
        loss_vs_iter={}
        loss_vs_iter['y_training']= list(np.array(scor_his['training_rmse'])[1:])
        loss_vs_iter['y_validation']= list(np.array(scor_his['validation_rmse'])[1:])
        loss_vs_iter['x'] =[i for i in range(len(loss_vs_iter['y_validation']))]
        loss_vs_iter['graph_type']= "line"
        return loss_vs_iter

    def calculate_loss_vs_time_glm(self, scor_his):
        loss_vs_iter={}
        loss_vs_iter['y_training']= list(np.array(scor_his['deviance_train'])[1:])
        loss_vs_iter['y_validation']= list(np.array(scor_his['deviance_train'])[1:])
        loss_vs_iter['x'] =[i for i in range(len(loss_vs_iter['y_validation']))]
        loss_vs_iter['graph_type']= "line"
        return loss_vs_iter

    def calculate_act_vs_pre(self, model, df, y_variable):


        act = np.array(df[y_variable].as_data_frame())[:,0]
        act= np.nan_to_num(act)
        hf = df
        p=model.predict(hf)
        pre= np.array(p['predict'].as_data_frame())[:,0]


        act_vs_pre={}
        actual= list(act)
        new_actual= []
        for a in actual:
            if a=="Nan":
                new_actual.append(float(0))
            else:
                new_actual.append(float(a))
        new_pre=[]
        for p in pre:
            new_pre.append(float(p))

        act_vs_pre['y_actual']= new_actual
        act_vs_pre['y_prediction']= new_pre
        act_vs_pre['x']= [i for i in range(len(act_vs_pre['y_prediction']))]
        act_vs_pre['graph_type']= "line"
        return act_vs_pre


    def predict(self, model, df, df_before=None, time=None):
        df2 = df.toPandas()
        hf = h2o.H2OFrame(df2)
        p = model.predict(hf)
        p_data_frame = p.as_data_frame()
        hf['prediction'] = p

        lst = list(np.array(p_data_frame['predict']))
        new_lst = []
        for l in lst:
            new_lst.append(float(l))
        return new_lst, hf.as_data_frame()


    def get_x_from_frame(self, df, time_var=None):
        if time_var == None:
            x = []
            for i in range(df.count()):
                x.append(i)
            return x
        else:
            lst = list(np.array(df.select(time_var).toPandas()))
            new_lst = []
            for l in lst:
                new_lst.append(str(l))
            return new_lst

    def x_and_y_graph(self, x, y):
        return {"x": x, "y": y}


    def save_model(self, ID=None, key=None, model=None, bucket='mltrons', local=False):
        if model==None:
            print("Model not given")
            return False

        if ID==None or key == None:
            print("ID and key not given")
            return False

        path= 'model/'+datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3].replace(" ","")

        # save the model
        try:
            model_path = h2o.save_model(model= model, path='/tmp/'+path, force=True)

            session = boto3.Session(
                    aws_access_key_id=ID,
                    aws_secret_access_key=key,
                )

            s3 = session.client('s3')
            res= s3.upload_file(model_path, bucket, path)
            print(res)
            os.remove(model_path)
            return path
        except Exception as e:
            print(e)
            return False

    def load_model(self, ID=None, key=None,  bucket='mltrons', path=None):
        if path==None:
            print("Path not given")
            return False

        if ID==None or key == None:
            print("ID and key not given")
            return False

        try:

            session = boto3.Session(
                    aws_access_key_id=ID,
                    aws_secret_access_key=key,
                )

            s3 = session.resource('s3')
            local_path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            res= s3.Bucket(bucket).download_file(path, '/tmp/'+local_path)
            print(res)
            h2o.init()
            model= h2o.load_model('/tmp/'+local_path)
            os.remove('/tmp/'+local_path)
            return model
        except Exception as e:
            print(e)
            return False


    def retrain(self, model=None, model_name=None, df=None, variables=None, y_variable=None):


        from h2o.estimators.gbm import H2OGradientBoostingEstimator
        from h2o.estimators.deeplearning import H2ODeepLearningEstimator
        from h2o.estimators.random_forest import H2ORandomForestEstimator


        if model_name==None:
            print("Please provide model_name.")
            return False

        predictors=[]
        for v in variables:
            predictors.append(v[0])


        if model_name== 'Gradient Boosting Machine':


            # build and train model with 5 additional trees:
            model_continued = H2OGradientBoostingEstimator(checkpoint= model.model_id, ntrees = model.ntrees+5)

            df2= df.toPandas()
            train = h2o.H2OFrame(df2)
            model_continued.train(x = predictors, y = y_variable, training_frame = train, validation_frame = valid)

            return model_continued

        elif model_name== 'Distributed Random Forest':


            # build and train model with 5 additional trees:
            model_continued = H2ORandomForestEstimator(checkpoint= model.model_id, ntrees = model.ntrees+5)

            df2= df.toPandas()
            train = h2o.H2OFrame(df2)
            model_continued.train(x = predictors, y = y_variable, training_frame = train, validation_frame = valid)

            return model_continued

        elif model_name== 'Deep Learning':


            # build and train model with 5 additional trees:
            model_continued = H2ODeepLearningEstimator(checkpoint= model.model_id, epochs = model.epochs+15)

            df2= df.toPandas()
            train = h2o.H2OFrame(df2)
            model_continued.train(x = predictors, y = y_variable, training_frame = train, validation_frame = valid)


            return model_continued

        else:
            print("Retraing not possible. Please run automl again.")
            return False
