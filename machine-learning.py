# Machine Learning Algorithm.
# By Tristan Caetano, Tate DeTerra, and Jason Pinto

import csv
import torch
import numpy as np

import pandas as pd
from pandas.core.arrays.sparse import dtype
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose
from sklearn.preprocessing import StandardScaler
# from pytorch.ppg_feature_dataset import FeatureDataset

# Import CSV file in PyTorch

filename = "UNSW-NB15_1.csv"

w_numpy = np.loadtxt(filename, dtype= np.float32, delimiter=";", skiprows=1)


type(w_numpy)
# numpy.ndarray

columns = next(csv.reader(open(filename), delimiter=';'))
w_pytorch = torch.from_numpy(w_numpy)

type(w_pytorch)
w_pytorch.dtype
w_pytorch.shape

# print(w_numpy)
print(w_pytorch)



# Test Example: >

# csv_file = pd.read_csv(filename, low_memory=False)

# feature_set = FeatureDataset('UNSW-NB15_1.csv')
# train_loader = torch.utils.data.DataLoader(feature_set, batch_size=10, shuffle=True)

# x = csv_file.iloc[1:700001, 1:49].values
# y = csv_file.iloc[1:700001, 49].values

# scaler = StandardScaler()
# x_train = scaler.fit_transform(x)

# self.x_train = torch.tensor(x_train, dtype = torch.float32)
# self.y = torch.tensor(y)


# def __len__(self):
#     return len(self.y)

# def __getitem__(self, idx):
#     return self.x_train[idx], self.y[idx]


