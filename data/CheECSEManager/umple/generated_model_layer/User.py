#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 14 "../model.ump"
# line 159 "../model.ump"
from abc import ABC, abstractmethod

class User(ABC):
    usersByEmail = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #User Attributes
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword):
        self._canSetEmail = None
        self._password = None
        self._email = None
        self._canSetEmail = True
        self._password = aPassword
        if not self.setEmail(aEmail) :
            raise RuntimeError ("Cannot create due to duplicate email. See https://manual.umple.org?RE003ViolationofUniqueness.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template attribute_SetImmutable 
    def setEmail(self, aEmail):
        wasSet = False
        if not self._canSetEmail :
            return False
        anOldEmail = self.getEmail()
        if not (anOldEmail is None) and anOldEmail == aEmail :
            return True
        if User.hasWithEmail(aEmail) :
            return wasSet
        self._canSetEmail = False
        self._email = aEmail
        wasSet = True
        if not (anOldEmail is None) :
            User.usersByEmail.pop(anOldEmail, None)
        User.usersByEmail[aEmail] = self
        return wasSet

    def setPassword(self, aPassword):
        wasSet = False
        self._password = aPassword
        wasSet = True
        return wasSet

    def getEmail(self):
        return self._email

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithEmail(aEmail):
        return User.usersByEmail.get(aEmail)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithEmail(aEmail):
        return not (User.getWithEmail(aEmail) is None)

    def getPassword(self):
        return self._password

    def delete(self):
        User.usersByEmail.pop(self.getEmail(), None)

    def __str__(self):
        return str(super().__str__()) + "[" + "email" + ":" + str(self.getEmail()) + "," + "password" + ":" + str(self.getPassword()) + "]"

