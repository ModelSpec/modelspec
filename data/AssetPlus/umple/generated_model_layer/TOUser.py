# %% NEW FILE TOUser BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 120 "model.ump"
# line 256 "model.ump"
from abc import ABC, abstractmethod
class TOUser(ABC):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOUser Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber):
        self._ticketsRaised = None
        self._phoneNumber = None
        self._password = None
        self._name = None
        self._email = None
        self._email = aEmail
        self._name = aName
        self._password = aPassword
        self._phoneNumber = aPhoneNumber
        self._ticketsRaised = []

    #------------------------
    # INTERFACE
    #------------------------
    def getEmail(self):
        return self._email

    def getName(self):
        return self._name

    def getPassword(self):
        return self._password

    def getPhoneNumber(self):
        return self._phoneNumber

    # Code from template attribute_GetMany 
    def getTicketsRaised1(self, index):
        aTicketsRaised = self._ticketsRaised[index]
        return aTicketsRaised

    def getTicketsRaised2(self):
        newTicketsRaised = self._ticketsRaised.copy()
        return newTicketsRaised

    def numberOfTicketsRaised(self):
        number = len(self._ticketsRaised)
        return number

    def hasTicketsRaised(self):
        has = len(self._ticketsRaised) > 0
        return has

    def indexOfTicketsRaised(self, aTicketsRaised):
        index = (-1 if not aTicketsRaised in self._ticketsRaised else self._ticketsRaised.index(aTicketsRaised))
        return index

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "email" + ":" + str(self.getEmail()) + "," + "name" + ":" + str(self.getName()) + "," + "password" + ":" + str(self.getPassword()) + "," + "phoneNumber" + ":" + str(self.getPhoneNumber()) + "]"

    def getTicketsRaised(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getTicketsRaised1(argv[0])
        if len(argv) == 0 :
            return self.getTicketsRaised2()
        raise TypeError("No method matches provided parameters")