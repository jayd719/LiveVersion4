class CacheStack:
    def __init__(self):
        self.data = []

        self.count = 0
        self.limit = 5
    

    def addtoStack(self, wo):
        if self.contains(wo) is None:
            self.data.append(wo)
            self.count+=1
            self.count > self.limit
            self.data.pop()


    def contains(self,WO):
        for wo in self.data:
            if wo.jobNumber == WO:
                return wo
        return None

