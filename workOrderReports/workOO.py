
from datetime import datetime


class WorkOrder:
    """
    -------------------------------------------------------
    Class representing a work order.
    Stores information about customer, PO number, TA, currency
    code, job number, description, status, unit price, unit,
    quantity ordered, quantity for stock, foreign unit price,
    total estimated hours, total actual hours, due date, 
    quantity, router, and create time.
    -------------------------------------------------------
    Attributes:
        customer: Customer (string)
        PO: PO number (string)
        TA: TA (string)
        currencyCode: Currency code (string)
        jobNumber: Job number (string)
        des: Description (string)
        status: Status (string)
        unitPrice: Unit price (float)
        unit: Unit (string)
        qtyOrdered: Quantity ordered (int)
        qtyForStock: Quantity for stock (int)
        forcur: Foreign unit price (string)
        totalEstimatedHours: Total estimated hours (float)
        totalActualHours: Total actual hours (float)
        dueDate: Due date (datetime)
        qty: Quantity (string)
        router: List of operations (list)
        createTime: Create time (datetime)
    -------------------------------------------------------
    """

    
    class Opertaion:
        """
        -------------------------------------------------------
        Class representing a work order operation.
        Stores information about work center, status, step number,
        estimated hours, actual hours, description, and time 
        tickets.
        -------------------------------------------------------
        Attributes:
            workCenter: Work center (string)
            status: Status (string)
            stepNumber: Step number (int)
            estimatedHours: Estimated hours (float)
            actualHours: Actual hours (float)
            des: Description (string)
            timeTickets: List of time tickets (list)
            displayTicket1: Display format for ticket employee codes (string)
            displayTicket2: Display format for ticket employee names (string)
            displayTicket3: Display format for ticket dates (string)
            displayTicket4: Display format for ticket cycle times (string)
        -------------------------------------------------------
        """
        def __init__(self, dataSetOne, tickets):
            self.workCenter = dataSetOne['workCenter']
            if self.workCenter is None:
                self.workCenter = dataSetOne['vendorCode']

            self.status = dataSetOne['status']
            self.stepNumber = dataSetOne['stepNumber']
            self.estimatedHours = round(float(dataSetOne['totalEstimatedHours']),2)
            self.actualHours = round(float(dataSetOne['totalActualHours']),2)
            self.des = dataSetOne['description']
            self.timeTickets = tickets

            self.displayTicket1 = ''
            self.displayTicket2 = ''
            self.displayTicket3 = ''
            self.displayTicket4 = ''

    class TimeTicket:
        """
        -------------------------------------------------------
        Class representing a work order operation time ticket.
        Stores information about employee code, name, cycle 
        time, and ticket date.
        -------------------------------------------------------
        Attributes:
            empCode: Employee code (string)
            empName: Employee name (string)
            cycleTime: Cycle time (float)
            date: Ticket date (string)
        -------------------------------------------------------
        """
        def __convertDate(self, x):
            x = (x.split('T')[0]).split('-')
            return datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%d-%B-%Y")

        def __init__(self, f):
            self.empCode = f['employeeCode']
            self.empName = f['employeeName']
            self.cycleTime = f['cycleTime']
            self.date = self.__convertDate(f['ticketDate'])
            
            if self.cycleTime is None:
                self.cycleTime =0

        def htmlTag(self):
            return f'{self.empCode:4d}  {self.empName:25s}  {round(self.cycleTime,2):5f}    {self.date}\n'
        
        
        

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
        self.totalActualHours =0
        self.dueDate = self.__convertDate(lineHeader['dueDate'])
        self.qty = ''
        self.router = self.createRouter(router, self.processTickets(rawTickets))

        self.__updateQty()

        self.createTime = datetime.today()
    
    def __updateQty(self):
        self.qty = f'{self.qtyOrdered}'
        if self.qtyForStock > 0:
            self.qty = f'{self.qtyOrdered}+{self.qtyForStock}'
            
    def __convertDate(self, x):
        x = (x.split('T')[0]).split('-')
        return datetime(int(x[0]), int(x[1]), int(x[2]))

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
    """
    -------------------------------------------------------
    Class representing a formatted work order.
    Inherits from the WorkOrder class and adds additional 
    attributes and methods for formatting and processing 
    data for display.
    -------------------------------------------------------
    Attributes:
        qoutedList: List of estimated hours for each operation (list)
        actualList: List of actual hours for each operation (list)
        actualColors: List of colors for actual hours visualization (list)
        operationList: List of operation step numbers (list)
        label: Label color for status (string)
        completedHours: Total completed hours (float)
        dueIn: Due in days (int)
        daysStat: Status based on due in days (string)
    -------------------------------------------------------
    Methods:
        daystat(days): Determines the status based on due in days (string)
    -------------------------------------------------------
    """

    def daystat(self,days):
        status = 'ontime'
        if days < 7:
            status='critical'
        if days< 0:
            status='late'
        return status

    def __init__(self, lineHeader, woHeader, router, rawTickets):
        super().__init__(lineHeader, woHeader, router, rawTickets)

        tags={'NOTPRINTED':'primary',
              'CRICTIAL':'warning'}


        self.qoutedList = []
        self.actualList = []
        self.actualColors = []
        self.operationList =[]

        self.label='warning'

        self.completedHours = 0

        self.dueIn =''
        self.daysStat =''
        if self.status =='Open':
            self.dueIn = (self.dueDate - datetime.today()).days
            self.daysStat = self.daystat(self.dueIn)
            
        self.dueDate = self.dueDate.strftime("%Y-%m-%d")

        for operation in self.router:
            self.actualList.append(operation.actualHours)
            self.qoutedList.append(operation.estimatedHours)
            self.operationList.append(operation.stepNumber)

            self.totalActualHours+=operation.actualHours
            if operation.actualHours > operation.estimatedHours:
                self.actualColors.append(f'rgba{(151,187,205,0.5)}')
            else:
                self.actualColors.append(f'rgba{(255,0,0,0.5)}')


            if operation.status == 'Finished':
                self.completedHours +=operation.estimatedHours
            
            for ticket in operation.timeTickets:
                operation.displayTicket1 += str(ticket.empCode)+'\n'
                operation.displayTicket2 += ticket.empName+'\n'
                operation.displayTicket3 += ticket.date+'\n'
                operation.displayTicket4 += str(round(ticket.cycleTime,2))+'\n'

        self.totalActualHours = round(self.totalActualHours,2)
        self.totalEstimatedHours = round(self.totalEstimatedHours,2)

