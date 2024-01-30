from requests import get,post
from datetime import datetime
from .workOO import WorkOrderFormated
from LiveVersion4.functions import TOKEN

from json import dump


        
def isWorkOrderValid(wo):
    isValid = False
    if len(wo) == 8 and wo[0:5].isnumeric() and wo[5] == '-' and wo[6:].isnumeric():
        isValid = True
    return isValid



def getWorkOrderDetails(wo):
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN()}'}
    orderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/orders?orderNumber={wo[:5]}', headers=headers).json()["Data"][0]
    workOrderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?jobNumber={wo}', headers=headers).json()["Data"][0]
    router = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?fields=vendorCode%2CstepNumber%2Cstatus%2CworkCenter%2Cdescription%2CworkCenterOrVendor%2CtotalActualHours%2CtotalEstimatedHours&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    timeTicketsRaw = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/time-ticket-details?fields=ticketDate%2CemployeeCode%2CemployeeName%2CstepNumber%2CcycleTime&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    
    # dump(workOrderHeader, open('../header.json','w',encoding='utf-8'))
    workOrder = WorkOrderFormated(workOrderHeader, orderHeader, router, timeTicketsRaw)
    return workOrder

# start = datetime.today()
# a = getWorkOrderDetails('19301-01')
# print(datetime.today() - start)

