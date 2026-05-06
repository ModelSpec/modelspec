# %% NEW FILE PriceList BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 238 "model.ump"
# line 385 "model.ump"
import os
from enum import Enum, auto

class PriceList():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class SubscriptionPeriod(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Month = auto()
        HalfYear = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #PriceList Attributes
    #PriceList Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aPricingStrategy, aPayments):
        self._payments = None
        self._priceListItems = None
        self._pricingStrategy = None
        self._pricingStrategy = aPricingStrategy
        self._priceListItems = []
        didAddPayments = self.setPayments(aPayments)
        if not didAddPayments :
            raise RuntimeError ("Unable to create priceList due to payments. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setPricingStrategy(self, aPricingStrategy):
        wasSet = False
        self._pricingStrategy = aPricingStrategy
        wasSet = True
        return wasSet

    def getPricingStrategy(self):
        return self._pricingStrategy

    # Code from template association_GetMany
    def getPriceListItem(self, index):
        aPriceListItem = self._priceListItems[index]
        return aPriceListItem

    def getPriceListItems(self):
        newPriceListItems = tuple(self._priceListItems)
        return newPriceListItems

    def numberOfPriceListItems(self):
        number = len(self._priceListItems)
        return number

    def hasPriceListItems(self):
        has = len(self._priceListItems) > 0
        return has

    def indexOfPriceListItem(self, aPriceListItem):
        index = (-1 if not aPriceListItem in self._priceListItems else self._priceListItems.index(aPriceListItem))
        return index

    # Code from template association_GetOne
    def getPayments(self):
        return self._payments

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfPriceListItems():
        return 0

    # Code from template association_AddManyToOne
    def addPriceListItem1(self, aIsActive, aCountryCode, aSubscriptionPeriod, aCategory, aPrice):
        from .PriceListItem import PriceListItem
        return PriceListItem(aIsActive, aCountryCode, aSubscriptionPeriod, aCategory, aPrice, self)

    def addPriceListItem2(self, aPriceListItem):
        wasAdded = False
        if (aPriceListItem) in self._priceListItems :
            return False
        existingPriceList = aPriceListItem.getPriceList()
        isNewPriceList = not (existingPriceList is None) and not self == existingPriceList
        if isNewPriceList :
            aPriceListItem.setPriceList(self)
        else :
            self._priceListItems.append(aPriceListItem)
        wasAdded = True
        return wasAdded

    def removePriceListItem(self, aPriceListItem):
        wasRemoved = False
        #Unable to remove aPriceListItem, as it must always have a priceList
        if not self == aPriceListItem.getPriceList() :
            self._priceListItems.remove(aPriceListItem)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addPriceListItemAt(self, aPriceListItem, index):
        wasAdded = False
        if self.addPriceListItem(aPriceListItem) :
            if index < 0 :
                index = 0
            if index > self.numberOfPriceListItems() :
                index = self.numberOfPriceListItems() - 1
            self._priceListItems.remove(aPriceListItem)
            self._priceListItems.insert(index, aPriceListItem)
            wasAdded = True
        return wasAdded

    def addOrMovePriceListItemAt(self, aPriceListItem, index):
        wasAdded = False
        if (aPriceListItem) in self._priceListItems :
            if index < 0 :
                index = 0
            if index > self.numberOfPriceListItems() :
                index = self.numberOfPriceListItems() - 1
            self._priceListItems.remove(aPriceListItem)
            self._priceListItems.insert(index, aPriceListItem)
            wasAdded = True
        else :
            wasAdded = self.addPriceListItemAt(aPriceListItem, index)
        return wasAdded

    # Code from template association_SetOneToMany
    def setPayments(self, aPayments):
        wasSet = False
        if aPayments is None :
            return wasSet
        existingPayments = self._payments
        self._payments = aPayments
        if not (existingPayments is None) and not existingPayments == aPayments :
            existingPayments.removePriceList(self)
        self._payments.addPriceList(self)
        wasSet = True
        return wasSet

    def delete(self):

        while len(self._priceListItems) > 0 :
            aPriceListItem = self._priceListItems[len(self._priceListItems) - 1]
            aPriceListItem.delete()
            self._priceListItems.remove(aPriceListItem)

        placeholderPayments = self._payments
        self._payments = None
        if not (placeholderPayments is None) :
            placeholderPayments.removePriceList(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "pricingStrategy" + ":" + str(self.getPricingStrategy()) + "]" + str(os.linesep) + "  " + "payments = " + ((format(id(self.getPayments()), "x")) if not (self.getPayments() is None) else "null")

    def addPriceListItem(self, *argv):
        from .Subscription import Subscription
        from .PriceListItem import PriceListItem
        from .MoneyValue import MoneyValue
        if len(argv) == 5 and isinstance(argv[0], bool) and isinstance(argv[1], str) and isinstance(argv[2], Subscription.SubscriptionPeriod) and isinstance(argv[3], PriceListItem.PriceListItemCategory) and isinstance(argv[4], MoneyValue) :
            return self.addPriceListItem1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], PriceListItem) :
            return self.addPriceListItem2(argv[0])
        raise TypeError("No method matches provided parameters")
