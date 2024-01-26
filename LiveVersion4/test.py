from .functions import TOKEN
from requests import get



def getListofAllOrders():
    print('Generating Master List')
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN()}'}
    r = get('https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?fields=jobNumber&sort=-dueDate&status=Open',headers=headers).json()['Data']
    number_list = []
    for wo in r:
        if wo['jobNumber'] is not None:
            number_list.append(str(wo['jobNumber']))
    return sorted(number_list)

def listString(numberList):
    template= open('workOrderReports\static\workOrderReports\AutocompleteTemp.js','r',encoding='utf-8').read()
    new =''
    for each in numberList:
        new+=f'"{each}",'
    new+=f'"{each}"'
    open('workOrderReports\static\workOrderReports\Autocomplete.js','w',encoding='utf-8').write(template.replace("*LIST*",new))
    return new


