# Multilayer Perceptron

#  ---------------  Libraries  ---------------
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# Prints full rows
pd.set_option("display.max_rows", None, "display.max_columns", None) 

#  ---------------  Parameters for models  ---------------
hidden_neurons = 50
epochs = 10000
learning_rate = 0.01
no_change_thresh = epochs


#  ---------------  Data set   ---------------
file = 'perceptron_test_set.csv'
Data_set = pd.read_csv(file, header=None)
# Data_set.columns = ['s_length', 's_width', 'p_length', 'p_width', 'class']
# print(Data_set)
x = Data_set.iloc[:, 0:4]
# y = Data_set['class']
print(x)

# Split test data from training data, 80% Training, 20% Test
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True, random_state=8)