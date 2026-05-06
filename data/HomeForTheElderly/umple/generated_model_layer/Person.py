# %% NEW FILE Person BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 36 "model.ump"
# line 134 "model.ump"
import os

class Person():
    personsById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Person Attributes
    #Person Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aName, aBirthdate, aHomeForTheElderly):
        self._invoices = None
        self._staies = None
        self._bed = None
        self._proposals = None
        self._homeForTheElderly = None
        self._abilities = None
        self._registrationDate = None
        self._birthdate = None
        self._name = None
        self._id = None
        self._name = aName
        self._birthdate = aBirthdate
        self._registrationDate = None
        self._abilities = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddHomeForTheElderly = self.setHomeForTheElderly(aHomeForTheElderly)
        if not didAddHomeForTheElderly :
            raise RuntimeError ("Unable to create people due to homeForTheElderly. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._proposals = []
        self._staies = []
        self._invoices = []

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if Person.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            Person.personsById.pop(anOldId, None)
        Person.personsById[aId] = self
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setBirthdate(self, aBirthdate):
        wasSet = False
        self._birthdate = aBirthdate
        wasSet = True
        return wasSet

    def setRegistrationDate(self, aRegistrationDate):
        wasSet = False
        self._registrationDate = aRegistrationDate
        wasSet = True
        return wasSet

    def setAbilities(self, aAbilities):
        wasSet = False
        self._abilities = aAbilities
        wasSet = True
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithId(aId):
        return Person.personsById.get(aId)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithId(aId):
        return not (Person.getWithId(aId) is None)

    def getName(self):
        return self._name

    def getBirthdate(self):
        return self._birthdate

    def getRegistrationDate(self):
        return self._registrationDate

    def getAbilities(self):
        return self._abilities

    # Code from template association_GetOne 
    def getHomeForTheElderly(self):
        return self._homeForTheElderly

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
    def getBed(self):
        return self._bed

    def hasBed(self):
        has = not (self._bed is None)
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

    # Code from template association_GetMany 
    def getInvoice(self, index):
        aInvoice = self._invoices[index]
        return aInvoice

    def getInvoices(self):
        newInvoices = tuple(self._invoices)
        return newInvoices

    def numberOfInvoices(self):
        number = len(self._invoices)
        return number

    def hasInvoices(self):
        has = len(self._invoices) > 0
        return has

    def indexOfInvoice(self, aInvoice):
        index = (-1 if not aInvoice in self._invoices else self._invoices.index(aInvoice))
        return index

    # Code from template association_SetOneToMany 
    def setHomeForTheElderly(self, aHomeForTheElderly):
        wasSet = False
        if aHomeForTheElderly is None :
            return wasSet
        existingHomeForTheElderly = self._homeForTheElderly
        self._homeForTheElderly = aHomeForTheElderly
        if not (existingHomeForTheElderly is None) and not existingHomeForTheElderly == aHomeForTheElderly :
            existingHomeForTheElderly.removePeople(self)
        self._homeForTheElderly.addPeople(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfProposals():
        return 0

    # Code from template association_AddManyToOne 
    def addProposal1(self, aStatus, aValidated, aBed):
        from .Proposal import Proposal
        return Proposal(aStatus, aValidated, aBed, self)

    def addProposal2(self, aProposal):
        wasAdded = False
        if (aProposal) in self._proposals :
            return False
        existingPerson = aProposal.getPerson()
        isNewPerson = not (existingPerson is None) and not self == existingPerson
        if isNewPerson :
            aProposal.setPerson(self)
        else :
            self._proposals.append(aProposal)
        wasAdded = True
        return wasAdded

    def removeProposal(self, aProposal):
        wasRemoved = False
        #Unable to remove aProposal, as it must always have a person
        if not self == aProposal.getPerson() :
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

    # Code from template association_SetOptionalOneToOptionalOne 
    def setBed(self, aNewBed):
        wasSet = False
        if aNewBed is None :
            existingBed = self._bed
            self._bed = None
            if not (existingBed is None) and not (existingBed.getPerson() is None) :
                existingBed.setPerson(None)
            wasSet = True
            return wasSet
        currentBed = self.getBed()
        if not (currentBed is None) and not currentBed == aNewBed :
            currentBed.setPerson(None)
        self._bed = aNewBed
        existingPerson = aNewBed.getPerson()
        if not self == existingPerson :
            aNewBed.setPerson(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfStaies():
        return 0

    # Code from template association_AddManyToOne 
    def addStay1(self, aIntakeDate, aEndDate, aBed):
        from .Stay import Stay
        return Stay(aIntakeDate, aEndDate, self, aBed)

    def addStay2(self, aStay):
        wasAdded = False
        if (aStay) in self._staies :
            return False
        existingPerson = aStay.getPerson()
        isNewPerson = not (existingPerson is None) and not self == existingPerson
        if isNewPerson :
            aStay.setPerson(self)
        else :
            self._staies.append(aStay)
        wasAdded = True
        return wasAdded

    def removeStay(self, aStay):
        wasRemoved = False
        #Unable to remove aStay, as it must always have a person
        if not self == aStay.getPerson() :
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

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfInvoices():
        return 0

    # Code from template association_AddManyToOne 
    def addInvoice1(self, aInvoiceDate, aOutstandingAmount, aStatus):
        from .Invoice import Invoice
        return Invoice(aInvoiceDate, aOutstandingAmount, aStatus, self)

    def addInvoice2(self, aInvoice):
        wasAdded = False
        if (aInvoice) in self._invoices :
            return False
        existingPerson = aInvoice.getPerson()
        isNewPerson = not (existingPerson is None) and not self == existingPerson
        if isNewPerson :
            aInvoice.setPerson(self)
        else :
            self._invoices.append(aInvoice)
        wasAdded = True
        return wasAdded

    def removeInvoice(self, aInvoice):
        wasRemoved = False
        #Unable to remove aInvoice, as it must always have a person
        if not self == aInvoice.getPerson() :
            self._invoices.remove(aInvoice)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addInvoiceAt(self, aInvoice, index):
        wasAdded = False
        if self.addInvoice(aInvoice) :
            if index < 0 :
                index = 0
            if index > self.numberOfInvoices() :
                index = self.numberOfInvoices() - 1
            self._invoices.remove(aInvoice)
            self._invoices.insert(index, aInvoice)
            wasAdded = True
        return wasAdded

    def addOrMoveInvoiceAt(self, aInvoice, index):
        wasAdded = False
        if (aInvoice) in self._invoices :
            if index < 0 :
                index = 0
            if index > self.numberOfInvoices() :
                index = self.numberOfInvoices() - 1
            self._invoices.remove(aInvoice)
            self._invoices.insert(index, aInvoice)
            wasAdded = True
        else :
            wasAdded = self.addInvoiceAt(aInvoice, index)
        return wasAdded

    def delete(self):
        Person.personsById.pop(self.getId(), None)
        placeholderHomeForTheElderly = self._homeForTheElderly
        self._homeForTheElderly = None
        if not (placeholderHomeForTheElderly is None) :
            placeholderHomeForTheElderly.removePeople(self)
        i = len(self._proposals)
        while i > 0 :
            aProposal = self._proposals[i - 1]
            aProposal.delete()
            i -= 1

        if not (self._bed is None) :
            self._bed.setPerson(None)
        i = len(self._staies)
        while i > 0 :
            aStay = self._staies[i - 1]
            aStay.delete()
            i -= 1

        i = len(self._invoices)
        while i > 0 :
            aInvoice = self._invoices[i - 1]
            aInvoice.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "name" + ":" + str(self.getName()) + "," + "abilities" + ":" + str(self.getAbilities()) + "]" + str(os.linesep) + "  " + "birthdate" + "=" + str((((self.getBirthdate().__str__().replaceAll("  ", "    ")) if not self.getBirthdate() == self else "this") if not (self.getBirthdate() is None) else "null")) + str(os.linesep) + "  " + "registrationDate" + "=" + str((((self.getRegistrationDate().__str__().replaceAll("  ", "    ")) if not self.getRegistrationDate() == self else "this") if not (self.getRegistrationDate() is None) else "null")) + str(os.linesep) + "  " + "homeForTheElderly = " + str(((format(id(self.getHomeForTheElderly()), "x")) if not (self.getHomeForTheElderly() is None) else "null")) + str(os.linesep) + "  " + "bed = " + ((format(id(self.getBed()), "x")) if not (self.getBed() is None) else "null")

    def addProposal(self, *argv):
        from .Bed import Bed
        from .Proposal import Proposal
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], bool) and isinstance(argv[2], Bed) :
            return self.addProposal1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Proposal) :
            return self.addProposal2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addStay(self, *argv):
        from .Stay import Stay
        from .Bed import Bed
        from datetime import date
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], date) and isinstance(argv[2], Bed) :
            return self.addStay1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Stay) :
            return self.addStay2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addInvoice(self, *argv):
        from .Invoice import Invoice
        from datetime import date
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], (float, int)) and isinstance(argv[2], str) :
            return self.addInvoice1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Invoice) :
            return self.addInvoice2(argv[0])
        raise TypeError("No method matches provided parameters")
