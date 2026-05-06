# %% NEW FILE Foo BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 2 "model.ump"
# line 10 "model.ump"

class Foo():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Foo Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aBar):
        self._bar = None
        didAddBar = self.setBar(aBar)
        if not didAddBar :
            raise RuntimeError ("Unable to create foo due to bar. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne
    def getBar(self):
        return self._bar

    # Code from template association_SetOneToMany
    def setBar(self, aBar):
        wasSet = False
        if aBar is None :
            return wasSet
        existingBar = self._bar
        self._bar = aBar
        if not (existingBar is None) and not existingBar == aBar :
            existingBar.removeFoo(self)
        self._bar.addFoo(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderBar = self._bar
        self._bar = None
        if not (placeholderBar is None) :
            placeholderBar.removeFoo(self)