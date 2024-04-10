from django.shortcuts import render
from .purchaseOrderItem import getPurchaseOrderData
from datetime import datetime, timedelta
# Create your views here.

def purchaseOrderReports(requests):
    dateRa=[
    f'{datetime.now().date()}',
    f'{(datetime.now()-timedelta(days=90)).date()}'
    ]

    print(getPurchaseOrderData(dateRa))

    return render(requests,'PO/index.html',{'title':'thisiiiii'})