# %% NEW FILE AdminViewModel BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 80 "model.ump"
# line 212 "model.ump"

class AdminViewModel():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #AdminViewModel Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAdminDashboardActivity):
        self._adminDashboardActivity = None
        self._userAccounts = None
        self._userAccounts = []
        didAddAdminDashboardActivity = self.setAdminDashboardActivity(aAdminDashboardActivity)
        if not didAddAdminDashboardActivity :
            raise RuntimeError ("Unable to create adminViewModel due to adminDashboardActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getUserAccount(self, index):
        aUserAccount = self._userAccounts[index]
        return aUserAccount

    def getUserAccounts(self):
        newUserAccounts = tuple(self._userAccounts)
        return newUserAccounts

    def numberOfUserAccounts(self):
        number = len(self._userAccounts)
        return number

    def hasUserAccounts(self):
        has = len(self._userAccounts) > 0
        return has

    def indexOfUserAccount(self, aUserAccount):
        index = (-1 if not aUserAccount in self._userAccounts else self._userAccounts.index(aUserAccount))
        return index

    # Code from template association_GetOne 
    def getAdminDashboardActivity(self):
        return self._adminDashboardActivity

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfUserAccounts():
        return 0

    # Code from template association_AddManyToOne 
    def addUserAccount1(self, aUserID, aFirstName, aLastName, aUsername, aEmail, aPhoneNumber, aRole):
        from .UserAccount import UserAccount
        return UserAccount(aUserID, aFirstName, aLastName, aUsername, aEmail, aPhoneNumber, aRole, self)

    def addUserAccount2(self, aUserAccount):
        wasAdded = False
        if (aUserAccount) in self._userAccounts :
            return False
        existingAdminViewModel = aUserAccount.getAdminViewModel()
        isNewAdminViewModel = not (existingAdminViewModel is None) and not self == existingAdminViewModel
        if isNewAdminViewModel :
            aUserAccount.setAdminViewModel(self)
        else :
            self._userAccounts.append(aUserAccount)
        wasAdded = True
        return wasAdded

    def removeUserAccount(self, aUserAccount):
        wasRemoved = False
        #Unable to remove aUserAccount, as it must always have a adminViewModel
        if not self == aUserAccount.getAdminViewModel() :
            self._userAccounts.remove(aUserAccount)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addUserAccountAt(self, aUserAccount, index):
        wasAdded = False
        if self.addUserAccount(aUserAccount) :
            if index < 0 :
                index = 0
            if index > self.numberOfUserAccounts() :
                index = self.numberOfUserAccounts() - 1
            self._userAccounts.remove(aUserAccount)
            self._userAccounts.insert(index, aUserAccount)
            wasAdded = True
        return wasAdded

    def addOrMoveUserAccountAt(self, aUserAccount, index):
        wasAdded = False
        if (aUserAccount) in self._userAccounts :
            if index < 0 :
                index = 0
            if index > self.numberOfUserAccounts() :
                index = self.numberOfUserAccounts() - 1
            self._userAccounts.remove(aUserAccount)
            self._userAccounts.insert(index, aUserAccount)
            wasAdded = True
        else :
            wasAdded = self.addUserAccountAt(aUserAccount, index)
        return wasAdded

    # Code from template association_SetOneToOptionalOne 
    def setAdminDashboardActivity(self, aNewAdminDashboardActivity):
        wasSet = False
        if aNewAdminDashboardActivity is None :
            #Unable to setAdminDashboardActivity to null, as adminViewModel must always be associated to a adminDashboardActivity
            return wasSet
        existingAdminViewModel = aNewAdminDashboardActivity.getAdminViewModel()
        if not (existingAdminViewModel is None) and not self == existingAdminViewModel :
            #Unable to setAdminDashboardActivity, the current adminDashboardActivity already has a adminViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldAdminDashboardActivity = self._adminDashboardActivity
        self._adminDashboardActivity = aNewAdminDashboardActivity
        self._adminDashboardActivity.setAdminViewModel(self)
        if not (anOldAdminDashboardActivity is None) :
            anOldAdminDashboardActivity.setAdminViewModel(None)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._userAccounts)
        while i > 0 :
            aUserAccount = self._userAccounts[i - 1]
            aUserAccount.delete()
            i -= 1

        existingAdminDashboardActivity = self._adminDashboardActivity
        self._adminDashboardActivity = None
        if not (existingAdminDashboardActivity is None) :
            existingAdminDashboardActivity.setAdminViewModel(None)

    def addUserAccount(self, *argv):
        from .UserAccount import UserAccount
        from .Role import Role
        if len(argv) == 7 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], str) and isinstance(argv[6], Role) :
            return self.addUserAccount1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])
        if len(argv) == 1 and isinstance(argv[0], UserAccount) :
            return self.addUserAccount2(argv[0])
        raise TypeError("No method matches provided parameters")
