from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from workOrderReports.views import workOrders
from LiveVersion4.test import getListofAllOrders
from workOrderReports.getData import getWorkOrderDetails
from .models import WorkOrderTracker
from .models import Operation
from .models import MEs
from .models import JobNotes
from django.contrib import messages
from django.http import JsonResponse
import json



class tempWO:
    def __init__(self,month):
        self.jobNumber =2
        self.month =month


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
     for wo in WorkOrderTracker.objects.filter(notes1='HOLD FOR CUSTOMER').order_by('dueDate'):
          wo.dueDate=wo.dueDate.strftime("%Y-%m-%d")
          wo.ops = Operation.objects.filter(jobNumber =wo.jobNumber)
          WORKORDERS.append(wo)

     WORKORDERS.append(1)
     
     currMonth=None
     for wo in WorkOrderTracker.objects.exclude(notes1 ='HOLD FOR CUSTOMER').order_by('dueDate'):
        wo.ops = Operation.objects.filter(jobNumber =wo.jobNumber)

        if(currMonth is None or wo.dueDate.strftime("%b")!=currMonth):
            WORKORDERS.append(tempWO(f'{wo.dueDate.strftime("%b")}'))

        currMonth = wo.dueDate.strftime("%b")

        wo.dueDate=wo.dueDate.strftime("%Y-%m-%d")
        WORKORDERS.append(wo)
    
         
     data= {'title':'CBB Live',
            'WORKORDERS': WORKORDERS,
            'sList':workOrders,
            'MEs':MEs.objects.all(),
            'jobNotes':JobNotes.objects.all()}   
     return render(requests,'tracker/tracker.html',data)








def updateNotes(userData):
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    WO.notes1=userData['data']
    WO.save()

def updateShipping(userData):
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    if userData['data']== 'true':
         WO.shippingThisMonth = True
    else:
        WO.shippingThisMonth=False
    WO.save()

def updateDueDate(userData):
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    WO.dueDate=userData['data']
    WO.save()
    





def writeBackToDatabase(request):
    if request.method == 'POST':
        try:
            userData = json.loads(request.body.decode('utf-8'))

            if userData['field']=='notes':
                updateNotes(userData)
            elif userData['field']=='stm':
                updateShipping(userData)
            elif userData['field']=='dueDate':
                updateDueDate(userData)
                

            


            
            

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)












