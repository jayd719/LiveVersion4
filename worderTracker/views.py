from django.shortcuts import render
from workOrderReports.views import workOrders

def monthly_forcast(requests):
    return render(requests,'tracker/tracker.html',{'title':'Live','sList':workOrders})
