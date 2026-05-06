# %% NEW FILE UserAccount BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 44 "model.ump"
# line 177 "model.ump"
import os

class UserAccount():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #UserAccount Attributes
    #UserAccount Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aUserID, aFirstName, aLastName, aUsername, aEmail, aPhoneNumber, aRole, aAdminViewModel):
        self._adminViewModel = None
        self._role = None
        self._phoneNumber = None
        self._email = None
        self._username = None
        self._lastName = None
        self._firstName = None
        self._userID = None
        self._userID = aUserID
        self._firstName = aFirstName
        self._lastName = aLastName
        self._username = aUsername
        self._email = aEmail
        self._phoneNumber = aPhoneNumber
        self._role = aRole
        didAddAdminViewModel = self.setAdminViewModel(aAdminViewModel)
        if not didAddAdminViewModel :
            raise RuntimeError ("Unable to create userAccount due to adminViewModel. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setUserID(self, aUserID):
        wasSet = False
        self._userID = aUserID
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

    def setUsername(self, aUsername):
        wasSet = False
        self._username = aUsername
        wasSet = True
        return wasSet

    def setEmail(self, aEmail):
        wasSet = False
        self._email = aEmail
        wasSet = True
        return wasSet

    def setPhoneNumber(self, aPhoneNumber):
        wasSet = False
        self._phoneNumber = aPhoneNumber
        wasSet = True
        return wasSet

    def setRole(self, aRole):
        wasSet = False
        self._role = aRole
        wasSet = True
        return wasSet

    def getUserID(self):
        return self._userID

    def getFirstName(self):
        return self._firstName

    def getLastName(self):
        return self._lastName

    def getUsername(self):
        return self._username

    def getEmail(self):
        return self._email

    def getPhoneNumber(self):
        return self._phoneNumber

    def getRole(self):
        return self._role

    # Code from template association_GetOne 
    def getAdminViewModel(self):
        return self._adminViewModel

    # Code from template association_SetOneToMany 
    def setAdminViewModel(self, aAdminViewModel):
        wasSet = False
        if aAdminViewModel is None :
            return wasSet
        existingAdminViewModel = self._adminViewModel
        self._adminViewModel = aAdminViewModel
        if not (existingAdminViewModel is None) and not existingAdminViewModel == aAdminViewModel :
            existingAdminViewModel.removeUserAccount(self)
        self._adminViewModel.addUserAccount(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderAdminViewModel = self._adminViewModel
        self._adminViewModel = None
        if not (placeholderAdminViewModel is None) :
            placeholderAdminViewModel.removeUserAccount(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "userID" + ":" + str(self.getUserID()) + "," + "firstName" + ":" + str(self.getFirstName()) + "," + "lastName" + ":" + str(self.getLastName()) + "," + "username" + ":" + str(self.getUsername()) + "," + "email" + ":" + str(self.getEmail()) + "," + "phoneNumber" + ":" + str(self.getPhoneNumber()) + "]" + str(os.linesep) + "  " + "role" + "=" + str((((self.getRole().__str__().replaceAll("  ", "    ")) if not self.getRole() == self else "this") if not (self.getRole() is None) else "null")) + str(os.linesep) + "  " + "adminViewModel = " + ((format(id(self.getAdminViewModel()), "x")) if not (self.getAdminViewModel() is None) else "null")
