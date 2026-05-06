# %% NEW FILE RegistrationForm BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 32 "model.ump"
# line 172 "model.ump"
import os

class RegistrationForm():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #RegistrationForm Attributes
    #RegistrationForm Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    @classmethod
    def alternateConstructor(cls, aFirstName, aLastName, aUsername, aEmail, aPhone, aPassword, aConfirmPassword, aIsOrganizer, aCompanyName, aCreateAccountActivity):
        self = cls.__new__(cls)
        self._createAccountActivity = None
        self._companyName = None
        self._isOrganizer = None
        self._confirmPassword = None
        self._password = None
        self._phone = None
        self._email = None
        self._username = None
        self._lastName = None
        self._firstName = None
        self._firstName = aFirstName
        self._lastName = aLastName
        self._username = aUsername
        self._email = aEmail
        self._phone = aPhone
        self._password = aPassword
        self._confirmPassword = aConfirmPassword
        self._isOrganizer = aIsOrganizer
        self._companyName = aCompanyName
        if aCreateAccountActivity is None or not (aCreateAccountActivity.getRegistrationForm() is None) :
            raise RuntimeError ("Unable to create RegistrationForm due to aCreateAccountActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._createAccountActivity = aCreateAccountActivity
        return self

    def __init__(self, aFirstName, aLastName, aUsername, aEmail, aPhone, aPassword, aConfirmPassword, aIsOrganizer, aCompanyName):
        from .CreateAccountActivity import CreateAccountActivity
        self._createAccountActivity = None
        self._companyName = None
        self._isOrganizer = None
        self._confirmPassword = None
        self._password = None
        self._phone = None
        self._email = None
        self._username = None
        self._lastName = None
        self._firstName = None
        self._firstName = aFirstName
        self._lastName = aLastName
        self._username = aUsername
        self._email = aEmail
        self._phone = aPhone
        self._password = aPassword
        self._confirmPassword = aConfirmPassword
        self._isOrganizer = aIsOrganizer
        self._companyName = aCompanyName
        self._createAccountActivity = CreateAccountActivity.alternateConstructor(self)

    #------------------------
    # INTERFACE
    #------------------------
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

    def setPhone(self, aPhone):
        wasSet = False
        self._phone = aPhone
        wasSet = True
        return wasSet

    def setPassword(self, aPassword):
        wasSet = False
        self._password = aPassword
        wasSet = True
        return wasSet

    def setConfirmPassword(self, aConfirmPassword):
        wasSet = False
        self._confirmPassword = aConfirmPassword
        wasSet = True
        return wasSet

    def setIsOrganizer(self, aIsOrganizer):
        wasSet = False
        self._isOrganizer = aIsOrganizer
        wasSet = True
        return wasSet

    def setCompanyName(self, aCompanyName):
        wasSet = False
        self._companyName = aCompanyName
        wasSet = True
        return wasSet

    def getFirstName(self):
        return self._firstName

    def getLastName(self):
        return self._lastName

    def getUsername(self):
        return self._username

    def getEmail(self):
        return self._email

    def getPhone(self):
        return self._phone

    def getPassword(self):
        return self._password

    def getConfirmPassword(self):
        return self._confirmPassword

    def getIsOrganizer(self):
        return self._isOrganizer

    def getCompanyName(self):
        return self._companyName

    # Code from template association_GetOne 
    def getCreateAccountActivity(self):
        return self._createAccountActivity

    def delete(self):
        existingCreateAccountActivity = self._createAccountActivity
        self._createAccountActivity = None
        if not (existingCreateAccountActivity is None) :
            existingCreateAccountActivity.delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "firstName" + ":" + str(self.getFirstName()) + "," + "lastName" + ":" + str(self.getLastName()) + "," + "username" + ":" + str(self.getUsername()) + "," + "email" + ":" + str(self.getEmail()) + "," + "phone" + ":" + str(self.getPhone()) + "," + "password" + ":" + str(self.getPassword()) + "," + "confirmPassword" + ":" + str(self.getConfirmPassword()) + "," + "isOrganizer" + ":" + str(self.getIsOrganizer()) + "," + "companyName" + ":" + str(self.getCompanyName()) + "]" + str(os.linesep) + "  " + "createAccountActivity = " + ((format(id(self.getCreateAccountActivity()), "x")) if not (self.getCreateAccountActivity() is None) else "null")
