from django.shortcuts import render

def monthly_forcast(requests):
    return render(requests,'tracker/tracker.html',{'title':'cn'})
