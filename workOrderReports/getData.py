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


TK='eyJraWQiOiJpelFuU21KYUdzMER2T05PSHNuMWVYK3NNOXdrSmh2dWt1UjFhR2VDTDZ3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4MTBjY2ZiMi1mNzYxLTQ0MjMtYjI2Mi1kMDBlYTk3NDg2NjgiLCJldmVudF9pZCI6IjQzZjk3MGMzLWE2MGUtNGE1Yi1hMjZmLTk4MzIwYzI5MjJhZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MDU4NjkzNzcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX2RraFJabjBycCIsImV4cCI6MTcwNTg3Mjk3NywiaWF0IjoxNzA1ODY5Mzc3LCJqdGkiOiJjYTA2MjRiOC0xZGZkLTQyMmQtYmYwNC02N2IxNzNmMjUyMTYiLCJjbGllbnRfaWQiOiI3amN1MWNnaXVqb3Jidmc0c2d0NzVybjhjZCIsInVzZXJuYW1lIjoiMWYzLXl5NWgtZW9uZy00d3d6LTZmYmItMzUzMiJ9.NGnRQEtCqcV6bFceR2rQ-jdFOrrw7-1Xn_RVaJVmsp9AjlcFqYTN3rLtTYylel48zsbdKEeTr7jjRetEhVWR8a5Kmm-nMYwHxc_k-bUIf9f2lTx2nFQeQH_zic9SovCQnawCet0-6Nh6URIvTkfHj1yhUuDGpOMhvWB_JmH26hqImev3776MCwkrME_RWAc1GmfUTJZ-efbd1sHGX1qxjy7rpd-iUYHeg-RuxLqMzsMGfBdcllQ0ahvXeTapvB2-Y2kpydujQ8uwPbnpyZtfmiYTYc1lxh3ihdkfIkRNCf9RRraQxRrYERco0-qiuIbP6zXY4Lx6VnXckUu-cXHiTA'


def getWorkOrderDetails(wo):
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TK}'}
    orderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/orders?orderNumber={wo[:5]}',headers=headers).json()["Data"][0]
    workOrderHeader=get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?jobNumber={wo}',headers=headers).json()["Data"][0]
    # print(workOrderHeader)
    
    # router= get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?sort=stepNumber&jobNumber={wo}',headers=headers).json()['Data']
    workOrder = WorkOrder(workOrderHeader,orderHeader)
    return workOrder

# getWorkOrderDetails('19301-01')