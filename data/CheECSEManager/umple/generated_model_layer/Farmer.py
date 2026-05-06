#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 24 "../model.ump"
# line 169 "../model.ump"
from .User import User
import os

class Farmer(User):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Farmer Attributes
    #Farmer Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword, aAddress, aCheECSEManager):
        self._cheECSEManager = None
        self._purchases = None
        self._address = None
        self._name = None
        super().__init__(aEmail, aPassword)
        self._name = None
        self._address = aAddress
        self._purchases = []
        didAddCheECSEManager = self.setCheECSEManager(aCheECSEManager)
        if not didAddCheECSEManager :
            raise RuntimeError ("Unable to create farmer due to cheECSEManager. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setAddress(self, aAddress):
        wasSet = False
        self._address = aAddress
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    def getAddress(self):
        return self._address

    # Code from template association_GetMany 
    def getPurchase(self, index):
        aPurchase = self._purchases[index]
        return aPurchase

    def getPurchases(self):
        newPurchases = tuple(self._purchases)
        return newPurchases

    def numberOfPurchases(self):
        number = len(self._purchases)
        return number

    def hasPurchases(self):
        has = len(self._purchases) > 0
        return has

    def indexOfPurchase(self, aPurchase):
        index = (-1 if not aPurchase in self._purchases else self._purchases.index(aPurchase))
        return index

    # Code from template association_GetOne 
    def getCheECSEManager(self):
        return self._cheECSEManager

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfPurchases():
        return 0

    # Code from template association_AddManyToOne 
    def addPurchase1(self, aTransactionDate, aCheECSEManager):
        from ..generated_model_layer.Purchase import Purchase
        return Purchase(aTransactionDate, aCheECSEManager, self)

    def addPurchase2(self, aPurchase):
        wasAdded = False
        if (aPurchase) in self._purchases :
            return False
        existingFarmer = aPurchase.getFarmer()
        isNewFarmer = not (existingFarmer is None) and not self == existingFarmer
        if isNewFarmer :
            aPurchase.setFarmer(self)
        else :
            self._purchases.append(aPurchase)
        wasAdded = True
        return wasAdded

    def removePurchase(self, aPurchase):
        wasRemoved = False
        #Unable to remove aPurchase, as it must always have a farmer
        if not self == aPurchase.getFarmer() :
            self._purchases.remove(aPurchase)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addPurchaseAt(self, aPurchase, index):
        wasAdded = False
        if self.addPurchase(aPurchase) :
            if index < 0 :
                index = 0
            if index > self.numberOfPurchases() :
                index = self.numberOfPurchases() - 1
            self._purchases.remove(aPurchase)
            self._purchases.insert(index, aPurchase)
            wasAdded = True
        return wasAdded

    def addOrMovePurchaseAt(self, aPurchase, index):
        wasAdded = False
        if (aPurchase) in self._purchases :
            if index < 0 :
                index = 0
            if index > self.numberOfPurchases() :
                index = self.numberOfPurchases() - 1
            self._purchases.remove(aPurchase)
            self._purchases.insert(index, aPurchase)
            wasAdded = True
        else :
            wasAdded = self.addPurchaseAt(aPurchase, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setCheECSEManager(self, aCheECSEManager):
        wasSet = False
        if aCheECSEManager is None :
            return wasSet
        existingCheECSEManager = self._cheECSEManager
        self._cheECSEManager = aCheECSEManager
        if not (existingCheECSEManager is None) and not existingCheECSEManager == aCheECSEManager :
            existingCheECSEManager.removeFarmer(self)
        self._cheECSEManager.addFarmer(self)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._purchases)
        while i > 0 :
            aPurchase = self._purchases[i - 1]
            aPurchase.delete()
            i -= 1

        placeholderCheECSEManager = self._cheECSEManager
        self._cheECSEManager = None
        if not (placeholderCheECSEManager is None) :
            placeholderCheECSEManager.removeFarmer(self)
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "address" + ":" + str(self.getAddress()) + "]" + str(os.linesep) + "  " + "cheECSEManager = " + ((format(id(self.getCheECSEManager()), "x")) if not (self.getCheECSEManager() is None) else "null")

    def addPurchase(self, *argv):
        from ..generated_model_layer.CheECSEManager import CheECSEManager
        from ..generated_model_layer.Purchase import Purchase
        from datetime import date
        if len(argv) == 2 and isinstance(argv[0], date) and isinstance(argv[1], CheECSEManager) :
            return self.addPurchase1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Purchase) :
            return self.addPurchase2(argv[0])
        raise TypeError("No method matches provided parameters")

