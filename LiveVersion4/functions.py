from datetime import datetime
from requests import post

from .settings import TK,TK_WRIGHT,KEY




def writeStatus(operationPerformed):
    fh= open('actions.txt','a',encoding='utf-8')
    fh.write(f'{operationPerformed},{datetime.today()}\n')
    fh.close()
    return None


def TOKEN():
    global TK
    global TK_WRIGHT
    if (datetime.today() - (TK_WRIGHT)).seconds > 3500:
        header = {'content-type': 'application/x-www-form-urlencoded', 'accept': 'text/plain'}
        TK = post('https://api-user.integrations.ecimanufacturing.com:443/oauth2/api-user/token', data=open(KEY,'r',encoding='utf-8').read(), headers=header).json()['access_token']
        TK_WRIGHT=datetime.today()
        print('Token Regenetated')
    return TK