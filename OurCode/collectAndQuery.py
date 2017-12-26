import collect_Util as util

addresses = util.readAllAddresses("city_of_new_york.csv")

import random
addresses_sample = random.sample(addresses, 1000)

code = "X1-ZWz18w8ig7zggb_728x4"

results = util.queryAndExtractFeatures(addresses_sample, code)

results = util.parseData(results)

##Write to File
filename = "Sol_output.csv"
util.writeToFile(filename, results)
