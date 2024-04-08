from openpyxl import load_workbook
from LiveVersion4.settings import BASE_DIR
import os

def createExcelSheet(jobList,workCenter):
    wb = load_workbook(os.path.join(BASE_DIR,'files','static','shd','Scheduling Format.xlsx'))
    schedule = wb[wb.sheetnames[0]]
    startRow =2
    for workOrder in jobList:
        schedule[f'B{startRow}'] = workOrder.jobNumber.jobNumber
        schedule[f'C{startRow}'] = workOrder.jobNumber.qty
        schedule[f'E{startRow}'] = workOrder.workCenter
        schedule[f'F{startRow}'] = workOrder.stepNumber
        startRow+=1
    wb.save(os.path.join(BASE_DIR,'files','static','excel',f'{workCenter}.xlsx'))


