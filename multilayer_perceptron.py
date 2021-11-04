# Multilayer Perceptron

#  ---------------  Libraries  ---------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split


#  ---------------  Dataset  ---------------

class StudentsPerformanceDataset(Dataset):
    """Students Performance dataset."""

    def __init__(self, csv_file):
        """Initializes instance of class StudentsPerformanceDataset.
        Args:
            csv_file (str): Path to the csv file with the students data.
        """
        df = pd.read_csv(csv_file)

        # Grouping variable names
        self.categorical = ["gender", "race/ethnicity", "parental level of education", "lunch",
                           "test preparation course"]
        self.target = "math score"

        # One-hot encoding of categorical variables
        self.students_frame = pd.get_dummies(df, prefix=self.categorical)

        # Save target and predictors
        self.X = self.students_frame.drop(self.target, axis=1)
        self.y = self.students_frame[self.target]

    def __len__(self):
        return len(self.students_frame)

    def __getitem__(self, idx):
        # Convert idx from tensor to list due to pandas bug (that arises when using pytorch's random_split)
        if isinstance(idx, torch.Tensor):
            idx = idx.tolist()

        return [self.X.iloc[idx].values, self.y[idx]]


#  ---------------  Model  ---------------

class Net(nn.Module):

    def __init__(self, D_in, H=15, D_out=1):
        super().__init__()
        self.fc1 = nn.Linear(D_in, H)
        self.fc2 = nn.Linear(H, D_out)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x.sequeze() 
        # The squeeze() function is used to remove single-dimensional entries from the shape of an array.

#  ---------------  Training  ---------------

def train(csv_file, n_epochs=100):
    """Trains the model.
    Args:
        csv_file (str): Absolute path of the dataset used for training.
        n_epochs (int): Number of epochs to train.
    """
    # Load dataset
    dataset = StudentsPerformanceDataset(csv_file)

    # Split into training and test
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    trainset, testset = random_split(dataset, [train_size, test_size])

    # Dataloaders
    trainloader = DataLoader(trainset, batch_size=200, shuffle=True)
    testloader = DataLoader(testset, batch_size=200, shuffle=False)

    # Set device to use gpu if available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Define the model
    D_in, H = 19, 15
    net = Net(D_in, H).to(device)

    # Loss function
    criterion = nn.MSELoss()
    # MSELoss() function creates a criterion that measures the mean squared error (squared L2 norm) between each element in the input x and target y.

    # Optimizer
    optimizer = optim.Adam(net.parameters(), weight_decay=0.0001)
    # Adam() function is an optimization algorithm.

    # Train the net
    loss_per_iter = []
    loss_per_batch = []
    for epoch in range(n_epochs):

        running_loss = 0.0
        for i, (inputs, labels) in enumerate(trainloader):
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward + backward + optimize
            outputs = net(inputs.float())
            loss = criterion(outputs, labels.float())
            loss.backward()
            optimizer.step()

            # Save loss to plot
            running_loss += loss.item()
            loss_per_iter.append(loss.item())

        loss_per_batch.append(running_loss / (i + 1))
        running_loss = 0.0

    # Comparing training to test
    dataiter = iter(testloader)
    inputs, labels = dataiter.next()
    inputs = inputs.to(device)
    labels = labels.to(device)
    outputs = net(inputs.float())
    print("Root mean squared error")
    print("Training:", np.sqrt(loss_per_batch[-1]))
    print("Test", np.sqrt(criterion(labels.float(), outputs).detach().cpu().numpy()))

    # Plot training loss curve
    plt.plot(np.arange(len(loss_per_iter)), loss_per_iter, "-", alpha=0.5, label="Loss per epoch")
    plt.plot(np.arange(len(loss_per_iter), step=4) + 3, loss_per_batch, ".-", label="Loss per mini-batch")
    plt.xlabel("Number of epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    import os
    import sys
    import argparse

    # By default, read csv file in the same directory as this script
    csv_file = os.path.join(sys.path[0], "StudentsPerformance.csv")

    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", nargs="?", const=csv_file, default=csv_file,
                        help="Dataset file used for training")

    parser.add_argument("--epochs", "-e", type=int, nargs="?", default=100, help="Number of epochs to train")
    args = parser.parse_args()

    # Call the main function of the script
    train(args.file, args.epochs)




# Multilayer perceptron

# PyTorch Tutorials
# https://www.youtube.com/watch?v=GIsg-ZUy0MY&ab_channel=freeCodeCamp.org
# https://www.youtube.com/watch?v=Ycp4Si89s5Q&ab_channel=SebastianRaschka

# Libraries
# import csv
# import torch
# import numpy as np
# import pandas as pd
# import torch.nn as nn

# import torch.optim as optim
# import torch.nn.functional as F
# from torch.utils.data import DataLoader
# import torchvision.datasets as datasets
# import torchvision.transforms as transfroms

# # Pandas Import CSV
# Data_set = pd.read_csv('perceptron_test_set.csv')

# # Converts the data to Pytorch tensor
# Pytorch_data = torch.tensor(Data_set.values)

# # Sets the data parameter 
# data = Pytorch_data[:, :]

# # The size of the data
# data_size = data.shape

# # Number of rows
# row_num = data.shape[0]

# # Number of columns
# col_num = data.shape[1]


# # print(data)
# print(data_size)
# print(row_num)
# print(col_num)
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
#       