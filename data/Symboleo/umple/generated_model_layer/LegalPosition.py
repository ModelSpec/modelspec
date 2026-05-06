# %% NEW FILE LegalPosition BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 33 "model.ump"
import os

class LegalPosition():
    legalpositionsByName = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #LegalPosition Attributes
    #LegalPosition Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAntecedent, aConsequent, aContract, aDebtor, aCreditor):
        self._asset = None
        self._creditor = None
        self._debtor = None
        self._contract = None
        self._trigger = None
        self._consequent = None
        self._antecedent = None
        self._rightHolder = None
        self._liable = None
        self._performer = None
        self._name = None
        if not self.setName(aName) :
            raise RuntimeError ("Cannot create due to duplicate name. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._performer = []
        self._liable = []
        self._rightHolder = []
        didAddAntecedent = self.setAntecedent(aAntecedent)
        if not didAddAntecedent :
            raise RuntimeError ("Unable to create antecedentOf due to antecedent. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddConsequent = self.setConsequent(aConsequent)
        if not didAddConsequent :
            raise RuntimeError ("Unable to create consequentOf due to consequent. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddContract = self.setContract(aContract)
        if not didAddContract :
            raise RuntimeError ("Unable to create legalPosition due to contract. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddDebtor = self.setDebtor(aDebtor)
        if not didAddDebtor :
            raise RuntimeError ("Unable to create debt due to debtor. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddCreditor = self.setCreditor(aCreditor)
        if not didAddCreditor :
            raise RuntimeError ("Unable to create credit due to creditor. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        anOldName = self.getName()
        if not (anOldName is None) and anOldName == aName :
            return True
        if LegalPosition.hasWithName(aName) :
            return wasSet
        self._name = aName
        wasSet = True
        if not (anOldName is None) :
            LegalPosition.legalpositionsByName.pop(anOldName, None)
        LegalPosition.legalpositionsByName[aName] = self
        return wasSet

    def getName(self):
        return self._name

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithName(aName):
        return LegalPosition.legalpositionsByName.get(aName)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithName(aName):
        return not (LegalPosition.getWithName(aName) is None)

    # Code from template association_GetMany
    def getPerformer1(self, index):
        aPerformer = self._performer[index]
        return aPerformer

    def getPerformer2(self):
        newPerformer = tuple(self._performer)
        return newPerformer

    def numberOfPerformer(self):
        number = len(self._performer)
        return number

    def hasPerformer(self):
        has = len(self._performer) > 0
        return has

    def indexOfPerformer(self, aPerformer):
        index = (-1 if not aPerformer in self._performer else self._performer.index(aPerformer))
        return index

    # Code from template association_GetMany
    def getLiable1(self, index):
        aLiable = self._liable[index]
        return aLiable

    def getLiable2(self):
        newLiable = tuple(self._liable)
        return newLiable

    def numberOfLiable(self):
        number = len(self._liable)
        return number

    def hasLiable(self):
        has = len(self._liable) > 0
        return has

    def indexOfLiable(self, aLiable):
        index = (-1 if not aLiable in self._liable else self._liable.index(aLiable))
        return index

    # Code from template association_GetMany
    def getRightHolder1(self, index):
        aRightHolder = self._rightHolder[index]
        return aRightHolder

    def getRightHolder2(self):
        newRightHolder = tuple(self._rightHolder)
        return newRightHolder

    def numberOfRightHolder(self):
        number = len(self._rightHolder)
        return number

    def hasRightHolder(self):
        has = len(self._rightHolder) > 0
        return has

    def indexOfRightHolder(self, aRightHolder):
        index = (-1 if not aRightHolder in self._rightHolder else self._rightHolder.index(aRightHolder))
        return index

    # Code from template association_GetOne
    def getAntecedent(self):
        return self._antecedent

    # Code from template association_GetOne
    def getConsequent(self):
        return self._consequent

    # Code from template association_GetOne
    def getTrigger(self):
        return self._trigger

    def hasTrigger(self):
        has = not (self._trigger is None)
        return has

    # Code from template association_GetOne
    def getContract(self):
        return self._contract

    # Code from template association_GetOne
    def getDebtor(self):
        return self._debtor

    # Code from template association_GetOne
    def getCreditor(self):
        return self._creditor

    # Code from template association_GetOne
    def getAsset(self):
        return self._asset

    def hasAsset(self):
        has = not (self._asset is None)
        return has

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfPerformer():
        return 0

    # Code from template association_AddManyToManyMethod
    def addPerformer(self, aPerformer):
        wasAdded = False
        if (aPerformer) in self._performer :
            return False
        self._performer.append(aPerformer)
        if aPerformer.indexOfPerformerOf(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aPerformer.addPerformerOf(self)
            if not wasAdded :
                self._performer.remove(aPerformer)
        return wasAdded

    # Code from template association_RemoveMany
    def removePerformer(self, aPerformer):
        wasRemoved = False
        if not (aPerformer) in self._performer :
            return wasRemoved
        oldIndex = (-1 if not aPerformer in self._performer else self._performer.index(aPerformer))
        self._performer.remove(oldIndex)
        if aPerformer.indexOfPerformerOf(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aPerformer.removePerformerOf(self)
            if not wasRemoved :
                self._performer.insert(oldIndex, aPerformer)
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addPerformerAt(self, aPerformer, index):
        wasAdded = False
        if self.addPerformer(aPerformer) :
            if index < 0 :
                index = 0
            if index > self.numberOfPerformer() :
                index = self.numberOfPerformer() - 1
            self._performer.remove(aPerformer)
            self._performer.insert(index, aPerformer)
            wasAdded = True
        return wasAdded

    def addOrMovePerformerAt(self, aPerformer, index):
        wasAdded = False
        if (aPerformer) in self._performer :
            if index < 0 :
                index = 0
            if index > self.numberOfPerformer() :
                index = self.numberOfPerformer() - 1
            self._performer.remove(aPerformer)
            self._performer.insert(index, aPerformer)
            wasAdded = True
        else :
            wasAdded = self.addPerformerAt(aPerformer, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfLiable():
        return 0

    # Code from template association_AddManyToManyMethod
    def addLiable(self, aLiable):
        wasAdded = False
        if (aLiable) in self._liable :
            return False
        self._liable.append(aLiable)
        if aLiable.indexOfLiableOf(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aLiable.addLiableOf(self)
            if not wasAdded :
                self._liable.remove(aLiable)
        return wasAdded

    # Code from template association_RemoveMany
    def removeLiable(self, aLiable):
        wasRemoved = False
        if not (aLiable) in self._liable :
            return wasRemoved
        oldIndex = (-1 if not aLiable in self._liable else self._liable.index(aLiable))
        self._liable.remove(oldIndex)
        if aLiable.indexOfLiableOf(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aLiable.removeLiableOf(self)
            if not wasRemoved :
                self._liable.insert(oldIndex, aLiable)
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addLiableAt(self, aLiable, index):
        wasAdded = False
        if self.addLiable(aLiable) :
            if index < 0 :
                index = 0
            if index > self.numberOfLiable() :
                index = self.numberOfLiable() - 1
            self._liable.remove(aLiable)
            self._liable.insert(index, aLiable)
            wasAdded = True
        return wasAdded

    def addOrMoveLiableAt(self, aLiable, index):
        wasAdded = False
        if (aLiable) in self._liable :
            if index < 0 :
                index = 0
            if index > self.numberOfLiable() :
                index = self.numberOfLiable() - 1
            self._liable.remove(aLiable)
            self._liable.insert(index, aLiable)
            wasAdded = True
        else :
            wasAdded = self.addLiableAt(aLiable, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfRightHolder():
        return 0

    # Code from template association_AddManyToManyMethod
    def addRightHolder(self, aRightHolder):
        wasAdded = False
        if (aRightHolder) in self._rightHolder :
            return False
        self._rightHolder.append(aRightHolder)
        if aRightHolder.indexOfRightHolderOf(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aRightHolder.addRightHolderOf(self)
            if not wasAdded :
                self._rightHolder.remove(aRightHolder)
        return wasAdded

    # Code from template association_RemoveMany
    def removeRightHolder(self, aRightHolder):
        wasRemoved = False
        if not (aRightHolder) in self._rightHolder :
            return wasRemoved
        oldIndex = (-1 if not aRightHolder in self._rightHolder else self._rightHolder.index(aRightHolder))
        self._rightHolder.remove(oldIndex)
        if aRightHolder.indexOfRightHolderOf(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aRightHolder.removeRightHolderOf(self)
            if not wasRemoved :
                self._rightHolder.insert(oldIndex, aRightHolder)
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addRightHolderAt(self, aRightHolder, index):
        wasAdded = False
        if self.addRightHolder(aRightHolder) :
            if index < 0 :
                index = 0
            if index > self.numberOfRightHolder() :
                index = self.numberOfRightHolder() - 1
            self._rightHolder.remove(aRightHolder)
            self._rightHolder.insert(index, aRightHolder)
            wasAdded = True
        return wasAdded

    def addOrMoveRightHolderAt(self, aRightHolder, index):
        wasAdded = False
        if (aRightHolder) in self._rightHolder :
            if index < 0 :
                index = 0
            if index > self.numberOfRightHolder() :
                index = self.numberOfRightHolder() - 1
            self._rightHolder.remove(aRightHolder)
            self._rightHolder.insert(index, aRightHolder)
            wasAdded = True
        else :
            wasAdded = self.addRightHolderAt(aRightHolder, index)
        return wasAdded

    # Code from template association_SetOneToMany
    def setAntecedent(self, aAntecedent):
        wasSet = False
        if aAntecedent is None :
            return wasSet
        existingAntecedent = self._antecedent
        self._antecedent = aAntecedent
        if not (existingAntecedent is None) and not existingAntecedent == aAntecedent :
            existingAntecedent.removeAntecedentOf(self)
        self._antecedent.addAntecedentOf(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setConsequent(self, aConsequent):
        wasSet = False
        if aConsequent is None :
            return wasSet
        existingConsequent = self._consequent
        self._consequent = aConsequent
        if not (existingConsequent is None) and not existingConsequent == aConsequent :
            existingConsequent.removeConsequentOf(self)
        self._consequent.addConsequentOf(self)
        wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOptionalOne
    def setTrigger(self, aNewTrigger):
        wasSet = False
        self._trigger = aNewTrigger
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMandatoryMany
    def setContract(self, aContract):
        from .Contract import Contract
        wasSet = False
        #Must provide contract to legalPosition
        if aContract is None :
            return wasSet
        if not (self._contract is None) and self._contract.numberOfLegalPositions() <= Contract.minimumNumberOfLegalPositions() :
            return wasSet
        existingContract = self._contract
        self._contract = aContract
        if not (existingContract is None) and not existingContract == aContract :
            didRemove = existingContract.removeLegalPosition(self)
            if not didRemove :
                self._contract = existingContract
                return wasSet
        self._contract.addLegalPosition(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setDebtor(self, aDebtor):
        wasSet = False
        if aDebtor is None :
            return wasSet
        existingDebtor = self._debtor
        self._debtor = aDebtor
        if not (existingDebtor is None) and not existingDebtor == aDebtor :
            existingDebtor.removeDebt(self)
        self._debtor.addDebt(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setCreditor(self, aCreditor):
        wasSet = False
        if aCreditor is None :
            return wasSet
        existingCreditor = self._creditor
        self._creditor = aCreditor
        if not (existingCreditor is None) and not existingCreditor == aCreditor :
            existingCreditor.removeCredit(self)
        self._creditor.addCredit(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany
    def setAsset(self, aAsset):
        wasSet = False
        existingAsset = self._asset
        self._asset = aAsset
        if not (existingAsset is None) and not existingAsset == aAsset :
            existingAsset.removeLegalPosition(self)
        if not (aAsset is None) :
            aAsset.addLegalPosition(self)
        wasSet = True
        return wasSet

    def delete(self):
        LegalPosition.legalpositionsByName.pop(self.getName(), None)
        copyOfPerformer = self._performer.copy()
        self._performer.clear()
        for aPerformer in copyOfPerformer:
            aPerformer.removePerformerOf(self)

        copyOfLiable = self._liable.copy()
        self._liable.clear()
        for aLiable in copyOfLiable:
            aLiable.removeLiableOf(self)

        copyOfRightHolder = self._rightHolder.copy()
        self._rightHolder.clear()
        for aRightHolder in copyOfRightHolder:
            aRightHolder.removeRightHolderOf(self)

        placeholderAntecedent = self._antecedent
        self._antecedent = None
        if not (placeholderAntecedent is None) :
            placeholderAntecedent.removeAntecedentOf(self)
        placeholderConsequent = self._consequent
        self._consequent = None
        if not (placeholderConsequent is None) :
            placeholderConsequent.removeConsequentOf(self)
        self._trigger = None
        placeholderContract = self._contract
        self._contract = None
        if not (placeholderContract is None) :
            placeholderContract.removeLegalPosition(self)
        placeholderDebtor = self._debtor
        self._debtor = None
        if not (placeholderDebtor is None) :
            placeholderDebtor.removeDebt(self)
        placeholderCreditor = self._creditor
        self._creditor = None
        if not (placeholderCreditor is None) :
            placeholderCreditor.removeCredit(self)
        if not (self._asset is None) :
            placeholderAsset = self._asset
            self._asset = None
            placeholderAsset.removeLegalPosition(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "]" + str(os.linesep) + "  " + "antecedent = " + str(((format(id(self.getAntecedent()), "x")) if not (self.getAntecedent() is None) else "null")) + str(os.linesep) + "  " + "consequent = " + str(((format(id(self.getConsequent()), "x")) if not (self.getConsequent() is None) else "null")) + str(os.linesep) + "  " + "trigger = " + str(((format(id(self.getTrigger()), "x")) if not (self.getTrigger() is None) else "null")) + str(os.linesep) + "  " + "contract = " + str(((format(id(self.getContract()), "x")) if not (self.getContract() is None) else "null")) + str(os.linesep) + "  " + "debtor = " + str(((format(id(self.getDebtor()), "x")) if not (self.getDebtor() is None) else "null")) + str(os.linesep) + "  " + "creditor = " + str(((format(id(self.getCreditor()), "x")) if not (self.getCreditor() is None) else "null")) + str(os.linesep) + "  " + "asset = " + ((format(id(self.getAsset()), "x")) if not (self.getAsset() is None) else "null")

    def getPerformer(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getPerformer1(argv[0])
        if len(argv) == 0 :
            return self.getPerformer2()
        raise TypeError("No method matches provided parameters")

    def getLiable(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getLiable1(argv[0])
        if len(argv) == 0 :
            return self.getLiable2()
        raise TypeError("No method matches provided parameters")

    def getRightHolder(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getRightHolder1(argv[0])
        if len(argv) == 0 :
            return self.getRightHolder2()
        raise TypeError("No method matches provided parameters")
