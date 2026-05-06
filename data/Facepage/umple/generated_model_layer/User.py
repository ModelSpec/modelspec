# %% NEW FILE User BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 8 "model.ump"
# line 82 "model.ump"
import os

class User():
    usersByUserID = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #User Attributes
    #User Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aUserID, aName, aEmail, aBirthDate, aFacepage):
        self._account = None
        self._facepage = None
        self._birthDate = None
        self._email = None
        self._name = None
        self._userID = None
        self._name = aName
        self._email = aEmail
        self._birthDate = aBirthDate
        if not self.setUserID(aUserID) :
            raise RuntimeError ("Cannot create due to duplicate userID. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddFacepage = self.setFacepage(aFacepage)
        if not didAddFacepage :
            raise RuntimeError ("Unable to create user due to facepage. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setUserID(self, aUserID):
        wasSet = False
        anOldUserID = self.getUserID()
        if not (anOldUserID is None) and anOldUserID == aUserID :
            return True
        if User.hasWithUserID(aUserID) :
            return wasSet
        self._userID = aUserID
        wasSet = True
        if not (anOldUserID is None) :
            User.usersByUserID.pop(anOldUserID, None)
        User.usersByUserID[aUserID] = self
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setEmail(self, aEmail):
        wasSet = False
        self._email = aEmail
        wasSet = True
        return wasSet

    def setBirthDate(self, aBirthDate):
        wasSet = False
        self._birthDate = aBirthDate
        wasSet = True
        return wasSet

    def getUserID(self):
        return self._userID

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithUserID(aUserID):
        return User.usersByUserID.get(aUserID)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithUserID(aUserID):
        return not (User.getWithUserID(aUserID) is None)

    def getName(self):
        return self._name

    def getEmail(self):
        return self._email

    def getBirthDate(self):
        return self._birthDate

    # Code from template association_GetOne 
    def getFacepage(self):
        return self._facepage

    # Code from template association_GetOne 
    def getAccount(self):
        return self._account

    def hasAccount(self):
        has = not (self._account is None)
        return has

    # Code from template association_SetOneToMany 
    def setFacepage(self, aFacepage):
        wasSet = False
        if aFacepage is None :
            return wasSet
        existingFacepage = self._facepage
        self._facepage = aFacepage
        if not (existingFacepage is None) and not existingFacepage == aFacepage :
            existingFacepage.removeUser(self)
        self._facepage.addUser(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOne 
    def setAccount(self, aNewAccount):
        wasSet = False
        if not (self._account is None) and not self._account == aNewAccount and self == self._account.getUser() :
            #Unable to setAccount, as existing account would become an orphan
            return wasSet
        self._account = aNewAccount
        anOldUser = (aNewAccount.getUser()) if not (aNewAccount is None) else None
        if not self == anOldUser :
            if not (anOldUser is None) :
                anOldUser.account = None
            if not (self._account is None) :
                self._account.setUser(self)
        wasSet = True
        return wasSet

    def delete(self):
        User.usersByUserID.pop(self.getUserID(), None)
        placeholderFacepage = self._facepage
        self._facepage = None
        if not (placeholderFacepage is None) :
            placeholderFacepage.removeUser(self)
        existingAccount = self._account
        self._account = None
        if not (existingAccount is None) :
            existingAccount.delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "userID" + ":" + str(self.getUserID()) + "," + "name" + ":" + str(self.getName()) + "," + "email" + ":" + str(self.getEmail()) + "]" + str(os.linesep) + "  " + "birthDate" + "=" + str((((self.getBirthDate().__str__().replaceAll("  ", "    ")) if not self.getBirthDate() == self else "this") if not (self.getBirthDate() is None) else "null")) + str(os.linesep) + "  " + "facepage = " + str(((format(id(self.getFacepage()), "x")) if not (self.getFacepage() is None) else "null")) + str(os.linesep) + "  " + "account = " + ((format(id(self.getAccount()), "x")) if not (self.getAccount() is None) else "null")
