#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 66 "../model.ump"
# line 199 "../model.ump"
from .Transaction import Transaction

class Purchase(Transaction):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Purchase Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTransactionDate, aCheECSEManager, aFarmer):
        self._cheeseWheels = None
        self._farmer = None
        super().__init__(aTransactionDate, aCheECSEManager)
        didAddFarmer = self.setFarmer(aFarmer)
        if not didAddFarmer :
            raise RuntimeError ("Unable to create purchase due to farmer. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._cheeseWheels = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getFarmer(self):
        return self._farmer

    # Code from template association_GetMany 
    def getCheeseWheel(self, index):
        aCheeseWheel = self._cheeseWheels[index]
        return aCheeseWheel

    def getCheeseWheels(self):
        newCheeseWheels = tuple(self._cheeseWheels)
        return newCheeseWheels

    def numberOfCheeseWheels(self):
        number = len(self._cheeseWheels)
        return number

    def hasCheeseWheels(self):
        has = len(self._cheeseWheels) > 0
        return has

    def indexOfCheeseWheel(self, aCheeseWheel):
        index = (-1 if not aCheeseWheel in self._cheeseWheels else self._cheeseWheels.index(aCheeseWheel))
        return index

    # Code from template association_SetOneToMany 
    def setFarmer(self, aFarmer):
        wasSet = False
        if aFarmer is None :
            return wasSet
        existingFarmer = self._farmer
        self._farmer = aFarmer
        if not (existingFarmer is None) and not existingFarmer == aFarmer :
            existingFarmer.removePurchase(self)
        self._farmer.addPurchase(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfCheeseWheels():
        return 0

    # Code from template association_AddManyToOne 
    def addCheeseWheel1(self, aMonthsAged, aIsSpoiled, aCheECSEManager):
        from ..generated_model_layer.CheeseWheel import CheeseWheel
        return CheeseWheel(aMonthsAged, aIsSpoiled, self, aCheECSEManager)

    def addCheeseWheel2(self, aCheeseWheel):
        wasAdded = False
        if (aCheeseWheel) in self._cheeseWheels :
            return False
        existingPurchase = aCheeseWheel.getPurchase()
        isNewPurchase = not (existingPurchase is None) and not self == existingPurchase
        if isNewPurchase :
            aCheeseWheel.setPurchase(self)
        else :
            self._cheeseWheels.append(aCheeseWheel)
        wasAdded = True
        return wasAdded

    def removeCheeseWheel(self, aCheeseWheel):
        wasRemoved = False
        #Unable to remove aCheeseWheel, as it must always have a purchase
        if not self == aCheeseWheel.getPurchase() :
            self._cheeseWheels.remove(aCheeseWheel)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addCheeseWheelAt(self, aCheeseWheel, index):
        wasAdded = False
        if self.addCheeseWheel(aCheeseWheel) :
            if index < 0 :
                index = 0
            if index > self.numberOfCheeseWheels() :
                index = self.numberOfCheeseWheels() - 1
            self._cheeseWheels.remove(aCheeseWheel)
            self._cheeseWheels.insert(index, aCheeseWheel)
            wasAdded = True
        return wasAdded

    def addOrMoveCheeseWheelAt(self, aCheeseWheel, index):
        wasAdded = False
        if (aCheeseWheel) in self._cheeseWheels :
            if index < 0 :
                index = 0
            if index > self.numberOfCheeseWheels() :
                index = self.numberOfCheeseWheels() - 1
            self._cheeseWheels.remove(aCheeseWheel)
            self._cheeseWheels.insert(index, aCheeseWheel)
            wasAdded = True
        else :
            wasAdded = self.addCheeseWheelAt(aCheeseWheel, index)
        return wasAdded

    def delete(self):
        placeholderFarmer = self._farmer
        self._farmer = None
        if not (placeholderFarmer is None) :
            placeholderFarmer.removePurchase(self)
        i = len(self._cheeseWheels)
        while i > 0 :
            aCheeseWheel = self._cheeseWheels[i - 1]
            aCheeseWheel.delete()
            i -= 1

        super().delete()

    def addCheeseWheel(self, *argv):
        from ..generated_model_layer.CheeseWheel import CheeseWheel
        from ..generated_model_layer.CheECSEManager import CheECSEManager
        if len(argv) == 3 and isinstance(argv[0], CheeseWheel.MaturationPeriod) and isinstance(argv[1], bool) and isinstance(argv[2], CheECSEManager) :
            return self.addCheeseWheel1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], CheeseWheel) :
            return self.addCheeseWheel2(argv[0])
        raise TypeError("No method matches provided parameters")

