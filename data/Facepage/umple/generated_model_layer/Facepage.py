# %% NEW FILE Facepage BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 2 "model.ump"
# line 77 "model.ump"
from datetime import date
class Facepage():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Facepage Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._pages = None
        self._accounts = None
        self._users = None
        self._users = []
        self._accounts = []
        self._pages = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getUser(self, index):
        aUser = self._users[index]
        return aUser

    def getUsers(self):
        newUsers = tuple(self._users)
        return newUsers

    def numberOfUsers(self):
        number = len(self._users)
        return number

    def hasUsers(self):
        has = len(self._users) > 0
        return has

    def indexOfUser(self, aUser):
        index = (-1 if not aUser in self._users else self._users.index(aUser))
        return index

    # Code from template association_GetMany 
    def getAccount(self, index):
        aAccount = self._accounts[index]
        return aAccount

    def getAccounts(self):
        newAccounts = tuple(self._accounts)
        return newAccounts

    def numberOfAccounts(self):
        number = len(self._accounts)
        return number

    def hasAccounts(self):
        has = len(self._accounts) > 0
        return has

    def indexOfAccount(self, aAccount):
        index = (-1 if not aAccount in self._accounts else self._accounts.index(aAccount))
        return index

    # Code from template association_GetMany 
    def getPage(self, index):
        aPage = self._pages[index]
        return aPage

    def getPages(self):
        newPages = tuple(self._pages)
        return newPages

    def numberOfPages(self):
        number = len(self._pages)
        return number

    def hasPages(self):
        has = len(self._pages) > 0
        return has

    def indexOfPage(self, aPage):
        index = (-1 if not aPage in self._pages else self._pages.index(aPage))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfUsers():
        return 0

    # Code from template association_AddManyToOne 
    def addUser1(self, aUserID, aName, aEmail, aBirthDate):
        from .User import User
        return User(aUserID, aName, aEmail, aBirthDate, self)

    def addUser2(self, aUser):
        wasAdded = False
        if (aUser) in self._users :
            return False
        existingFacepage = aUser.getFacepage()
        isNewFacepage = not (existingFacepage is None) and not self == existingFacepage
        if isNewFacepage :
            aUser.setFacepage(self)
        else :
            self._users.append(aUser)
        wasAdded = True
        return wasAdded

    def removeUser(self, aUser):
        wasRemoved = False
        #Unable to remove aUser, as it must always have a facepage
        if not self == aUser.getFacepage() :
            self._users.remove(aUser)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addUserAt(self, aUser, index):
        wasAdded = False
        if self.addUser(aUser) :
            if index < 0 :
                index = 0
            if index > self.numberOfUsers() :
                index = self.numberOfUsers() - 1
            self._users.remove(aUser)
            self._users.insert(index, aUser)
            wasAdded = True
        return wasAdded

    def addOrMoveUserAt(self, aUser, index):
        wasAdded = False
        if (aUser) in self._users :
            if index < 0 :
                index = 0
            if index > self.numberOfUsers() :
                index = self.numberOfUsers() - 1
            self._users.remove(aUser)
            self._users.insert(index, aUser)
            wasAdded = True
        else :
            wasAdded = self.addUserAt(aUser, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfAccounts():
        return 0

    # Code from template association_AddManyToOne 
    def addAccount(self, aAccount):
        wasAdded = False
        if (aAccount) in self._accounts :
            return False
        existingFacepage = aAccount.getFacepage()
        isNewFacepage = not (existingFacepage is None) and not self == existingFacepage
        if isNewFacepage :
            aAccount.setFacepage(self)
        else :
            self._accounts.append(aAccount)
        wasAdded = True
        return wasAdded

    def removeAccount(self, aAccount):
        wasRemoved = False
        #Unable to remove aAccount, as it must always have a facepage
        if not self == aAccount.getFacepage() :
            self._accounts.remove(aAccount)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addAccountAt(self, aAccount, index):
        wasAdded = False
        if self.addAccount(aAccount) :
            if index < 0 :
                index = 0
            if index > self.numberOfAccounts() :
                index = self.numberOfAccounts() - 1
            self._accounts.remove(aAccount)
            self._accounts.insert(index, aAccount)
            wasAdded = True
        return wasAdded

    def addOrMoveAccountAt(self, aAccount, index):
        wasAdded = False
        if (aAccount) in self._accounts :
            if index < 0 :
                index = 0
            if index > self.numberOfAccounts() :
                index = self.numberOfAccounts() - 1
            self._accounts.remove(aAccount)
            self._accounts.insert(index, aAccount)
            wasAdded = True
        else :
            wasAdded = self.addAccountAt(aAccount, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfPages():
        return 0

    # Code from template association_AddManyToOne 
    def addPage(self, aPage):
        wasAdded = False
        if (aPage) in self._pages :
            return False
        existingFacepage = aPage.getFacepage()
        isNewFacepage = not (existingFacepage is None) and not self == existingFacepage
        if isNewFacepage :
            aPage.setFacepage(self)
        else :
            self._pages.append(aPage)
        wasAdded = True
        return wasAdded

    def removePage(self, aPage):
        wasRemoved = False
        #Unable to remove aPage, as it must always have a facepage
        if not self == aPage.getFacepage() :
            self._pages.remove(aPage)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addPageAt(self, aPage, index):
        wasAdded = False
        if self.addPage(aPage) :
            if index < 0 :
                index = 0
            if index > self.numberOfPages() :
                index = self.numberOfPages() - 1
            self._pages.remove(aPage)
            self._pages.insert(index, aPage)
            wasAdded = True
        return wasAdded

    def addOrMovePageAt(self, aPage, index):
        wasAdded = False
        if (aPage) in self._pages :
            if index < 0 :
                index = 0
            if index > self.numberOfPages() :
                index = self.numberOfPages() - 1
            self._pages.remove(aPage)
            self._pages.insert(index, aPage)
            wasAdded = True
        else :
            wasAdded = self.addPageAt(aPage, index)
        return wasAdded

    def delete(self):

        while len(self._users) > 0 :
            aUser = self._users[len(self._users) - 1]
            aUser.delete()
            self._users.remove(aUser)

        while len(self._accounts) > 0 :
            aAccount = self._accounts[len(self._accounts) - 1]
            aAccount.delete()
            self._accounts.remove(aAccount)

        while len(self._pages) > 0 :
            aPage = self._pages[len(self._pages) - 1]
            aPage.delete()
            self._pages.remove(aPage)

    def addUser(self, *argv):
        from .User import User
        if len(argv) == 4 and isinstance(argv[0], int) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], date) :
            return self.addUser1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], User) :
            return self.addUser2(argv[0])
        raise TypeError("No method matches provided parameters")