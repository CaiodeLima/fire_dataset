import pandas as pd
import tensorflow as tf
import numpy as np
import math
import csv
from tensorflow import feature_column

def demo(feature_layer):#feature_column):
  #feature_layer = tf.keras.layers.DenseFeatures(feature_column)
  #print(feature_layer(example_batch).numpy())
  return feature_layer(example_batch).numpy()

def df_to_dataset(dataframe):
  dataframe = dataframe.copy()
  labels = dataframe.pop('cicatriz')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  ds = ds.batch(len(dataframe))
  return ds

def bucketizar_lat_lon(feature, example_batch):
  column = feature_column.numeric_column(feature)
  feature_layer = tf.keras.layers.DenseFeatures(column)
  valor = min(feature_layer(example_batch).numpy())[0]
  maximo = max(feature_layer(example_batch).numpy())[0]
  limites = []

  while valor < maximo:
    limites.append(valor)
    valor += 0.5

  limites.append(maximo)

  print('Tamanho:',len(limites))

  return feature_column.bucketized_column(column, boundaries=limites)
    


# INÍ?CIO DO CÓ?DIGO

path = '/home/saigg/Desktop/sandbox_scholles/Dataset/treino.csv'
col_list = ['latitude','longitude','cicatriz']
csv = pd.read_csv(path, sep = ';',usecols=col_list)
dataset = df_to_dataset(csv)
example_batch = next(iter(dataset))[0]

latitude = bucketizar_lat_lon('latitude', example_batch)
longitude = bucketizar_lat_lon('longitude', example_batch)
crossed_feature = feature_column.crossed_column([latitude, longitude], hash_bucket_size=3038)

feature_layer = tf.keras.layers.DenseFeatures(feature_column.indicator_column(crossed_feature))

local = demo(feature_layer)
new_feat = []

for i in local:
    ind = np.where(i == 1)
    new_feat.append(ind[0][0])

#print(new_feat)
csv = pd.read_csv(path, sep = ';')
csv['local_crossed'] = new_feat
#print(csv)
#dicio = {'local_crossed':new_feat}
#shazem = pd.DataFrame.from_dict(dicio)

csv.to_csv('/home/saigg/Desktop/sandbox_scholles/Dataset/treino.csv', sep = ';', index = False)