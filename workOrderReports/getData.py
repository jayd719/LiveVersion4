from requests import get
from datetime import datetime
from workOO import WorkOrderFormated


        
def isWorkOrderValid(wo):
    isValid = False
    if len(wo) == 8 and wo[0:5].isnumeric() and wo[5] == '-' and wo[6:].isnumeric():
        isValid = True
    return isValid


TK = 'eyJraWQiOiJpelFuU21KYUdzMER2T05PSHNuMWVYK3NNOXdrSmh2dWt1UjFhR2VDTDZ3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4MTBjY2ZiMi1mNzYxLTQ0MjMtYjI2Mi1kMDBlYTk3NDg2NjgiLCJldmVudF9pZCI6IjYwYTU2N2E1LTE2MzktNDAwMS05NzI4LTljYTJlNjFiYWE5NCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MDYwMjU2MjgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX2RraFJabjBycCIsImV4cCI6MTcwNjAyOTIyOCwiaWF0IjoxNzA2MDI1NjI4LCJqdGkiOiJiZmEwZGQyNi1kMWFlLTQyYmMtYjEwZi0xMTZjNDE2MTU1YjEiLCJjbGllbnRfaWQiOiI3amN1MWNnaXVqb3Jidmc0c2d0NzVybjhjZCIsInVzZXJuYW1lIjoiMWYzLXl5NWgtZW9uZy00d3d6LTZmYmItMzUzMiJ9.R-DQRXaI662-wxQNJlKhrIXE7TcLS3LJLeXEPiZhvBgoyMn-a8aR0bFbvbHUypYdqtgEWyB23RfarCjLn2pQ5M5Av5JcHToIqCIMrCrlotwPq3Ix70TCUu2qQ8-eTQkzXi6Cf0hqDlz_uZt3iPP9Pj4prlrgfvHBFppPGlvVUeJlaqRVd8hTkc5xMhq5VfoAlgiGb6nb5SP1ldOcN6uk8U8bdOrIhJ2ZsQ0-sg_xnd9-sJXlo5wsn1lQRD4HRnU2lQKNmE-m_W51adUGjvv0ToRegrUMIfX0BvwdhjhaTyQpYilhAQpBNzxkggNOfDSXN2R-Iplh4OASPxJidxHPtw'


def getWorkOrderDetails(wo):
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TK}'}
    orderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/orders?orderNumber={wo[:5]}', headers=headers).json()["Data"][0]
    workOrderHeader = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?jobNumber={wo}', headers=headers).json()["Data"][0]
    router = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?fields=vendorCode%2CstepNumber%2Cstatus%2CworkCenter%2Cdescription%2CworkCenterOrVendor%2CtotalActualHours%2CtotalEstimatedHours&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    timeTicketsRaw = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/time-ticket-details?fields=ticketDate%2CemployeeCode%2CemployeeName%2CstepNumber%2CcycleTime&sort=stepNumber&jobNumber={wo}', headers=headers).json()['Data']
    workOrder = WorkOrderFormated(workOrderHeader, orderHeader, router, timeTicketsRaw)
    return workOrder

start = datetime.today()
a = getWorkOrderDetails('19301-01')
print(datetime.today() - start)

