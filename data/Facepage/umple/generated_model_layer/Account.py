# %% NEW FILE Account BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 15 "model.ump"
# line 87 "model.ump"
from abc import ABC, abstractmethod
import os

class Account(ABC):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Account Attributes
    #Account Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAccountNumber, aFacepage, aUser):
        self._user = None
        self._facepage = None
        self._accountNumber = None
        self._accountNumber = aAccountNumber
        didAddFacepage = self.setFacepage(aFacepage)
        if not didAddFacepage :
            raise RuntimeError ("Unable to create account due to facepage. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddUser = self.setUser(aUser)
        if not didAddUser :
            raise RuntimeError ("Unable to create account due to user. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setAccountNumber(self, aAccountNumber):
        wasSet = False
        self._accountNumber = aAccountNumber
        wasSet = True
        return wasSet

    def getAccountNumber(self):
        return self._accountNumber

    # Code from template association_GetOne 
    def getFacepage(self):
        return self._facepage

    # Code from template association_GetOne 
    def getUser(self):
        return self._user

    # Code from template association_SetOneToMany 
    def setFacepage(self, aFacepage):
        wasSet = False
        if aFacepage is None :
            return wasSet
        existingFacepage = self._facepage
        self._facepage = aFacepage
        if not (existingFacepage is None) and not existingFacepage == aFacepage :
            existingFacepage.removeAccount(self)
        self._facepage.addAccount(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToOptionalOne 
    def setUser(self, aNewUser):
        wasSet = False
        if aNewUser is None :
            #Unable to setUser to null, as account must always be associated to a user
            return wasSet
        existingAccount = aNewUser.getAccount()
        if not (existingAccount is None) and not self == existingAccount :
            #Unable to setUser, the current user already has a account, which would be orphaned if it were re-assigned
            return wasSet
        anOldUser = self._user
        self._user = aNewUser
        self._user.setAccount(self)
        if not (anOldUser is None) :
            anOldUser.setAccount(None)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderFacepage = self._facepage
        self._facepage = None
        if not (placeholderFacepage is None) :
            placeholderFacepage.removeAccount(self)
        existingUser = self._user
        self._user = None
        if not (existingUser is None) :
            existingUser.setAccount(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "accountNumber" + ":" + str(self.getAccountNumber()) + "]" + str(os.linesep) + "  " + "facepage = " + str(((format(id(self.getFacepage()), "x")) if not (self.getFacepage() is None) else "null")) + str(os.linesep) + "  " + "user = " + ((format(id(self.getUser()), "x")) if not (self.getUser() is None) else "null")
