from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from .getData import isWorkOrderValid, getWorkOrderDetails
from LiveVersion4.functions import writeStatus,checkStaffStatus
from django.contrib import messages
from LiveVersion4.test import getListofAllOrders
from worderTracker.models import WorkOrderTracker
from worderTracker.models import Operation
from LiveVersion4.settings import cache

global workOrders 
workOrders= getListofAllOrders()

INCOMINGLIST=['INC QC B4','INC QC']

def notEnoughPerm(requests):
    messages.error(requests,f'Verification Required!')
    return render(requests,'hp/verificationreq.html',{'title':'No No NO','sList':workOrders})

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
    completed=None
    notes=None
    if(WorkOrderTracker.objects.filter(jobNumber=jobNumber).exists()):
        onLive =True
        fromModel = WorkOrderTracker.objects.get(jobNumber=jobNumber)
        WO.dueDate=fromModel.dueDate.strftime("%Y-%m-%d")
        completed=round((fromModel.completedHours/fromModel.estimatedHours)*100,2)
        notes= fromModel.notes1
    
    i = operations(jobNumber)
    data = {'title':jobNumber,
            'workOrder':WO,
            'next':workOrders[i+1],
            'prev':workOrders[i-1],
            'sList':workOrders,
            'onLive':onLive,
            'completed':completed,
            'notes':notes}
    return data



@login_required
def workOrderReport(requests):
    checkStaffStatus(requests)
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
        WO = WorkOrderTracker(jobNumber= dataObj.jobNumber,customer=dataObj.customer,dueDate = dataObj.dueDate,qty=dataObj.qty,shippingThisMonth=False,TA=dataObj.TA,incomingInspection=False,rush= False, estimatedHours= dataObj.totalEstimatedHours,completedHours=0,des=dataObj.des)
        WO.save()

        WO.incomingInspection =False
        for operation in dataObj.router:
            op=Operation(jobNumber=WO,workCenter = operation.workCenter,description= operation.des,estimatedHours= operation.estimatedHours, stepNumber=operation.stepNumber,status = 'pending')
            op.save()

            if WO.incomingInspection != True  and op.workCenter in INCOMINGLIST:
                WO.incomingInspection =True
        
        WO.save()
        messages.info(requests,f'{jobNumber} Added To Live!')
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

   



def clockedIn(requests):
    data={'sList':workOrders}
    return render(requests, 'workOrderReports/clockedIn.html',context=data)