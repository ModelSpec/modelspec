# %% NEW FILE AdminDashboardActivity BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 107 "model.ump"
# line 247 "model.ump"
from .AppCompatActivity import AppCompatActivity

class AdminDashboardActivity(AppCompatActivity):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #AdminDashboardActivity Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._adminViewModel = None
        super().__init__()

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getAdminViewModel(self):
        return self._adminViewModel

    def hasAdminViewModel(self):
        has = not (self._adminViewModel is None)
        return has

    # Code from template association_SetOptionalOneToOne 
    def setAdminViewModel(self, aNewAdminViewModel):
        wasSet = False
        if not (self._adminViewModel is None) and not self._adminViewModel == aNewAdminViewModel and self == self._adminViewModel.getAdminDashboardActivity() :
            #Unable to setAdminViewModel, as existing adminViewModel would become an orphan
            return wasSet
        self._adminViewModel = aNewAdminViewModel
        anOldAdminDashboardActivity = (aNewAdminViewModel.getAdminDashboardActivity()) if not (aNewAdminViewModel is None) else None
        if not self == anOldAdminDashboardActivity :
            if not (anOldAdminDashboardActivity is None) :
                anOldAdminDashboardActivity.adminViewModel = None
            if not (self._adminViewModel is None) :
                self._adminViewModel.setAdminDashboardActivity(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingAdminViewModel = self._adminViewModel
        self._adminViewModel = None
        if not (existingAdminViewModel is None) :
            existingAdminViewModel.delete()
        super().delete()