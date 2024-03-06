from typing import Any
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from workOrderReports.views import workOrders
from LiveVersion4.test import getListofAllOrders
from workOrderReports.getData import getWorkOrderDetails
from django.views.generic import ListView
from .models import WorkOrderTracker,Operation
from django.contrib import messages







def monthly_forcast(requests):
    
    workorders  =[]
    list1 = getListofAllOrders()
    for WO in list1[:1]:
         workorders.append(getWorkOrderDetails(WO))
         
         print(workorders)
    return render(requests,'tracker/tracker.html',{'title':'Live','WORKORDERS':workorders})


def lastFY(requests):
     return render(requests,'tracker/tracker.html',{'title':'Livesssss','sList':workOrders})



# update shipping this month
def updateShippingThisMonth(requests):
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        shipping = requests.POST.get('shippingThisMonth')
        JobData =WorkOrderTracker.objects.get(jobNumber=jobNumber)

        if shipping:
            JobData.shippingThisMonth = True
            messages.info(requests,f'{jobNumber} Will be Shipped This Month!')
        else:
             JobData.shippingThisMonth = False
             messages.info(requests,f'{jobNumber} Will Not Shipped This Month!')

        JobData.save()  
        
        return HttpResponseRedirect(requests.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("Invalid request method.")

def live(requests):
     WORKORDERS=[]
     for wo in WorkOrderTracker.objects.all():
          WORKORDERS.append(wo)
         
          


     return render(requests,'tracker/tracker.html',{'title':'Livesssss','WORKORDERS': WORKORDERS,'sList':workOrders})


