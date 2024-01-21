from requests import get
from datetime import datetime

class WorkOrder:
    def __init__(self,d,l):
        
        self.customer = l['customerDescription']
        self.PO = l['PONumber']
        self.TA = l['salesID']
        self.currencyCode = l['currencyCode']
        
        self.jobNumber =d['jobNumber']
        self.des = d['partDescription']
        self.status = d['status']
        self.unitPrice = d['unitPrice']
        self.unit= d['pricingUnit']
        self.qtyOrdered = d['quantityOrdered']
        self.qtyForStock = d['quantityToStock']
        self.forcur = d['unitPriceForeign']
        self.dueDate = self.__convertDate(d['dueDate'])
        self.qty=''

        self.__updateQty()
    
    def __updateQty(self):
        self.qty=f'{self.qtyOrdered}'
        if self.qtyForStock>0:
            self.qty=f'{self.qtyOrdered}+{self.qtyForStock}'
            
    def __convertDate(self, x):
        x = (x.split('T')[0]).split('-')
        return datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%d-%B-%Y")
        
def isWorkOrderValid(wo):
    isValid = False
    if len(wo)==8 and wo[0:5].isnumeric() and wo[5]=='-' and wo[6:].isnumeric():
        isValid=True
    return isValid


TK=''


def getWorkOrderDetails(wo):
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TK}'}
    orderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/orders?orderNumber={wo[:5]}',headers=headers).json()["Data"][0]
    workOrderHeader=get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?jobNumber={wo}',headers=headers).json()["Data"][0]
    # print(workOrderHeader)
    
    # router= get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?sort=stepNumber&jobNumber={wo}',headers=headers).json()['Data']
    workOrder = WorkOrder(workOrderHeader,orderHeader)
    return workOrder

# getWorkOrderDetails('19301-01')