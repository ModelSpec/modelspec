# %% NEW FILE Administration BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 7 "model.ump"
# line 250 "model.ump"

class Administration():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Administration Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._administrators = None
        self._administrators = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany
    def getAdministrator(self, index):
        aAdministrator = self._administrators[index]
        return aAdministrator

    def getAdministrators(self):
        newAdministrators = tuple(self._administrators)
        return newAdministrators

    def numberOfAdministrators(self):
        number = len(self._administrators)
        return number

    def hasAdministrators(self):
        has = len(self._administrators) > 0
        return has

    def indexOfAdministrator(self, aAdministrator):
        index = (-1 if not aAdministrator in self._administrators else self._administrators.index(aAdministrator))
        return index

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfAdministrators():
        return 0

    # Code from template association_AddManyToOne
    def addAdministrator1(self, aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess):
        from .Administrator import Administrator
        return Administrator(aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess, self)

    def addAdministrator2(self, aAdministrator):
        wasAdded = False
        if (aAdministrator) in self._administrators :
            return False
        existingAdministration = aAdministrator.getAdministration()
        isNewAdministration = not (existingAdministration is None) and not self == existingAdministration
        if isNewAdministration :
            aAdministrator.setAdministration(self)
        else :
            self._administrators.append(aAdministrator)
        wasAdded = True
        return wasAdded

    def removeAdministrator(self, aAdministrator):
        wasRemoved = False
        #Unable to remove aAdministrator, as it must always have a administration
        if not self == aAdministrator.getAdministration() :
            self._administrators.remove(aAdministrator)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addAdministratorAt(self, aAdministrator, index):
        wasAdded = False
        if self.addAdministrator(aAdministrator) :
            if index < 0 :
                index = 0
            if index > self.numberOfAdministrators() :
                index = self.numberOfAdministrators() - 1
            self._administrators.remove(aAdministrator)
            self._administrators.insert(index, aAdministrator)
            wasAdded = True
        return wasAdded

    def addOrMoveAdministratorAt(self, aAdministrator, index):
        wasAdded = False
        if (aAdministrator) in self._administrators :
            if index < 0 :
                index = 0
            if index > self.numberOfAdministrators() :
                index = self.numberOfAdministrators() - 1
            self._administrators.remove(aAdministrator)
            self._administrators.insert(index, aAdministrator)
            wasAdded = True
        else :
            wasAdded = self.addAdministratorAt(aAdministrator, index)
        return wasAdded

    def delete(self):

        while len(self._administrators) > 0 :
            aAdministrator = self._administrators[len(self._administrators) - 1]
            aAdministrator.delete()
            self._administrators.remove(aAdministrator)

    def addAdministrator(self, *argv):
        from .Administrator import Administrator
        from .UserAccess import UserAccess
        if len(argv) == 7 and isinstance(argv[0], int) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], str) and isinstance(argv[6], UserAccess) :
            return self.addAdministrator1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])
        if len(argv) == 1 and isinstance(argv[0], Administrator) :
            return self.addAdministrator2(argv[0])
        raise TypeError("No method matches provided parameters")
