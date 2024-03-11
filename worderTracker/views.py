from typing import Any
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from workOrderReports.views import workOrders
from LiveVersion4.test import getListofAllOrders
from workOrderReports.getData import getWorkOrderDetails
from django.views.generic import ListView
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
     for wo in WorkOrderTracker.objects.all():
          WORKORDERS.append(wo)
         
     return render(requests,'tracker/tracker.html',{'title':'Livesssss','WORKORDERS': WORKORDERS,'sList':workOrders})











@csrf_exempt  # Use this decorator if you want to disable CSRF protection for this view (for simplicity in this example)
def handle_json_data(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))

            json.dump(json_data,open('test.json','w',encoding='utf-8'),ensure_ascii=False, indent=4)
            # Process the JSON data as needed (e.g., save to the database)
            # Example: assuming you have a model named 'Person'
            # for data in json_data:
            #     Person.objects.create(name=data['Name'], age=data['Age'], city=data['City'])

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)












