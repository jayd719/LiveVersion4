from django.db import models
from datetime import date

# Create your models here.

class WorkOrderTracker(models.Model):
    """
    -------------------------------------------------------
    Model representing a work order tracker.
    Fields:
        jobNumber - Unique identifier for the work order (CharField)
        customer - Name of the customer (CharField)
        des - Description of the work order (TextField)
        qty - Quantity of items for the work order (CharField)
        dueDate - Due date for the work order (DateField)
        shippingThisMonth - Indicates if the order is scheduled for shipping this month (BooleanField)
        TA - Technical Assistance code (CharField)
        notes1 - Additional notes for the work order (TextField)
        incomingInspection - Indicates if the work order requires incoming inspection (BooleanField)
        ME - Manufacturing Engineer assigned to the work order (CharField)
        rush - Indicates if the work order is marked as rush (BooleanField)
        notes2 - Additional notes for the work order (TextField)
        estimatedHours - Estimated hours for the work order (FloatField)
        completedHours - Completed hours for the work order (FloatField)
        ops - Operations for the work order (CharField)
        onHold - Indicates if the work order is on hold (BooleanField)
    Use: WorkOrderTracker
    -------------------------------------------------------
    """
    jobNumber =models.CharField(max_length=8,primary_key = True)
    customer = models.CharField(max_length=50)
    des = models.TextField(null=True)
    qty= models.CharField(max_length=5)
    dueDate = models.DateField()
    shippingThisMonth = models.BooleanField(blank=True,null=True)
    TA = models.CharField(max_length=5)
    notes1 = models.TextField(blank=True,null=True)
    incomingInspection = models.BooleanField(blank=True,null=True)
    ME = models.CharField(blank=True,max_length=2,null=True)
    rush = models.BooleanField(blank=True,null=True)
    notes2 = models.TextField(blank=True,null=True)
    estimatedHours = models.FloatField()
    completedHours = models.FloatField()
    ops = models.CharField(max_length=2,default='0')
    onHold=models.BooleanField(blank=True,default=False)



class Operation(models.Model):
    """
    -------------------------------------------------------
    Model representing an operation associated with a work order.
    Fields:
        jobNumber - Foreign key referencing the WorkOrderTracker model (ForeignKey)
        workCenter - Work center where the operation is carried out (CharField)
        description - Description of the operation (TextField)
        estimatedHours - Estimated hours required for the operation (CharField)
        status - Status of the operation (CharField)
        stepNumber - Step number of the operation (IntegerField)
        customNotes - Custom notes for the operation (TextField)
    Use: Operation
    -------------------------------------------------------
    """
    jobNumber= models.ForeignKey(WorkOrderTracker, on_delete=models.CASCADE)
    workCenter = models.CharField(max_length=25)
    description = models.TextField(null=True)
    estimatedHours = models.CharField(max_length=5)
    status = models.CharField(max_length=15)
    stepNumber = models.IntegerField()
    customNotes = models.TextField(blank=True,null=True)



class MEs(models.Model):
    """
    -------------------------------------------------------
    Model representing Manufacturing Engineers (MEs).
    Fields:
        name - Name of the ME (CharField, primary key)
        intials - Initials of the ME (CharField)
    Use: MEs
    -------------------------------------------------------
    """
    name=models.CharField(max_length=50,primary_key=True)
    intials = models.CharField(max_length=2)



class JobNotes(models.Model):
    """
    -------------------------------------------------------
    Model representing job notes or reason codes.
    Fields:
        reasonCode - Description of the reason code (TextField)
    Use: JobNotes
    -------------------------------------------------------
    """
    reasonCode = models.TextField()


class Machines(models.Model):
    """
    -------------------------------------------------------
    Model representing machines used in operations.
    Fields:
        machineCode - Code identifying the machine (CharField)
        machineName - Name of the machine (CharField)
    Use: Machines
    -------------------------------------------------------
    """
    machineCode = models.CharField(max_length=20)
    machineName= models.CharField(max_length = 100)




class CompltedOrders(models.Model):
    jobNumber =models.CharField(max_length=8,primary_key = True)
    customer = models.CharField(max_length=50)
    des = models.TextField()
    qty= models.CharField(max_length=5)
    dueDate = models.DateField()
    TA = models.CharField(max_length=5)
    estimatedHours = models.FloatField()
    actualHours = models.FloatField()
    completedDate = models.DateField(("Date"), auto_now_add=True)

class Dropped(models.Model):
    jobNumber =models.CharField(max_length=8,primary_key = True)
    