# %% NEW FILE PriceListItem BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 229 "model.ump"
# line 380 "model.ump"
import os
from enum import Enum, auto

class PriceListItem():
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

    class PriceListItemCategory(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        New = auto()
        Renewal = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #PriceListItem Attributes
    #PriceListItem Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aIsActive, aCountryCode, aSubscriptionPeriod, aCategory, aPrice, aPriceList):
        self._priceList = None
        self._price = None
        self._category = None
        self._subscriptionPeriod = None
        self._countryCode = None
        self._isActive = None
        self._isActive = aIsActive
        self._countryCode = aCountryCode
        self._subscriptionPeriod = aSubscriptionPeriod
        self._category = aCategory
        if not self.setPrice(aPrice) :
            raise RuntimeError ("Unable to create PriceListItem due to aPrice. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddPriceList = self.setPriceList(aPriceList)
        if not didAddPriceList :
            raise RuntimeError ("Unable to create priceListItem due to priceList. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setIsActive(self, aIsActive):
        wasSet = False
        self._isActive = aIsActive
        wasSet = True
        return wasSet

    def setCountryCode(self, aCountryCode):
        wasSet = False
        self._countryCode = aCountryCode
        wasSet = True
        return wasSet

    def setSubscriptionPeriod(self, aSubscriptionPeriod):
        wasSet = False
        self._subscriptionPeriod = aSubscriptionPeriod
        wasSet = True
        return wasSet

    def setCategory(self, aCategory):
        wasSet = False
        self._category = aCategory
        wasSet = True
        return wasSet

    def getIsActive(self):
        return self._isActive

    def getCountryCode(self):
        return self._countryCode

    def getSubscriptionPeriod(self):
        return self._subscriptionPeriod

    def getCategory(self):
        return self._category

    # Code from template association_GetOne
    def getPrice(self):
        return self._price

    # Code from template association_GetOne
    def getPriceList(self):
        return self._priceList

    # Code from template association_SetUnidirectionalOne
    def setPrice(self, aNewPrice):
        wasSet = False
        if not (aNewPrice is None) :
            self._price = aNewPrice
            wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setPriceList(self, aPriceList):
        wasSet = False
        if aPriceList is None :
            return wasSet
        existingPriceList = self._priceList
        self._priceList = aPriceList
        if not (existingPriceList is None) and not existingPriceList == aPriceList :
            existingPriceList.removePriceListItem(self)
        self._priceList.addPriceListItem(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._price = None
        placeholderPriceList = self._priceList
        self._priceList = None
        if not (placeholderPriceList is None) :
            placeholderPriceList.removePriceListItem(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "countryCode" + ":" + str(self.getCountryCode()) + "]" + str(os.linesep) + "  " + "isActive" + "=" + str((((self.getIsActive().__str__().replaceAll("  ", "    ")) if not self.getIsActive() == self else "this") if not (self.getIsActive() is None) else "null")) + str(os.linesep) + "  " + "subscriptionPeriod" + "=" + str((((self.getSubscriptionPeriod().__str__().replaceAll("  ", "    ")) if not self.getSubscriptionPeriod() == self else "this") if not (self.getSubscriptionPeriod() is None) else "null")) + str(os.linesep) + "  " + "category" + "=" + str((((self.getCategory().__str__().replaceAll("  ", "    ")) if not self.getCategory() == self else "this") if not (self.getCategory() is None) else "null")) + str(os.linesep) + "  " + "price = " + str(((format(id(self.getPrice()), "x")) if not (self.getPrice() is None) else "null")) + str(os.linesep) + "  " + "priceList = " + ((format(id(self.getPriceList()), "x")) if not (self.getPriceList() is None) else "null")
