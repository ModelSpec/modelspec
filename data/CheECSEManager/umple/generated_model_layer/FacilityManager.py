#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 20 "../model.ump"
# line 164 "../model.ump"
from .User import User

class FacilityManager(User):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #FacilityManager Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword, aCheECSEManager):
        self._cheECSEManager = None
        super().__init__(aEmail, aPassword)
        didAddCheECSEManager = self.setCheECSEManager(aCheECSEManager)
        if not didAddCheECSEManager :
            raise RuntimeError ("Unable to create manager due to cheECSEManager. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getCheECSEManager(self):
        return self._cheECSEManager

    # Code from template association_SetOneToOptionalOne 
    def setCheECSEManager(self, aNewCheECSEManager):
        wasSet = False
        if aNewCheECSEManager is None :
            #Unable to setCheECSEManager to null, as manager must always be associated to a cheECSEManager
            return wasSet
        existingManager = aNewCheECSEManager.getManager()
        if not (existingManager is None) and not self == existingManager :
            #Unable to setCheECSEManager, the current cheECSEManager already has a manager, which would be orphaned if it were re-assigned
            return wasSet
        anOldCheECSEManager = self._cheECSEManager
        self._cheECSEManager = aNewCheECSEManager
        self._cheECSEManager.setManager(self)
        if not (anOldCheECSEManager is None) :
            anOldCheECSEManager.setManager(None)
        wasSet = True
        return wasSet

    def delete(self):
        existingCheECSEManager = self._cheECSEManager
        self._cheECSEManager = None
        if not (existingCheECSEManager is None) :
            existingCheECSEManager.setManager(None)
        super().delete()

