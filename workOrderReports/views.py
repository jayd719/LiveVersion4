from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#19301-01
def isWorkOrderValid(wo):
    isValid = False
    if len(wo)==8 and wo[0:5].isnumeric() and wo[5]=='-' and wo[6:].isnumeric():
        isValid=True
    return isValid



@login_required
def workOrderReport(requests):
    data={}
    

    if 'search-for-work-order' in requests.GET:
        workOrder = requests.GET.get('search-for-work-order')
        
        if(isWorkOrderValid(workOrder)):
            data = {'title':workOrder,
                    'workOrder':workOrder}
        else:
            data ={'message':f'{workOrder} is Not a Valid Work Order Number',}

    return render(requests, 'workOrderReports/report.html', context=data)




    
    
   
