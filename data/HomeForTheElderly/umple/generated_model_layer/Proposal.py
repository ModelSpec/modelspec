# %% NEW FILE Proposal BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 24 "model.ump"
# line 122 "model.ump"
import os

class Proposal():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Proposal Attributes
    #Proposal Associations
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aStatus, aValidated, aBed, aPerson):
        self._canSetPerson = None
        self._canSetBed = None
        self._cachedHashCode = None
        self._person = None
        self._bed = None
        self._validated = None
        self._status = None
        self._cachedHashCode = -1
        self._canSetBed = True
        self._canSetPerson = True
        self._status = aStatus
        self._validated = aValidated
        didAddBed = self.setBed(aBed)
        if not didAddBed :
            raise RuntimeError ("Unable to create proposal due to bed. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddPerson = self.setPerson(aPerson)
        if not didAddPerson :
            raise RuntimeError ("Unable to create proposal due to person. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def setValidated(self, aValidated):
        wasSet = False
        self._validated = aValidated
        wasSet = True
        return wasSet

    def getStatus(self):
        return self._status

    def getValidated(self):
        return self._validated

    # Code from template association_GetOne 
    def getBed(self):
        return self._bed

    # Code from template association_GetOne 
    def getPerson(self):
        return self._person

    # Code from template association_SetOneToManyAssociationClass 
    def setBed(self, aBed):
        wasSet = False
        if not self._canSetBed :
            return False
        if aBed is None :
            return wasSet
        existingBed = self._bed
        self._bed = aBed
        if not (existingBed is None) and not existingBed == aBed :
            existingBed.removeProposal(self)
        if not self._bed.addProposal(self) :
            self._bed = existingBed
            wasSet = False
        else :
            wasSet = True
        return wasSet

    # Code from template association_SetOneToManyAssociationClass 
    def setPerson(self, aPerson):
        wasSet = False
        if not self._canSetPerson :
            return False
        if aPerson is None :
            return wasSet
        existingPerson = self._person
        self._person = aPerson
        if not (existingPerson is None) and not existingPerson == aPerson :
            existingPerson.removeProposal(self)
        if not self._person.addProposal(self) :
            self._person = existingPerson
            wasSet = False
        else :
            wasSet = True
        return wasSet

    def equals(self, obj):
        if obj is None :
            return False
        if not type(self) is type(obj) :
            return False
        compareTo = obj
        if self.getBed() is None and not (compareTo.getBed() is None) :
            return False
        elif not (self.getBed() is None) and not self.getBed() == compareTo.getBed() :
            return False
        if self.getPerson() is None and not (compareTo.getPerson() is None) :
            return False
        elif not (self.getPerson() is None) and not self.getPerson() == compareTo.getPerson() :
            return False
        return True

    def __hash__(self):
        if self._cachedHashCode != -1 :
            return self._cachedHashCode
        self._cachedHashCode = 17
        if not (self.getBed() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getBed().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        if not (self.getPerson() is None) :
            self._cachedHashCode = self._cachedHashCode * 23 + self.getPerson().__hash__()
        else :
            self._cachedHashCode = self._cachedHashCode * 23
        self._canSetBed = False
        self._canSetPerson = False
        return self._cachedHashCode

    def delete(self):
        placeholderBed = self._bed
        self._bed = None
        if not (placeholderBed is None) :
            placeholderBed.removeProposal(self)
        placeholderPerson = self._person
        self._person = None
        if not (placeholderPerson is None) :
            placeholderPerson.removeProposal(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "status" + ":" + str(self.getStatus()) + "," + "validated" + ":" + str(self.getValidated()) + "]" + str(os.linesep) + "  " + "bed = " + str(((format(id(self.getBed()), "x")) if not (self.getBed() is None) else "null")) + str(os.linesep) + "  " + "person = " + ((format(id(self.getPerson()), "x")) if not (self.getPerson() is None) else "null")
