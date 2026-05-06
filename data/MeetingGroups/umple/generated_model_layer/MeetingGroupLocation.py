# %% NEW FILE MeetingGroupLocation BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 62 "model.ump"
# line 285 "model.ump"

class MeetingGroupLocation():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingGroupLocation Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aCity, aCountryCode):
        self._countryCode = None
        self._city = None
        self._city = aCity
        self._countryCode = aCountryCode

    #------------------------
    # INTERFACE
    #------------------------
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

    def getCity(self):
        return self._city

    def getCountryCode(self):
        return self._countryCode

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "city" + ":" + str(self.getCity()) + "," + "countryCode" + ":" + str(self.getCountryCode()) + "]"
