from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from mlbot.models import UserDocs
from mlbot.algorithms.dashboard import *
from mlbot.algorithms.graph import *
from mlbot.algorithms.models import *
from mlbot.algorithms.preprocess import *
import datetime
from django.conf import settings
import pickle
import os.path
import json
import dill

@receiver(post_save, sender=UserDocs)
def model_training_request(sender, instance, created, **kwargs):
    if created:
        print('start training here')


        print(instance.file_url)
        file_object = Dashboard(instance.file_url, instance.y_variables)
        file_object.file_transformation()
        file_object.finding_best_model()
        file_object.update_best_model()
        file_name = file_object.save()
        key_for_graph = file_object.get_prediction_key()
        print(key_for_graph)

        # file_name = 'dashboard1.pickle'

        basename = "dashbaord"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        file_name = "_".join([basename, suffix]) + ".pickle"  # e.g. 'mylogfile_120508_171442'



        path = os.path.join(settings.MEDIA_ROOT, 'Images', 'User', 'Dashboard', file_name);
        print(path)

        file = open(path, 'w+')
        pickle.dump(file_object, file)

        instance.dashboard.dashboard_url = 'Images/User/Dashboard/'+file_name
        instance.dashboard.graph_key=json.dumps(key_for_graph)
        instance.dashboard.save()

        instance.doc_status = 'Processed'
        instance.save()
        
        
        # file_object.check_for_new_data()
        #
        # key= file_object.prediction_key()
        #
        # [ graph_index, variables_array,
        # dic= {
        #     var1: {
        #         op1: 'val'('val' is not important)
        #     },
        #     var2: {}
        #     ,
        #     'salesmonth' : {}
        # }   ]
        #
        # dic[var2] = {}
        #
        #
        # inputtomycode= [key[0], { month: [12,1], day:[1,21], year:[2017,2018], var1:[13424342,], varstring:["opt1"]}
        #
        #
        # output_dataframe= file_object.make_graph(key[0],in)
        #
        # file=open('dashboard.pickle', 'w+')
        # pickle.dump(file_object,file)






