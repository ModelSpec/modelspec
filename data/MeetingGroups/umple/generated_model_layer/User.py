# %% NEW FILE User BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 44 "model.ump"
# line 270 "model.ump"
import os

class User():
    usersById = dict()
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
    def __init__(self, aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess):
        self._userAccess = None
        self._createDate = None
        self._name = None
        self._lastName = None
        self._firstName = None
        self._email = None
        self._login = None
        self._id = None
        self._login = aLogin
        self._email = aEmail
        self._firstName = aFirstName
        self._lastName = aLastName
        self._name = aName
        self._createDate = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddUserAccess = self.setUserAccess(aUserAccess)
        if not didAddUserAccess :
            raise RuntimeError ("Unable to create user due to userAccess. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if User.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            User.usersById.pop(anOldId, None)
        User.usersById[aId] = self
        return wasSet

    def setLogin(self, aLogin):
        wasSet = False
        self._login = aLogin
        wasSet = True
        return wasSet

    def setEmail(self, aEmail):
        wasSet = False
        self._email = aEmail
        wasSet = True
        return wasSet

    def setFirstName(self, aFirstName):
        wasSet = False
        self._firstName = aFirstName
        wasSet = True
        return wasSet

    def setLastName(self, aLastName):
        wasSet = False
        self._lastName = aLastName
        wasSet = True
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setCreateDate(self, aCreateDate):
        wasSet = False
        self._createDate = aCreateDate
        wasSet = True
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithId(aId):
        return User.usersById.get(aId)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithId(aId):
        return not (User.getWithId(aId) is None)

    def getLogin(self):
        return self._login

    def getEmail(self):
        return self._email

    def getFirstName(self):
        return self._firstName

    def getLastName(self):
        return self._lastName

    def getName(self):
        return self._name

    def getCreateDate(self):
        return self._createDate

    # Code from template association_GetOne
    def getUserAccess(self):
        return self._userAccess

    # Code from template association_SetOneToMany
    def setUserAccess(self, aUserAccess):
        wasSet = False
        if aUserAccess is None :
            return wasSet
        existingUserAccess = self._userAccess
        self._userAccess = aUserAccess
        if not (existingUserAccess is None) and not existingUserAccess == aUserAccess :
            existingUserAccess.removeUser(self)
        self._userAccess.addUser(self)
        wasSet = True
        return wasSet

    def delete(self):
        User.usersById.pop(self.getId(), None)
        placeholderUserAccess = self._userAccess
        self._userAccess = None
        if not (placeholderUserAccess is None) :
            placeholderUserAccess.removeUser(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "login" + ":" + str(self.getLogin()) + "," + "email" + ":" + str(self.getEmail()) + "," + "firstName" + ":" + str(self.getFirstName()) + "," + "lastName" + ":" + str(self.getLastName()) + "," + "name" + ":" + str(self.getName()) + "]" + str(os.linesep) + "  " + "createDate" + "=" + str((((self.getCreateDate().__str__().replaceAll("  ", "    ")) if not self.getCreateDate() == self else "this") if not (self.getCreateDate() is None) else "null")) + str(os.linesep) + "  " + "userAccess = " + ((format(id(self.getUserAccess()), "x")) if not (self.getUserAccess() is None) else "null")
