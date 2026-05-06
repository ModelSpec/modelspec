# %% NEW FILE JobLog BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 31 "model.ump"
# line 101 "model.ump"
import os

class JobLog():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #JobLog Attributes
    #JobLog Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aHours, aPrice, aHouse, aCompany):
        self._company = None
        self._house = None
        self._Price = None
        self._Hours = None
        self._Hours = aHours
        self._Price = aPrice
        didAddHouse = self.setHouse(aHouse)
        if not didAddHouse :
            raise RuntimeError ("Unable to create jobLog due to house. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddCompany = self.setCompany(aCompany)
        if not didAddCompany :
            raise RuntimeError ("Unable to create jobLog due to company. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setHours(self, aHours):
        wasSet = False
        self._Hours = aHours
        wasSet = True
        return wasSet

    def setPrice(self, aPrice):
        wasSet = False
        self._Price = aPrice
        wasSet = True
        return wasSet

    def getHours(self):
        return self._Hours

    def getPrice(self):
        return self._Price

    # Code from template association_GetOne 
    def getHouse(self):
        return self._house

    # Code from template association_GetOne 
    def getCompany(self):
        return self._company

    # Code from template association_SetOneToMany 
    def setHouse(self, aHouse):
        wasSet = False
        if aHouse is None :
            return wasSet
        existingHouse = self._house
        self._house = aHouse
        if not (existingHouse is None) and not existingHouse == aHouse :
            existingHouse.removeJobLog(self)
        self._house.addJobLog(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setCompany(self, aCompany):
        wasSet = False
        if aCompany is None :
            return wasSet
        existingCompany = self._company
        self._company = aCompany
        if not (existingCompany is None) and not existingCompany == aCompany :
            existingCompany.removeJobLog(self)
        self._company.addJobLog(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderHouse = self._house
        self._house = None
        if not (placeholderHouse is None) :
            placeholderHouse.removeJobLog(self)
        placeholderCompany = self._company
        self._company = None
        if not (placeholderCompany is None) :
            placeholderCompany.removeJobLog(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "Hours" + ":" + str(self.getHours()) + "," + "Price" + ":" + str(self.getPrice()) + "]" + str(os.linesep) + "  " + "house = " + str(((format(id(self.getHouse()), "x")) if not (self.getHouse() is None) else "null")) + str(os.linesep) + "  " + "company = " + ((format(id(self.getCompany()), "x")) if not (self.getCompany() is None) else "null")
