import training_Util as util

##Read in our data
keys, dataMap = util.readData("finalData.csv")

##Parse Round 2 (Get rid of second to last value)
dataMap = util.parse2(dataMap)

dataMap = util.inflationCorrectedPrice(dataMap)

dataMap = util.transformFeature(dataMap)

##Seperate label from data (split into x and y data)
data, labels = util.splitLabel(dataMap)

##Use k fold to get partitions of data into train and test data
k = 4
X_trains, X_tests, y_trains, y_tests = util.partition(data, labels, k)

print len(X_trains[0])
print len(X_tests[0])
print len(y_trains[0])
print len(y_tests[0])


##Train Linear Models and get Error
totalLinear = (0.0, 0.0)
totalLasso = (0.0, 0.0)
totalElastic = (0.0, 0.0)
totalRidge = (0.0, 0.0)

import operator
for i in range(k):
    linear, lasso, elastic, ridge = util.trainAndTestModels(X_trains[i], y_trains[i], X_tests[i], y_tests[i])
    totalLinear = tuple(map(operator.add, totalLinear, linear))
    totalLasso = tuple(map(operator.add, totalLasso, lasso))
    totalElastic = tuple(map(operator.add, totalElastic, elastic))
    totalRidge = tuple(map(operator.add, totalRidge, ridge))
    
util.printError(totalLinear, k)
util.printError(totalLasso, k)
util.printError(totalElastic, k)
util.printError(totalRidge, k)


    
