from ast import literal_eval
from sklearn import preprocessing
from sklearn import datasets
def readData(filename):
    data = {}
    addresses = []
    with open(filename, "r") as f:
        for line in f:
            key = literal_eval(line[:line.find(")")+1])
            addresses.append(key)
            data[key] = literal_eval(line[line.find(")")+1:])
    return addresses, data

def parse2(data):
    newData = {}
    for key in data:
        newData[key] = data[key][:-4]
    return newData

def getCorrectedPrice(dataPoint):
    inflationRate = 0.0322
    price = float(dataPoint[124])
    for i in range(2017 - int(str(dataPoint[123])[0:4])):
        price += inflationRate*price
    return price

def inflationCorrectedPrice(data):
    newData = {}
    for key in data:
        newData[key] = data[key][:-1] + [getCorrectedPrice(data[key])] + [data[key][-1]]
    return newData

def transformFeature(data):
    newData = {}
    for key in data:
        newData[key] = data[key][:-1] + [data[key][122]*data[key][124]] + [data[key][-1]]
    return newData

import pandas as pd
import numpy as np

def addRace(data, attribute):
    df = pd.read_csv('race_221.csv')
    df.set_index('zipcode', inplace=True)
    newData = {}
    for key in data:
        value = data[key]
        if int(key[1] != '11249'):
            newData[key] = [float(df.loc[int(key[1])][attribute])**2] + value
        else:
            newData[key] = [0.3] + value
    return newData

def splitLabel(data):
    #Partition X and Y
    xData = []
    yData = []
    for value in data.values():
        xData.append(value[0:111]) #changed
        xData.append(value[112:-1])
        #xData.append(value[:-1])
        yData.append(int(value[-1]))
    return xData, yData

import numpy as np
from sklearn.model_selection import KFold
def partition(xData, yData,  k):
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    X = np.array(xData)
    y = np.array(yData)
    kf = KFold(n_splits=k)
    kf.get_n_splits(X)
    KFold(n_splits=2, random_state=None, shuffle=False)
    for train_index, test_index in kf.split(X):
        X_train.append(X[train_index])
        X_test.append(X[test_index])
        y_train.append(y[train_index])
        y_test.append(y[test_index])
    return X_train, X_test, y_train, y_test

def avg(trueVals):
    sum = 0
    for i in range(len(trueVals)):
        sum+= trueVals[i]
    return sum/(len(trueVals)*1.0)

def MPE(predVals, trueVals):
    err = 0
    for i in range(len(trueVals)):
        err += abs((trueVals[i] - predVals[i])/trueVals[i])
    return err/(len(trueVals)*1.0)

from sklearn.metrics import r2_score
def getError(predVals, trueVals):
    return r2_score(trueVals, predVals), MPE(predVals, trueVals)

def trainAndTestModel(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    return getError(model.predict(X_test), y_test)
    #return getError(model.predict(X_scaled_test), y_test)

from sklearn import linear_model
def trainAndTestModels(X_train, y_train, X_test, y_test):
    results = []
    results.append(tuple(trainAndTestModel(linear_model.LinearRegression(), X_train, y_train, X_test, y_test)))
    results.append(tuple(trainAndTestModel(linear_model.Lasso(alpha = 0.5, fit_intercept = True, max_iter = 100), X_train, y_train, X_test, y_test)))
    results.append(tuple(trainAndTestModel(linear_model.ElasticNet(), X_train, y_train, X_test, y_test)))
    results.append(tuple(trainAndTestModel(linear_model.BayesianRidge(), X_train, y_train, X_test, y_test)))
    return results

def printError(errors, k):
    print "RSquared: " + str(errors[0]/k) + " MSE: " + str(errors[1]/k)
