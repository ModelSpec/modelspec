# %% NEW FILE AdvertisementPage BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 47 "model.ump"
# line 122 "model.ump"
from .Page import Page
import os

class AdvertisementPage(Page):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #AdvertisementPage Attributes
    #AdvertisementPage Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aPageName, aVisits, aFacepage, aBounceRate, aClickThroughRate, aConversionRate, aBusinessAccount):
        self._businessAccount = None
        self._conversionRate = None
        self._clickThroughRate = None
        self._bounceRate = None
        super().__init__(aPageName, aVisits, aFacepage)
        self._bounceRate = aBounceRate
        self._clickThroughRate = aClickThroughRate
        self._conversionRate = aConversionRate
        didAddBusinessAccount = self.setBusinessAccount(aBusinessAccount)
        if not didAddBusinessAccount :
            raise RuntimeError ("Unable to create advertisementPage due to businessAccount. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setBounceRate(self, aBounceRate):
        wasSet = False
        self._bounceRate = aBounceRate
        wasSet = True
        return wasSet

    def setClickThroughRate(self, aClickThroughRate):
        wasSet = False
        self._clickThroughRate = aClickThroughRate
        wasSet = True
        return wasSet

    def setConversionRate(self, aConversionRate):
        wasSet = False
        self._conversionRate = aConversionRate
        wasSet = True
        return wasSet

    def getBounceRate(self):
        return self._bounceRate

    def getClickThroughRate(self):
        return self._clickThroughRate

    def getConversionRate(self):
        return self._conversionRate

    # Code from template association_GetOne 
    def getBusinessAccount(self):
        return self._businessAccount

    # Code from template association_SetOneToMany 
    def setBusinessAccount(self, aBusinessAccount):
        wasSet = False
        if aBusinessAccount is None :
            return wasSet
        existingBusinessAccount = self._businessAccount
        self._businessAccount = aBusinessAccount
        if not (existingBusinessAccount is None) and not existingBusinessAccount == aBusinessAccount :
            existingBusinessAccount.removeAdvertisementPage(self)
        self._businessAccount.addAdvertisementPage(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderBusinessAccount = self._businessAccount
        self._businessAccount = None
        if not (placeholderBusinessAccount is None) :
            placeholderBusinessAccount.removeAdvertisementPage(self)
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "bounceRate" + ":" + str(self.getBounceRate()) + "," + "clickThroughRate" + ":" + str(self.getClickThroughRate()) + "," + "conversionRate" + ":" + str(self.getConversionRate()) + "]" + str(os.linesep) + "  " + "businessAccount = " + ((format(id(self.getBusinessAccount()), "x")) if not (self.getBusinessAccount() is None) else "null")
