# %% NEW FILE RegistrationViewModel BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 89 "model.ump"
# line 222 "model.ump"
import os

class RegistrationViewModel():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #RegistrationViewModel Attributes
    #RegistrationViewModel Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aRepository, aOrganizerDashboardActivity):
        self._organizerDashboardActivity = None
        self._repository = None
        self._pendingRegistrations = None
        self._pendingRegistrations = []
        didAddRepository = self.setRepository(aRepository)
        if not didAddRepository :
            raise RuntimeError ("Unable to create registrationViewModel due to repository. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddOrganizerDashboardActivity = self.setOrganizerDashboardActivity(aOrganizerDashboardActivity)
        if not didAddOrganizerDashboardActivity :
            raise RuntimeError ("Unable to create registrationViewModel due to organizerDashboardActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template attribute_SetMany 
    def addPendingRegistration(self, aPendingRegistration):
        wasAdded = False
        wasAdded = self._pendingRegistrations.append(aPendingRegistration)
        return wasAdded

    def removePendingRegistration(self, aPendingRegistration):
        wasRemoved = False
        wasRemoved = self._pendingRegistrations.remove(aPendingRegistration)
        return wasRemoved

    # Code from template attribute_GetMany 
    def getPendingRegistration(self, index):
        aPendingRegistration = self._pendingRegistrations[index]
        return aPendingRegistration

    def getPendingRegistrations(self):
        newPendingRegistrations = self._pendingRegistrations.copy()
        return newPendingRegistrations

    def numberOfPendingRegistrations(self):
        number = len(self._pendingRegistrations)
        return number

    def hasPendingRegistrations(self):
        has = len(self._pendingRegistrations) > 0
        return has

    def indexOfPendingRegistration(self, aPendingRegistration):
        index = (-1 if not aPendingRegistration in self._pendingRegistrations else self._pendingRegistrations.index(aPendingRegistration))
        return index

    # Code from template association_GetOne 
    def getRepository(self):
        return self._repository

    # Code from template association_GetOne 
    def getOrganizerDashboardActivity(self):
        return self._organizerDashboardActivity

    # Code from template association_SetOneToOptionalOne 
    def setRepository(self, aNewRepository):
        wasSet = False
        if aNewRepository is None :
            #Unable to setRepository to null, as registrationViewModel must always be associated to a repository
            return wasSet
        existingRegistrationViewModel = aNewRepository.getRegistrationViewModel()
        if not (existingRegistrationViewModel is None) and not self == existingRegistrationViewModel :
            #Unable to setRepository, the current repository already has a registrationViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldRepository = self._repository
        self._repository = aNewRepository
        self._repository.setRegistrationViewModel(self)
        if not (anOldRepository is None) :
            anOldRepository.setRegistrationViewModel(None)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToOptionalOne 
    def setOrganizerDashboardActivity(self, aNewOrganizerDashboardActivity):
        wasSet = False
        if aNewOrganizerDashboardActivity is None :
            #Unable to setOrganizerDashboardActivity to null, as registrationViewModel must always be associated to a organizerDashboardActivity
            return wasSet
        existingRegistrationViewModel = aNewOrganizerDashboardActivity.getRegistrationViewModel()
        if not (existingRegistrationViewModel is None) and not self == existingRegistrationViewModel :
            #Unable to setOrganizerDashboardActivity, the current organizerDashboardActivity already has a registrationViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldOrganizerDashboardActivity = self._organizerDashboardActivity
        self._organizerDashboardActivity = aNewOrganizerDashboardActivity
        self._organizerDashboardActivity.setRegistrationViewModel(self)
        if not (anOldOrganizerDashboardActivity is None) :
            anOldOrganizerDashboardActivity.setRegistrationViewModel(None)
        wasSet = True
        return wasSet

    def delete(self):
        existingRepository = self._repository
        self._repository = None
        if not (existingRepository is None) :
            existingRepository.setRegistrationViewModel(None)
        existingOrganizerDashboardActivity = self._organizerDashboardActivity
        self._organizerDashboardActivity = None
        if not (existingOrganizerDashboardActivity is None) :
            existingOrganizerDashboardActivity.setRegistrationViewModel(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "repository = " + str(((format(id(self.getRepository()), "x")) if not (self.getRepository() is None) else "null")) + str(os.linesep) + "  " + "organizerDashboardActivity = " + ((format(id(self.getOrganizerDashboardActivity()), "x")) if not (self.getOrganizerDashboardActivity() is None) else "null")
