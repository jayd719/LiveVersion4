from typing import Any
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from workOrderReports.views import workOrders
from LiveVersion4.test import getListofAllOrders
from workOrderReports.getData import getWorkOrderDetails
from .models import WorkOrderTracker,Operation
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json






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
     for wo in WorkOrderTracker.objects.all().order_by('dueDate'):
          WORKORDERS.append(wo)
         
     return render(requests,'tracker/tracker.html',{'title':'Livesssss','WORKORDERS': WORKORDERS,'sList':workOrders})








def updateNotes(userData):
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    WO.notes1=userData['data']
    WO.save()

def updateShipping(userData):
    WO = WorkOrderTracker.objects.get(jobNumber=userData['workOrder'])
    print(userData['data'])
    if userData['data']== 'true':
         WO.shippingThisMonth = True
    else:
        WO.shippingThisMonth=False
    WO.save()





def writeBackToDatabase(request):
    if request.method == 'POST':
        try:
            userData = json.loads(request.body.decode('utf-8'))

            if userData['field']=='notes':
                updateNotes(userData)
            elif userData['field']=='stm':
                updateShipping(userData)

            # print(userData)
            # print(type(userData))


            
            

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)












