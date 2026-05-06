#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 32 "../model.ump"
# line 174 "../model.ump"
import os

class WholesaleCompany():
    wholesalecompanysByName = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #WholesaleCompany Attributes
    #WholesaleCompany Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAddress, aCheECSEManager):
        self._cheECSEManager = None
        self._orders = None
        self._address = None
        self._name = None
        self._address = aAddress
        if not self.setName(aName) :
            raise RuntimeError ("Cannot create due to duplicate name. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._orders = []
        didAddCheECSEManager = self.setCheECSEManager(aCheECSEManager)
        if not didAddCheECSEManager :
            raise RuntimeError ("Unable to create company due to cheECSEManager. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        anOldName = self.getName()
        if not (anOldName is None) and anOldName == aName :
            return True
        if WholesaleCompany.hasWithName(aName) :
            return wasSet
        self._name = aName
        wasSet = True
        if not (anOldName is None) :
            WholesaleCompany.wholesalecompanysByName.pop(anOldName, None)
        WholesaleCompany.wholesalecompanysByName[aName] = self
        return wasSet

    def setAddress(self, aAddress):
        wasSet = False
        self._address = aAddress
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithName(aName):
        return WholesaleCompany.wholesalecompanysByName.get(aName)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithName(aName):
        return not (WholesaleCompany.getWithName(aName) is None)

    def getAddress(self):
        return self._address

    # Code from template association_GetMany 
    def getOrder(self, index):
        aOrder = self._orders[index]
        return aOrder

    def getOrders(self):
        newOrders = tuple(self._orders)
        return newOrders

    def numberOfOrders(self):
        number = len(self._orders)
        return number

    def hasOrders(self):
        has = len(self._orders) > 0
        return has

    def indexOfOrder(self, aOrder):
        index = (-1 if not aOrder in self._orders else self._orders.index(aOrder))
        return index

    # Code from template association_GetOne 
    def getCheECSEManager(self):
        return self._cheECSEManager

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfOrders():
        return 0

    # Code from template association_AddManyToOne 
    def addOrder1(self, aTransactionDate, aCheECSEManager, aNrCheeseWheels, aMonthsAged, aDeliveryDate):
        from ..generated_model_layer.Order import Order
        return Order(aTransactionDate, aCheECSEManager, aNrCheeseWheels, aMonthsAged, aDeliveryDate, self)

    def addOrder2(self, aOrder):
        wasAdded = False
        if (aOrder) in self._orders :
            return False
        existingCompany = aOrder.getCompany()
        isNewCompany = not (existingCompany is None) and not self == existingCompany
        if isNewCompany :
            aOrder.setCompany(self)
        else :
            self._orders.append(aOrder)
        wasAdded = True
        return wasAdded

    def removeOrder(self, aOrder):
        wasRemoved = False
        #Unable to remove aOrder, as it must always have a company
        if not self == aOrder.getCompany() :
            self._orders.remove(aOrder)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addOrderAt(self, aOrder, index):
        wasAdded = False
        if self.addOrder(aOrder) :
            if index < 0 :
                index = 0
            if index > self.numberOfOrders() :
                index = self.numberOfOrders() - 1
            self._orders.remove(aOrder)
            self._orders.insert(index, aOrder)
            wasAdded = True
        return wasAdded

    def addOrMoveOrderAt(self, aOrder, index):
        wasAdded = False
        if (aOrder) in self._orders :
            if index < 0 :
                index = 0
            if index > self.numberOfOrders() :
                index = self.numberOfOrders() - 1
            self._orders.remove(aOrder)
            self._orders.insert(index, aOrder)
            wasAdded = True
        else :
            wasAdded = self.addOrderAt(aOrder, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setCheECSEManager(self, aCheECSEManager):
        wasSet = False
        if aCheECSEManager is None :
            return wasSet
        existingCheECSEManager = self._cheECSEManager
        self._cheECSEManager = aCheECSEManager
        if not (existingCheECSEManager is None) and not existingCheECSEManager == aCheECSEManager :
            existingCheECSEManager.removeCompany(self)
        self._cheECSEManager.addCompany(self)
        wasSet = True
        return wasSet

    def delete(self):
        WholesaleCompany.wholesalecompanysByName.pop(self.getName(), None)
        i = len(self._orders)
        while i > 0 :
            aOrder = self._orders[i - 1]
            aOrder.delete()
            i -= 1

        placeholderCheECSEManager = self._cheECSEManager
        self._cheECSEManager = None
        if not (placeholderCheECSEManager is None) :
            placeholderCheECSEManager.removeCompany(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "address" + ":" + str(self.getAddress()) + "]" + str(os.linesep) + "  " + "cheECSEManager = " + ((format(id(self.getCheECSEManager()), "x")) if not (self.getCheECSEManager() is None) else "null")

    def addOrder(self, *argv):
        from ..generated_model_layer.CheECSEManager import CheECSEManager
        from ..generated_model_layer.Order import Order
        from datetime import date
        from ..generated_model_layer.CheeseWheel import CheeseWheel
        if len(argv) == 5 and isinstance(argv[0], date) and isinstance(argv[1], CheECSEManager) and isinstance(argv[2], int) and isinstance(argv[3], CheeseWheel.MaturationPeriod) and isinstance(argv[4], date) :
            return self.addOrder1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], Order) :
            return self.addOrder2(argv[0])
        raise TypeError("No method matches provided parameters")

