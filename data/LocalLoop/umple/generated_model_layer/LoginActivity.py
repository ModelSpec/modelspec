# %% NEW FILE LoginActivity BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 144 "model.ump"
# line 277 "model.ump"
from .AppCompatActivity import AppCompatActivity

class LoginActivity(AppCompatActivity):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #LoginActivity Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._loginService = None
        super().__init__()

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getLoginService(self):
        return self._loginService

    def hasLoginService(self):
        has = not (self._loginService is None)
        return has

    # Code from template association_SetOptionalOneToOne 
    def setLoginService(self, aNewLoginService):
        wasSet = False
        if not (self._loginService is None) and not self._loginService == aNewLoginService and self == self._loginService.getLoginActivity() :
            #Unable to setLoginService, as existing loginService would become an orphan
            return wasSet
        self._loginService = aNewLoginService
        anOldLoginActivity = (aNewLoginService.getLoginActivity()) if not (aNewLoginService is None) else None
        if not self == anOldLoginActivity :
            if not (anOldLoginActivity is None) :
                anOldLoginActivity.loginService = None
            if not (self._loginService is None) :
                self._loginService.setLoginActivity(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingLoginService = self._loginService
        self._loginService = None
        if not (existingLoginService is None) :
            existingLoginService.delete()
        super().delete()
