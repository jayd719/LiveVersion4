from django.shortcuts import render
from django.contrib import messages
from workOrderReports.views import workOrders

# Create your views here.
def home(requests):
    messages.success(requests,f'Signed In')
    return render(requests,'hp/home.html',{'sList':workOrders})