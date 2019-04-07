import os
import subprocess
from mlbot_webservices.settings import BASE_DIR
from mlbot_webservices.celery import app
from celery import current_task
from time import sleep
from mlbot.algorithms.data_summary import *
from mlbot.algorithms.save_read import *
from mlbot.algorithms.save_read import *
from mlbot.algorithms.merge import *
from mlbot.algorithms.transform import *
from mlbot.algorithms.automl import *
from mlbot.algorithms.graph import *
import traceback
from django.conf import settings
from project.models import Project, MetaType, Meta, DataSet, MergeColumn, TrainingDetail, Metric, TrainingModel, ModelMetric,\
    FeatureImportance, LossVsInteraction, ActualVsPrediction, TestingData, DeployedModel, Graph
import pusher
from django.db import transaction
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.ml.feature import Imputer
import time as tme
import uuid

pusher_client = pusher.Pusher(
  app_id='698737',
  key=settings.PUSHER_ID,
  secret=settings.PUSHER_SECRET,
  cluster='ap2',
  ssl=True
)

def send_notification(retry, id, event, message):
    if retry == 10:
        return
    try:
        pusher_client.trigger(str(id), event, {'message': message})
    except Exception as e:
        tme.sleep(0.5)
        send_notification(retry+1, id, event, message)

@app.task
def read_and_process_csv(dataset_id, dataset_path, user_id, count):
    try:
        reader = save_read(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        summary = data_summary(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        graph = generate_graph(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        print("initialization done")

        event = {'output': 'Start reading csv data', 'step': 1, 'event': 'read_csv'}
        # current_task.update_state(state='PROGRESS', meta=event)
        send_notification(0, user_id, 'read_csv', event)

        frame = reader.read_as_df_local(dataset_path, count)
        summary.set_dataframe(frame)
        print("read as df local done")

        event = {'output': 'Doing calculations on csv data', 'step': 2, 'event': 'read_csv'}
        current_task.update_state(state='PROGRESS', meta=event)
        send_notification(0, user_id, 'read_csv', event)

        summary.calculate()
        b = summary.get_parameter()
        print("summary done")

        # try:
        #     correlation = graph.correlation(frame)
        # except Exception as e:
        #     print(e)
        correlation={'spearman':{}, 'pearson': {}}

        try:
            histogram = graph.histogram_from_df(frame)
        except Exception as e:
            print(e)
            histogram={}
        # correlation = graph.correlation(frame)

        event={'output': 'Processing csv meta', 'step': 3, 'event': 'read_csv'}
        current_task.update_state(state='PROGRESS', meta=event)
        send_notification(0, user_id, 'read_csv', event)

        c_types = b['column_types']

        with transaction.atomic():
            d_set = DataSet.objects.get(id=dataset_id)
            d_set.rows=frame.count()
            d_set.columns=len(c_types)
            d_set.grid_map = correlation
            d_set.save()

            for column in c_types:
                type = column[1]
                meta_type, created = MetaType.objects.get_or_create(name=type)
                obj = Meta.objects.create(data_id=dataset_id, column_name=column[0], type=meta_type)
                summary = b['summary'][column[0]]
                missing = b['num_missing_values'][column[0]][0]
                try:
                    obj.distribution_data = histogram[column[0]]
                except:
                    pass
                obj.min = summary[3]
                obj.max = summary[4]
                obj.count = summary[0]
                obj.mean = summary[1]
                obj.stdev = summary[2]
                obj.missing = missing
                obj.save()

        event = {'output': 'Uploading frame as parquet to S3', 'step': 3, 'event': 'read_csv'}
        current_task.update_state(state='PROGRESS',meta=event)
        send_notification(0, user_id, 'read_csv', event)
        path = reader.save_df_on_s3(frame)
        if path:
            dataset = DataSet.objects.get(id=dataset_id)
            dataset.frame_path = path
            dataset.suffix = count
            dataset.save()
            event = {'step': 4, 'output': 'Process completed', 'event': 'read_csv'}
            send_notification(0, user_id, 'read_csv', event)
            os.remove(dataset_path)
            # # # # reader.sql.stop()
            return event
        else:
            DataSet.objects.get(id=dataset_id).delete()
            event = {'step': 5, 'output': 'Process  failed', 'event': 'read_csv'}
            send_notification(0, user_id, 'read_csv', event)
            os.remove(dataset_path)
            # # # # reader.sql.stop()

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        DataSet.objects.get(id=dataset_id).delete()
        event = {'step': 5, 'output': 'Process  failed', 'event': 'read_csv'}
        send_notification(0, user_id, 'read_csv', event)
        # try:
        #     # # # # reader.sql.stop()
        # except:
        #     pass
        return event


@app.task
def read_and_process_training_csv(testing_id, dataset_path, user_id, count):
    try:
        reader = save_read(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        event = {'output': 'Start reading training data', 'step': 1, 'event': 'test_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'test_csv', event)

        frame = reader.read_as_df_local(dataset_path, count)

        event = {'output': 'Uploading frame as parquet to S3', 'step': 2, 'event': 'test_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'test_csv', event)
        path = reader.save_df_on_s3(frame)

        if path:
            data = TestingData.objects.get(id=testing_id)
            data.frame_path = path
            data.save()

        event = {'step': 4, 'output': 'Process completed', 'event': 'test_csv'}
        send_notification(0, user_id, 'test_csv', event)
        # # # reader.sql.stop()
        return event

    except Exception as e:
        TestingData.objects.get(id=testing_id).delete()
        event = {'step': 5, 'output': 'Process  failed', 'event': 'test_csv'}
        send_notification(0, user_id, 'test_csv', event)
        # try:
        #     # # # reader.sql.stop()
        # except:
        #     pass
        return event



def check_columns(con, trans_columns, i):
    for j in range(len(con['connections'])):
        if con['connections'][j][i] in trans_columns.keys():
            con['connections'][j][i]= trans_columns[con['connections'][j][i]]
    return con


def check_df_col(con, trans_df, trans_columns):
    if con['from']['id'] in trans_df.keys():
        con['from']= trans_df[con['from']['id']]
        con= check_columns(con, trans_columns, 0)

    if con['to']['id'] in trans_df.keys():
        con['to']= trans_df[con['to']['id']]
        con= check_columns(con, trans_columns, 1)
    return con


def check_concat(connection_list, k, k3):
    if connection_list[k]['from']['id'] == connection_list[k3]['from']['id'] and connection_list[k]['to']['id'] == connection_list[k3]['to']['id']:
        connection_list[k]['connections'].concat(connection_list[k3]['connections'])
        connection_list[k]['used']= True

    if connection_list[k]['from']['id'] == connection_list[k3]['to']['id'] and connection_list[k]['to']['id'] == connection_list[k3]['from']['id']:
        for p in connection_list[k3]['connections']:
            connection_list[k]['connections'].append([p[1], p[0]])
            connection_list[k]['used']= True
    return connection_list


def merge_frames(connections_list):
    merger = merge(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
    trans_df = {}
    trans_columns = {}
    merged = None

    for k in range(len(connections_list)):
        if connections_list[k]['used'] == True:
            continue
        for k2 in range(k, len(connections_list)):
            if connections_list[k2]['used'] == True:
                continue
            connections_list[k2] = check_df_col(connections_list[k2], trans_df, trans_columns)
        for k3 in range(k + 1, len(connections_list)):
            if connections_list[k3]['used'] == True:
                continue
            connections_list = check_concat(connections_list, k, k3)

        #     merge coonnection list at k
        df, pairs = merger.merge(connections_list[k]['from']['frame'], connections_list[k]['to']['frame'],
                                 connections_list[k]['connections'])
        if df == False:
            return False
        else:
            trans_df[connections_list[k]['from']['id']] = {
                'id': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3].replace(" ", ""),
                'frame': df
            }
            trans_df[connections_list[k]['to']['id']] = {
                'id': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3].replace(" ", ""),
                'frame': df
            }
            for p in pairs:
                trans_columns[p[0]] = p[1]
            merged = df
    return merged

@app.task
def merge_and_process_csv(project_id, user_id):
    try:
        merger = merge(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        reader = save_read(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        graph = generate_graph(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        connections = MergeColumn.objects.filter(project_id=project_id)
        connections_list = []
        testing_list = []

        event = {'output': 'Loading dataframes', 'step': 1, 'event': 'merge_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'merge_csv', event)

        distinct_dataframes = set()

        for connection in connections:
            frm = connection.from_column.data
            to = connection.to_column.data
            frm_frame = reader.read_as_df(settings.S3_BUCKET, frm.frame_path)
            to_frame = reader.read_as_df(settings.S3_BUCKET, to.frame_path)


            distinct_dataframes.add(frm.id)
            distinct_dataframes.add(to.id)

            connections_list.append({
                'index': len(connections_list) + 1,
                'from': {'id': frm.id, 'frame': frm_frame},
                'to': {'id': to.id, 'frame': to_frame},
                'connections': [[connection.from_column.column_name, connection.to_column.column_name]],
                'used': False
            })
            testing_list.append({
                'from': frm.id,
                'to': to.id,
                'connections': [[connection.from_column.column_name, connection.to_column.column_name]],
            })
        merged = None
        event = {'output': 'Merging dataframes', 'step': 2, 'event': 'merge_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'merge_csv', event)
        merged = merge_frames(connections_list)
        if not merged:
            MergeColumn.objects.filter(project_id=project_id).delete()
            event = {'step': 5, 'output': 'Process  failed', 'event': 'merge_csv'}
            send_notification(0, user_id, 'merge_csv', event)
            return event

        event = {'output': 'Frame analysis', 'step': 3, 'event': 'merge_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'merge_csv', event)

        print('merged', merged)

        # try:
        #     correlation = graph.correlation(merged)
        # except Exception as e:
        #     print(e)
        correlation={'spearman':{}, 'pearson': {}}

        try:
            histogram = graph.histogram_from_df(merged)
        except Exception as e:
            print(e)
            histogram={}


        d_set = DataSet.objects.create(
            project_id=project_id,
            name='merged_' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3].replace(" ", ""),
            status=DataSet.Processed,
            parent={'dataset': list(distinct_dataframes)},
            connections={'connections': testing_list},
            grid_map = correlation
        )
        summary = data_summary(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        summary.set_dataframe(merged)
        summary.calculate()
        b = summary.get_parameter()
        c_types = b['column_types']

        with transaction.atomic():
            for column in c_types:
                type = column[1]
                meta_type, created = MetaType.objects.get_or_create(name=type)
                obj = Meta.objects.create(data=d_set, column_name=column[0], type=meta_type)
                summary = b['summary'][column[0]]
                missing = b['num_missing_values'][column[0]][0]
                try:
                    obj.distribution_data = histogram[column[0]]
                except Exception as e:
                    pass
                obj.min = summary[3]
                obj.max = summary[4]
                obj.count = summary[0]
                obj.mean = summary[1]
                obj.stdev = summary[2]
                obj.missing = missing
                obj.save()

            event = {'output': 'Saving dataframe', 'step': 3, 'event': 'merge_csv'}
            current_task.update_state(state='PROGRESS',
                                      meta=event)
            send_notification(0, user_id, 'merge_csv', event)

            path = reader.save_df_on_s3(merged)
            d_set.frame_path = path
            d_set.rows = merged.count()
            d_set.columns = len(c_types)
            d_set.save()

            event = {'step': 4, 'output': 'Process completed', 'event': 'merge_csv'}
            send_notification(0, user_id, 'merge_csv', event)
            # # # reader.sql.stop()
            return event
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        MergeColumn.objects.filter(project_id=project_id).delete()
        event = {'step': 5, 'output': 'Process  failed', 'event': 'merge_csv'}
        send_notification(0, user_id, 'merge_csv', event)
        # try:
        #     # # # reader.sql.stop()
        # except:
        #     pass
        return event

@app.task
def start_training(training_id, user_id):
    try:
        training = TrainingDetail.objects.get(id=training_id)
        reader = save_read(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)

        event = {'output': 'Loading data', 'step': 0, 'event': 'train_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'train_csv', event)

        input_frame = reader.read_as_df(settings.S3_BUCKET, training.processed_file.frame_path)
        input_frame= input_frame.drop('id')
        input_frame = input_frame.repartition(300)

        event = {'output': 'Transforming data', 'step': 1, 'event': 'train_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'train_csv', event)

        t = transform_pipeline(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)

        input_frame = input_frame.select(training.selected_columns['columns'])

        variables = input_frame.dtypes
        y_var = training.y_yariable.column_name
        # time= ['Date_1', 'dd/MM/yyyy']
        time = []
        if training.time_yariable:
            time = [training.time_yariable.column_name, training.time_type.format]

        variables = t.remove_y_from_variables(variables, y_var, True)

        t.set_parameter('columns', variables)
        t.set_parameter('y_varaible', y_var)
        t.set_parameter('time_variable', time)
        t.set_parameter('variables_updated', True)

        metas = training.processed_file.metas.all()
        correct_types = {}
        for meta in metas:
            correct_types[meta.column_name] = meta.type.name
        t.set_parameter('correct_var_types', correct_types)
        print("Done")
        ans = t.build_pipeline(input_frame)
        print(ans)
        if ans == False:
            training.project.status = Project.Pending
            training.project.save()
            training.delete()
            event = {'step': 6, 'output': 'Transformation  failed', 'event': 'train_csv'}
            send_notification(0, user_id, 'train_csv', event)
            return event
        transformed_frame = t.transform(input_frame)
        ## based on the type of probelm
        if training.problem_type.name== 'Classification':
            pass
        else:
            transformed_frame = t.convert_y_to_float(transformed_frame, y_var)
        print("transformation done")
        path = t.save_pipeline(bucket=settings.S3_BUCKET)
        training.pipeline_path = path
        training.save()
        print("Pipeline saved")

        event = {'output': 'Training data', 'step': 2, 'completed': 0, 'ETR': 'N/A', 'event': 'train_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'train_csv', event)

        t = train_test(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)

        project_name = str(uuid.uuid4())

        start = tme.time()
        max_model = settings.TRAINING_MODELS
        try:
            transformed_frame = transformed_frame.na.drop(subset=[training.y_yariable.column_name])
        except:
            print('na removed failed')
        print("nan removed")
        for i in range(max_model):
            interupt = TrainingDetail.objects.get(id=training_id).interupt
            if interupt:
                event = {'step': 5, 'output': 'Training completed', 'event': 'train_csv'}
                current_task.update_state(state='PROGRESS',
                                          meta=event)
                send_notification(0, user_id, 'train_csv', event)
                training.project.status = Project.Completed
                training.project.save()
                return event
            ans = t.run_automl(transformed_frame, prediction_col=training.y_yariable.column_name, project_name=project_name,problem_type=training.problem_type.name)
            end = tme.time()
            time_lapsed = end - start
            ### ETR
            ETR_s = time_lapsed / (i + 1) * (max_model - i + 1)

            ETR = tme.strftime('%H:%M:%S', tme.gmtime(ETR_s))
            time_lap = tme.strftime('%H:%M:%S', tme.gmtime(time_lapsed))
            print('ETR', ETR)
            if ans == True:
                details = t.get_details()
                with transaction.atomic():
                    for detail in details:
                        model = detail['model']
                        model_name = detail['name']
                        path = t.save_model(ID=settings.S3_CLIENT_ID, key=settings.S3_CLIENT_SECRET, model=model, bucket=settings.S3_BUCKET)
                        training_model = TrainingModel.objects.create(training=training, name=model_name, path=path)

                        metric = detail['Metric']
                        for key in metric.keys():
                            m, created = Metric.objects.get_or_create(name = key)
                            ModelMetric.objects.create(metric=m, model=training_model, value=metric[key])

                        graphs = detail['graph']

                        for key in graphs.keys():
                            if key == 'Loss vs Iterations':
                                LossVsInteraction.objects.create(project=training.project, training_model=training_model, data=graphs[key])
                            if key == 'Actual vs Predictions':
                                ActualVsPrediction.objects.create(project=training.project, training_model=training_model,
                                                                 data=graphs[key])
                                pass
                            if key == 'Variable Importance':
                                FeatureImportance.objects.create(project=training.project, training_model=training_model,
                                                                 data=graphs[key])

                ### save in the database

            ### percent remaining
            percentage_completed = (i + 1) / max_model * 100
            print('% Completed', percentage_completed)

            event = {'output': 'Training in progress', 'step': 3, 'completed': percentage_completed, 'ETR': ETR, 'time_lap':time_lap, 'event': 'train_csv'}
            current_task.update_state(state='PROGRESS',
                                      meta=event)
            send_notification(0, user_id, 'train_csv', event)

        training.project.status = Project.Completed
        training.project.save()

        event = {'step': 5, 'output': 'Training completed', 'event': 'train_csv'}
        send_notification(0, user_id, 'train_csv', event)
        # # # reader.sql.stop()
        return event
    except Exception as e:
        print(e)
        training = TrainingDetail.objects.get(id=training_id)
        training.project.status = Project.Pending
        training.project.save()
        training.delete()
        event = {'step': 6, 'output': 'Training  failed', 'event': 'train_csv'}
        send_notification(0, user_id, 'train_csv', event)
        # try:
        #     # # # reader.sql.stop()
        # except:
        #     pass
        return event

@app.task
def start_testing(model_id, user_id):
    try:
        deployed_model = DeployedModel.objects.get(id=model_id)
        frame = None
        reader = save_read(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        t = transform_pipeline(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        automl = train_test(settings.S3_CLIENT_ID, settings.S3_CLIENT_SECRET)
        data = deployed_model.model.training.processed_file

        event = {'output': 'Reading data', 'step': 0, 'event': 'generate_graph_csv'}
        current_task.update_state(state='PROGRESS',
                                  meta=event)
        send_notification(0, user_id, 'generate_graph_csv', event)

        if data.parent == None:
            testing = TestingData.objects.filter(data=data, status=TestingData.Pending)
            if testing.count() > 0:
                frame = reader.read_as_df(settings.S3_BUCKET, testing[0].frame_path)
        else:
            # merge testing frames here
            connections = data.connections['connections']
            connections_list = []
            for connection in connections:
                frm = TestingData.objects.filter(data_id=connection['from'], status=TestingData.Pending)[0]
                to = TestingData.objects.filter(data_id=connection['to'], status=TestingData.Pending)[0]
                frm_frame = reader.read_as_df(settings.S3_BUCKET, frm.frame_path)
                to_frame = reader.read_as_df(settings.S3_BUCKET, to.frame_path)

                connections_list.append({
                    'index': len(connections_list) + 1,
                    'from': {'id': frm.id, 'frame': frm_frame},
                    'to': {'id': to.id, 'frame': to_frame},
                    'connections': [[connection.from_column.column_name, connection.to_column.column_name]],
                    'used': False
                })
            # merge code and return frame
            frame = merge_frames(connections_list)
        if frame:
            event = {'output': 'Transforming data', 'step': 1, 'event': 'generate_graph_csv'}
            current_task.update_state(state='PROGRESS',
                                      meta=event)
            send_notification(0, user_id, 'generate_graph_csv', event)
            # transform here
            pipeline = t.load_pipeline(frame, settings.S3_BUCKET, deployed_model.model.training.pipeline_path)
            transformed_frame = pipeline.transform(frame)
            x_var = None
            if deployed_model.model.training.time_yariable:
                x_var = deployed_model.model.training.time_yariable.column_name
            event = {'output': 'Predicting data', 'step': 2, 'event': 'generate_graph_csv'}
            current_task.update_state(state='PROGRESS',
                                      meta=event)
            send_notification(0, user_id, 'generate_graph_csv', event)

            model = automl.load_model(ID=settings.S3_CLIENT_ID, key=settings.S3_CLIENT_SECRET,
                                      path=deployed_model.model.path)
            y, df_pandas = automl.predict(model=model, df=transformed_frame)


            from django.core.files.base import ContentFile
            csv = df_pandas.to_csv(index=False, header=True)
            temp_file = ContentFile(csv, name='data.csv')

            x = automl.get_x_from_frame(df=frame, time_var=x_var)

            graph = automl.x_and_y_graph(x, y)

            event = {'output': 'Displaying data data', 'step': 3, 'event': 'generate_graph_csv'}
            current_task.update_state(state='PROGRESS',
                                      meta=event)
            send_notification(0, user_id, 'generate_graph_csv', event)

            Graph.objects.create(project=deployed_model.project, data=graph, csv_url= temp_file)

            print(graph)
        else:
            event = {'step': 5, 'output': 'Testing  failed', 'event': 'generate_graph_csv'}
            send_notification(0, user_id, 'generate_graph_csv', event)
            # # # reader.sql.stop()
            return event

        event = {'step': 4, 'output': 'Testing  completed', 'event': 'generate_graph_csv'}
        send_notification(0, user_id, 'generate_graph_csv', event)
        # # # reader.sql.stop()
        return event
    except Exception as e:
        event = {'step': 5, 'output': 'Testing  failed', 'event': 'generate_graph_csv'}
        send_notification(0, user_id, 'generate_graph_csv', event)
        # try:
        #     # # # reader.sql.stop()
        # except:
        #     pass
        return event
