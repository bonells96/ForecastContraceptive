import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from typing import List, Union


######################################## Prediction function for classical ML ###############################################

def predict_sklearn_pipeline(model, val_dataset:pd.DataFrame, update_cols: Union[List, str], features: Union[List, str], targets: Union[List, str], \
                                 val_start:str ='2019-03-01', val_end: str='2019-06-01'):

    val_copy = val_dataset.copy()
    start_date = datetime.strptime(val_start, '%Y-%m-%d')
    end_date = datetime.strptime(val_end, '%Y-%m-%d')
    
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month  - start_date.month) + 1
    dates = [(start_date + relativedelta(months=i)) for i in range(num_months)]
    
    if type(update_cols)==str:
        update_cols = [update_cols]
    if type(targets)==str:
        targets = [targets]
    cols_lag_1 = [cols for cols in update_cols if 'lag_1' in cols]
    cols_lag_2 = [cols for cols in update_cols if 'lag_2' in cols]

    for k, date in enumerate(dates[:-1]):
        df_preds = pd.DataFrame(columns=targets)
        val_month = val_copy.loc[val_copy.loc[:,'date']==date,]
    
        preds = model.predict(val_month.loc[:,features])

        preds = np.where(preds<0, 0, preds)
        
        if len(targets)==1:
            df_preds.loc[:,targets[0]] = preds
        else:
            for j, col in enumerate(targets):
                df_preds.loc[:,col] = preds[:,j]
        if len(cols_lag_1)>0:
            target_cols_lag_1 = [col.replace("_lag_1", "") for col in cols_lag_1]
            for col, target_col in zip(cols_lag_1, target_cols_lag_1):
                val_copy.loc[val_copy.loc[:,'date']==dates[k+1],col] = df_preds.loc[:,target_col].values
            #val_copy.loc[val_copy.loc[:,'date']==dates[k+1],cols_lag_1] = df_preds.loc[:,target_cols_lag_1].values

        if len(cols_lag_2)>0 and (k+2)<= len(dates):
            target_cols_lag_2 = [col.replace("_lag_2", "") for col in cols_lag_2]
            for col, target_col in zip(cols_lag_2, target_cols_lag_2):
                val_copy.loc[val_copy.loc[:,'date']==dates[k+1],col] = df_preds.loc[:,target_col].values
            #val_copy.loc[val_copy.loc[:,'date']==dates[k+2],cols_lag_2] = df_preds.loc[:,target_cols_lag_2].values
        
    
    preds_final = model.predict(val_copy.loc[:,features])

    return np.where(preds_final<0, 0, preds_final)






######################################## Dataset ########################################




class ContraceptiveDataset(Dataset):
  def __init__(self, data, cat_cols=None, cont_cols=None,  output_col=None):
    """
    Characterizes a Dataset for PyTorch

    Parameters
    ----------

    data: pandas data frame
      The data frame object for the input data. It must
      contain all the continuous, categorical and the
      output columns to be used.

    cat_cols: List of strings
      The names of the categorical columns in the data.
      These columns will be passed through the embedding
      layers in the model. These columns must be
      label encoded beforehand. 

    output_col: string
      The name of the output variable column in the data
      provided.
    """

    self.n = data.shape[0]

    if output_col:
      self.y = data[output_col].astype(np.float32).values#.reshape(-1, 1)
    else:
      self.y =  np.zeros((self.n, 1))

    self.cat_cols = cat_cols 
    self.cont_cols = cont_cols 

    self.cont_X = data[self.cont_cols].astype(np.float32).values

    self.cat_X = data[cat_cols].astype(np.int64).values


  def __len__(self):

    return self.n

  def __getitem__(self, idx):
 
    return [self.y[idx], self.cont_X[idx], self.cat_X[idx]]



######################################## Neural Network ########################################



class FeedForwardNN(nn.Module):

  def __init__(self, emb_dims, num_cont, lin_layer_sizes, output_size, emb_dropout, lin_layer_dropouts):

    """
    Parameters:

    emb_dims, List: List of two element tuples where the first element of a tuple represents
    number of unique values of the categorical  feature. The second element is the embedding
    dimension to be used for that feature.

    num_cont, Integer: The number of continuous features in the data.

    lin_layer_sizes, List: 
      The size of each linear layer. The length will be equal
      to the total number
      of linear layers in the network.

    output_size: Integer
      The size of the final output.

    emb_dropout: Float
      The dropout to be used after the embedding layers.

    lin_layer_dropouts: List of floats
      The dropouts to be used after each linear layer.
    """

    super().__init__()

    # Embedding layers
    self.emb_layers = nn.ModuleList([nn.Embedding(x, y) for x, y in emb_dims])

    num_embs = sum([y for x, y in emb_dims])
    self.num_embs = num_embs
    self.num_cont = num_cont

    # Linear Layers
    first_lin_layer = nn.Linear(self.num_embs + self.num_cont,
                                lin_layer_sizes[0])

    self.lin_layers =\
     nn.ModuleList([first_lin_layer] +\
          [nn.Linear(lin_layer_sizes[i], lin_layer_sizes[i + 1])
           for i in range(len(lin_layer_sizes) - 1)])

    # Output Layer
    self.output_layer = nn.Linear(lin_layer_sizes[-1],
                                  output_size)

    # Batch Norm Layers
    self.first_bn_layer = nn.BatchNorm1d(self.num_cont)
    self.bn_layers = nn.ModuleList([nn.BatchNorm1d(size)
                                    for size in lin_layer_sizes])

    # Dropout Layers
    self.emb_dropout_layer = nn.Dropout(emb_dropout)
    self.droput_layers = nn.ModuleList([nn.Dropout(size)
                                  for size in lin_layer_dropouts])

  def forward(self, cont_data, cat_data):

    x = [emb_layer(cat_data[:, i])
           for i,emb_layer in enumerate(self.emb_layers)]
    x = torch.cat(x, 1)
    x = self.emb_dropout_layer(x)

    
    normalized_cont_data = self.first_bn_layer(cont_data)

    x = torch.cat([x, normalized_cont_data], 1) 

    for lin_layer, dropout_layer, bn_layer in\
        zip(self.lin_layers, self.droput_layers, self.bn_layers):
      
      x = F.relu(lin_layer(x))
      x = bn_layer(x)
      x = dropout_layer(x)

    x = self.output_layer(x)

    return x