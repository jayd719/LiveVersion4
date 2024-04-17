from django.shortcuts import render
from .purchaseOrderItem import getPurchaseOrderData
from datetime import datetime, timedelta
from datetime import datetime
# Create your views here.

def purchaseOrderReports(requests):
    start = datetime.now()
    dateRa=[
    f'{datetime.now().date()}',
    f'{(datetime.now()-timedelta(days=90)).date()}'
    ]

    
    head,lineItems =getPurchaseOrderData(dateRa)
    data={'title':"Purchase Order Tracker" ,'lineItems':lineItems}
    print(datetime.now()-start) 
    return render(requests,'PO/index.html',data)