# %% NEW FILE LoginService BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 101 "model.ump"
# line 237 "model.ump"

class LoginService():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #LoginService Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aLoginActivity):
        self._loginActivity = None
        didAddLoginActivity = self.setLoginActivity(aLoginActivity)
        if not didAddLoginActivity :
            raise RuntimeError ("Unable to create loginService due to loginActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getLoginActivity(self):
        return self._loginActivity

    # Code from template association_SetOneToOptionalOne 
    def setLoginActivity(self, aNewLoginActivity):
        wasSet = False
        if aNewLoginActivity is None :
            #Unable to setLoginActivity to null, as loginService must always be associated to a loginActivity
            return wasSet
        existingLoginService = aNewLoginActivity.getLoginService()
        if not (existingLoginService is None) and not self == existingLoginService :
            #Unable to setLoginActivity, the current loginActivity already has a loginService, which would be orphaned if it were re-assigned
            return wasSet
        anOldLoginActivity = self._loginActivity
        self._loginActivity = aNewLoginActivity
        self._loginActivity.setLoginService(self)
        if not (anOldLoginActivity is None) :
            anOldLoginActivity.setLoginService(None)
        wasSet = True
        return wasSet

    def delete(self):
        existingLoginActivity = self._loginActivity
        self._loginActivity = None
        if not (existingLoginActivity is None) :
            existingLoginActivity.setLoginService(None)
