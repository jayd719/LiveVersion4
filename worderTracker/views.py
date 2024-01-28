from django.shortcuts import render
from workOrderReports.views import workOrders
from LiveVersion4.test import getListofAllOrders
from workOrderReports.getData import getWorkOrderDetails
from django.views.generic import ListView
from .models import WorkOrderTracker
from datetime import datetime



def get_year_data(date):
     return 




def monthly_forcast(requests):
    
    workorders  =[]
    list1 = getListofAllOrders()
    for WO in list1[:1]:
         workorders.append(getWorkOrderDetails(WO))
         
         print(workorders)
    return render(requests,'tracker/tracker.html',{'title':'Live','WORKORDERS':workorders})


def lastFY(requests):
     return render(requests,'tracker/tracker.html',{'title':'Livesssss','sList':workOrders})



class LIVE(ListView):
     model = WorkOrderTracker
     template_name='tracker/tracker.html'
     context_object_name='WORKORDERS'