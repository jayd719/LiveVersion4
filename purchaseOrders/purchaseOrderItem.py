import requests
from LiveVersion4.functions import TOKEN
from Datastructures.BinarySearch import binarySearch



class PurchaseOrderItem():
    def __init__(self):
        self.inquiryNumber =1
        self.qouteNumber = 1
        self.sentDate =1
        self.customer =1
        self.qouteAmount =1
        self.currency =1
        self.salesID =1
        self.remark = None
        self.followUpDate =1
        self.nextFollowUpdate =None
        self.status = 1
        self.oppStatus = 1




def getPurchaseOrderData(dateRange):
    print(dateRange)
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN()}'}
    data=[]
    limit,skip =200,0
    while(limit>199):
        tempData = requests.get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/quotes?sort=-quoteNumber&dateEntered%5Bgt%5D={dateRange[1]}T00%3A00%3A00Z&dateEntered%5Blt%5D={dateRange[0]}T00%3A00%3A00Z&skip={skip}&take=200',headers=headers).json()["Data"]
        limit = len(tempData)
        # print(limit)
        skip+=200
        data +=tempData
    
    lastElement = data[-1]['quoteNumber']
    print(f'LAST ELM: {lastElement}')
    checkElement = lastElement
    lineItems = []
    skip=0
    while(checkElement>=lastElement):
        tempData = requests.get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/quote-line-items?sort=-quoteNumber&skip={skip}&take=200',headers=headers).json()["Data"]
        lineItems+=tempData
        # print(len(tempData))
        skip+=200
        checkElement = tempData[-1]['quoteNumber']
        print(checkElement)
  
    return data,lineItems




def processPO(headerData,lineData):
    for PO in lineData:
       tempData = binarySearch(headerData,PO['quoteNumber'])
       if tempData is not None:
           PO.update(tempData)
    return lineData
