# %% NEW FILE ManageEventActivity BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 128 "model.ump"
# line 267 "model.ump"
from .AppCompatActivity import AppCompatActivity
import os

class ManageEventActivity(AppCompatActivity):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #ManageEventActivity Attributes
    #ManageEventActivity Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aIsEditMode, aEventToEdit, aOrganizerId, aSelectedCategoryId):
        self._categoryViewModel = None
        self._organizerViewModel = None
        self._categoryList = None
        self._selectedCategoryId = None
        self._organizerId = None
        self._eventToEdit = None
        self._isEditMode = None
        super().__init__()
        self._isEditMode = aIsEditMode
        self._eventToEdit = aEventToEdit
        self._organizerId = aOrganizerId
        self._selectedCategoryId = aSelectedCategoryId
        self._categoryList = []

    #------------------------
    # INTERFACE
    #------------------------
    def setIsEditMode(self, aIsEditMode):
        wasSet = False
        self._isEditMode = aIsEditMode
        wasSet = True
        return wasSet

    def setEventToEdit(self, aEventToEdit):
        wasSet = False
        self._eventToEdit = aEventToEdit
        wasSet = True
        return wasSet

    def setOrganizerId(self, aOrganizerId):
        wasSet = False
        self._organizerId = aOrganizerId
        wasSet = True
        return wasSet

    def setSelectedCategoryId(self, aSelectedCategoryId):
        wasSet = False
        self._selectedCategoryId = aSelectedCategoryId
        wasSet = True
        return wasSet

    # Code from template attribute_SetMany 
    def addCategoryList(self, aCategoryList):
        wasAdded = False
        wasAdded = self._categoryList.append(aCategoryList)
        return wasAdded

    def removeCategoryList(self, aCategoryList):
        wasRemoved = False
        wasRemoved = self._categoryList.remove(aCategoryList)
        return wasRemoved

    def getIsEditMode(self):
        return self._isEditMode

    def getEventToEdit(self):
        return self._eventToEdit

    def getOrganizerId(self):
        return self._organizerId

    def getSelectedCategoryId(self):
        return self._selectedCategoryId

    # Code from template attribute_GetMany 
    def getCategoryList1(self, index):
        aCategoryList = self._categoryList[index]
        return aCategoryList

    def getCategoryList2(self):
        newCategoryList = self._categoryList.copy()
        return newCategoryList

    def numberOfCategoryList(self):
        number = len(self._categoryList)
        return number

    def hasCategoryList(self):
        has = len(self._categoryList) > 0
        return has

    def indexOfCategoryList(self, aCategoryList):
        index = (-1 if not aCategoryList in self._categoryList else self._categoryList.index(aCategoryList))
        return index

    # Code from template association_GetOne 
    def getOrganizerViewModel(self):
        return self._organizerViewModel

    def hasOrganizerViewModel(self):
        has = not (self._organizerViewModel is None)
        return has

    # Code from template association_GetOne 
    def getCategoryViewModel(self):
        return self._categoryViewModel

    def hasCategoryViewModel(self):
        has = not (self._categoryViewModel is None)
        return has

    # Code from template association_SetOptionalOneToOne 
    def setOrganizerViewModel(self, aNewOrganizerViewModel):
        wasSet = False
        if not (self._organizerViewModel is None) and not self._organizerViewModel == aNewOrganizerViewModel and self == self._organizerViewModel.getManageEventActivity() :
            #Unable to setOrganizerViewModel, as existing organizerViewModel would become an orphan
            return wasSet
        self._organizerViewModel = aNewOrganizerViewModel
        anOldManageEventActivity = (aNewOrganizerViewModel.getManageEventActivity()) if not (aNewOrganizerViewModel is None) else None
        if not self == anOldManageEventActivity :
            if not (anOldManageEventActivity is None) :
                anOldManageEventActivity.organizerViewModel = None
            if not (self._organizerViewModel is None) :
                self._organizerViewModel.setManageEventActivity(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOne 
    def setCategoryViewModel(self, aNewCategoryViewModel):
        wasSet = False
        if not (self._categoryViewModel is None) and not self._categoryViewModel == aNewCategoryViewModel and self == self._categoryViewModel.getManageEventActivity() :
            #Unable to setCategoryViewModel, as existing categoryViewModel would become an orphan
            return wasSet
        self._categoryViewModel = aNewCategoryViewModel
        anOldManageEventActivity = (aNewCategoryViewModel.getManageEventActivity()) if not (aNewCategoryViewModel is None) else None
        if not self == anOldManageEventActivity :
            if not (anOldManageEventActivity is None) :
                anOldManageEventActivity.categoryViewModel = None
            if not (self._categoryViewModel is None) :
                self._categoryViewModel.setManageEventActivity(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingOrganizerViewModel = self._organizerViewModel
        self._organizerViewModel = None
        if not (existingOrganizerViewModel is None) :
            existingOrganizerViewModel.delete()
        existingCategoryViewModel = self._categoryViewModel
        self._categoryViewModel = None
        if not (existingCategoryViewModel is None) :
            existingCategoryViewModel.delete()
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "isEditMode" + ":" + str(self.getIsEditMode()) + "," + "organizerId" + ":" + str(self.getOrganizerId()) + "," + "selectedCategoryId" + ":" + str(self.getSelectedCategoryId()) + "]" + str(os.linesep) + "  " + "eventToEdit" + "=" + str((((self.getEventToEdit().__str__().replaceAll("  ", "    ")) if not self.getEventToEdit() == self else "this") if not (self.getEventToEdit() is None) else "null")) + str(os.linesep) + "  " + "organizerViewModel = " + str(((format(id(self.getOrganizerViewModel()), "x")) if not (self.getOrganizerViewModel() is None) else "null")) + str(os.linesep) + "  " + "categoryViewModel = " + ((format(id(self.getCategoryViewModel()), "x")) if not (self.getCategoryViewModel() is None) else "null")

    def getCategoryList(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getCategoryList1(argv[0])
        if len(argv) == 0 :
            return self.getCategoryList2()
        raise TypeError("No method matches provided parameters")
