# %% NEW FILE ParticipantViewModel BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 94 "model.ump"
# line 227 "model.ump"

class ParticipantViewModel():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #ParticipantViewModel Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aParticipantDashboardActivity):
        self._participantDashboardActivity = None
        didAddParticipantDashboardActivity = self.setParticipantDashboardActivity(aParticipantDashboardActivity)
        if not didAddParticipantDashboardActivity :
            raise RuntimeError ("Unable to create participantViewModel due to participantDashboardActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getParticipantDashboardActivity(self):
        return self._participantDashboardActivity

    # Code from template association_SetOneToOptionalOne 
    def setParticipantDashboardActivity(self, aNewParticipantDashboardActivity):
        wasSet = False
        if aNewParticipantDashboardActivity is None :
            #Unable to setParticipantDashboardActivity to null, as participantViewModel must always be associated to a participantDashboardActivity
            return wasSet
        existingParticipantViewModel = aNewParticipantDashboardActivity.getParticipantViewModel()
        if not (existingParticipantViewModel is None) and not self == existingParticipantViewModel :
            #Unable to setParticipantDashboardActivity, the current participantDashboardActivity already has a participantViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldParticipantDashboardActivity = self._participantDashboardActivity
        self._participantDashboardActivity = aNewParticipantDashboardActivity
        self._participantDashboardActivity.setParticipantViewModel(self)
        if not (anOldParticipantDashboardActivity is None) :
            anOldParticipantDashboardActivity.setParticipantViewModel(None)
        wasSet = True
        return wasSet

    def delete(self):
        existingParticipantDashboardActivity = self._participantDashboardActivity
        self._participantDashboardActivity = None
        if not (existingParticipantDashboardActivity is None) :
            existingParticipantDashboardActivity.setParticipantViewModel(None)
