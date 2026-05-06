# %% NEW FILE Situation BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 43 "model.ump"

class Situation():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Situation Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTime):
        self._time = None
        self._postEvents = None
        self._preEvents = None
        self._preEvents = []
        self._postEvents = []
        if not self.setTime(aTime) :
            raise RuntimeError ("Unable to create Situation due to aTime. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany
    def getPreEvent(self, index):
        aPreEvent = self._preEvents[index]
        return aPreEvent

    def getPreEvents(self):
        newPreEvents = tuple(self._preEvents)
        return newPreEvents

    def numberOfPreEvents(self):
        number = len(self._preEvents)
        return number

    def hasPreEvents(self):
        has = len(self._preEvents) > 0
        return has

    def indexOfPreEvent(self, aPreEvent):
        index = (-1 if not aPreEvent in self._preEvents else self._preEvents.index(aPreEvent))
        return index

    # Code from template association_GetMany
    def getPostEvent(self, index):
        aPostEvent = self._postEvents[index]
        return aPostEvent

    def getPostEvents(self):
        newPostEvents = tuple(self._postEvents)
        return newPostEvents

    def numberOfPostEvents(self):
        number = len(self._postEvents)
        return number

    def hasPostEvents(self):
        has = len(self._postEvents) > 0
        return has

    def indexOfPostEvent(self, aPostEvent):
        index = (-1 if not aPostEvent in self._postEvents else self._postEvents.index(aPostEvent))
        return index

    # Code from template association_GetOne
    def getTime(self):
        return self._time

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfPreEvents():
        return 0

    # Code from template association_AddManyToOptionalOne
    def addPreEvent(self, aPreEvent):
        wasAdded = False
        if (aPreEvent) in self._preEvents :
            return False
        existingPostState = aPreEvent.getPostState()
        if existingPostState is None :
            aPreEvent.setPostState(self)
        elif not self == existingPostState :
            existingPostState.removePreEvent(aPreEvent)
            self.addPreEvent(aPreEvent)
        else :
            self._preEvents.append(aPreEvent)
        wasAdded = True
        return wasAdded

    def removePreEvent(self, aPreEvent):
        wasRemoved = False
        if (aPreEvent) in self._preEvents :
            self._preEvents.remove(aPreEvent)
            aPreEvent.setPostState(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addPreEventAt(self, aPreEvent, index):
        wasAdded = False
        if self.addPreEvent(aPreEvent) :
            if index < 0 :
                index = 0
            if index > self.numberOfPreEvents() :
                index = self.numberOfPreEvents() - 1
            self._preEvents.remove(aPreEvent)
            self._preEvents.insert(index, aPreEvent)
            wasAdded = True
        return wasAdded

    def addOrMovePreEventAt(self, aPreEvent, index):
        wasAdded = False
        if (aPreEvent) in self._preEvents :
            if index < 0 :
                index = 0
            if index > self.numberOfPreEvents() :
                index = self.numberOfPreEvents() - 1
            self._preEvents.remove(aPreEvent)
            self._preEvents.insert(index, aPreEvent)
            wasAdded = True
        else :
            wasAdded = self.addPreEventAt(aPreEvent, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfPostEvents():
        return 0

    # Code from template association_AddManyToOptionalOne
    def addPostEvent(self, aPostEvent):
        wasAdded = False
        if (aPostEvent) in self._postEvents :
            return False
        existingPreState = aPostEvent.getPreState()
        if existingPreState is None :
            aPostEvent.setPreState(self)
        elif not self == existingPreState :
            existingPreState.removePostEvent(aPostEvent)
            self.addPostEvent(aPostEvent)
        else :
            self._postEvents.append(aPostEvent)
        wasAdded = True
        return wasAdded

    def removePostEvent(self, aPostEvent):
        wasRemoved = False
        if (aPostEvent) in self._postEvents :
            self._postEvents.remove(aPostEvent)
            aPostEvent.setPreState(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addPostEventAt(self, aPostEvent, index):
        wasAdded = False
        if self.addPostEvent(aPostEvent) :
            if index < 0 :
                index = 0
            if index > self.numberOfPostEvents() :
                index = self.numberOfPostEvents() - 1
            self._postEvents.remove(aPostEvent)
            self._postEvents.insert(index, aPostEvent)
            wasAdded = True
        return wasAdded

    def addOrMovePostEventAt(self, aPostEvent, index):
        wasAdded = False
        if (aPostEvent) in self._postEvents :
            if index < 0 :
                index = 0
            if index > self.numberOfPostEvents() :
                index = self.numberOfPostEvents() - 1
            self._postEvents.remove(aPostEvent)
            self._postEvents.insert(index, aPostEvent)
            wasAdded = True
        else :
            wasAdded = self.addPostEventAt(aPostEvent, index)
        return wasAdded

    # Code from template association_SetUnidirectionalOne
    def setTime(self, aNewTime):
        wasSet = False
        if not (aNewTime is None) :
            self._time = aNewTime
            wasSet = True
        return wasSet

    def delete(self):

        while not self._preEvents.isEmpty() :
            self._preEvents[0].setPostState(None)

        while not self._postEvents.isEmpty() :
            self._postEvents[0].setPreState(None)

        self._time = None
