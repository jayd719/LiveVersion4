def binarySearch(array, quoteNumber):
    l = len(array)
    i =0
    while(i<l):
        if(array[i]['quoteNumber']==quoteNumber):
            return array[i]
        i+=1
    return None
    