from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .getData import isWorkOrderValid, getWorkOrderDetails


@login_required
def workOrderReport(requests):
    data={}
    if 'search-for-work-order' in requests.GET:
        workOrder = requests.GET.get('search-for-work-order')
        
        if(isWorkOrderValid(workOrder)):
            data = {'title':workOrder,
                    'workOrder':getWorkOrderDetails(workOrder)}
            return render(requests, 'workOrderReports/reportdata.html', context=data)
        
        else:
            data ={'message':f'{workOrder} is Not a Valid Work Order Number',}

    return render(requests, 'workOrderReports/report.html', context=data)




    
    
   
