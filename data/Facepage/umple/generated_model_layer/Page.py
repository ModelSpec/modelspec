# %% NEW FILE Page BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 31 "model.ump"
# line 107 "model.ump"
from abc import ABC, abstractmethod
import os

class Page(ABC):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Page Attributes
    #Page Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aPageName, aVisits, aFacepage):
        self._facepage = None
        self._visits = None
        self._pageName = None
        self._pageName = aPageName
        self._visits = aVisits
        didAddFacepage = self.setFacepage(aFacepage)
        if not didAddFacepage :
            raise RuntimeError ("Unable to create page due to facepage. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setPageName(self, aPageName):
        wasSet = False
        self._pageName = aPageName
        wasSet = True
        return wasSet

    def setVisits(self, aVisits):
        wasSet = False
        self._visits = aVisits
        wasSet = True
        return wasSet

    def getPageName(self):
        return self._pageName

    def getVisits(self):
        return self._visits

    # Code from template association_GetOne 
    def getFacepage(self):
        return self._facepage

    # Code from template association_SetOneToMany 
    def setFacepage(self, aFacepage):
        wasSet = False
        if aFacepage is None :
            return wasSet
        existingFacepage = self._facepage
        self._facepage = aFacepage
        if not (existingFacepage is None) and not existingFacepage == aFacepage :
            existingFacepage.removePage(self)
        self._facepage.addPage(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderFacepage = self._facepage
        self._facepage = None
        if not (placeholderFacepage is None) :
            placeholderFacepage.removePage(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "pageName" + ":" + str(self.getPageName()) + "," + "visits" + ":" + str(self.getVisits()) + "]" + str(os.linesep) + "  " + "facepage = " + ((format(id(self.getFacepage()), "x")) if not (self.getFacepage() is None) else "null")
