# Multilayer perceptron

# PyTorch Tutorials
# https://www.youtube.com/watch?v=GIsg-ZUy0MY&ab_channel=freeCodeCamp.org
# https://www.youtube.com/watch?v=Ycp4Si89s5Q&ab_channel=SebastianRaschka

# Libraries
import csv
import torch
import numpy as np
import pandas as pd

# Pandas Import CSV
Data_set = pd.read_csv('perceptron_test_set.csv')

# Converts the data to Pytorch tensor
Pytorch_data = torch.tensor(Data_set.values)
# print(Pytorch_data)
# print(type(Pytorch_data))

data = Pytorch_data[:, :-1]
# print(data)

target = Pytorch_data[:, :]

# print(target)
# print(target.shape) # prints: torch.Size([473])
print(target.unique())

# target_onehot = torch.zeros(target.shape[0], 10)
# print(target_onehot)

