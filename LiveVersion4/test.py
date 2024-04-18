from .functions import TOKEN
from requests import get



def getListofAllOrders():
    print('Generating Master List')
    try:
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN()}'}
        r = get('https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-line-items?fields=jobNumber&sort=-dueDate&status=Open',headers=headers).json()['Data']
        number_list = []
        for wo in r:
            if wo['jobNumber'] is not None:
                number_list.append(wo['jobNumber'])
    except:
        number_list=['workOrder1','WorkOrder2','WorkOrder3','WorkOrder4','WorkOrder5','WorkOrder6','WorkOrder7','WorkOrder8','WorkOrder9']
    return sorted(number_list)



