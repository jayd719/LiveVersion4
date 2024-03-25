from requests import get,post
from datetime import datetime, date,timedelta
from .workOO import WorkOrderFormated
from LiveVersion4.functions import TOKEN

from json import dump


        
def isWorkOrderValid(wo):
    """
    -------------------------------------------------------
    Checks if a work order number is valid.
    A valid work order number must be 8 characters long,
    with the first five characters being numeric, followed
    by a hyphen, and the last two characters being numeric.
    -------------------------------------------------------
    Parameters:
        wo: Work order number to validate (string)
    Returns:
        isValid: True if the work order number is valid, False otherwise (bool)
    -------------------------------------------------------
    """
    isValid = False
    if len(wo) == 8 and wo[0:5].isnumeric() and wo[5] == '-' and wo[6:].isnumeric():
        isValid = True
    return isValid



def getWorkOrderDetails(wo):
    """
    -------------------------------------------------------
    Retrieves details of a work order from an external API.
    Makes API calls to retrieve information about the work 
    order header, order routing, and time tickets.
    Returns a formatted WorkOrderFormated object containing
    the retrieved data.
    -------------------------------------------------------
    Parameters:
        wo: Work order number to retrieve details for (string)
    Returns:
        workOrder: Formatted work order object with retrieved details (WorkOrderFormated)
    -------------------------------------------------------
    """
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN()}'}
    orderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/orders?orderNumber={wo[:5]}', headers=headers).json()["Data"][0]
    workOrderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?jobNumber={wo}', headers=headers).json()["Data"][0]
    router = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?fields=vendorCode%2CstepNumber%2Cstatus%2CworkCenter%2Cdescription%2CworkCenterOrVendor%2CtotalActualHours%2CtotalEstimatedHours&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    timeTicketsRaw = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/time-ticket-details?fields=ticketDate%2CemployeeCode%2CemployeeName%2CstepNumber%2CcycleTime&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    workOrder = WorkOrderFormated(workOrderHeader, orderHeader, router, timeTicketsRaw)
    return workOrder



def getTimeTicketsData():
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN()}'}
    timeDelta_ =date.today()-timedelta(days=30)
    l=200
    data=[]
    skip=0
    while(l>199):
        url=f"https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/time-tickets?sort=-ticketDate&ticketDate%5Bgt%5D={timeDelta_}T12%3A19%3A27.0000000%2B00%3A00&skip={skip}&take=200"
        timeTicketData=get(url, headers=headers).json()["Data"]
        data=data+timeTicketData
        skip+=200
        l=len(timeTicketData)


    daySlit={}
    for item in data:
        value = item['ticketDate'].split("T")[0]
        if value in daySlit:
            daySlit[value]+=1
        else:
         daySlit[value]=1
    print(daySlit)     
    return daySlit

