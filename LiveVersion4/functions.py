from datetime import datetime

def writeStatus(operationPerformed):
    fh= open('actions.txt','a',encoding='utf-8')
    fh.write(f'{operationPerformed},{datetime.today()}\n')
    fh.close()
    return None


writeStatus('jj')