from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.utils import to_categorical 
import random, logging
import pandas as pd
import numpy as np

x1 = [random.randint(1, 100) for _ in range(100000)]
#X = np.array([(k, k-(int(k/2)*2)) for k in x1])
X = np.array([(k) for k in x1])
#X = X.reshape(-1, 1)

Y = np.array(to_categorical([bool(x % 2) for x in X]))
#Y = Y.reshape(-1, 1)

# Split the data into a training and testing set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# Create and train the logistic regression model
model = Sequential()
model.add(Dense(256, input_dim=1, activation='sigmoid'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='sigmoid'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='sigmoid'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='sigmoid'))
model.add(Dense(2, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# Lists to store epoch results
accuracy_per_epoch = []

print(X_train.shape)
print(Y_train.shape)

# Training loop for multiple epochs
num_epochs = 10
for _epoch in range(num_epochs):
    model.fit(x=X_train, y=Y_train, epochs=10, verbose=2)

    # Calculate accuracy for this epoch
    _, accuracy = model.evaluate(X_test, Y_test, verbose=2)
    t0 = random.randint(1, 100)
    t1 = (t0)
    nn = np.array([t1])
    #print(nn)
    #print(nn.shape)
    z = model.predict(nn)
    #z=1
    print(_epoch, " : ", accuracy, " --> [", t0, ", ", z, "]")
    
    # Append the accuracy to the list
    accuracy_per_epoch.append(accuracy)

# Create a DataFrame to store the results
results_df = pd.DataFrame({'Epoch': range(1, num_epochs + 1), 'Accuracy': accuracy_per_epoch})

# Save the DataFrame to a single CSV file
results_df.to_csv('classification_accuracy_per_epoch.csv', index=False)
