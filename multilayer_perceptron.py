# Multilayer perceptron

# PyTorch Tutorials
# https://www.youtube.com/watch?v=GIsg-ZUy0MY&ab_channel=freeCodeCamp.org
# https://www.youtube.com/watch?v=Ycp4Si89s5Q&ab_channel=SebastianRaschka

# Libraries
import csv
import torch
import numpy as np
import pandas as pd
import torch.nn as nn

import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transfroms

# Pandas Import CSV
Data_set = pd.read_csv('perceptron_test_set.csv')

# Converts the data to Pytorch tensor
Pytorch_data = torch.tensor(Data_set.values)

# Sets the data parameter 
data = Pytorch_data[:, :]

# The size of the data
data_size = data.shape

# Number of rows
row_num = data.shape[0]

# Number of columns
col_num = data.shape[1]


# print(data)
print(data_size)
print(row_num)
print(col_num)
# print(data.unique())


##########################
# Neural-Network Template
# https://www.youtube.com/watch?v=Jy4wM2X21u0&ab_channel=AladdinPersson
##########################

# # Create fully connected network
# class NeuralNet(nn.Module):
#     def __init__(self, input_size, num_classes):
#         super(NeuralNet, self).__init__()
#         self.fc1 = nn.Linear(input_size, 50)
#         self.fc2 = nn.Linear(50, num_classes)
    
#     def forward(self, x):
#         x = F.relu(self.fc1(x))
#         x = self.fc2(x)
#         return x


# # Set device
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# # Hyperparameters
# input_size = 784
# num_classes = 10
# learning_rate = 0.001
# batch_size = 64
# num_epochs = 1

# # Load Data
# train_dataset = datasets.MNIST(root='dataset/', train=True, transform=transfroms.ToTensor(), download=True)
# train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
# test_dataset = datasets.MNIST(root='dataset/', train=False, transform=transfroms.ToTensor(), download=True)
# test_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)


# # Initialize network
# model = NeuralNet(input_size=input_size, num_classes=num_classes).to(device)

# # Loss and optimizer
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=learning_rate)


# # Train network
# for epoch in range(num_epochs):
#     for batch_idx, (data, targets) in enumerate(train_loader):
#         # Get data to cuda if possible
#         data = data.to(device=device)
#         targets = targets.to(device=device)

#         # Get to correct shape
#         data = data.reshape(data.shape[0], -1)

#         # Forward
#         scores = model(data)
#         loss = criterion(scores, targets)

#         # Backwards
#         optimizer.zero_grad()
#         loss.backward()

#         # gradient descent or adam stop
#         optimizer.step()


# # Check accuracy on training & test to see how good the model is
# def check_accuracy(loader, model):
#     if loader.dataset.train:
#         print("Checking accuracy on training data")
#     else:
#         print("Checking accuracy on test data")

#     num_correct = 0
#     num_samples = 0
#     model.eval()

#     with torch.no_grad():
#         for x, y in loader:
#             x = x.to(device=device)
#             y = y.to(device=device)
#             x = x.reshape(x.shape[0], -1)

#             scores = model(x)
#             _, predictions = scores.max(1)
#             num_correct += (predictions == y).sum()
#             num_samples += predictions.size(0)

#         print(f'Got {num_correct} / {num_samples} with accuracy {float(num_correct)/float(num_samples)*100:.2f}')

#     model.train()

# check_accuracy(train_loader, model)
# check_accuracy(test_loader, model)
        