from ctypes.wintypes import tagRECT
import os
from os import listdir
from os.path import join, dirname
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
from datetime import datetime
from tqdm import tqdm
import pickle 

PATH_REPO = (os.getcwd())
PATH_DATA = join(PATH_REPO, 'data')
PATH_UTILS = join(PATH_REPO, 'src')
PATH_MODELS = join(PATH_REPO, 'models')

sys.path.append(PATH_UTILS)

print(PATH_REPO)
import preprocess
import models_
from models_ import predict_sklearn_pipeline

submission = pd.read_csv(join(PATH_DATA, 'SampleSubmission.csv'))
train = pd.read_csv(join(PATH_DATA, 'Train.csv'))
model = pickle.load(open(join(PATH_MODELS, 'random_forest_contraceptive.sav'), 'rb'))


##############################PREPROCESSING##############################

test = submission.copy()
test[['year', 'month', 'site_code', 'product_code']] = test['ID'].str.split(' X ', expand=True)
test = preprocess.format_categorical_submission(test)

data = pd.concat((train, test))

data_format = preprocess.format_data(data)
data_format = preprocess.replaceNAv0(data)

##############################Features##############################

data_format = preprocess.add_features(data)

##############################Forecast##############################

target = ['stock_distributed', 'stock_initial', 'stock_received', 'stock_adjustment', 'stock_end', 'average_monthly_consumption', 'stock_ordered']
numerical_features = ['stock_distributed_lag_1', 'stock_distributed_lag_2', 'stock_initial_lag_1', 'stock_received_lag_1', 'stock_adjustment_lag_1', 'stock_end_lag_1', 'average_monthly_consumption_lag_1', 'stock_ordered_lag_1']
categorical_features = ['month', 'region', 'product_code', 'site_code', 'service_type', 'product_type']

data_forecast = data_format.loc[(data_format.loc[:,'date']>=datetime.strptime('2019-07-01', '%Y-%m-%d')) & \
             (data_format.loc[:,'date']<=datetime.strptime('2019-09-01', '%Y-%m-%d')), ]

print(data_forecast)

data_forecast.loc[:,target] = predict_sklearn_pipeline(model, data_forecast, numerical_features, numerical_features+categorical_features, target, val_start='2019-07-01', val_end='2019-09-01')

############################Submit############################

data_forecast.loc[:,'id'] = data_forecast.apply(lambda x: str(x['year']) + ' X ' + str(x['month']) + ' X ' + x['site_code'] + ' X ' + x['product_code'], axis=1)

for id in np.unique(test['ID']):
    test.loc[test.loc[:,'ID']==id, 'prediction'] = data_forecast.loc[data_forecast.loc[:,'id']==id, 'stock_distributed'].values

submission['prediction'] = test['prediction']

submission.to_csv(join(PATH_DATA, 'SampleSubmission.csv'))