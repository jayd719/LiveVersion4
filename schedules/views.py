from django.shortcuts import render,HttpResponse
from worderTracker.models import Operation
from django.contrib import messages
def shd_home(requests):
    workCenters=Operation.objects.values_list('workCenter', flat=True).order_by('workCenter').distinct()

    workCenter=None
    jobList = None
    if 'shd-for-workCenter' in requests.GET:
        workCenter = requests.GET.get('shd-for-workCenter')
        jobList = Operation.objects.filter(workCenter=workCenter,status='pending').order_by('jobNumber')
    data={
        'workCenters':workCenters,
        'workCenter':workCenter,
        'jobList':jobList
    }
    messages.success(requests,f'the testing data, Does not accurately reflect the current status of work orders')
    return render(requests,'homepage.html',data)





def post_shd(requests):
    workC = requests.GET.get('shd-for-workCenter') 
    return render(requests,'schedules/shd-jobs.html',workC)

# Create your views here.