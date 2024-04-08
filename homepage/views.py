from django.shortcuts import render, redirect
from django.contrib import messages
from workOrderReports.views import workOrders
from django.contrib.auth.decorators import login_required
from LiveVersion4.test import getListofAllOrders
from .functions import userInfo

@login_required
def home(requests):
    """
    -------------------------------------------------------
    View function for the home page. Requires users to be 
    authenticated. Displays a greeting message for the logged-
    in user and renders the 'home.html' template.
    Use: home(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response containing the rendered template (HttpResponse)
    -------------------------------------------------------
    """
    messages.success(requests,f'Hello {requests.user.first_name}!  ')
    userInfo(requests)
    return render(requests,'hp/home.html',{'sList':workOrders})


@login_required
def update(requests):
    """
    -------------------------------------------------------
    View function for updating data. Requires users to be 
    authenticated. Retrieves a list of all orders, displays 
    a success message, and renders the 'home.html' template 
    with the updated list of orders.
    Use: update(request)
    -------------------------------------------------------
    Parameters:
        request - the HTTP request object (HttpRequest)
    Returns:
        HTTP response containing the rendered template (HttpResponse)
    -------------------------------------------------------
    """
    workOrders=getListofAllOrders()
    messages.success(requests,f'Update Successful!')
    return render(requests,'hp/home.html',{'sList':workOrders})