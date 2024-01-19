from django.shortcuts import render


def check_work_order_number():
    pass

def workOrderReport(requests):
    
    workOrder = requests.GET.get('workOrderBar')
    



    data = {'title':workOrder}

    return render(requests, 'workOrderReports/report.html', context=data)




    
    
   
