# %% NEW FILE MeetingLimit BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 176 "model.ump"
# line 345 "model.ump"

class MeetingLimit():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingLimit Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAttendeesLimit, aGuestsLimit):
        self._guestsLimit = None
        self._attendeesLimit = None
        self._attendeesLimit = aAttendeesLimit
        self._guestsLimit = aGuestsLimit

    #------------------------
    # INTERFACE
    #------------------------
    def setAttendeesLimit(self, aAttendeesLimit):
        wasSet = False
        self._attendeesLimit = aAttendeesLimit
        wasSet = True
        return wasSet

    def setGuestsLimit(self, aGuestsLimit):
        wasSet = False
        self._guestsLimit = aGuestsLimit
        wasSet = True
        return wasSet

    def getAttendeesLimit(self):
        return self._attendeesLimit

    def getGuestsLimit(self):
        return self._guestsLimit

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "attendeesLimit" + ":" + str(self.getAttendeesLimit()) + "," + "guestsLimit" + ":" + str(self.getGuestsLimit()) + "]"
