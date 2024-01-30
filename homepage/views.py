from django.shortcuts import render, redirect
from django.contrib import messages
from workOrderReports.views import workOrders
from django.contrib.auth.decorators import login_required
from LiveVersion4.test import getListofAllOrders

# Create your views here.
@login_required
def home(requests):
    messages.success(requests,f'Hello {requests.user.first_name}!  ')
    return render(requests,'hp/home.html',{'sList':workOrders})



def update(requests):
    workOrders
    workOrders=getListofAllOrders()
    messages.success(requests,f'Update Successful!')
    return render(requests,'hp/home.html',{'sList':workOrders})