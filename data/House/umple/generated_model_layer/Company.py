# %% NEW FILE Company BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 46 "model.ump"
# line 116 "model.ump"

class Company():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Company Attributes
    #Company Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAddress):
        self._jobLogs = None
        self._Address = None
        self._Name = None
        self._Name = aName
        self._Address = aAddress
        self._jobLogs = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        self._Name = aName
        wasSet = True
        return wasSet

    def setAddress(self, aAddress):
        wasSet = False
        self._Address = aAddress
        wasSet = True
        return wasSet

    def getName(self):
        return self._Name

    def getAddress(self):
        return self._Address

    # Code from template association_GetMany 
    def getJobLog(self, index):
        aJobLog = self._jobLogs[index]
        return aJobLog

    def getJobLogs(self):
        newJobLogs = tuple(self._jobLogs)
        return newJobLogs

    def numberOfJobLogs(self):
        number = len(self._jobLogs)
        return number

    def hasJobLogs(self):
        has = len(self._jobLogs) > 0
        return has

    def indexOfJobLog(self, aJobLog):
        index = (-1 if not aJobLog in self._jobLogs else self._jobLogs.index(aJobLog))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfJobLogs():
        return 0

    # Code from template association_AddManyToOne 
    def addJobLog1(self, aHours, aPrice, aHouse):
        from .JobLog import JobLog
        return JobLog(aHours, aPrice, aHouse, self)

    def addJobLog2(self, aJobLog):
        wasAdded = False
        if (aJobLog) in self._jobLogs :
            return False
        existingCompany = aJobLog.getCompany()
        isNewCompany = not (existingCompany is None) and not self == existingCompany
        if isNewCompany :
            aJobLog.setCompany(self)
        else :
            self._jobLogs.append(aJobLog)
        wasAdded = True
        return wasAdded

    def removeJobLog(self, aJobLog):
        wasRemoved = False
        #Unable to remove aJobLog, as it must always have a company
        if not self == aJobLog.getCompany() :
            self._jobLogs.remove(aJobLog)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addJobLogAt(self, aJobLog, index):
        wasAdded = False
        if self.addJobLog(aJobLog) :
            if index < 0 :
                index = 0
            if index > self.numberOfJobLogs() :
                index = self.numberOfJobLogs() - 1
            self._jobLogs.remove(aJobLog)
            self._jobLogs.insert(index, aJobLog)
            wasAdded = True
        return wasAdded

    def addOrMoveJobLogAt(self, aJobLog, index):
        wasAdded = False
        if (aJobLog) in self._jobLogs :
            if index < 0 :
                index = 0
            if index > self.numberOfJobLogs() :
                index = self.numberOfJobLogs() - 1
            self._jobLogs.remove(aJobLog)
            self._jobLogs.insert(index, aJobLog)
            wasAdded = True
        else :
            wasAdded = self.addJobLogAt(aJobLog, index)
        return wasAdded

    def delete(self):
        i = len(self._jobLogs)
        while i > 0 :
            aJobLog = self._jobLogs[i - 1]
            aJobLog.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "Name" + ":" + str(self.getName()) + "," + "Address" + ":" + str(self.getAddress()) + "]"

    def addJobLog(self, *argv):
        from .House import House
        from .JobLog import JobLog
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], (float, int)) and isinstance(argv[2], House) :
            return self.addJobLog1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], JobLog) :
            return self.addJobLog2(argv[0])
        raise TypeError("No method matches provided parameters")
