# %% NEW FILE Event BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 49 "model.ump"
import os

class Event():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Event Attributes
    #Event Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTriggered, aTimestamp):
        self._preState = None
        self._postState = None
        self._timestamp = None
        self._triggered = None
        self._triggered = aTriggered
        self._timestamp = aTimestamp

    #------------------------
    # INTERFACE
    #------------------------
    def setTriggered(self, aTriggered):
        wasSet = False
        self._triggered = aTriggered
        wasSet = True
        return wasSet

    def setTimestamp(self, aTimestamp):
        wasSet = False
        self._timestamp = aTimestamp
        wasSet = True
        return wasSet

    def getTriggered(self):
        return self._triggered

    def getTimestamp(self):
        return self._timestamp

    # Code from template attribute_IsBoolean
    def isTriggered(self):
        return self._triggered

    # Code from template association_GetOne
    def getPostState(self):
        return self._postState

    def hasPostState(self):
        has = not (self._postState is None)
        return has

    # Code from template association_GetOne
    def getPreState(self):
        return self._preState

    def hasPreState(self):
        has = not (self._preState is None)
        return has

    # Code from template association_SetOptionalOneToMany
    def setPostState(self, aPostState):
        wasSet = False
        existingPostState = self._postState
        self._postState = aPostState
        if not (existingPostState is None) and not existingPostState == aPostState :
            existingPostState.removePreEvent(self)
        if not (aPostState is None) :
            aPostState.addPreEvent(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany
    def setPreState(self, aPreState):
        wasSet = False
        existingPreState = self._preState
        self._preState = aPreState
        if not (existingPreState is None) and not existingPreState == aPreState :
            existingPreState.removePostEvent(self)
        if not (aPreState is None) :
            aPreState.addPostEvent(self)
        wasSet = True
        return wasSet

    def delete(self):
        if not (self._postState is None) :
            placeholderPostState = self._postState
            self._postState = None
            placeholderPostState.removePreEvent(self)
        if not (self._preState is None) :
            placeholderPreState = self._preState
            self._preState = None
            placeholderPreState.removePostEvent(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "triggered" + ":" + str(self.getTriggered()) + "]" + str(os.linesep) + "  " + "timestamp" + "=" + str((((self.getTimestamp().__str__().replaceAll("  ", "    ")) if not self.getTimestamp() == self else "this") if not (self.getTimestamp() is None) else "null")) + str(os.linesep) + "  " + "postState = " + str(((format(id(self.getPostState()), "x")) if not (self.getPostState() is None) else "null")) + str(os.linesep) + "  " + "preState = " + ((format(id(self.getPreState()), "x")) if not (self.getPreState() is None) else "null")
