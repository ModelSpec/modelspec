# %% NEW FILE User BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 12 "model.ump"
# line 201 "model.ump"
from abc import ABC, abstractmethod
from datetime import date
class User(ABC):
    usersByEmail = dict()
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
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber):
        self._raisedTickets = None
        self._phoneNumber = None
        self._password = None
        self._name = None
        self._email = None
        self._name = aName
        self._password = aPassword
        self._phoneNumber = aPhoneNumber
        if not self.setEmail(aEmail) :
            raise RuntimeError ("Cannot create due to duplicate email. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._raisedTickets = []

    #------------------------
    # INTERFACE
    #------------------------
    def setEmail(self, aEmail):
        wasSet = False
        anOldEmail = self.getEmail()
        if not (anOldEmail is None) and anOldEmail == aEmail :
            return True
        if User.hasWithEmail(aEmail) :
            return wasSet
        self._email = aEmail
        wasSet = True
        if not (anOldEmail is None) :
            User.usersByEmail.pop(anOldEmail, None)
        User.usersByEmail[aEmail] = self
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setPassword(self, aPassword):
        wasSet = False
        self._password = aPassword
        wasSet = True
        return wasSet

    def setPhoneNumber(self, aPhoneNumber):
        wasSet = False
        self._phoneNumber = aPhoneNumber
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

    def getName(self):
        return self._name

    def getPassword(self):
        return self._password

    def getPhoneNumber(self):
        return self._phoneNumber

    # Code from template association_GetMany 
    def getRaisedTicket(self, index):
        aRaisedTicket = self._raisedTickets[index]
        return aRaisedTicket

    def getRaisedTickets(self):
        newRaisedTickets = tuple(self._raisedTickets)
        return newRaisedTickets

    def numberOfRaisedTickets(self):
        number = len(self._raisedTickets)
        return number

    def hasRaisedTickets(self):
        has = len(self._raisedTickets) > 0
        return has

    def indexOfRaisedTicket(self, aRaisedTicket):
        index = (-1 if not aRaisedTicket in self._raisedTickets else self._raisedTickets.index(aRaisedTicket))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfRaisedTickets():
        return 0

    # Code from template association_AddManyToOne 
    def addRaisedTicket1(self, aId, aRaisedOnDate, aDescription, aAssetPlus):
        from .MaintenanceTicket import MaintenanceTicket
        return MaintenanceTicket(aId, aRaisedOnDate, aDescription, aAssetPlus, self)

    def addRaisedTicket2(self, aRaisedTicket):
        wasAdded = False
        if (aRaisedTicket) in self._raisedTickets :
            return False
        existingTicketRaiser = aRaisedTicket.getTicketRaiser()
        isNewTicketRaiser = not (existingTicketRaiser is None) and not self == existingTicketRaiser
        if isNewTicketRaiser :
            aRaisedTicket.setTicketRaiser(self)
        else :
            self._raisedTickets.append(aRaisedTicket)
        wasAdded = True
        return wasAdded

    def removeRaisedTicket(self, aRaisedTicket):
        wasRemoved = False
        #Unable to remove aRaisedTicket, as it must always have a ticketRaiser
        if not self == aRaisedTicket.getTicketRaiser() :
            self._raisedTickets.remove(aRaisedTicket)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addRaisedTicketAt(self, aRaisedTicket, index):
        wasAdded = False
        if self.addRaisedTicket(aRaisedTicket) :
            if index < 0 :
                index = 0
            if index > self.numberOfRaisedTickets() :
                index = self.numberOfRaisedTickets() - 1
            self._raisedTickets.remove(aRaisedTicket)
            self._raisedTickets.insert(index, aRaisedTicket)
            wasAdded = True
        return wasAdded

    def addOrMoveRaisedTicketAt(self, aRaisedTicket, index):
        wasAdded = False
        if (aRaisedTicket) in self._raisedTickets :
            if index < 0 :
                index = 0
            if index > self.numberOfRaisedTickets() :
                index = self.numberOfRaisedTickets() - 1
            self._raisedTickets.remove(aRaisedTicket)
            self._raisedTickets.insert(index, aRaisedTicket)
            wasAdded = True
        else :
            wasAdded = self.addRaisedTicketAt(aRaisedTicket, index)
        return wasAdded

    def delete(self):
        User.usersByEmail.pop(self.getEmail(), None)
        i = len(self._raisedTickets)
        while i > 0 :
            aRaisedTicket = self._raisedTickets[i - 1]
            aRaisedTicket.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "email" + ":" + str(self.getEmail()) + "," + "name" + ":" + str(self.getName()) + "," + "password" + ":" + str(self.getPassword()) + "," + "phoneNumber" + ":" + str(self.getPhoneNumber()) + "]"

    def addRaisedTicket(self, *argv):
        from .AssetPlus import AssetPlus
        from .MaintenanceTicket import MaintenanceTicket
        if len(argv) == 4 and isinstance(argv[0], int) and isinstance(argv[1], date) and isinstance(argv[2], str) and isinstance(argv[3], AssetPlus) :
            return self.addRaisedTicket1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], MaintenanceTicket) :
            return self.addRaisedTicket2(argv[0])
        raise TypeError("No method matches provided parameters")
