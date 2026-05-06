# %% NEW FILE OrganizerDashboardActivity BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 112 "model.ump"
# line 252 "model.ump"
from .AppCompatActivity import AppCompatActivity

class OrganizerDashboardActivity(AppCompatActivity):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #OrganizerDashboardActivity Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._registrationViewModel = None
        self._organizerViewModel = None
        super().__init__()

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getOrganizerViewModel(self):
        return self._organizerViewModel

    def hasOrganizerViewModel(self):
        has = not (self._organizerViewModel is None)
        return has

    # Code from template association_GetOne 
    def getRegistrationViewModel(self):
        return self._registrationViewModel

    def hasRegistrationViewModel(self):
        has = not (self._registrationViewModel is None)
        return has

    # Code from template association_SetOptionalOneToOne 
    def setOrganizerViewModel(self, aNewOrganizerViewModel):
        wasSet = False
        if not (self._organizerViewModel is None) and not self._organizerViewModel == aNewOrganizerViewModel and self == self._organizerViewModel.getOrganizerDashboardActivity() :
            #Unable to setOrganizerViewModel, as existing organizerViewModel would become an orphan
            return wasSet
        self._organizerViewModel = aNewOrganizerViewModel
        anOldOrganizerDashboardActivity = (aNewOrganizerViewModel.getOrganizerDashboardActivity()) if not (aNewOrganizerViewModel is None) else None
        if not self == anOldOrganizerDashboardActivity :
            if not (anOldOrganizerDashboardActivity is None) :
                anOldOrganizerDashboardActivity.organizerViewModel = None
            if not (self._organizerViewModel is None) :
                self._organizerViewModel.setOrganizerDashboardActivity(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToOne 
    def setRegistrationViewModel(self, aNewRegistrationViewModel):
        wasSet = False
        if not (self._registrationViewModel is None) and not self._registrationViewModel == aNewRegistrationViewModel and self == self._registrationViewModel.getOrganizerDashboardActivity() :
            #Unable to setRegistrationViewModel, as existing registrationViewModel would become an orphan
            return wasSet
        self._registrationViewModel = aNewRegistrationViewModel
        anOldOrganizerDashboardActivity = (aNewRegistrationViewModel.getOrganizerDashboardActivity()) if not (aNewRegistrationViewModel is None) else None
        if not self == anOldOrganizerDashboardActivity :
            if not (anOldOrganizerDashboardActivity is None) :
                anOldOrganizerDashboardActivity.registrationViewModel = None
            if not (self._registrationViewModel is None) :
                self._registrationViewModel.setOrganizerDashboardActivity(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingOrganizerViewModel = self._organizerViewModel
        self._organizerViewModel = None
        if not (existingOrganizerViewModel is None) :
            existingOrganizerViewModel.delete()
        existingRegistrationViewModel = self._registrationViewModel
        self._registrationViewModel = None
        if not (existingRegistrationViewModel is None) :
            existingRegistrationViewModel.delete()
        super().delete()
