# %% NEW FILE MeetingLocation BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 106 "model.ump"
# line 310 "model.ump"
import os

class MeetingLocation():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingLocation Attributes
    #MeetingLocation Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAddress, aCity, aCountryCode, aMeetings):
        self._meetings = None
        self._countryCode = None
        self._city = None
        self._address = None
        self._name = None
        self._name = aName
        self._address = aAddress
        self._city = aCity
        self._countryCode = aCountryCode
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create meetingLocation due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setAddress(self, aAddress):
        wasSet = False
        self._address = aAddress
        wasSet = True
        return wasSet

    def setCity(self, aCity):
        wasSet = False
        self._city = aCity
        wasSet = True
        return wasSet

    def setCountryCode(self, aCountryCode):
        wasSet = False
        self._countryCode = aCountryCode
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    def getAddress(self):
        return self._address

    def getCity(self):
        return self._city

    def getCountryCode(self):
        return self._countryCode

    # Code from template association_GetOne
    def getMeetings(self):
        return self._meetings

    # Code from template association_SetOneToMany
    def setMeetings(self, aMeetings):
        wasSet = False
        if aMeetings is None :
            return wasSet
        existingMeetings = self._meetings
        self._meetings = aMeetings
        if not (existingMeetings is None) and not existingMeetings == aMeetings :
            existingMeetings.removeMeetingLocation(self)
        self._meetings.addMeetingLocation(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMeetingLocation(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "address" + ":" + str(self.getAddress()) + "," + "city" + ":" + str(self.getCity()) + "," + "countryCode" + ":" + str(self.getCountryCode()) + "]" + str(os.linesep) + "  " + "meetings = " + ((format(id(self.getMeetings()), "x")) if not (self.getMeetings() is None) else "null")
