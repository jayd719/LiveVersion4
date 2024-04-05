from django.shortcuts import render,HttpResponse,HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from workOrderReports.views import workOrders
from LiveVersion4.test import getListofAllOrders
from workOrderReports.getData import getWorkOrderDetails
from workOrderReports.views import writeToTracker
from .models import WorkOrderTracker
from .models import Operation
from .models import MEs
from .models import JobNotes
from .models import Machines
from .models import Dropped
from .models import CompltedOrders
from django.contrib import messages
from django.http import JsonResponse
import json



class tempWO:
    """
    -------------------------------------------------------
    Temp Work Order Object used to create divider in CBB Live
    Use: tempWO(text)
    -------------------------------------------------------
    Parameters:
       text: Text of the splitter
    Returns:
        None
    -------------------------------------------------------
    """
    def __init__(self,month):
        self.jobNumber =2
        self.month =month

def updateShippingThisMonth(requests):
    """
    -------------------------------------------------------
    Updates the shipping status for a particular job. This 
    function handles POST requests.
    Use: updateShippingThisMonth(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response indicating the success or failure of the operation (HttpResponse)
    -------------------------------------------------------
    """
    
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



@login_required
def live(requests):
     """
        -------------------------------------------------------
        Creates the CBB Live view by fetching work orders, 
        organizing them by due date, and rendering the 
        'tracker.html' template.
        Use: live(request)
        -------------------------------------------------------
        Parameters:
            request - the HTTP request object (HttpRequest)
        Returns:
            HTTP response containing the rendered template (HttpResponse)
        -------------------------------------------------------
    """

     WORKORDERS=[]
     for wo in WorkOrderTracker.objects.filter(notes1='HOLD FOR CUSTOMER').order_by('dueDate'):
          wo.dueDate=wo.dueDate.strftime("%Y-%m-%d")
          wo.ops = Operation.objects.filter(jobNumber =wo.jobNumber)
          WORKORDERS.append(wo)
     WORKORDERS.append(1)
     currMonth=None
     for wo in WorkOrderTracker.objects.exclude(notes1 ='HOLD FOR CUSTOMER').order_by('dueDate'):
        wo.ops = Operation.objects.filter(jobNumber =wo.jobNumber)
        if(currMonth is None or wo.dueDate.strftime("%b")!=currMonth):
            WORKORDERS.append(tempWO(f'{wo.dueDate.strftime("%b").upper()}'))
        currMonth = wo.dueDate.strftime("%b")
        wo.dueDate=wo.dueDate.strftime("%Y-%m-%d")
        WORKORDERS.append(wo)         
     data= {'title':'CBB Live',
            'WORKORDERS': WORKORDERS,
            'sList':workOrders,
            'MEs':MEs.objects.all(),
            'jobNotes':JobNotes.objects.all()} 
     messages.success(requests,f'the testing data, Does not accurately reflect the current status of work orders')  
     return render(requests,'tracker/tracker.html',data)
 
 
@login_required
def writeBackToDatabase(request):
    """
    -------------------------------------------------------
    Writes back updates to the database based on the received 
    JSON data.
    Use: writeBackToDatabase(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        JSON response indicating the success or failure of the operation (JsonResponse)
    -------------------------------------------------------
    """
    if request.method == 'POST':
        try:
            userData = json.loads(request.body.decode('utf-8'))
            if userData['field']=='notes':
                updateNotes(userData)
            elif userData['field']=='stm':
                updateShipping(userData)
            elif userData['field']=='dueDate':
                updateDueDate(userData)
            elif userData['field']=='ME':
                updateME(userData)
            elif userData['field']=='inspection':
                updateInsp(userData)
            elif userData['field']=='operation':
                updateOperation(userData)
            elif userData['field']=='updateOperation':
                updateWorkCenter(userData)

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def updateNotes(userData):
    """
    -------------------------------------------------------
    Updates the notes for a particular work order.
    Use: updateNotes(userData)
    -------------------------------------------------------
    Parameters:
        userData - dictionary containing information about the update (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    WO.notes1=userData['data']
    if WO.notes1=='HOLD FOR CUSTOMER':
        WO.shippingThisMonth=False
    WO.save()

def updateShipping(userData):
    """
    -------------------------------------------------------
    Updates the shipping status for a particular work order.
    Use: updateShipping(userData)
    -------------------------------------------------------
    Parameters:
        userData - dictionary containing information about the update (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    if userData['data']== 'true':
         WO.shippingThisMonth = True
    else:
        WO.shippingThisMonth=False
    WO.save()

def updateDueDate(userData):
    """
    -------------------------------------------------------
    Updates the due date for a particular work order.
    Use: updateDueDate(userData)
    -------------------------------------------------------
    Parameters:
        userData - dictionary containing information about the update (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    WO.dueDate=userData['data']
    WO.save()
    
def updateME(userData):
    """
    -------------------------------------------------------
    Updates the Manufacturing Engineer (ME) for a particular 
    work order.
    Use: updateME(userData)
    -------------------------------------------------------
    Parameters:
        userData - dictionary containing information about the update (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    WO.ME=userData['data']
    WO.save()

def updateInsp(userData):
    """
    -------------------------------------------------------
    Updates the inspection status for a particular work order.
    Use: updateInsp(userData)
    -------------------------------------------------------
    Parameters:
        userData - dictionary containing information about the update (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    if userData['data']== 'true':
         WO.incomingInspection = True
    else:
        WO.incomingInspection=False
    WO.save()

def updateOperation(userData):
    """
    -------------------------------------------------------
    Updates the operation status for a particular work order.
    Use: updateOperation(userData)
    -------------------------------------------------------
    Parameters:
        userData - dictionary containing information about the update (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    WO.completedHours=userData['comp']
    WO.save()
    OP = Operation.objects.get(jobNumber=userData['workOrder'],stepNumber=userData['op'])
    OP.status=userData['data']
    OP.save()

def updateWorkCenter(userData):
    """
    -------------------------------------------------------
    Updates the work center for a particular operation.
    Use: updateWorkCenter(userData)
    -------------------------------------------------------
    Parameters:
        userData - dictionary containing information about the update (dict)
    Returns:
        None
    -------------------------------------------------------
    """
    OP = Operation.objects.get(jobNumber=userData['workOrder'],stepNumber=userData['op'])
    OP.workCenter=userData['data']
    # OP.description=userData['des']
    OP.save()

def getWorkOrderDes(requests):

    if 'work-order' in requests.GET:
        workOrder = requests.GET.get('work-order')
        op = requests.GET.get('op')
        print('res')
        # /?shd-for-workCenter=ACUGRO
    json_data = {
            'list': 1
        }
    return JsonResponse(json_data)


def get_machineList(request):
    li = []
    for machine in Machines.objects.all():
        li.append(machine.machineName)
    json_data = {
        'list': li
    }
    return JsonResponse(json_data)
def monthly_forcast(requests):
    workorders  =[]
    list1 = getListofAllOrders()
    for WO in list1[:1]:
         workorders.append(getWorkOrderDetails(WO))
         print(workorders)
    return render(requests,'tracker/tracker.html',{'title':'Live','WORKORDERS':workorders})


def fetchNewOrders(requests):
     acknowledgedOrders =WorkOrderTracker.objects.values_list('jobNumber', flat=True).union(CompltedOrders.objects.values_list('jobNumber', flat=True),Dropped.objects.values_list('jobNumber', flat=True))
     newOrders  = [value for value in getListofAllOrders() if value  not in acknowledgedOrders]
     for newWorkOrder in newOrders[:10]:
         writeToTracker(getWorkOrderDetails(newWorkOrder))
         print(f'\tAdded:\t{newWorkOrder}')
     return redirect(f'/work-order-tracker/')

def testinh(requests):
    
     return render(requests,'tracker/this.html',{'title':'testing','sList':None})
