#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 71 "../model.ump"
# line 204 "../model.ump"
from .Transaction import Transaction
import os

class Order(Transaction):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Order Attributes
    #Order Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTransactionDate, aCheECSEManager, aNrCheeseWheels, aMonthsAged, aDeliveryDate, aCompany):
        self._cheeseWheels = None
        self._company = None
        self._deliveryDate = None
        self._monthsAged = None
        self._nrCheeseWheels = None
        super().__init__(aTransactionDate, aCheECSEManager)
        self._nrCheeseWheels = aNrCheeseWheels
        self._monthsAged = aMonthsAged
        self._deliveryDate = aDeliveryDate
        didAddCompany = self.setCompany(aCompany)
        if not didAddCompany :
            raise RuntimeError ("Unable to create order due to company. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._cheeseWheels = []

    #------------------------
    # INTERFACE
    #------------------------
    def setNrCheeseWheels(self, aNrCheeseWheels):
        wasSet = False
        self._nrCheeseWheels = aNrCheeseWheels
        wasSet = True
        return wasSet

    def setMonthsAged(self, aMonthsAged):
        wasSet = False
        self._monthsAged = aMonthsAged
        wasSet = True
        return wasSet

    def setDeliveryDate(self, aDeliveryDate):
        wasSet = False
        self._deliveryDate = aDeliveryDate
        wasSet = True
        return wasSet

    def getNrCheeseWheels(self):
        return self._nrCheeseWheels

    def getMonthsAged(self):
        return self._monthsAged

    def getDeliveryDate(self):
        return self._deliveryDate

    # Code from template association_GetOne 
    def getCompany(self):
        return self._company

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
    def setCompany(self, aCompany):
        wasSet = False
        if aCompany is None :
            return wasSet
        existingCompany = self._company
        self._company = aCompany
        if not (existingCompany is None) and not existingCompany == aCompany :
            existingCompany.removeOrder(self)
        self._company.addOrder(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfCheeseWheels():
        return 0

    # Code from template association_AddManyToOptionalOne 
    def addCheeseWheel(self, aCheeseWheel):
        wasAdded = False
        if (aCheeseWheel) in self._cheeseWheels :
            return False
        existingOrder = aCheeseWheel.getOrder()
        if existingOrder is None :
            aCheeseWheel.setOrder(self)
        elif not self == existingOrder :
            existingOrder.removeCheeseWheel(aCheeseWheel)
            self.addCheeseWheel(aCheeseWheel)
        else :
            self._cheeseWheels.append(aCheeseWheel)
        wasAdded = True
        return wasAdded

    def removeCheeseWheel(self, aCheeseWheel):
        wasRemoved = False
        if (aCheeseWheel) in self._cheeseWheels :
            self._cheeseWheels.remove(aCheeseWheel)
            aCheeseWheel.setOrder(None)
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
        placeholderCompany = self._company
        self._company = None
        if not (placeholderCompany is None) :
            placeholderCompany.removeOrder(self)

        while not self._cheeseWheels.isEmpty() :
            self._cheeseWheels[0].setOrder(None)

        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "nrCheeseWheels" + ":" + str(self.getNrCheeseWheels()) + "]" + str(os.linesep) + "  " + "monthsAged" + "=" + str((((self.getMonthsAged().__str__().replaceAll("  ", "    ")) if not self.getMonthsAged() == self else "this") if not (self.getMonthsAged() is None) else "null")) + str(os.linesep) + "  " + "deliveryDate" + "=" + str((((self.getDeliveryDate().__str__().replaceAll("  ", "    ")) if not self.getDeliveryDate() == self else "this") if not (self.getDeliveryDate() is None) else "null")) + str(os.linesep) + "  " + "company = " + ((format(id(self.getCompany()), "x")) if not (self.getCompany() is None) else "null")

