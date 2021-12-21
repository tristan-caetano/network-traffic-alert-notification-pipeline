# Network Traffic Alert Notification Pipeline Project MVP 
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Multilayer Perceptron

#  ---------------  Our goal   ---------------

# Develop an Artificial Intelligence / Machine Learning (AI/ML) solution, which monitors real-time network 
# traffic, classifies groups of packets as either malicious or normal, and notifies the LAN Admin 
# immediately when consistent, sustained malicious activity has been observed. 

#  ---------------  Libraries  ---------------
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


#  ---------------  Data set   ---------------
file = 'perceptron_test_set.csv'
Data_set = pd.read_csv(file)
Data_set.head()


#  ---------------  Spliting data into Feature   ---------------
X = Data_set[[Data_set.columns[0], Data_set.columns[1], Data_set.columns[2], Data_set.columns[3], Data_set.columns[4], Data_set.columns[5], Data_set.columns[6], Data_set.columns[7], Data_set.columns[8], Data_set.columns[9], Data_set.columns[10], Data_set.columns[11], Data_set.columns[12], Data_set.columns[13], Data_set.columns[14], Data_set.columns[15], Data_set.columns[16], Data_set.columns[17], Data_set.columns[18], Data_set.columns[19], Data_set.columns[20], Data_set.columns[21], Data_set.columns[22], Data_set.columns[23], Data_set.columns[24], Data_set.columns[25], Data_set.columns[26], Data_set.columns[27], Data_set.columns[28], Data_set.columns[29], Data_set.columns[30], Data_set.columns[31], Data_set.columns[32], Data_set.columns[33], Data_set.columns[34], Data_set.columns[35], Data_set.columns[36], Data_set.columns[37], Data_set.columns[38], Data_set.columns[39], Data_set.columns[40], Data_set.columns[41], Data_set.columns[42], Data_set.columns[43], Data_set.columns[44], Data_set.columns[45], Data_set.columns[46]]]
y = Data_set[Data_set.columns[47]]



#  ---------------  Split dataset into training set and test set   ---------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)  # 70% training and 30% test


#  ---------------  Create model object   ---------------
clf = MLPClassifier(hidden_layer_sizes=(6,5),
                    random_state=5,
                    verbose=True,
                    learning_rate_init=0.01)


#  ---------------  Fit data onto the model   ---------------
clf.fit(X_train, y_train)


#  ---------------  Make prediction   ---------------
ypred = clf.predict(X_test)


#  ---------------  Calcuate accuracy   ---------------
print('\nOutput:')
print(accuracy_score(y_test, ypred))