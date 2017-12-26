##Read in full CSV of Addresses from OpenAdresses.io
def readAllAddresses(filename):
    inputs = []
    with open(filename, 'r') as f:
        f.readline() ##omit header
        for line in f:
            record = line.split(",")
            ##Select for the address and ZIP code
            inputs.append((record[2]+" "+record[3], record[8]))
    return inputs

def extractFeatures(result):
    features = []
    features.append(result.home_type)
    features.append(result.latitude)
    features.append(result.longitude)
    features.append(result.tax_year)
    features.append(result.year_built)
    features.append(result.property_size)
    features.append(result.home_size)
    features.append(result.last_sold_date)
    features.append(result.last_sold_price)
    features.append(result.zestimate_amount)
    features.append(result.zestimate_last_updated)
    features.append(result.zestimate_value_change)
    features.append(result.zestimate_valuation_range_high)
    features.append(result.zestimate_valuation_range_high)
    return features

##Querying Zillow API and Extracting Relevant Features
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
def queryAndExtractFeatures(inputs, code):
    results = {}
    for address, zipcode in inputs:
        zillow_data = ZillowWrapper(code)
        try:
            deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
            result = GetDeepSearchResults(deep_search_response)
            results[(address, zipcode)] = extractFeatures(result)+[zipcode]
        except:
            continue
    return results

def removeAllNones(data):
    newData = {}
    for key in data:
        if None in data[key]: continue
        newData[key] = data[key]
    return newData

def convertDateToInt(s):
    sv = s.split("/")
    return int(sv[2] + sv[0] + sv[1])

def isDate(s):
    if "/" in str(s) and s.count("/") == 2: return True
    return False

def discretizeDates(data):
    newData = {}
    for key in data:
        newDp = []
        for elem in data[key]:
            if isDate(elem): newDp.append(convertDateToInt(elem))
            else: newDp.append(float(elem))
        newData[key] = newDp
    return newData

def discretizeBuildingTypes(data):
    buildingTypes = []
    for key in data:
        buildingTypes.append(data[key][0])
    buildingTypes = set(buildingTypes)
    buildingTypesToInt = {}
    i = 0
    for bType in buildingTypes:
        buildingTypesToInt[bType] = i
        i+=1

    newData = {}
    for key in data:
        newDp = [buildingTypesToInt[data[key][0]]] + data[key][1:]
        newData[key] = newDp
    return newData

from geopy.distance import vincenty
def getDist(a, b):
    return (vincenty(a, b).miles)

def getMinSubwayDist(subways, house):
    return min([getDist(stop, house) for stop in subways])

def addDistanceToSubways(all_dataMap):
    newData = {}
    for key in all_dataMap:
        value = all_dataMap[key]
        newData[key] = [getMinSubwayDist(entranceCoords, value[1:3])] + value
    return newData

def parseData(results):
    results = removeAllNones(results)
    results = discretizeBuildingTypes(results)
    results = discretizeDates(results)
    results = addDistanceToSubways(results)
    return results

def writeToFile(filename, results):
    with open(filename, "a+") as f:
        for i in range(0, len(results)):
            f.write(str(results.keys()[i]) + str(results[results.keys()[i]])+"\n")
