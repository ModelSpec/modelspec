# %% NEW FILE BikeTourPlus BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 2 "model.ump"
# line 96 "model.ump"
import os

class BikeTourPlus():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #BikeTourPlus Attributes
    #BikeTourPlus Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aStartDate, aNrWeeks, aPriceOfGuidePerWeek):
        self._bikeTours = None
        self._lodges = None
        self._comboItems = None
        self._combos = None
        self._gear = None
        self._bookedItems = None
        self._participants = None
        self._guides = None
        self._manager = None
        self._priceOfGuidePerWeek = None
        self._nrWeeks = None
        self._startDate = None
        self._startDate = aStartDate
        self._nrWeeks = aNrWeeks
        self._priceOfGuidePerWeek = aPriceOfGuidePerWeek
        self._guides = []
        self._participants = []
        self._bookedItems = []
        self._gear = []
        self._combos = []
        self._comboItems = []
        self._lodges = []
        self._bikeTours = []

    #------------------------
    # INTERFACE
    #------------------------
    def setStartDate(self, aStartDate):
        wasSet = False
        self._startDate = aStartDate
        wasSet = True
        return wasSet

    def setNrWeeks(self, aNrWeeks):
        wasSet = False
        self._nrWeeks = aNrWeeks
        wasSet = True
        return wasSet

    def setPriceOfGuidePerWeek(self, aPriceOfGuidePerWeek):
        wasSet = False
        self._priceOfGuidePerWeek = aPriceOfGuidePerWeek
        wasSet = True
        return wasSet

    def getStartDate(self):
        return self._startDate

    def getNrWeeks(self):
        return self._nrWeeks

    def getPriceOfGuidePerWeek(self):
        return self._priceOfGuidePerWeek

    # Code from template association_GetOne
    def getManager(self):
        return self._manager

    def hasManager(self):
        has = not (self._manager is None)
        return has

    # Code from template association_GetMany
    def getGuide(self, index):
        aGuide = self._guides[index]
        return aGuide

    def getGuides(self):
        newGuides = tuple(self._guides)
        return newGuides

    def numberOfGuides(self):
        number = len(self._guides)
        return number

    def hasGuides(self):
        has = len(self._guides) > 0
        return has

    def indexOfGuide(self, aGuide):
        index = (-1 if not aGuide in self._guides else self._guides.index(aGuide))
        return index

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

    # Code from template association_GetMany
    def getBookedItem(self, index):
        aBookedItem = self._bookedItems[index]
        return aBookedItem

    def getBookedItems(self):
        newBookedItems = tuple(self._bookedItems)
        return newBookedItems

    def numberOfBookedItems(self):
        number = len(self._bookedItems)
        return number

    def hasBookedItems(self):
        has = len(self._bookedItems) > 0
        return has

    def indexOfBookedItem(self, aBookedItem):
        index = (-1 if not aBookedItem in self._bookedItems else self._bookedItems.index(aBookedItem))
        return index

    # Code from template association_GetMany
    def getGear1(self, index):
        aGear = self._gear[index]
        return aGear

    def getGear2(self):
        newGear = tuple(self._gear)
        return newGear

    def numberOfGear(self):
        number = len(self._gear)
        return number

    def hasGear(self):
        has = len(self._gear) > 0
        return has

    def indexOfGear(self, aGear):
        index = (-1 if not aGear in self._gear else self._gear.index(aGear))
        return index

    # Code from template association_GetMany
    def getCombo(self, index):
        aCombo = self._combos[index]
        return aCombo

    def getCombos(self):
        newCombos = tuple(self._combos)
        return newCombos

    def numberOfCombos(self):
        number = len(self._combos)
        return number

    def hasCombos(self):
        has = len(self._combos) > 0
        return has

    def indexOfCombo(self, aCombo):
        index = (-1 if not aCombo in self._combos else self._combos.index(aCombo))
        return index

    # Code from template association_GetMany
    def getComboItem(self, index):
        aComboItem = self._comboItems[index]
        return aComboItem

    def getComboItems(self):
        newComboItems = tuple(self._comboItems)
        return newComboItems

    def numberOfComboItems(self):
        number = len(self._comboItems)
        return number

    def hasComboItems(self):
        has = len(self._comboItems) > 0
        return has

    def indexOfComboItem(self, aComboItem):
        index = (-1 if not aComboItem in self._comboItems else self._comboItems.index(aComboItem))
        return index

    # Code from template association_GetMany
    def getLodge(self, index):
        aLodge = self._lodges[index]
        return aLodge

    def getLodges(self):
        newLodges = tuple(self._lodges)
        return newLodges

    def numberOfLodges(self):
        number = len(self._lodges)
        return number

    def hasLodges(self):
        has = len(self._lodges) > 0
        return has

    def indexOfLodge(self, aLodge):
        index = (-1 if not aLodge in self._lodges else self._lodges.index(aLodge))
        return index

    # Code from template association_GetMany
    def getBikeTour(self, index):
        aBikeTour = self._bikeTours[index]
        return aBikeTour

    def getBikeTours(self):
        newBikeTours = tuple(self._bikeTours)
        return newBikeTours

    def numberOfBikeTours(self):
        number = len(self._bikeTours)
        return number

    def hasBikeTours(self):
        has = len(self._bikeTours) > 0
        return has

    def indexOfBikeTour(self, aBikeTour):
        index = (-1 if not aBikeTour in self._bikeTours else self._bikeTours.index(aBikeTour))
        return index

    # Code from template association_SetOptionalOneToOne
    def setManager(self, aNewManager):
        wasSet = False
        if not (self._manager is None) and not self._manager == aNewManager and self == self._manager.getBikeTourPlus() :
            #Unable to setManager, as existing manager would become an orphan
            return wasSet
        self._manager = aNewManager
        anOldBikeTourPlus = (aNewManager.getBikeTourPlus()) if not (aNewManager is None) else None
        if not self == anOldBikeTourPlus :
            if not (anOldBikeTourPlus is None) :
                anOldBikeTourPlus.manager = None
            if not (self._manager is None) :
                self._manager.setBikeTourPlus(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfGuides():
        return 0

    # Code from template association_AddManyToOne
    def addGuide1(self, aEmail, aPassword, aName, aEmergencyContact):
        from .Guide import Guide
        return Guide(aEmail, aPassword, aName, aEmergencyContact, self)

    def addGuide2(self, aGuide):
        wasAdded = False
        if (aGuide) in self._guides :
            return False
        existingBikeTourPlus = aGuide.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aGuide.setBikeTourPlus(self)
        else :
            self._guides.append(aGuide)
        wasAdded = True
        return wasAdded

    def removeGuide(self, aGuide):
        wasRemoved = False
        #Unable to remove aGuide, as it must always have a bikeTourPlus
        if not self == aGuide.getBikeTourPlus() :
            self._guides.remove(aGuide)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addGuideAt(self, aGuide, index):
        wasAdded = False
        if self.addGuide(aGuide) :
            if index < 0 :
                index = 0
            if index > self.numberOfGuides() :
                index = self.numberOfGuides() - 1
            self._guides.remove(aGuide)
            self._guides.insert(index, aGuide)
            wasAdded = True
        return wasAdded

    def addOrMoveGuideAt(self, aGuide, index):
        wasAdded = False
        if (aGuide) in self._guides :
            if index < 0 :
                index = 0
            if index > self.numberOfGuides() :
                index = self.numberOfGuides() - 1
            self._guides.remove(aGuide)
            self._guides.insert(index, aGuide)
            wasAdded = True
        else :
            wasAdded = self.addGuideAt(aGuide, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfParticipants():
        return 0

    # Code from template association_AddManyToOne
    def addParticipant1(self, aEmail, aPassword, aName, aEmergencyContact, aNrWeeks, aWeekAvailableFrom, aWeekAvailableUntil, aLodgeRequired, aAuthorizationCode, aRefundedPercentageAmount):
        from .Participant import Participant
        return Participant(aEmail, aPassword, aName, aEmergencyContact, aNrWeeks, aWeekAvailableFrom, aWeekAvailableUntil, aLodgeRequired, aAuthorizationCode, aRefundedPercentageAmount, self)

    def addParticipant2(self, aParticipant):
        wasAdded = False
        if (aParticipant) in self._participants :
            return False
        existingBikeTourPlus = aParticipant.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aParticipant.setBikeTourPlus(self)
        else :
            self._participants.append(aParticipant)
        wasAdded = True
        return wasAdded

    def removeParticipant(self, aParticipant):
        wasRemoved = False
        #Unable to remove aParticipant, as it must always have a bikeTourPlus
        if not self == aParticipant.getBikeTourPlus() :
            self._participants.remove(aParticipant)
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

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfBookedItems():
        return 0

    # Code from template association_AddManyToOne
    def addBookedItem1(self, aQuantity, aParticipant, aItem):
        from .BookedItem import BookedItem
        return BookedItem(aQuantity, self, aParticipant, aItem)

    def addBookedItem2(self, aBookedItem):
        wasAdded = False
        if (aBookedItem) in self._bookedItems :
            return False
        existingBikeTourPlus = aBookedItem.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aBookedItem.setBikeTourPlus(self)
        else :
            self._bookedItems.append(aBookedItem)
        wasAdded = True
        return wasAdded

    def removeBookedItem(self, aBookedItem):
        wasRemoved = False
        #Unable to remove aBookedItem, as it must always have a bikeTourPlus
        if not self == aBookedItem.getBikeTourPlus() :
            self._bookedItems.remove(aBookedItem)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addBookedItemAt(self, aBookedItem, index):
        wasAdded = False
        if self.addBookedItem(aBookedItem) :
            if index < 0 :
                index = 0
            if index > self.numberOfBookedItems() :
                index = self.numberOfBookedItems() - 1
            self._bookedItems.remove(aBookedItem)
            self._bookedItems.insert(index, aBookedItem)
            wasAdded = True
        return wasAdded

    def addOrMoveBookedItemAt(self, aBookedItem, index):
        wasAdded = False
        if (aBookedItem) in self._bookedItems :
            if index < 0 :
                index = 0
            if index > self.numberOfBookedItems() :
                index = self.numberOfBookedItems() - 1
            self._bookedItems.remove(aBookedItem)
            self._bookedItems.insert(index, aBookedItem)
            wasAdded = True
        else :
            wasAdded = self.addBookedItemAt(aBookedItem, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfGear():
        return 0

    # Code from template association_AddManyToOne
    def addGear1(self, aName, aPricePerWeek):
        from .Gear import Gear
        return Gear(aName, aPricePerWeek, self)

    def addGear2(self, aGear):
        wasAdded = False
        if (aGear) in self._gear :
            return False
        existingBikeTourPlus = aGear.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aGear.setBikeTourPlus(self)
        else :
            self._gear.append(aGear)
        wasAdded = True
        return wasAdded

    def removeGear(self, aGear):
        wasRemoved = False
        #Unable to remove aGear, as it must always have a bikeTourPlus
        if not self == aGear.getBikeTourPlus() :
            self._gear.remove(aGear)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addGearAt(self, aGear, index):
        wasAdded = False
        if self.addGear(aGear) :
            if index < 0 :
                index = 0
            if index > self.numberOfGear() :
                index = self.numberOfGear() - 1
            self._gear.remove(aGear)
            self._gear.insert(index, aGear)
            wasAdded = True
        return wasAdded

    def addOrMoveGearAt(self, aGear, index):
        wasAdded = False
        if (aGear) in self._gear :
            if index < 0 :
                index = 0
            if index > self.numberOfGear() :
                index = self.numberOfGear() - 1
            self._gear.remove(aGear)
            self._gear.insert(index, aGear)
            wasAdded = True
        else :
            wasAdded = self.addGearAt(aGear, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfCombos():
        return 0

    # Code from template association_AddManyToOne
    def addCombo1(self, aName, aDiscount):
        from .Combo import Combo
        return Combo(aName, aDiscount, self)

    def addCombo2(self, aCombo):
        wasAdded = False
        if (aCombo) in self._combos :
            return False
        existingBikeTourPlus = aCombo.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aCombo.setBikeTourPlus(self)
        else :
            self._combos.append(aCombo)
        wasAdded = True
        return wasAdded

    def removeCombo(self, aCombo):
        wasRemoved = False
        #Unable to remove aCombo, as it must always have a bikeTourPlus
        if not self == aCombo.getBikeTourPlus() :
            self._combos.remove(aCombo)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addComboAt(self, aCombo, index):
        wasAdded = False
        if self.addCombo(aCombo) :
            if index < 0 :
                index = 0
            if index > self.numberOfCombos() :
                index = self.numberOfCombos() - 1
            self._combos.remove(aCombo)
            self._combos.insert(index, aCombo)
            wasAdded = True
        return wasAdded

    def addOrMoveComboAt(self, aCombo, index):
        wasAdded = False
        if (aCombo) in self._combos :
            if index < 0 :
                index = 0
            if index > self.numberOfCombos() :
                index = self.numberOfCombos() - 1
            self._combos.remove(aCombo)
            self._combos.insert(index, aCombo)
            wasAdded = True
        else :
            wasAdded = self.addComboAt(aCombo, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfComboItems():
        return 0

    # Code from template association_AddManyToOne
    def addComboItem1(self, aQuantity, aCombo, aGear):
        from .ComboItem import ComboItem
        return ComboItem(aQuantity, self, aCombo, aGear)

    def addComboItem2(self, aComboItem):
        wasAdded = False
        if (aComboItem) in self._comboItems :
            return False
        existingBikeTourPlus = aComboItem.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aComboItem.setBikeTourPlus(self)
        else :
            self._comboItems.append(aComboItem)
        wasAdded = True
        return wasAdded

    def removeComboItem(self, aComboItem):
        wasRemoved = False
        #Unable to remove aComboItem, as it must always have a bikeTourPlus
        if not self == aComboItem.getBikeTourPlus() :
            self._comboItems.remove(aComboItem)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addComboItemAt(self, aComboItem, index):
        wasAdded = False
        if self.addComboItem(aComboItem) :
            if index < 0 :
                index = 0
            if index > self.numberOfComboItems() :
                index = self.numberOfComboItems() - 1
            self._comboItems.remove(aComboItem)
            self._comboItems.insert(index, aComboItem)
            wasAdded = True
        return wasAdded

    def addOrMoveComboItemAt(self, aComboItem, index):
        wasAdded = False
        if (aComboItem) in self._comboItems :
            if index < 0 :
                index = 0
            if index > self.numberOfComboItems() :
                index = self.numberOfComboItems() - 1
            self._comboItems.remove(aComboItem)
            self._comboItems.insert(index, aComboItem)
            wasAdded = True
        else :
            wasAdded = self.addComboItemAt(aComboItem, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfLodges():
        return 0

    # Code from template association_AddManyToOne
    def addLodge1(self, aName, aAddress, aRating):
        from .Lodge import Lodge
        return Lodge(aName, aAddress, aRating, self)

    def addLodge2(self, aLodge):
        wasAdded = False
        if (aLodge) in self._lodges :
            return False
        existingBikeTourPlus = aLodge.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aLodge.setBikeTourPlus(self)
        else :
            self._lodges.append(aLodge)
        wasAdded = True
        return wasAdded

    def removeLodge(self, aLodge):
        wasRemoved = False
        #Unable to remove aLodge, as it must always have a bikeTourPlus
        if not self == aLodge.getBikeTourPlus() :
            self._lodges.remove(aLodge)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addLodgeAt(self, aLodge, index):
        wasAdded = False
        if self.addLodge(aLodge) :
            if index < 0 :
                index = 0
            if index > self.numberOfLodges() :
                index = self.numberOfLodges() - 1
            self._lodges.remove(aLodge)
            self._lodges.insert(index, aLodge)
            wasAdded = True
        return wasAdded

    def addOrMoveLodgeAt(self, aLodge, index):
        wasAdded = False
        if (aLodge) in self._lodges :
            if index < 0 :
                index = 0
            if index > self.numberOfLodges() :
                index = self.numberOfLodges() - 1
            self._lodges.remove(aLodge)
            self._lodges.insert(index, aLodge)
            wasAdded = True
        else :
            wasAdded = self.addLodgeAt(aLodge, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfBikeTours():
        return 0

    # Code from template association_AddManyToOne
    def addBikeTour1(self, aId, aStartWeek, aEndWeek, aGuide):
        from .BikeTour import BikeTour
        return BikeTour(aId, aStartWeek, aEndWeek, aGuide, self)

    def addBikeTour2(self, aBikeTour):
        wasAdded = False
        if (aBikeTour) in self._bikeTours :
            return False
        existingBikeTourPlus = aBikeTour.getBikeTourPlus()
        isNewBikeTourPlus = not (existingBikeTourPlus is None) and not self == existingBikeTourPlus
        if isNewBikeTourPlus :
            aBikeTour.setBikeTourPlus(self)
        else :
            self._bikeTours.append(aBikeTour)
        wasAdded = True
        return wasAdded

    def removeBikeTour(self, aBikeTour):
        wasRemoved = False
        #Unable to remove aBikeTour, as it must always have a bikeTourPlus
        if not self == aBikeTour.getBikeTourPlus() :
            self._bikeTours.remove(aBikeTour)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addBikeTourAt(self, aBikeTour, index):
        wasAdded = False
        if self.addBikeTour(aBikeTour) :
            if index < 0 :
                index = 0
            if index > self.numberOfBikeTours() :
                index = self.numberOfBikeTours() - 1
            self._bikeTours.remove(aBikeTour)
            self._bikeTours.insert(index, aBikeTour)
            wasAdded = True
        return wasAdded

    def addOrMoveBikeTourAt(self, aBikeTour, index):
        wasAdded = False
        if (aBikeTour) in self._bikeTours :
            if index < 0 :
                index = 0
            if index > self.numberOfBikeTours() :
                index = self.numberOfBikeTours() - 1
            self._bikeTours.remove(aBikeTour)
            self._bikeTours.insert(index, aBikeTour)
            wasAdded = True
        else :
            wasAdded = self.addBikeTourAt(aBikeTour, index)
        return wasAdded

    def delete(self):
        existingManager = self._manager
        self._manager = None
        if not (existingManager is None) :
            existingManager.delete()
            existingManager.setBikeTourPlus(None)

        while len(self._guides) > 0 :
            aGuide = self._guides[len(self._guides) - 1]
            aGuide.delete()
            self._guides.remove(aGuide)

        while len(self._participants) > 0 :
            aParticipant = self._participants[len(self._participants) - 1]
            aParticipant.delete()
            self._participants.remove(aParticipant)

        while len(self._bookedItems) > 0 :
            aBookedItem = self._bookedItems[len(self._bookedItems) - 1]
            aBookedItem.delete()
            self._bookedItems.remove(aBookedItem)

        while len(self._gear) > 0 :
            aGear = self._gear[len(self._gear) - 1]
            aGear.delete()
            self._gear.remove(aGear)

        while len(self._combos) > 0 :
            aCombo = self._combos[len(self._combos) - 1]
            aCombo.delete()
            self._combos.remove(aCombo)

        while len(self._comboItems) > 0 :
            aComboItem = self._comboItems[len(self._comboItems) - 1]
            aComboItem.delete()
            self._comboItems.remove(aComboItem)

        while len(self._lodges) > 0 :
            aLodge = self._lodges[len(self._lodges) - 1]
            aLodge.delete()
            self._lodges.remove(aLodge)

        while len(self._bikeTours) > 0 :
            aBikeTour = self._bikeTours[len(self._bikeTours) - 1]
            aBikeTour.delete()
            self._bikeTours.remove(aBikeTour)

    def __str__(self):
        return str(super().__str__()) + "[" + "nrWeeks" + ":" + str(self.getNrWeeks()) + "," + "priceOfGuidePerWeek" + ":" + str(self.getPriceOfGuidePerWeek()) + "]" + str(os.linesep) + "  " + "startDate" + "=" + str((((self.getStartDate().__str__().replaceAll("  ", "    ")) if not self.getStartDate() == self else "this") if not (self.getStartDate() is None) else "null")) + str(os.linesep) + "  " + "manager = " + ((format(id(self.getManager()), "x")) if not (self.getManager() is None) else "null")

    def getGear(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getGear1(argv[0])
        if len(argv) == 0 :
            return self.getGear2()
        raise TypeError("No method matches provided parameters")

    def addGuide(self, *argv):
        from .Guide import Guide
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) :
            return self.addGuide1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], Guide) :
            return self.addGuide2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addParticipant(self, *argv):
        from .Participant import Participant
        if len(argv) == 10 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], int) and isinstance(argv[5], int) and isinstance(argv[6], int) and isinstance(argv[7], bool) and isinstance(argv[8], str) and isinstance(argv[9], int) :
            return self.addParticipant1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], argv[9])
        if len(argv) == 1 and isinstance(argv[0], Participant) :
            return self.addParticipant2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addBookedItem(self, *argv):
        from .BookedItem import BookedItem
        from .Participant import Participant
        from .BookableItem import BookableItem
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], Participant) and isinstance(argv[2], BookableItem) :
            return self.addBookedItem1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], BookedItem) :
            return self.addBookedItem2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addGear(self, *argv):
        from .Gear import Gear
        if len(argv) == 2 and isinstance(argv[0], str) and isinstance(argv[1], int) :
            return self.addGear1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Gear) :
            return self.addGear2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addCombo(self, *argv):
        from .Combo import Combo
        if len(argv) == 2 and isinstance(argv[0], str) and isinstance(argv[1], int) :
            return self.addCombo1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Combo) :
            return self.addCombo2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addComboItem(self, *argv):
        from .ComboItem import ComboItem
        from .Combo import Combo
        from .Gear import Gear
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], Combo) and isinstance(argv[2], Gear) :
            return self.addComboItem1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], ComboItem) :
            return self.addComboItem2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addLodge(self, *argv):
        from .Lodge import Lodge
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], Lodge.LodgeRating) :
            return self.addLodge1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Lodge) :
            return self.addLodge2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addBikeTour(self, *argv):
        from .BikeTour import BikeTour
        from .Guide import Guide
        if len(argv) == 4 and isinstance(argv[0], int) and isinstance(argv[1], int) and isinstance(argv[2], int) and isinstance(argv[3], Guide) :
            return self.addBikeTour1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], BikeTour) :
            return self.addBikeTour2(argv[0])
        raise TypeError("No method matches provided parameters")
