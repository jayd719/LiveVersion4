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



def operations(wo):
    try:
        i = workOrders.index(wo)
        if i== len(workOrders)-1:
            i=-1
    except:
        i=1
    return i


def getData(jobNumber):
    WO = cache.contains(jobNumber)
    if  WO is None:
        WO = getWorkOrderDetails(jobNumber)
        cache.addtoStack(WO)

    onLive =False
    if(WorkOrderTracker.objects.filter(jobNumber=jobNumber).exists()):
        onLive =True
        fromModel = WorkOrderTracker.objects.get(jobNumber=jobNumber)
        WO.dueDate=fromModel.dueDate.strftime("%Y-%m-%d")
    
    i = operations(jobNumber)
    data = {'title':jobNumber,
            'workOrder':WO,
            'next':workOrders[i+1],
            'prev':workOrders[i-1],
            'sList':workOrders,
            'onLive':onLive}
    return data



@login_required
def workOrderReport(requests):
    data={'sList':workOrders}
    if 'search-for-work-order' in requests.GET:
        workOrder = requests.GET.get('search-for-work-order')        
        if(isWorkOrderValid(workOrder)):
            data = getData(workOrder)
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

        dataObj = cache.contains(jobNumber)
        WO = WorkOrderTracker(jobNumber= dataObj.jobNumber,dueDate = dataObj.dueDate)
        WO.save()
        messages.info(requests,f'{jobNumber} Added To Live!')
        data = getData(jobNumber)
        writeStatus(f"1:Job Detial: {jobNumber}:printed")  
        return redirect(f'/live/?search-for-work-order={jobNumber}')
    else:
        return HttpResponse("Invalid request method.")


@login_required
def removeFormLive(requests):
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        WorkOrderTracker(jobNumber=jobNumber).delete()
        messages.info(requests,f'{jobNumber} Removed From Live!')
        data = getData(jobNumber)
        writeStatus(f"1:Job Detial: {jobNumber}:printed")  
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

   
