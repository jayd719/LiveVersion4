wo = '19355-01'
from requests import get
from datetime import datetime

now = datetime.now()
TOKEN=""
headers = {'accept': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
router = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/order-routings?sort=stepNumber&jobNumber={wo}', headers=headers)
print(router)
# timeTickets = get(f'https://api-jb2.integrations.ecimanufacturing.com:443/api/v1/time-ticket-details?sort=stepNumber&jobNumber={wo}', headers=headers)
# print(timeTickets.json())

print(datetime.now()-now)