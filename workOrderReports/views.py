from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .getData import isWorkOrderValid, getWorkOrderDetails
from LiveVersion4.functions import writeStatus
from django.contrib import messages
from LiveVersion4.test import getListofAllOrders
from worderTracker.models import WorkOrderTracker

from LiveVersion4.settings import cache

global workOrders 
workOrders= getListofAllOrders()





@login_required
def workOrderReport(requests):
    data={'sList':workOrders}
    if 'search-for-work-order' in requests.GET:
        workOrder = requests.GET.get('search-for-work-order')        
        if(isWorkOrderValid(workOrder)):
            try:
                i = workOrders.index(workOrder)
                if i== len(workOrders)-1:
                    i=-1
            except:
                i=1

            WO =getWorkOrderDetails(workOrder)
            onLive=False
            if(WorkOrderTracker.objects.filter(jobNumber=workOrder).exists()):
                onLive =True
                fromModel = WorkOrderTracker.objects.get(jobNumber=workOrder)
                WO.dueDate=fromModel.dueDate.strftime("%Y-%m-%d")

            data = {'title':workOrder,
                    'workOrder':WO,
                    'next':workOrders[i+1],
                    'prev':workOrders[i-1],
                    'sList':workOrders,
                    'onLive':onLive}
            
            cache.addtoStack(WO)

            writeStatus(f"1:Job Detial: {workOrder}:printed")  
            return render(requests, 'workOrderReports/reportdata.html', context=data)
        

        elif(len(workOrder)==0):
            data ={'message':'Blank Value',
                   'sList':workOrders}
            messages.info(requests,f'Job Number Cannot Be Blank!')


        else:
            data ={'message':'Invalid Work Order',
                   'sList':workOrders}
            messages.warning(requests,f'{workOrder} Is Not A Valid Number!')
            writeStatus("0:Job Detial: Invalid WO")    

    return render(requests, 'workOrderReports/report.html', context=data)


@login_required
def addToLive(requests):
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        # WO = WorkOrderTracker(cache.contains(jobNumber))
        # WO.save()
        messages.info(requests,f'{jobNumber} Added To Live!')
        return redirect(f'/live/?search-for-work-order={jobNumber}')
    else:
        return HttpResponse("Invalid request method.")


@login_required
def removeFormLive(requests):
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        WorkOrderTracker(jobNumber=jobNumber).delete()
        messages.info(requests,f'{jobNumber} Removed From Live!')
        return redirect(f'/live/?search-for-work-order={jobNumber}')
    else:
        return HttpResponse("Invalid request method.")
    
@login_required    
def updateDate(requests):
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        dueDate = requests.POST.get('dueDate')
        fromModel =WorkOrderTracker.objects.get(jobNumber=jobNumber)
        fromModel.dueDate = dueDate
        fromModel.save()
        messages.info(requests,f'{jobNumber} Due Date Updated!')
        return redirect(f'/live/?search-for-work-order={jobNumber}')
    else:
        return HttpResponse("Invalid request method.")

   
