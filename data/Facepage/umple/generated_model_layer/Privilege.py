# %% NEW FILE Privilege BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 41 "model.ump"
# line 117 "model.ump"
import os

class Privilege():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Privilege Attributes
    #Privilege Associations
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTypeOfPrivilege, aPersonalAccount, aPersonalPage):
        self._canSetPersonalPage = None
        self._canSetPersonalAccount = None
        self._cachedHashCode = None
        self._personalPage = None
        self._personalAccount = None
        self._typeOfPrivilege = None
        self._cachedHashCode = -1
        self._canSetPersonalAccount = True
        self._canSetPersonalPage = True
        self._typeOfPrivilege = aTypeOfPrivilege
        didAddPersonalAccount = self.setPersonalAccount(aPersonalAccount)
        if not didAddPersonalAccount :
            raise RuntimeError ("Unable to create privilege due to personalAccount. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddPersonalPage = self.setPersonalPage(aPersonalPage)
        if not didAddPersonalPage :
            raise RuntimeError ("Unable to create privilege due to personalPage. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setTypeOfPrivilege(self, aTypeOfPrivilege):
        wasSet = False
        self._typeOfPrivilege = aTypeOfPrivilege
        wasSet = True
        return wasSet

    def getTypeOfPrivilege(self):
        return self._typeOfPrivilege

    # Code from template association_GetOne 
    def getPersonalAccount(self):
        return self._personalAccount

    # Code from template association_GetOne 
    def getPersonalPage(self):
        return self._personalPage

    # Code from template association_SetOneToManyAssociationClass 
    def setPersonalAccount(self, aPersonalAccount):
        wasSet = False
        if not self._canSetPersonalAccount :
            return False
        if aPersonalAccount is None :
            return wasSet
        existingPersonalAccount = self._personalAccount
        self._personalAccount = aPersonalAccount
        if not (existingPersonalAccount is None) and not existingPersonalAccount == aPersonalAccount :
            existingPersonalAccount.removePrivilege(self)
        if not self._personalAccount.addPrivilege(self) :
            self._personalAccount = existingPersonalAccount
            wasSet = False
        else :
            wasSet = True
        return wasSet

    # Code from template association_SetOneToManyAssociationClass 
    def setPersonalPage(self, aPersonalPage):
        wasSet = False
        if not self._canSetPersonalPage :
            return False
        if aPersonalPage is None :
            return wasSet
        existingPersonalPage = self._personalPage
        self._personalPage = aPersonalPage
        if not (existingPersonalPage is None) and not existingPersonalPage == aPersonalPage :
            existingPersonalPage.removePrivilege(self)
        if not self._personalPage.addPrivilege(self) :
            self._personalPage = existingPersonalPage
            wasSet = False
        else :
            wasSet = True
        return wasSet

    def equals(self, obj):
        if obj is None :
            return False
        if not type(self) is type(obj) :
            return False
        compareTo = obj
        if self.getPersonalAccount() is None and not (compareTo.getPersonalAccount() is None) :
            return False
        elif not (self.getPersonalAccount() is None) and not self.getPersonalAccount() == compareTo.getPersonalAccount() :
            return False
        if self.getPersonalPage() is None and not (compareTo.getPersonalPage() is None) :
            return False
        elif not (self.getPersonalPage() is None) and not self.getPersonalPage() == compareTo.getPersonalPage() :
            return False
        return True

    def __hash__(self):
        if self._cachedHashCode != -1 :
            return self._cachedHashCode
        self._cachedHashCode = 17
        if not (self.getPersonalAccount() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getPersonalAccount().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        if not (self.getPersonalPage() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getPersonalPage().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        self._canSetPersonalAccount = False
        self._canSetPersonalPage = False
        return self._cachedHashCode

    def delete(self):
        placeholderPersonalAccount = self._personalAccount
        self._personalAccount = None
        if not (placeholderPersonalAccount is None) :
            placeholderPersonalAccount.removePrivilege(self)
        placeholderPersonalPage = self._personalPage
        self._personalPage = None
        if not (placeholderPersonalPage is None) :
            placeholderPersonalPage.removePrivilege(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "typeOfPrivilege" + ":" + str(self.getTypeOfPrivilege()) + "]" + str(os.linesep) + "  " + "personalAccount = " + str(((format(id(self.getPersonalAccount()), "x")) if not (self.getPersonalAccount() is None) else "null")) + str(os.linesep) + "  " + "personalPage = " + ((format(id(self.getPersonalPage()), "x")) if not (self.getPersonalPage() is None) else "null")
