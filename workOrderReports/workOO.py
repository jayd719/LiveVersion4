
from datetime import datetime


class WorkOrder:
    
    class Opertaion:

        def __init__(self, dataSetOne, tickets):
            self.workCenter = dataSetOne['workCenter']
            if self.workCenter is None:
                self.workCenter = dataSetOne['vendorCode']

            self.status = dataSetOne['status']
            self.stepNumber = dataSetOne['stepNumber']
            self.estimatedHours = dataSetOne['totalEstimatedHours']
            self.actualHours = dataSetOne['totalActualHours']
            self.des = dataSetOne['description']
            self.timeTickets = tickets

            self.displayTicket = ''

    class TimeTicket:

        def __init__(self, f):
            self.empCode = f['employeeCode']
            self.empName = f['employeeName']
            self.cycleTime = f['cycleTime']
            self.date = f['ticketDate']

        def htmlTag(self):
            return f'<pre>{self.empCode}    {self.empName} {self.cycleTime}{self.date}<pre>'

    def __init__(self, lineHeader, woHeader, router, rawTickets):
        
        self.customer = woHeader['customerDescription']
        self.PO = woHeader['PONumber']
        self.TA = woHeader['salesID']
        self.currencyCode = woHeader['currencyCode']
        
        self.jobNumber = lineHeader['jobNumber']
        self.des = lineHeader['partDescription']
        self.status = lineHeader['status']
        self.unitPrice = lineHeader['unitPrice']
        self.unit = lineHeader['pricingUnit']
        self.qtyOrdered = lineHeader['quantityOrdered']
        self.qtyForStock = lineHeader['quantityToStock']
        self.forcur = lineHeader['unitPriceForeign']
        self.totalEstimatedHours = lineHeader['totalEstimatedHours']
        self.dueDate = self.__convertDate(lineHeader['dueDate'])
        self.qty = ''
        
        self.router = self.createRouter(router, self.processTickets(rawTickets))

        self.__updateQty()
    
    def __updateQty(self):
        self.qty = f'{self.qtyOrdered}'
        if self.qtyForStock > 0:
            self.qty = f'{self.qtyOrdered}+{self.qtyForStock}'
            
    def __convertDate(self, x):
        x = (x.split('T')[0]).split('-')
        return datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%d-%B-%Y")

    def createRouter(self, router, tickets):
        newRouter = []
        for each in router:
            if each['stepNumber'] in tickets:
                newRouter.append(self.Opertaion(each, tickets[each['stepNumber']]))
            else:
                newRouter.append(self.Opertaion(each, []))
        return newRouter

    def processTickets(self, tickets):
        ticketsSorted = {}
        for ticket in tickets:
            if ticket['stepNumber'] in ticketsSorted:
                ticketsSorted[ticket['stepNumber']].append(self.TimeTicket(ticket))
            else:
                ticketsSorted[ticket['stepNumber']] = []
                ticketsSorted[ticket['stepNumber']].append(self.TimeTicket(ticket))
        return ticketsSorted


class WorkOrderFormated(WorkOrder):

    def __init__(self, lineHeader, woHeader, router, rawTickets):
        super().__init__(lineHeader, woHeader, router, rawTickets)

        self.qoutedList = []
        self.actualList = []
        self.actualColors = []

        for operation in self.router:
            self.actualList.append(operation.actualHours)
            self.qoutedList.append(operation.estimatedHours)

            if operation.actualHours > operation.estimatedHours:
                self.actualColors.append('red')
            else:
                self.actualColors.append('green')
            
            for ticket in operation.timeTickets:
                operation.displayTicket += ticket.htmlTag()
