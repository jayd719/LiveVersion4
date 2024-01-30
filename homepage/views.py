from django.shortcuts import render
from django.contrib import messages
from workOrderReports.views import workOrders
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(requests):
    messages.success(requests,f'Signed In')
    return render(requests,'hp/home.html',{'sList':workOrders})