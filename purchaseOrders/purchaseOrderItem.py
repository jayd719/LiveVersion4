import requests
from LiveVersion4.functions import TOKEN

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
    limit =200
    skip=0
    while(limit>199):
        tempData = requests.get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/quotes?sort=-quoteNumber&dateEntered%5Bgt%5D={dateRange[1]}T00%3A00%3A00Z&dateEntered%5Blt%5D={dateRange[0]}T00%3A00%3A00Z&skip={skip}&take=200',headers=headers).json()["Data"]
        limit = len(tempData)
        print(limit)
        skip+=200
        data +=tempData
    return data



