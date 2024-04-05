from django.shortcuts import render,HttpResponse
from worderTracker.models import Operation
from django.contrib import messages
from django.http import JsonResponse
from django.views.static import serve
import json
import os

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
    return render(requests,'homepage.html',data)





def post_shd(requests):
    workC = requests.GET.get('shd-for-workCenter') 
    return render(requests,'schedules/shd-jobs.html',workC)


def download_shd(requests):
    if requests.method == 'POST':
        try:
            userData = json.loads(requests.body.decode('utf-8'))
            workCenter = userData['workCenter']
            # jobList = Operation.objects.filter(workCenter=workCenter,status='pending').order_by('jobNumber')
            print(workCenter)

            
            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)