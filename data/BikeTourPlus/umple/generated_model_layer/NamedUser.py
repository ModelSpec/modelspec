# %% NEW FILE NamedUser BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 27 "model.ump"
# line 111 "model.ump"
from abc import ABC, abstractmethod
from .User import User

class NamedUser(User):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #NamedUser Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword, aName, aEmergencyContact):
        self._emergencyContact = None
        self._name = None
        super().__init__(aEmail, aPassword)
        self._name = aName
        self._emergencyContact = aEmergencyContact

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setEmergencyContact(self, aEmergencyContact):
        wasSet = False
        self._emergencyContact = aEmergencyContact
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    def getEmergencyContact(self):
        return self._emergencyContact

    def delete(self):
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "emergencyContact" + ":" + str(self.getEmergencyContact()) + "]"
