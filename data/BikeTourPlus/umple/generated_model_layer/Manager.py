# %% NEW FILE Manager BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 23 "model.ump"
# line 106 "model.ump"
from .User import User

class Manager(User):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Manager Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword, aBikeTourPlus):
        self._bikeTourPlus = None
        super().__init__(aEmail, aPassword)
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create manager due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne
    def getBikeTourPlus(self):
        return self._bikeTourPlus

    # Code from template association_SetOneToOptionalOne
    def setBikeTourPlus(self, aNewBikeTourPlus):
        wasSet = False
        if aNewBikeTourPlus is None :
            #Unable to setBikeTourPlus to null, as manager must always be associated to a bikeTourPlus
            return wasSet
        existingManager = aNewBikeTourPlus.getManager()
        if not (existingManager is None) and not self == existingManager :
            #Unable to setBikeTourPlus, the current bikeTourPlus already has a manager, which would be orphaned if it were re-assigned
            return wasSet
        anOldBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aNewBikeTourPlus
        self._bikeTourPlus.setManager(self)
        if not (anOldBikeTourPlus is None) :
            anOldBikeTourPlus.setManager(None)
        wasSet = True
        return wasSet

    def delete(self):
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (existingBikeTourPlus is None) :
            existingBikeTourPlus.setManager(None)
        super().delete()
