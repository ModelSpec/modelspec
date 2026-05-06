# %% NEW FILE ParticipantDashboardActivity BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 118 "model.ump"
# line 257 "model.ump"
from .AppCompatActivity import AppCompatActivity

class ParticipantDashboardActivity(AppCompatActivity):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #ParticipantDashboardActivity Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._participantViewModel = None
        super().__init__()

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getParticipantViewModel(self):
        return self._participantViewModel

    def hasParticipantViewModel(self):
        has = not (self._participantViewModel is None)
        return has

    # Code from template association_SetOptionalOneToOne 
    def setParticipantViewModel(self, aNewParticipantViewModel):
        wasSet = False
        if not (self._participantViewModel is None) and not self._participantViewModel == aNewParticipantViewModel and self == self._participantViewModel.getParticipantDashboardActivity() :
            #Unable to setParticipantViewModel, as existing participantViewModel would become an orphan
            return wasSet
        self._participantViewModel = aNewParticipantViewModel
        anOldParticipantDashboardActivity = (aNewParticipantViewModel.getParticipantDashboardActivity()) if not (aNewParticipantViewModel is None) else None
        if not self == anOldParticipantDashboardActivity :
            if not (anOldParticipantDashboardActivity is None) :
                anOldParticipantDashboardActivity.participantViewModel = None
            if not (self._participantViewModel is None) :
                self._participantViewModel.setParticipantDashboardActivity(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingParticipantViewModel = self._participantViewModel
        self._participantViewModel = None
        if not (existingParticipantViewModel is None) :
            existingParticipantViewModel.delete()
        super().delete()
