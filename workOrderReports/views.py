from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .getData import isWorkOrderValid, getWorkOrderDetails
from LiveVersion4.functions import writeStatus
from django.contrib import messages

@login_required
def workOrderReport(requests):
    data={}
    if 'search-for-work-order' in requests.GET:
        workOrder = requests.GET.get('search-for-work-order')
        
        if(isWorkOrderValid(workOrder)):
            data = {'title':workOrder,
                    'workOrder':getWorkOrderDetails(workOrder)}
            writeStatus(f"1:Job Detial: {workOrder}:printed")  
            return render(requests, 'workOrderReports/reportdata.html', context=data)
        
        else:
            data ={'message':'null'}
            messages.warning(requests,f'{workOrder} Is Not A Valid Number!')

    writeStatus("0:Job Detial: Invalid WO")    
    return render(requests, 'workOrderReports/report.html', context=data)




    
    
   
