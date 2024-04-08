from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from .getData import isWorkOrderValid, getWorkOrderDetails, getTimeTicketsData
from LiveVersion4.functions import writeStatus,checkStaffStatus
from django.contrib import messages
from LiveVersion4.test import getListofAllOrders
from worderTracker.models import WorkOrderTracker
from worderTracker.models import Operation
from LiveVersion4.settings import cache
from homepage.functions import userInfo

global workOrders 
workOrders= getListofAllOrders()

INCOMINGLIST=['INC QC B4','INC QC']

def notEnoughPerm(requests):
    """
    -------------------------------------------------------
    View function for displaying a page indicating not enough 
    permissions. Renders 'verificationreq.html' template with 
    an error message.
    Use: notEnoughPerm(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response containing the rendered template (HttpResponse)
    -------------------------------------------------------
    """
    messages.error(requests,f'Verification Required!')
    return render(requests,'hp/verificationreq.html',{'title':'No No NO','sList':workOrders})



def operations(wo):
    """
    -------------------------------------------------------
    Helper function to determine the index of a work order 
    in the global workOrders list.
    Use: operations(wo)
    -------------------------------------------------------
    Parameters:
        wo - the work order number (string)
    Returns:
        Index of the work order in the workOrders list (int)
    -------------------------------------------------------
    """
    try:
        i = workOrders.index(wo)
        if i== len(workOrders)-1:
            i=-1
    except:
        i=1
    return i


def getData(jobNumber):
    """
    -------------------------------------------------------
    Helper function to get data associated with a specific 
    work order from the cache or the database.
    Use: getData(jobNumber)
    -------------------------------------------------------
    Parameters:
        jobNumber - the work order number (string)
    Returns:
        Dictionary containing data associated with the work order (dict)
    -------------------------------------------------------
    """

    WO = cache.contains(jobNumber)
    if  WO is None:
        WO = getWorkOrderDetails(jobNumber)
        cache.addtoStack(WO)

    onLive =False
    completed=0
    notes=None
    if(WorkOrderTracker.objects.filter(jobNumber=jobNumber).exists()):
        onLive =True
        fromModel = WorkOrderTracker.objects.get(jobNumber=jobNumber)
        WO.dueDate=fromModel.dueDate.strftime("%Y-%m-%d")
        if(fromModel.estimatedHours!=0):
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
    """
    -------------------------------------------------------
    View function for displaying the work order report page.
    Requires users to be authenticated. Retrieves data based 
    on the provided work order number, performs validation, 
    and renders the appropriate template.
    Use: workOrderReport(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response containing the rendered template (HttpResponse)
    -------------------------------------------------------
    """
    checkStaffStatus(requests)
    data={'sList':workOrders}
    if 'search-for-work-order' in requests.GET:
        workOrder = requests.GET.get('search-for-work-order')        
        if(isWorkOrderValid(workOrder)):
            data = getData(workOrder)
            writeStatus(f"1:Job Detial: {workOrder}:printed")
            userInfo(requests)
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
       
    userInfo(requests)
    return render(requests, 'workOrderReports/report.html', context=data)




def writeToTracker(dataObj):
    WO = WorkOrderTracker(jobNumber= dataObj.jobNumber,customer=dataObj.customer,dueDate = dataObj.dueDate,qty=dataObj.qty,shippingThisMonth=False,TA=dataObj.TA,incomingInspection=False,rush= False, estimatedHours= dataObj.totalEstimatedHours,completedHours=0,des=dataObj.des)
    WO.save()
    WO.incomingInspection =False
    for operation in dataObj.router:
        op=Operation(jobNumber=WO,workCenter = operation.workCenter,description= operation.des,estimatedHours= operation.estimatedHours, stepNumber=operation.stepNumber,status = 'pending')
        op.save()

        if WO.incomingInspection != True  and op.workCenter in INCOMINGLIST:
            WO.incomingInspection =True
    WO.save()

@login_required
def addToLive(requests):
    """
    -------------------------------------------------------
    View function for adding a work order to the live 
    version. Requires users to be authenticated. Retrieves 
    data from the cache and saves it to the database, then 
    redirects to the live version page.
    Use: addToLive(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response redirecting to the live version page (HttpResponseRedirect)
    -------------------------------------------------------
    """
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        dataObj = cache.contains(jobNumber)
        writeToTracker(dataObj)
        messages.info(requests,f'{jobNumber} Added To Live!')
        writeStatus(f"1:Job Detial: {jobNumber}:printed")
        userInfo(requests)  
        return redirect(f'/live/?search-for-work-order={jobNumber}')
    else:
        return HttpResponse("Invalid request method.")


@login_required
def removeFormLive(requests):
    """
    -------------------------------------------------------
    View function for removing a work order from the live 
    version. Requires users to be authenticated. Deletes 
    the specified work order from the database and redirects 
    to the live version page.
    Use: removeFormLive(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response redirecting to the live version page (HttpResponseRedirect)
    -------------------------------------------------------
    """
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        WorkOrderTracker(jobNumber=jobNumber).delete()
        messages.info(requests,f'{jobNumber} Removed From Live!')
        writeStatus(f"1:Job Detial: {jobNumber}:printed")
        userInfo(requests)  
        return redirect(f'/live/?search-for-work-order={jobNumber}')
    else:
        return HttpResponse("Invalid request method.")
    
@login_required    
def updateDate(requests):
    """
    -------------------------------------------------------
    View function for updating the due date of a work order. 
    Requires users to be authenticated. Retrieves the 
    specified work order from the database, updates its due 
    date, and redirects to the live version page.
    Use: updateDate(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response redirecting to the live version page (HttpResponseRedirect)
    -------------------------------------------------------
    """
    if requests.method == 'POST':
        jobNumber = requests.POST.get('jobNumber')
        dueDate = requests.POST.get('dueDate')
        fromModel =WorkOrderTracker.objects.get(jobNumber=jobNumber)
        fromModel.dueDate = dueDate
        fromModel.save()
        messages.info(requests,f'{jobNumber} Due Date Updated!')
        userInfo(requests)
        return redirect(f'/live/?search-for-work-order={jobNumber}')
    else:
        return HttpResponse("Invalid request method.")

   



def clockedIn(requests):
    """
    -------------------------------------------------------
    View function for displaying the clocked-in page.
    Renders 'clockedIn.html' template.
    Use: clockedIn(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response containing the rendered template (HttpResponse)
    -------------------------------------------------------
    """
    data={'sList':workOrders}
    messages.success(requests,f'the testing data, Does not accurately reflect the current status of clockind Employees')
    return render(requests, 'workOrderReports/clockedIn.html',context=data)



def incomingInspect(requests):
    data={'sList':workOrders,
          'workOrders':WorkOrderTracker.objects.filter(incomingInspection=True).order_by('dueDate').exclude(notes1 ='HOLD FOR CUSTOMER'),
          'title':'Orders For Incoming Inspection'}
    messages.success(requests,f'the testing data, Does not accurately reflect the current status of work orders')
    return render(requests, 'workOrderReports/incoming.html',context=data)



def timeTimeData(requests):
    info = getTimeTicketsData()
    print(len(info))

    data={
        'labels':list(info.keys()),
        'data': list(info.values()),
    }


    return render(requests, 'workOrderReports/chart.html',data)