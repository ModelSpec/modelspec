# %% NEW FILE OrganizerViewModel BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 84 "model.ump"
# line 217 "model.ump"
import os

class OrganizerViewModel():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #OrganizerViewModel Attributes
    #OrganizerViewModel Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEventRepo, aEventRepository, aOrganizerDashboardActivity, aManageEventActivity):
        self._manageEventActivity = None
        self._organizerDashboardActivity = None
        self._eventRepository = None
        self._eventRepo = None
        self._eventRepo = aEventRepo
        didAddEventRepository = self.setEventRepository(aEventRepository)
        if not didAddEventRepository :
            raise RuntimeError ("Unable to create organizerViewModel due to eventRepository. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddOrganizerDashboardActivity = self.setOrganizerDashboardActivity(aOrganizerDashboardActivity)
        if not didAddOrganizerDashboardActivity :
            raise RuntimeError ("Unable to create organizerViewModel due to organizerDashboardActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddManageEventActivity = self.setManageEventActivity(aManageEventActivity)
        if not didAddManageEventActivity :
            raise RuntimeError ("Unable to create organizerViewModel due to manageEventActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setEventRepo(self, aEventRepo):
        wasSet = False
        self._eventRepo = aEventRepo
        wasSet = True
        return wasSet

    def getEventRepo(self):
        return self._eventRepo

    # Code from template association_GetOne 
    def getEventRepository(self):
        return self._eventRepository

    # Code from template association_GetOne 
    def getOrganizerDashboardActivity(self):
        return self._organizerDashboardActivity

    # Code from template association_GetOne 
    def getManageEventActivity(self):
        return self._manageEventActivity

    # Code from template association_SetOneToOptionalOne 
    def setEventRepository(self, aNewEventRepository):
        wasSet = False
        if aNewEventRepository is None :
            #Unable to setEventRepository to null, as organizerViewModel must always be associated to a eventRepository
            return wasSet
        existingOrganizerViewModel = aNewEventRepository.getOrganizerViewModel()
        if not (existingOrganizerViewModel is None) and not self == existingOrganizerViewModel :
            #Unable to setEventRepository, the current eventRepository already has a organizerViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldEventRepository = self._eventRepository
        self._eventRepository = aNewEventRepository
        self._eventRepository.setOrganizerViewModel(self)
        if not (anOldEventRepository is None) :
            anOldEventRepository.setOrganizerViewModel(None)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToOptionalOne 
    def setOrganizerDashboardActivity(self, aNewOrganizerDashboardActivity):
        wasSet = False
        if aNewOrganizerDashboardActivity is None :
            #Unable to setOrganizerDashboardActivity to null, as organizerViewModel must always be associated to a organizerDashboardActivity
            return wasSet
        existingOrganizerViewModel = aNewOrganizerDashboardActivity.getOrganizerViewModel()
        if not (existingOrganizerViewModel is None) and not self == existingOrganizerViewModel :
            #Unable to setOrganizerDashboardActivity, the current organizerDashboardActivity already has a organizerViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldOrganizerDashboardActivity = self._organizerDashboardActivity
        self._organizerDashboardActivity = aNewOrganizerDashboardActivity
        self._organizerDashboardActivity.setOrganizerViewModel(self)
        if not (anOldOrganizerDashboardActivity is None) :
            anOldOrganizerDashboardActivity.setOrganizerViewModel(None)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToOptionalOne 
    def setManageEventActivity(self, aNewManageEventActivity):
        wasSet = False
        if aNewManageEventActivity is None :
            #Unable to setManageEventActivity to null, as organizerViewModel must always be associated to a manageEventActivity
            return wasSet
        existingOrganizerViewModel = aNewManageEventActivity.getOrganizerViewModel()
        if not (existingOrganizerViewModel is None) and not self == existingOrganizerViewModel :
            #Unable to setManageEventActivity, the current manageEventActivity already has a organizerViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldManageEventActivity = self._manageEventActivity
        self._manageEventActivity = aNewManageEventActivity
        self._manageEventActivity.setOrganizerViewModel(self)
        if not (anOldManageEventActivity is None) :
            anOldManageEventActivity.setOrganizerViewModel(None)
        wasSet = True
        return wasSet

    def delete(self):
        existingEventRepository = self._eventRepository
        self._eventRepository = None
        if not (existingEventRepository is None) :
            existingEventRepository.setOrganizerViewModel(None)
        existingOrganizerDashboardActivity = self._organizerDashboardActivity
        self._organizerDashboardActivity = None
        if not (existingOrganizerDashboardActivity is None) :
            existingOrganizerDashboardActivity.setOrganizerViewModel(None)
        existingManageEventActivity = self._manageEventActivity
        self._manageEventActivity = None
        if not (existingManageEventActivity is None) :
            existingManageEventActivity.setOrganizerViewModel(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "eventRepo" + "=" + str((((self.getEventRepo().__str__().replaceAll("  ", "    ")) if not self.getEventRepo() == self else "this") if not (self.getEventRepo() is None) else "null")) + str(os.linesep) + "  " + "eventRepository = " + str(((format(id(self.getEventRepository()), "x")) if not (self.getEventRepository() is None) else "null")) + str(os.linesep) + "  " + "organizerDashboardActivity = " + str(((format(id(self.getOrganizerDashboardActivity()), "x")) if not (self.getOrganizerDashboardActivity() is None) else "null")) + str(os.linesep) + "  " + "manageEventActivity = " + ((format(id(self.getManageEventActivity()), "x")) if not (self.getManageEventActivity() is None) else "null")
