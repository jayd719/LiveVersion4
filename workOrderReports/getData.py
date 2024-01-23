from requests import get,post
from datetime import datetime
from .workOO import WorkOrderFormated


        
def isWorkOrderValid(wo):
    isValid = False
    if len(wo) == 8 and wo[0:5].isnumeric() and wo[5] == '-' and wo[6:].isnumeric():
        isValid = True
    return isValid



def getWorkOrderDetails(wo):
    
    TOKENFILE = open('../hh1.txt', 'r', encoding='utf-8').read().split('\n')
    if (datetime.today() - datetime.strptime(TOKENFILE[0], '%m/%d/%y %H:%M:%S')).seconds > 3550:
        payload= open('../hh.txt','r',encoding='utf-8').read()
        header = {'content-type': 'application/x-www-form-urlencoded', 'accept': 'text/plain'}
        TK = post('https://api-user.integrations.ecimanufacturing.com:443/oauth2/api-user/token', data=payload, headers=header).json()['access_token']
        fh = open('../hh1.txt', 'w', encoding='utf-8')
        fh.write(f"{datetime.today().strftime('%m/%d/%y %H:%M:%S')}\n{TK}")
        print('Token Regenetated')
        
    else:
        TK = TOKENFILE[1]

    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TK}'}
    orderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/orders?orderNumber={wo[:5]}', headers=headers).json()["Data"][0]
    workOrderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?jobNumber={wo}', headers=headers).json()["Data"][0]
    router = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?fields=vendorCode%2CstepNumber%2Cstatus%2CworkCenter%2Cdescription%2CworkCenterOrVendor%2CtotalActualHours%2CtotalEstimatedHours&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    timeTicketsRaw = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/time-ticket-details?fields=ticketDate%2CemployeeCode%2CemployeeName%2CstepNumber%2CcycleTime&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    workOrder = WorkOrderFormated(workOrderHeader, orderHeader, router, timeTicketsRaw)
    return workOrder

# start = datetime.today()
# a = getWorkOrderDetails('19301-01')
# print(datetime.today() - start)

