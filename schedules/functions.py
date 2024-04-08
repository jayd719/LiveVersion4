from openpyxl import load_workbook

def createExcelSheet(jobList,workCenter):
    wb = load_workbook('files\static\excel\Scheduling Format.xlsx')
    schedule = wb[wb.sheetnames[0]]

    startRow =2
    for workOrder in jobList:
        schedule[f'B{startRow}'] = workOrder.jobNumber.jobNumber
        schedule[f'C{startRow}'] = workOrder.jobNumber.qty
        schedule[f'E{startRow}'] = workOrder.workCenter
        schedule[f'F{startRow}'] = workOrder.stepNumber
        startRow+=1
    wb.save(f"files\static\excel\{workCenter}.xlsx")


