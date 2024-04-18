from django.shortcuts import render
from .purchaseOrderItem import getPurchaseOrderData
from .purchaseOrderItem import processPO
from datetime import datetime, timedelta
from datetime import datetime
# Create your views here.

def purchaseOrderReports(requests):
    start = datetime.now()
    dateRa=[
    f'{(datetime.now()+timedelta(days=2)).date()}',
    f'{(datetime.now()-timedelta(days=90)).date()}'
    ]

    headerData,lineData = getPurchaseOrderData(dateRa)
    lineItems =processPO(headerData,lineData)
    data={'title':"Purchase Order Tracker" ,'lineItems':lineItems[3:]}
    print(datetime.now()-start) 
    return render(requests,'PO/index.html',data)