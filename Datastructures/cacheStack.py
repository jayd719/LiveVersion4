from datetime import datetime
class CacheStack:
    def __init__(self):
        self.data = []

        self.count = 0
        self.limit = 5
    

    def addtoStack(self, wo):
        self.data.insert(0,wo)
        self.count+=1

        if self.count > self.limit:
            self.data.pop()
            self.count -=1


    def contains(self,WO):
        for wo in self.data:
            if wo.jobNumber == WO:
                if  (datetime.today()- wo.createTime).seconds<500:
                    return wo
        return None

