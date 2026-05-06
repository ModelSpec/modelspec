# %% NEW FILE ManageCategoriesActivity BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 123 "model.ump"
# line 262 "model.ump"
from .AppCompatActivity import AppCompatActivity

class ManageCategoriesActivity(AppCompatActivity):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #ManageCategoriesActivity Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._categoryViewModel = None
        super().__init__()

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getCategoryViewModel(self):
        return self._categoryViewModel

    def hasCategoryViewModel(self):
        has = not (self._categoryViewModel is None)
        return has

    # Code from template association_SetOptionalOneToOne 
    def setCategoryViewModel(self, aNewCategoryViewModel):
        wasSet = False
        if not (self._categoryViewModel is None) and not self._categoryViewModel == aNewCategoryViewModel and self == self._categoryViewModel.getManageCategoriesActivity() :
            #Unable to setCategoryViewModel, as existing categoryViewModel would become an orphan
            return wasSet
        self._categoryViewModel = aNewCategoryViewModel
        anOldManageCategoriesActivity = (aNewCategoryViewModel.getManageCategoriesActivity()) if not (aNewCategoryViewModel is None) else None
        if not self == anOldManageCategoriesActivity :
            if not (anOldManageCategoriesActivity is None) :
                anOldManageCategoriesActivity.categoryViewModel = None
            if not (self._categoryViewModel is None) :
                self._categoryViewModel.setManageCategoriesActivity(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingCategoryViewModel = self._categoryViewModel
        self._categoryViewModel = None
        if not (existingCategoryViewModel is None) :
            existingCategoryViewModel.delete()
        super().delete()
