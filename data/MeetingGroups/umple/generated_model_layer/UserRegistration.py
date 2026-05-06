# %% NEW FILE UserRegistration BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 31 "model.ump"
# line 265 "model.ump"
import os
from enum import Enum, auto

class UserRegistration():
    nextId = 1
    #------------------------
    # ENUMERATIONS
    #------------------------
    class UserRegistrationStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        WaitingForConfirmation = auto()
        Confirmed = auto()
        Expired = auto()

    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #UserRegistration Attributes
    #Autounique Attributes
    #UserRegistration Associations
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aLogin, aEmail, aFirstName, aLastName, aUserAccess):
        self._canSetConfirmedDate = None
        self._canSetRegisterDate = None
        self._userAccess = None
        self._id = None
        self._status = None
        self._confirmedDate = None
        self._registerDate = None
        self._name = None
        self._lastName = None
        self._firstName = None
        self._email = None
        self._login = None
        self._login = aLogin
        self._email = aEmail
        self._firstName = aFirstName
        self._lastName = aLastName
        self._name = None
        self._canSetRegisterDate = True
        self._canSetConfirmedDate = True
        self._id, UserRegistration.nextId = UserRegistration.nextId, UserRegistration.nextId + 1
        didAddUserAccess = self.setUserAccess(aUserAccess)
        if not didAddUserAccess :
            raise RuntimeError ("Unable to create userRegistration due to userAccess. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
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

    # Code from template attribute_SetImmutable
    def setRegisterDate(self, aRegisterDate):
        wasSet = False
        if not self._canSetRegisterDate :
            return False
        self._canSetRegisterDate = False
        self._registerDate = aRegisterDate
        wasSet = True
        return wasSet

    # Code from template attribute_SetImmutable
    def setConfirmedDate(self, aConfirmedDate):
        wasSet = False
        if not self._canSetConfirmedDate :
            return False
        self._canSetConfirmedDate = False
        self._confirmedDate = aConfirmedDate
        wasSet = True
        return wasSet

    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

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

    def getRegisterDate(self):
        return self._registerDate

    def getConfirmedDate(self):
        return self._confirmedDate

    def getStatus(self):
        return self._status

    def getId(self):
        return self._id

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
            existingUserAccess.removeUserRegistration(self)
        self._userAccess.addUserRegistration(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderUserAccess = self._userAccess
        self._userAccess = None
        if not (placeholderUserAccess is None) :
            placeholderUserAccess.removeUserRegistration(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "login" + ":" + str(self.getLogin()) + "," + "email" + ":" + str(self.getEmail()) + "," + "firstName" + ":" + str(self.getFirstName()) + "," + "lastName" + ":" + str(self.getLastName()) + "," + "name" + ":" + str(self.getName()) + "]" + str(os.linesep) + "  " + "registerDate" + "=" + str((((self.getRegisterDate().__str__().replaceAll("  ", "    ")) if not self.getRegisterDate() == self else "this") if not (self.getRegisterDate() is None) else "null")) + str(os.linesep) + "  " + "confirmedDate" + "=" + str((((self.getConfirmedDate().__str__().replaceAll("  ", "    ")) if not self.getConfirmedDate() == self else "this") if not (self.getConfirmedDate() is None) else "null")) + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "userAccess = " + ((format(id(self.getUserAccess()), "x")) if not (self.getUserAccess() is None) else "null")
