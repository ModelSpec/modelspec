#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 102 "../model.ump"
# line 139 "../model.ump"

class TOWholesaleCompany():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOWholesaleCompany Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAddress):
        self._deliveryDates = None
        self._nrCheeseWheelsMissings = None
        self._nrCheeseWheelsOrdereds = None
        self._monthsAgeds = None
        self._orderDates = None
        self._address = None
        self._name = None
        self._name = aName
        self._address = aAddress
        self._orderDates = []
        self._monthsAgeds = []
        self._nrCheeseWheelsOrdereds = []
        self._nrCheeseWheelsMissings = []
        self._deliveryDates = []

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

    # Code from template attribute_SetMany 
    def addOrderDate(self, aOrderDate):
        wasAdded = False
        wasAdded = self._orderDates.append(aOrderDate)
        return wasAdded

    def removeOrderDate(self, aOrderDate):
        wasRemoved = False
        wasRemoved = self._orderDates.remove(aOrderDate)
        return wasRemoved

    # Code from template attribute_SetMany 
    def addMonthsAged(self, aMonthsAged):
        wasAdded = False
        wasAdded = self._monthsAgeds.append(aMonthsAged)
        return wasAdded

    def removeMonthsAged(self, aMonthsAged):
        wasRemoved = False
        wasRemoved = self._monthsAgeds.remove(aMonthsAged)
        return wasRemoved

    # Code from template attribute_SetMany 
    def addNrCheeseWheelsOrdered(self, aNrCheeseWheelsOrdered):
        wasAdded = False
        wasAdded = self._nrCheeseWheelsOrdereds.append(aNrCheeseWheelsOrdered)
        return wasAdded

    def removeNrCheeseWheelsOrdered(self, aNrCheeseWheelsOrdered):
        wasRemoved = False
        wasRemoved = self._nrCheeseWheelsOrdereds.remove(aNrCheeseWheelsOrdered)
        return wasRemoved

    # Code from template attribute_SetMany 
    def addNrCheeseWheelsMissing(self, aNrCheeseWheelsMissing):
        wasAdded = False
        wasAdded = self._nrCheeseWheelsMissings.append(aNrCheeseWheelsMissing)
        return wasAdded

    def removeNrCheeseWheelsMissing(self, aNrCheeseWheelsMissing):
        wasRemoved = False
        wasRemoved = self._nrCheeseWheelsMissings.remove(aNrCheeseWheelsMissing)
        return wasRemoved

    # Code from template attribute_SetMany 
    def addDeliveryDate(self, aDeliveryDate):
        wasAdded = False
        wasAdded = self._deliveryDates.append(aDeliveryDate)
        return wasAdded

    def removeDeliveryDate(self, aDeliveryDate):
        wasRemoved = False
        wasRemoved = self._deliveryDates.remove(aDeliveryDate)
        return wasRemoved

    def getName(self):
        return self._name

    def getAddress(self):
        return self._address

    # Code from template attribute_GetMany 
    def getOrderDate(self, index):
        aOrderDate = self._orderDates[index]
        return aOrderDate

    def getOrderDates(self):
        newOrderDates = self._orderDates.copy()
        return newOrderDates

    def numberOfOrderDates(self):
        number = len(self._orderDates)
        return number

    def hasOrderDates(self):
        has = len(self._orderDates) > 0
        return has

    def indexOfOrderDate(self, aOrderDate):
        index = (-1 if not aOrderDate in self._orderDates else self._orderDates.index(aOrderDate))
        return index

    # Code from template attribute_GetMany 
    def getMonthsAged(self, index):
        aMonthsAged = self._monthsAgeds[index]
        return aMonthsAged

    def getMonthsAgeds(self):
        newMonthsAgeds = self._monthsAgeds.copy()
        return newMonthsAgeds

    def numberOfMonthsAgeds(self):
        number = len(self._monthsAgeds)
        return number

    def hasMonthsAgeds(self):
        has = len(self._monthsAgeds) > 0
        return has

    def indexOfMonthsAged(self, aMonthsAged):
        index = (-1 if not aMonthsAged in self._monthsAgeds else self._monthsAgeds.index(aMonthsAged))
        return index

    # Code from template attribute_GetMany 
    def getNrCheeseWheelsOrdered(self, index):
        aNrCheeseWheelsOrdered = self._nrCheeseWheelsOrdereds[index]
        return aNrCheeseWheelsOrdered

    def getNrCheeseWheelsOrdereds(self):
        newNrCheeseWheelsOrdereds = self._nrCheeseWheelsOrdereds.copy()
        return newNrCheeseWheelsOrdereds

    def numberOfNrCheeseWheelsOrdereds(self):
        number = len(self._nrCheeseWheelsOrdereds)
        return number

    def hasNrCheeseWheelsOrdereds(self):
        has = len(self._nrCheeseWheelsOrdereds) > 0
        return has

    def indexOfNrCheeseWheelsOrdered(self, aNrCheeseWheelsOrdered):
        index = (-1 if not aNrCheeseWheelsOrdered in self._nrCheeseWheelsOrdereds else self._nrCheeseWheelsOrdereds.index(aNrCheeseWheelsOrdered))
        return index

    # Code from template attribute_GetMany 
    def getNrCheeseWheelsMissing(self, index):
        aNrCheeseWheelsMissing = self._nrCheeseWheelsMissings[index]
        return aNrCheeseWheelsMissing

    def getNrCheeseWheelsMissings(self):
        newNrCheeseWheelsMissings = self._nrCheeseWheelsMissings.copy()
        return newNrCheeseWheelsMissings

    def numberOfNrCheeseWheelsMissings(self):
        number = len(self._nrCheeseWheelsMissings)
        return number

    def hasNrCheeseWheelsMissings(self):
        has = len(self._nrCheeseWheelsMissings) > 0
        return has

    def indexOfNrCheeseWheelsMissing(self, aNrCheeseWheelsMissing):
        index = (-1 if not aNrCheeseWheelsMissing in self._nrCheeseWheelsMissings else self._nrCheeseWheelsMissings.index(aNrCheeseWheelsMissing))
        return index

    # Code from template attribute_GetMany 
    def getDeliveryDate(self, index):
        aDeliveryDate = self._deliveryDates[index]
        return aDeliveryDate

    def getDeliveryDates(self):
        newDeliveryDates = self._deliveryDates.copy()
        return newDeliveryDates

    def numberOfDeliveryDates(self):
        number = len(self._deliveryDates)
        return number

    def hasDeliveryDates(self):
        has = len(self._deliveryDates) > 0
        return has

    def indexOfDeliveryDate(self, aDeliveryDate):
        index = (-1 if not aDeliveryDate in self._deliveryDates else self._deliveryDates.index(aDeliveryDate))
        return index

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "address" + ":" + str(self.getAddress()) + "]"

