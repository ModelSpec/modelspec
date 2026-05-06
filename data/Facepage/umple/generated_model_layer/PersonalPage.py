# %% NEW FILE PersonalPage BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 37 "model.ump"
# line 112 "model.ump"
from .Page import Page

class PersonalPage(Page):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #PersonalPage Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aPageName, aVisits, aFacepage, aPersonalAccount):
        self._personalAccount = None
        self._privileges = None
        super().__init__(aPageName, aVisits, aFacepage)
        self._privileges = []
        didAddPersonalAccount = self.setPersonalAccount(aPersonalAccount)
        if not didAddPersonalAccount :
            raise RuntimeError ("Unable to create administrator due to personalAccount. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getPrivilege(self, index):
        aPrivilege = self._privileges[index]
        return aPrivilege

    def getPrivileges(self):
        newPrivileges = tuple(self._privileges)
        return newPrivileges

    def numberOfPrivileges(self):
        number = len(self._privileges)
        return number

    def hasPrivileges(self):
        has = len(self._privileges) > 0
        return has

    def indexOfPrivilege(self, aPrivilege):
        index = (-1 if not aPrivilege in self._privileges else self._privileges.index(aPrivilege))
        return index

    # Code from template association_GetOne 
    def getPersonalAccount(self):
        return self._personalAccount

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfPrivileges():
        return 0

    # Code from template association_AddManyToOne 
    def addPrivilege1(self, aTypeOfPrivilege, aPersonalAccount):
        from .Privilege import Privilege
        return Privilege(aTypeOfPrivilege, aPersonalAccount, self)

    def addPrivilege2(self, aPrivilege):
        wasAdded = False
        if (aPrivilege) in self._privileges :
            return False
        existingPersonalPage = aPrivilege.getPersonalPage()
        isNewPersonalPage = not (existingPersonalPage is None) and not self == existingPersonalPage
        if isNewPersonalPage :
            aPrivilege.setPersonalPage(self)
        else :
            self._privileges.append(aPrivilege)
        wasAdded = True
        return wasAdded

    def removePrivilege(self, aPrivilege):
        wasRemoved = False
        #Unable to remove aPrivilege, as it must always have a personalPage
        if not self == aPrivilege.getPersonalPage() :
            self._privileges.remove(aPrivilege)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addPrivilegeAt(self, aPrivilege, index):
        wasAdded = False
        if self.addPrivilege(aPrivilege) :
            if index < 0 :
                index = 0
            if index > self.numberOfPrivileges() :
                index = self.numberOfPrivileges() - 1
            self._privileges.remove(aPrivilege)
            self._privileges.insert(index, aPrivilege)
            wasAdded = True
        return wasAdded

    def addOrMovePrivilegeAt(self, aPrivilege, index):
        wasAdded = False
        if (aPrivilege) in self._privileges :
            if index < 0 :
                index = 0
            if index > self.numberOfPrivileges() :
                index = self.numberOfPrivileges() - 1
            self._privileges.remove(aPrivilege)
            self._privileges.insert(index, aPrivilege)
            wasAdded = True
        else :
            wasAdded = self.addPrivilegeAt(aPrivilege, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setPersonalAccount(self, aPersonalAccount):
        wasSet = False
        if aPersonalAccount is None :
            return wasSet
        existingPersonalAccount = self._personalAccount
        self._personalAccount = aPersonalAccount
        if not (existingPersonalAccount is None) and not existingPersonalAccount == aPersonalAccount :
            existingPersonalAccount.removeAdministrator(self)
        self._personalAccount.addAdministrator(self)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._privileges)
        while i > 0 :
            aPrivilege = self._privileges[i - 1]
            aPrivilege.delete()
            i -= 1

        placeholderPersonalAccount = self._personalAccount
        self._personalAccount = None
        if not (placeholderPersonalAccount is None) :
            placeholderPersonalAccount.removeAdministrator(self)
        super().delete()

    def addPrivilege(self, *argv):
        from .PersonalAccount import PersonalAccount
        from .Privilege import Privilege
        if len(argv) == 2 and isinstance(argv[0], str) and isinstance(argv[1], PersonalAccount) :
            return self.addPrivilege1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Privilege) :
            return self.addPrivilege2(argv[0])
        raise TypeError("No method matches provided parameters")
