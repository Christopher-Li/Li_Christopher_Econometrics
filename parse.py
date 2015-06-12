import csv, collections

# DOCUMENTATION
# ========================================
# parse - takes a filename and returns information and all the data in array of arrays
#

def parse(filename):
    # initialize variables
    array = []
    csvfile = open(filename,'rb')
    fileToRead = csv.reader(csvfile, delimiter=' ',quotechar=',')

    # iterate through rows of actual data
    for row in fileToRead:
        # change each line of data into an array
        temp =row[0].split(',')
        for i in range(len(temp)):
            # data preprocessing
            if temp[i] == '.':
                temp[i] = None

        array.append(temp)

    names = array.pop(0)
    dictionary = {}
    for index,val in enumerate(names):
        dictionary[val.lower()] = index


    return dictionary, array