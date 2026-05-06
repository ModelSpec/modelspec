# %% NEW FILE Administrator BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 54 "model.ump"
# line 275 "model.ump"
from .User import User

class Administrator(User):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Administrator Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess, aAdministration):
        self._administration = None
        super().__init__(aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess)
        didAddAdministration = self.setAdministration(aAdministration)
        if not didAddAdministration :
            raise RuntimeError ("Unable to create administrator due to administration. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne
    def getAdministration(self):
        return self._administration

    # Code from template association_SetOneToMany
    def setAdministration(self, aAdministration):
        wasSet = False
        if aAdministration is None :
            return wasSet
        existingAdministration = self._administration
        self._administration = aAdministration
        if not (existingAdministration is None) and not existingAdministration == aAdministration :
            existingAdministration.removeAdministrator(self)
        self._administration.addAdministrator(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderAdministration = self._administration
        self._administration = None
        if not (placeholderAdministration is None) :
            placeholderAdministration.removeAdministrator(self)
        super().delete()
