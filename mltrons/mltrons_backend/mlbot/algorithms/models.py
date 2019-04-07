import numpy
numpy.random.seed(123)
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
#import xgboost as xgb
from sklearn import neighbors
from sklearn.preprocessing import Normalizer
from keras.layers import LSTM
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Reshape
from keras.layers import Merge
from keras.layers.embeddings import Embedding
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn import decomposition
import numpy as np
import random as rd

def embed_features(X, saved_embeddings_fname):
    # f_embeddings = open("embeddings_shuffled.pickle", "rb")
    f_embeddings = open(saved_embeddings_fname, "rb")
    embeddings = pickle.load(f_embeddings)

    index_embedding_mapping = {1: 0, 2: 1, 4: 2, 5: 3, 6: 4, 7: 5}
    X_embedded = []

    (num_records, num_features) = X.shape
    for record in X:
        embedded_features = []
        for i, feat in enumerate(record):
            feat = int(feat)
            if i not in index_embedding_mapping.keys():
                embedded_features += [feat]
            else:
                embedding_index = index_embedding_mapping[i]
                embedded_features += embeddings[embedding_index][feat].tolist()

        X_embedded.append(embedded_features)

    return numpy.array(X_embedded)


def split_features(X):
    X_list = []
    for i in range(len(X[0])):
        
        temp = X[..., [i]]
        X_list.append(temp)
    
    return X_list


class Model(object):

    def evaluate(self, X_val, y_val):
        assert(min(y_val)+4 > 0)
        guessed_sales = self.guess(X_val)
        relative_err = numpy.absolute((y_val - guessed_sales) / y_val)
        result = numpy.sum(relative_err) / len(y_val)
        return result
    
    
    def rmspe(self, X_val, y_val):
        assert(min(y_val)+4 > 0)
        guessed_sales = self.guess(X_val)
        relative_err = (y_val - guessed_sales) / (y_val)
        r_err_sq= numpy.square(relative_err)
        result = numpy.sum(r_err_sq) / len(y_val)
        return result**.5
    
    def rmse(self, X_val, y_val):
        assert(min(y_val) +4> 0)
        guessed_sales = self.guess(X_val)
#        relative_err = numpy.square(numpy.absolute((y_val - guessed_sales)))
#        result = numpy.sum(relative_err) / len(y_val)
        result= mean_squared_error(y_val, guessed_sales)**.5
        return result

    def rmsle(self, X_val, y_val):
        #assert(min(y_val) > 0)
        guessed_sales = numpy.log(numpy.array(self.guess(X_val))+1)
        y_val= numpy.log(numpy.array(y_val)+1)
#        relative_err = numpy.square(numpy.absolute((y_val - guessed_sales)))
#        result = numpy.sum(relative_err) / len(y_val)
        result= mean_squared_error( guessed_sales, y_val)**.5
        return result

###############################################################################
class LinearModel(Model):

    def __init__(self):
        super(LinearModel).__init__()
        
    def input(self, preprss_file_name):
        # generating random file name to dump preprocessing
        
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None   
        
        self.clf = linear_model.LinearRegression()
        self.clf.fit(self.preprocess_object.get_train_x(), numpy.log(self.preprocess_object.get_train_y()))
        self.model_results= self.evaluate(self.preprocess_object.get_test_x(), self.preprocess_object.get_test_y())
        print("Result on validation data: ", self.model_results)

    def guess(self, feature):
        return numpy.exp(self.clf.predict(feature))

    def train(self):
        self.load_preprocess_object()
        self.clf.fit(self.preprocess_object.get_train_x(), numpy.log(self.preprocess_object.get_train_y()))       

    def get_results(self):
        return self.model_results
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object
##############################################################################3
class RF(Model): # complete but not tested

    def __init__(self):
        super(RF).__init__()

    def input(self, preprss_file_name):
        # generating random file name to dump preprocessing
        
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None    
    
        self.clf = RandomForestRegressor(n_estimators=200, verbose=True, max_depth=35, min_samples_split=2,
                                         min_samples_leaf=1)
        self.clf.fit(self.preprocess_object.get_train_x(), numpy.log(self.preprocess_object.get_train_y()))
        self.model_results= self.evaluate(self.preprocess_object.get_test_x(), self.preprocess_object.get_test_y())
        print("Result on validation data: ", self.model_results)

    def guess(self, feature):
        return numpy.exp(self.clf.predict(feature))
    
    def train(self):
        self.load_preprocess_object()
        self.clf.fit(self.preprocess_object.get_train_x(), numpy.log(self.preprocess_object.get_train_y()))       

    def get_results(self):
        return self.model_results
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object

###############################################################################
class SVM(Model):

    def __init__(self):
        super(SVM, self).__init__()
        
    def input(self, preprss_file_name):
        # generating random file name to dump preprocessing
        
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None    
        self.X_train= None
        
        self.__normalize_data()
        self.clf = SVR(kernel='linear', degree=3, gamma='auto', coef0=0.0, tol=0.001,
                       C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)

        self.clf.fit(self.X_train, numpy.log(self.preprocess_object.get_train_y()))
        self.model_results= self.rmspe(self.preprocess_object.get_test_x(), self.preprocess_object.get_test_y())
        print("Result on validation data: ", self.model_results)

    def __normalize_data(self):
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.preprocess_object.get_train_x())
        
    def train(self):
        self.load_preprocess_object()
        self.__normalize_data()
        self.clf.fit(self.X_train, numpy.log(self.preprocess_object.get_train_y()))

    def guess(self, feature):
        return numpy.exp(self.clf.predict(feature))

    def get_results(self):
        return self.model_results
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object

###############################################################################
# class XGBoost(Model):
#
#     def __init__(self):
#         super(XGBoost, self).__init__()
#
#     def input(self, preprss_file_name):
#         # generating random file name to dump preprocessing
#
#         self.preprocess_p_file = preprss_file_name
#         self.preprocess_object= None
#         self.load_preprocess_object()
#         self.save_preprocess_object()
#         self.model_results=None
#         self.train()
#
#
#     def train(self):
#         self.load_preprocess_object()
#         dtrain = xgb.DMatrix(self.preprocess_object.get_train_x(), label=numpy.log(self.preprocess_object.get_train_y()))
#         evallist = [(dtrain, 'train')]
#         param = {'nthread': -1,
#                  'max_depth': 7,
#                  'eta': 0.02,
#                  'silent': 1,
#                  'objective': 'reg:linear',
#                  'colsample_bytree': 0.7,
#                  'subsample': 0.7}
#         num_round = 2000
#         self.bst = xgb.train(param, dtrain, num_round, evallist)
#         self.model_results= self.rmspe(self.preprocess_object.get_test_x(), self.preprocess_object.get_test_y())
#         print("Result on validation data: ", self.model_results)
#
#     def guess(self, feature):
#         dtest = xgb.DMatrix(feature)
#         return numpy.exp(self.bst.predict(dtest))
#
#     def get_results(self):
#         return self.model_results
#
#     def save_preprocess_object(self):
#         with open(self.preprocess_p_file, 'wb') as f:
#             pickle.dump((self.preprocess_object), f)
#
#     def load_preprocess_object(self):
#         with open(self.preprocess_p_file, 'rb') as f:
#             self.preprocess_object= pickle.load(f)
#
#     def get_preprocess_object(self):
#         return self.preprocess_object

    
######################################################################################33
class HistricalMedian(Model):  # not complete not trested

    def __init__(self):
        super(HistricalMedian).__init__()
 
    def input(self, preprss_file_name ):
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None
        
        self.history = {}
        self.feature_index = [1, 2, 3, 4]
        for x, y in zip(self.preprocess_object.get_train_x(), self.preprocess_object.get_train_y()):
            key = tuple(x[self.feature_index])
            self.history.setdefault(key, []).append(y)
        print("Result on validation data: ", self.evaluate(self.preprocess_object.get_test_x(), self.preprocess_object.get_test_y()))

    def guess(self, features):
        features = numpy.array(features)
        features = features[:, self.feature_index]
        guessed_sales = [numpy.median(self.history[tuple(feature)]) for feature in features]
        return numpy.array(guessed_sales)

    def train(self):
        pass
    
    
    def get_results(self):
        return self.model_results
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object

###############################################################################
class KNN(Model):   

    def __init__(self):
        super(KNN, self).__init__()
        
    def input(self, preprss_file_name ):
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None
        
        self.normalizer = Normalizer()
        self.normalizer.fit(self.preprocess_object.get_train_x())
        self.clf = neighbors.KNeighborsRegressor(n_neighbors=10, weights='distance', p=1)
        self.clf.fit(self.normalizer.transform(self.preprocess_object.get_train_x()), numpy.log(self.preprocess_object.get_train_y()))
        self.model_results= self.rmsle(self.guess(self.preprocess_object.get_test_x()), self.preprocess_object.get_test_y())
        print("Result on validation data: ", self.model_results)

    def guess(self, feature):
        self.normalizer.fit(self.preprocess_object.get_train_x())
        return numpy.exp(self.clf.predict(self.normalizer.transform(feature)))
    
    def train(self):
        self.load_preprocess_object()
        self.clf.fit(self.normalizer.transform(self.preprocess_object.get_train_x()), numpy.log(self.preprocess_object.get_train_y()))
    
    def get_results(self):
        return self.model_results
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object
    

###############################################################################
class LSTM_M(Model):  # complete but not tested yet

    def __init__(self):
        super(LSTM_M, self).__init__()
        
    def input(self, preprss_file_name):
        # generating random file name to dump preprocessing
        
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None
        

        self.train_x= np.array(self.preprocess_object.get_train_x()).reshape((len(self.preprocess_object.get_train_x()),1,(len(self.preprocess_object.get_train_x()[0]))))
        self.test_x= np.array(self.preprocess_object.get_test_x()).reshape((self.preprocess_object.get_test_x(),1,(len(self.preprocess_object.get_test_x()[0]))))
        
        self.normalizer = Normalizer()
        self.normalizer.fit(self.train_x)
        self.clf = neighbors.KNeighborsRegressor(n_neighbors=10, weights='distance', p=1)
        self.clf.fit(self.normalizer.transform(self.train_x), numpy.log(self.preprocess_object.get_train_y()))
        self.model_results= self.rmsle(numpy.exp(self.clf.predict(self.normalizer.transform(self.test_x))), self.preprocess_object.get_test_y())
        print("Result on validation data: " + str(self.model_results) )
    
    def train(self):
        self.load_preprocess_object()
        self.train_x= np.array(self.preprocess_object.get_train_x()).reshape((len(self.preprocess_object.get_train_x()),1,(len(self.preprocess_object.get_train_x()[0]))))
        self.normalizer.fit(self.train_x)
        self.clf.fit(self.normalizer.transform(self.train_x), numpy.log(self.preprocess_object.get_train_y()))
        
        
    def guess(self, feature):
        self.guess_temp = np.array(feature).reshape((len(feature),1,(len(feature[0]))))

        return numpy.exp(self.clf.predict(self.normalizer.transform(feature)))
    
    def get_results(self):
        return self.model_results
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object
    
################################################### 
  
class NN_with_EntityEmbedding(Model):

    def __init__(self):
        super(NN_with_EntityEmbedding, self).__init__()
        
    def input(self, preprss_file_name):
        # generating random file name to dump preprocessing
        
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None
        self.nb_epoch = 2
        self.checkpointer = ModelCheckpoint(filepath="best_model_weights.hdf5", verbose=1, save_best_only=True)
        self.max_log_y = max(numpy.max(numpy.log(self.preprocess_object.get_train_y())), numpy.max(numpy.log(self.preprocess_object.get_test_y())))
        self.__build_keras_model(self.preprocess_object.get_dim()[0], self.preprocess_object.get_dim()[1])
        self.fit(self.preprocess_object.get_train_x(), self.preprocess_object.get_train_y(), self.preprocess_object.get_test_x(), self.preprocess_object.get_test_y())

    def preprocessing(self, X):
        X_list = split_features(X)
        return X_list
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object
    
    def __build_keras_model(self, input_dim, output_dim):
        models = []

        for i in range(len(input_dim)):
            model_temp = Sequential()
            if input_dim[i]==1:
                model_temp.add(Dense(1, input_dim=1))
            else:    
                model_temp.add(Embedding(input_dim[i], output_dim[i], input_length=1))
                model_temp.add(Reshape(target_shape=(output_dim[i],)))
            models.append(model_temp)
            


        self.model = Sequential()
        self.model.add(Merge(models, mode='concat'))
        self.model.add(Dense(1000, init='uniform'))
        self.model.add(Activation('relu'))
        self.model.add(Dense(500, init='uniform'))
        self.model.add(Activation('relu'))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def _val_for_fit(self, val):
        val = numpy.log(val) / self.max_log_y

        return val

    def _val_for_pred(self, val):
        ans = numpy.exp(val * self.max_log_y) 
        return ans

    def fit(self, X_train, y_train, X_val, y_val):

        self.model.fit(self.preprocessing(X_train), self._val_for_fit(y_train),
                       validation_data=(self.preprocessing(X_val), self._val_for_fit(y_val)),
                       nb_epoch=self.nb_epoch, batch_size=128,
                       # callbacks=[self.checkpointer],
                       )
        # self.model.load_weights('best_model_weights.hdf5')
        self.model_results=self.rmspe(X_val, y_val)
        print("Result on validation data: ",self.model_results )
   

    def train(self):
        self.load_preprocess_object()
        self.model.fit(self.preprocessing(self.preprocess_object.get_train_x()), self._val_for_fit(self.preprocess_object.get_train_y()),
                       nb_epoch=self.nb_epoch, batch_size=128,
                       # callbacks=[self.checkpointer],
                       )

        print("Training with new data done")  
        
        
    def guess(self, features):
        features = self.preprocessing(features)
        result = self.model.predict(features).flatten()
        return self._val_for_pred(result)
    
    def get_results(self):
        return self.model_results

##########################################################################
class LSTM_with_Pca(Model):  # not tested yet 

    def __init__(self, X_train, y_train, X_val, y_val):
        super(LSTM_with_Pca, self).__init__()
        self.pca = decomposition.PCA(n_components=3)
        self.pca.fit(X_train)
        self.x_train= self.pca.transform(X_train)
        self.x_test =  self.pca.transform(X_val)
        self.y_train= y_train
        self.y_test= y_val
    def preprocessing(self, X):
        X_list = split_features(X)
        return X_list

    def __build_keras_model(self, input_dim, output_dim):

#        input_dim=[1115,7,1,3,12,31,12]
#        output_dim=[10,6,0,2,6,10,6]
#        models = []        
#        for i in range(len(input_dim)):
#            model_temp = Sequential()
#            if input_dim[i]==1:
#                model_temp.add(Dense(1, input_dim=1))
#            else:    
#                model_temp.add(Embedding(input_dim[i], output_dim[i], input_length=1))
#                model_temp.add(Reshape(target_shape=(output_dim[i],)))
#            models.append(model_temp)
            

        self.model = Sequential()
#        self.model.add(Merge(models, mode='concat'))
        self.model.add(LSTM(1000, input_shape=(1, len(input_dim))))
#        self.model.add(Dense(1000, init='uniform'))
#        self.model.add(Activation('relu'))
#        self.model.add(LSTM(500))
#        self.model.add(Dense(500, init='uniform'))
#        self.model.add(Activation('relu'))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def _val_for_fit(self, val):
        val = numpy.log(val) / self.max_log_y
        return val

    def _val_for_pred(self, val):
        return numpy.exp(val * self.max_log_y)

    def fit(self, X_train, y_train, X_val, y_val):

        self.model.fit(X_train, self._val_for_fit(y_train),
                       validation_data=(X_val, self._val_for_fit(y_val)),nb_epoch=self.nb_epoch, batch_size=128)
                       # callbacks=[self.checkpointer],
                       
        # self.model.load_weights('best_model_weights.hdf5')
        print("Result on validation data: ", self.rmspe(X_val, y_val))
        
    def guess(self, features):
#        features = self.preprocessing(features)
        result = self.model.predict(features).flatten()
        return self._val_for_pred(result)


class NN2_with_EntityEmbedding(Model):  # not required right now

    def __init__(self, X_train, y_train , input_dim, output_dim):
        super(NN2_with_EntityEmbedding, self).__init__()
        self.nb_epoch = 5
        self.checkpointer = ModelCheckpoint(filepath="best_model_weights.hdf5", verbose=1, save_best_only=True)
        self.max_log_y = numpy.log(y_train)
        self.__build_keras_model(input_dim, output_dim)
        self.fit(X_train, y_train)

    def preprocessing(self, X):
        X_list = split_features(X)
        return X_list

    def __build_keras_model(self, input_dim, output_dim):
        models = []

        for i in range(len(input_dim)):
            model_temp = Sequential()
            if input_dim[i]==1:
                model_temp.add(Dense(1, input_dim=1))
            else:    
                model_temp.add(Embedding(input_dim[i], output_dim[i], input_length=1))
                model_temp.add(Reshape(target_shape=(output_dim[i],)))
            models.append(model_temp)
 

        self.model = Sequential()
        self.model.add(Merge(models, mode='concat'))
        self.model.add(Dense(1000, init='uniform'))
        self.model.add(Activation('relu'))
        self.model.add(Dense(500, init='uniform'))
        self.model.add(Activation('relu'))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def _val_for_fit(self, val):
        val = numpy.log(val) / self.max_log_y
        return val

    def _val_for_pred(self, val):
        return numpy.exp(val * self.max_log_y)

    def fit(self, X_train, y_train):# this is a case when y_test is unavailable
    
            self.model.fit(self.preprocessing(X_train), self._val_for_fit(y_train),
                           nb_epoch=self.nb_epoch, batch_size=128,
                           # callbacks=[self.checkpointer],
                           )
            # self.model.load_weights('best_model_weights.hdf5')
            print("Result on validation data: ", self.rmse(X_train, y_train))

    def guess(self, features):
        features = self.preprocessing(features)
        result = self.model.predict(features).flatten()
        return self._val_for_pred(result)
    
#################################################################################    
class NN(Model):

    def __init__(self):
        super(NN).__init__()
        
    def input(self, preprss_file_name):
        # generating random file name to dump preprocessing
        
        self.preprocess_p_file = preprss_file_name
        self.preprocess_object= None
        self.load_preprocess_object()
        self.save_preprocess_object()
        self.model_results=None
        
        self.nb_epoch = 10
        self.checkpointer = ModelCheckpoint(filepath="best_model_weights.hdf5", verbose=1, save_best_only=True)
        self.max_log_y = max(numpy.max(numpy.log(self.preprocess_object.get_train_y())), numpy.max(numpy.log(self.preprocess_object.get_test_x())))
        self.__build_keras_model()
        self.fit()

    def __build_keras_model(self):
        self.model = Sequential()
        self.model.add(Dense(1000, init='uniform', input_dim=1183))
        self.model.add(Activation('relu'))
        self.model.add(Dense(500, init='uniform'))
        self.model.add(Activation('relu'))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='mean_absolute_error', optimizer='adam')

    def _val_for_fit(self, val):
        val = numpy.log(val) / self.max_log_y
        return val

    def _val_for_pred(self, val):
        return numpy.exp(val * self.max_log_y)

    def fit(self):
        self.model.fit(self.preprocess_object.get_train_x(), self._val_for_fit(self.preprocess_object.get_train_y()),
                       validation_data=(self.preprocess_object.get_test_x(), self._val_for_fit(self.preprocess_object.get_test_y())),
                       nb_epoch=self.nb_epoch, batch_size=128,
                       # callbacks=[self.checkpointer],
                       )
        # self.model.load_weights('best_model_weights.hdf5')
        self.model_results= self.evaluate(self.preprocess_object.get_test_x(), self.preprocess_object.get_test_y())
        print("Result on validation data: ", self.model_results)

    def guess(self, features):
        result = self.model.predict(features).flatten()
        return self._val_for_pred(result)

    def train(self):
        self.load_preprocess_object()
        self.model.fit(self.preprocess_object.get_train_x(), self._val_for_fit(self.preprocess_object.get_train_y()),
                       validation_data=(self.preprocess_object.get_test_x(), self._val_for_fit(self.preprocess_object.get_test_y())),
                       nb_epoch=self.nb_epoch, batch_size=128,
                       # callbacks=[self.checkpointer],
                       )
        # self.model.load_weights('best_model_weights.hdf5')

    def get_results(self):
        return self.model_results
    
    def save_preprocess_object(self):
        with open(self.preprocess_p_file, 'wb') as f:
            pickle.dump((self.preprocess_object), f)
            
    def load_preprocess_object(self):
        with open(self.preprocess_p_file, 'rb') as f:
            self.preprocess_object= pickle.load(f)
        
    def get_preprocess_object(self):
        return self.preprocess_object