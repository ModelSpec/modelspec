# %% NEW FILE Bed BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 20 "model.ump"
# line 117 "model.ump"
import os

class Bed():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Bed Attributes
    #Bed Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aBedNumber, aRoom):
        self._staies = None
        self._person = None
        self._room = None
        self._proposals = None
        self._bedNumber = None
        self._bedNumber = aBedNumber
        self._proposals = []
        didAddRoom = self.setRoom(aRoom)
        if not didAddRoom :
            raise RuntimeError ("Unable to create bed due to room. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._staies = []

    #------------------------
    # INTERFACE
    #------------------------
    def setBedNumber(self, aBedNumber):
        wasSet = False
        self._bedNumber = aBedNumber
        wasSet = True
        return wasSet

    def getBedNumber(self):
        return self._bedNumber

    # Code from template association_GetMany 
    def getProposal(self, index):
        aProposal = self._proposals[index]
        return aProposal

    def getProposals(self):
        newProposals = tuple(self._proposals)
        return newProposals

    def numberOfProposals(self):
        number = len(self._proposals)
        return number

    def hasProposals(self):
        has = len(self._proposals) > 0
        return has

    def indexOfProposal(self, aProposal):
        index = (-1 if not aProposal in self._proposals else self._proposals.index(aProposal))
        return index

    # Code from template association_GetOne 
    def getRoom(self):
        return self._room

    # Code from template association_GetOne 
    def getPerson(self):
        return self._person

    def hasPerson(self):
        has = not (self._person is None)
        return has

    # Code from template association_GetMany 
    def getStay(self, index):
        aStay = self._staies[index]
        return aStay

    def getStaies(self):
        newStaies = tuple(self._staies)
        return newStaies

    def numberOfStaies(self):
        number = len(self._staies)
        return number

    def hasStaies(self):
        has = len(self._staies) > 0
        return has

    def indexOfStay(self, aStay):
        index = (-1 if not aStay in self._staies else self._staies.index(aStay))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfProposals():
        return 0

    # Code from template association_AddManyToOne 
    def addProposal1(self, aStatus, aValidated, aPerson):
        from .Proposal import Proposal
        return Proposal(aStatus, aValidated, self, aPerson)

    def addProposal2(self, aProposal):
        wasAdded = False
        if (aProposal) in self._proposals :
            return False
        existingBed = aProposal.getBed()
        isNewBed = not (existingBed is None) and not self == existingBed
        if isNewBed :
            aProposal.setBed(self)
        else :
            self._proposals.append(aProposal)
        wasAdded = True
        return wasAdded

    def removeProposal(self, aProposal):
        wasRemoved = False
        #Unable to remove aProposal, as it must always have a bed
        if not self == aProposal.getBed() :
            self._proposals.remove(aProposal)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addProposalAt(self, aProposal, index):
        wasAdded = False
        if self.addProposal(aProposal) :
            if index < 0 :
                index = 0
            if index > self.numberOfProposals() :
                index = self.numberOfProposals() - 1
            self._proposals.remove(aProposal)
            self._proposals.insert(index, aProposal)
            wasAdded = True
        return wasAdded

    def addOrMoveProposalAt(self, aProposal, index):
        wasAdded = False
        if (aProposal) in self._proposals :
            if index < 0 :
                index = 0
            if index > self.numberOfProposals() :
                index = self.numberOfProposals() - 1
            self._proposals.remove(aProposal)
            self._proposals.insert(index, aProposal)
            wasAdded = True
        else :
            wasAdded = self.addProposalAt(aProposal, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setRoom(self, aRoom):
        wasSet = False
        if aRoom is None :
            return wasSet
        existingRoom = self._room
        self._room = aRoom
        if not (existingRoom is None) and not existingRoom == aRoom :
            existingRoom.removeBed(self)
        self._room.addBed(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOptionalOne 
    def setPerson(self, aNewPerson):
        wasSet = False
        if aNewPerson is None :
            existingPerson = self._person
            self._person = None
            if not (existingPerson is None) and not (existingPerson.getBed() is None) :
                existingPerson.setBed(None)
            wasSet = True
            return wasSet
        currentPerson = self.getPerson()
        if not (currentPerson is None) and not currentPerson == aNewPerson :
            currentPerson.setBed(None)
        self._person = aNewPerson
        existingBed = aNewPerson.getBed()
        if not self == existingBed :
            aNewPerson.setBed(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfStaies():
        return 0

    # Code from template association_AddManyToOne 
    def addStay1(self, aIntakeDate, aEndDate, aPerson):
        from .Stay import Stay
        return Stay(aIntakeDate, aEndDate, aPerson, self)

    def addStay2(self, aStay):
        wasAdded = False
        if (aStay) in self._staies :
            return False
        existingBed = aStay.getBed()
        isNewBed = not (existingBed is None) and not self == existingBed
        if isNewBed :
            aStay.setBed(self)
        else :
            self._staies.append(aStay)
        wasAdded = True
        return wasAdded

    def removeStay(self, aStay):
        wasRemoved = False
        #Unable to remove aStay, as it must always have a bed
        if not self == aStay.getBed() :
            self._staies.remove(aStay)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addStayAt(self, aStay, index):
        wasAdded = False
        if self.addStay(aStay) :
            if index < 0 :
                index = 0
            if index > self.numberOfStaies() :
                index = self.numberOfStaies() - 1
            self._staies.remove(aStay)
            self._staies.insert(index, aStay)
            wasAdded = True
        return wasAdded

    def addOrMoveStayAt(self, aStay, index):
        wasAdded = False
        if (aStay) in self._staies :
            if index < 0 :
                index = 0
            if index > self.numberOfStaies() :
                index = self.numberOfStaies() - 1
            self._staies.remove(aStay)
            self._staies.insert(index, aStay)
            wasAdded = True
        else :
            wasAdded = self.addStayAt(aStay, index)
        return wasAdded

    def delete(self):
        i = len(self._proposals)
        while i > 0 :
            aProposal = self._proposals[i - 1]
            aProposal.delete()
            i -= 1

        placeholderRoom = self._room
        self._room = None
        if not (placeholderRoom is None) :
            placeholderRoom.removeBed(self)
        if not (self._person is None) :
            self._person.setBed(None)
        i = len(self._staies)
        while i > 0 :
            aStay = self._staies[i - 1]
            aStay.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "bedNumber" + ":" + str(self.getBedNumber()) + "]" + str(os.linesep) + "  " + "room = " + str(((format(id(self.getRoom()), "x")) if not (self.getRoom() is None) else "null")) + str(os.linesep) + "  " + "person = " + ((format(id(self.getPerson()), "x")) if not (self.getPerson() is None) else "null")

    def addProposal(self, *argv):
        from .Person import Person
        from .Proposal import Proposal
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], bool) and isinstance(argv[2], Person) :
            return self.addProposal1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Proposal) :
            return self.addProposal2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addStay(self, *argv):
        from .Stay import Stay
        from .Person import Person
        from datetime import date
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], date) and isinstance(argv[2], Person) :
            return self.addStay1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Stay) :
            return self.addStay2(argv[0])
        raise TypeError("No method matches provided parameters")
