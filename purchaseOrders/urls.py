from django.urls import path
from .views import purchaseOrderReports

urlpatterns = [
    path('purchase-orders-reporting/',purchaseOrderReports,name='purchaseOrders-home'),
    
]
