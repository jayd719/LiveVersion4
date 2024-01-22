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


TK='eyJraWQiOiJpelFuU21KYUdzMER2T05PSHNuMWVYK3NNOXdrSmh2dWt1UjFhR2VDTDZ3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4MTBjY2ZiMi1mNzYxLTQ0MjMtYjI2Mi1kMDBlYTk3NDg2NjgiLCJldmVudF9pZCI6ImFiNDE1ODUwLWU3MjYtNGQyZC1iZjYzLTgyMWNjYjU3MDdlYyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MDU4Nzc1NDUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX2RraFJabjBycCIsImV4cCI6MTcwNTg4MTE0NSwiaWF0IjoxNzA1ODc3NTQ1LCJqdGkiOiI0NDZhMjM2OC01YzNiLTQ5NWMtOGRhYy02ZGFkZGRjMzczMjAiLCJjbGllbnRfaWQiOiI3amN1MWNnaXVqb3Jidmc0c2d0NzVybjhjZCIsInVzZXJuYW1lIjoiMWYzLXl5NWgtZW9uZy00d3d6LTZmYmItMzUzMiJ9.e0EM_e5kfDMDB2ComRrZk1FNXeOwmE8lSU3fgU7j3qEgWFte_faNxJXxyrtmhLmlcfol-rxJjSzExMqHasSU9Nr29oMhn5KOu5QzlVm3swwZHbpfw0loskzMTDoZIDWvMUMCHZe9BbPtCFks5mMs_5TOKC5-YXk_FM8IAcvLNM0JLHp5PYmCXABPUUgrJe0mu3X1Tthg2fiCOfACpe3Mdkq3YokRXGrmT-VSyeuP0X3YGczAkvJGuRiBl0D_sE8Rt5OBEYo1S8m7UD7oN0pIry7C8ACVqA9twdCt2zsseriZIeuILb2C3bDLZRQLeSZ7EL3XrtGHUesgj32kF2XtrA'


def getWorkOrderDetails(wo):
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TK}'}
    orderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/orders?orderNumber={wo[:5]}',headers=headers).json()["Data"][0]
    workOrderHeader=get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?jobNumber={wo}',headers=headers).json()["Data"][0]
    # print(workOrderHeader)
    
    # router= get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?sort=stepNumber&jobNumber={wo}',headers=headers).json()['Data']
    workOrder = WorkOrder(workOrderHeader,orderHeader)
    return workOrder

# getWorkOrderDetails('19301-01')