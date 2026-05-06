# %% NEW FILE TOHotelStaff BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 135 "model.ump"
# line 266 "model.ump"
from .TOUser import TOUser

class TOHotelStaff(TOUser):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOHotelStaff Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber):
        self._ticketFixed = None
        super().__init__(aEmail, aName, aPassword, aPhoneNumber)
        self._ticketFixed = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template attribute_GetMany 
    def getTicketFixed1(self, index):
        aTicketFixed = self._ticketFixed[index]
        return aTicketFixed

    def getTicketFixed2(self):
        newTicketFixed = self._ticketFixed.copy()
        return newTicketFixed

    def numberOfTicketFixed(self):
        number = len(self._ticketFixed)
        return number

    def hasTicketFixed(self):
        has = len(self._ticketFixed) > 0
        return has

    def indexOfTicketFixed(self, aTicketFixed):
        index = (-1 if not aTicketFixed in self._ticketFixed else self._ticketFixed.index(aTicketFixed))
        return index

    def delete(self):
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "]"

    def getTicketFixed(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getTicketFixed1(argv[0])
        if len(argv) == 0 :
            return self.getTicketFixed2()
        raise TypeError("No method matches provided parameters")
