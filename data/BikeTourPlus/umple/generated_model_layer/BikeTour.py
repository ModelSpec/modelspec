# %% NEW FILE BikeTour BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 84 "model.ump"
# line 156 "model.ump"
import os

class BikeTour():
    biketoursById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #BikeTour Attributes
    #BikeTour Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aStartWeek, aEndWeek, aGuide, aBikeTourPlus):
        self._bikeTourPlus = None
        self._lodge = None
        self._guide = None
        self._participants = None
        self._endWeek = None
        self._startWeek = None
        self._id = None
        self._startWeek = aStartWeek
        self._endWeek = aEndWeek
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._participants = []
        didAddGuide = self.setGuide(aGuide)
        if not didAddGuide :
            raise RuntimeError ("Unable to create bikeTour due to guide. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create bikeTour due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if BikeTour.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            BikeTour.biketoursById.pop(anOldId, None)
        BikeTour.biketoursById[aId] = self
        return wasSet

    def setStartWeek(self, aStartWeek):
        wasSet = False
        self._startWeek = aStartWeek
        wasSet = True
        return wasSet

    def setEndWeek(self, aEndWeek):
        wasSet = False
        self._endWeek = aEndWeek
        wasSet = True
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithId(aId):
        return BikeTour.biketoursById.get(aId)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithId(aId):
        return not (BikeTour.getWithId(aId) is None)

    def getStartWeek(self):
        return self._startWeek

    def getEndWeek(self):
        return self._endWeek

    # Code from template association_GetMany
    def getParticipant(self, index):
        aParticipant = self._participants[index]
        return aParticipant

    def getParticipants(self):
        newParticipants = tuple(self._participants)
        return newParticipants

    def numberOfParticipants(self):
        number = len(self._participants)
        return number

    def hasParticipants(self):
        has = len(self._participants) > 0
        return has

    def indexOfParticipant(self, aParticipant):
        index = (-1 if not aParticipant in self._participants else self._participants.index(aParticipant))
        return index

    # Code from template association_GetOne
    def getGuide(self):
        return self._guide

    # Code from template association_GetOne
    def getLodge(self):
        return self._lodge

    def hasLodge(self):
        has = not (self._lodge is None)
        return has

    # Code from template association_GetOne
    def getBikeTourPlus(self):
        return self._bikeTourPlus

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfParticipants():
        return 0

    # Code from template association_AddManyToOptionalOne
    def addParticipant(self, aParticipant):
        wasAdded = False
        if (aParticipant) in self._participants :
            return False
        existingBikeTour = aParticipant.getBikeTour()
        if existingBikeTour is None :
            aParticipant.setBikeTour(self)
        elif not self == existingBikeTour :
            existingBikeTour.removeParticipant(aParticipant)
            self.addParticipant(aParticipant)
        else :
            self._participants.append(aParticipant)
        wasAdded = True
        return wasAdded

    def removeParticipant(self, aParticipant):
        wasRemoved = False
        if (aParticipant) in self._participants :
            self._participants.remove(aParticipant)
            aParticipant.setBikeTour(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addParticipantAt(self, aParticipant, index):
        wasAdded = False
        if self.addParticipant(aParticipant) :
            if index < 0 :
                index = 0
            if index > self.numberOfParticipants() :
                index = self.numberOfParticipants() - 1
            self._participants.remove(aParticipant)
            self._participants.insert(index, aParticipant)
            wasAdded = True
        return wasAdded

    def addOrMoveParticipantAt(self, aParticipant, index):
        wasAdded = False
        if (aParticipant) in self._participants :
            if index < 0 :
                index = 0
            if index > self.numberOfParticipants() :
                index = self.numberOfParticipants() - 1
            self._participants.remove(aParticipant)
            self._participants.insert(index, aParticipant)
            wasAdded = True
        else :
            wasAdded = self.addParticipantAt(aParticipant, index)
        return wasAdded

    # Code from template association_SetOneToMany
    def setGuide(self, aGuide):
        wasSet = False
        if aGuide is None :
            return wasSet
        existingGuide = self._guide
        self._guide = aGuide
        if not (existingGuide is None) and not existingGuide == aGuide :
            existingGuide.removeBikeTour(self)
        self._guide.addBikeTour(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany
    def setLodge(self, aLodge):
        wasSet = False
        existingLodge = self._lodge
        self._lodge = aLodge
        if not (existingLodge is None) and not existingLodge == aLodge :
            existingLodge.removeBikeTour(self)
        if not (aLodge is None) :
            aLodge.addBikeTour(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setBikeTourPlus(self, aBikeTourPlus):
        wasSet = False
        if aBikeTourPlus is None :
            return wasSet
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aBikeTourPlus
        if not (existingBikeTourPlus is None) and not existingBikeTourPlus == aBikeTourPlus :
            existingBikeTourPlus.removeBikeTour(self)
        self._bikeTourPlus.addBikeTour(self)
        wasSet = True
        return wasSet

    def delete(self):
        BikeTour.biketoursById.pop(self.getId(), None)

        while not self._participants.isEmpty() :
            self._participants[0].setBikeTour(None)

        placeholderGuide = self._guide
        self._guide = None
        if not (placeholderGuide is None) :
            placeholderGuide.removeBikeTour(self)
        if not (self._lodge is None) :
            placeholderLodge = self._lodge
            self._lodge = None
            placeholderLodge.removeBikeTour(self)
        placeholderBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (placeholderBikeTourPlus is None) :
            placeholderBikeTourPlus.removeBikeTour(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "startWeek" + ":" + str(self.getStartWeek()) + "," + "endWeek" + ":" + str(self.getEndWeek()) + "]" + str(os.linesep) + "  " + "guide = " + str(((format(id(self.getGuide()), "x")) if not (self.getGuide() is None) else "null")) + str(os.linesep) + "  " + "lodge = " + str(((format(id(self.getLodge()), "x")) if not (self.getLodge() is None) else "null")) + str(os.linesep) + "  " + "bikeTourPlus = " + ((format(id(self.getBikeTourPlus()), "x")) if not (self.getBikeTourPlus() is None) else "null")
