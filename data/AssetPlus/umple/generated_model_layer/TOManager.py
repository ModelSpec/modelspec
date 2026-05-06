# %% NEW FILE TOManager BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 147 "model.ump"
# line 276 "model.ump"
from .TOHotelStaff import TOHotelStaff

class TOManager(TOHotelStaff):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOManager Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber):
        self._ticketApproved = None
        super().__init__(aEmail, aName, aPassword, aPhoneNumber)
        self._ticketApproved = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template attribute_GetMany 
    def getTicketApproved1(self, index):
        aTicketApproved = self._ticketApproved[index]
        return aTicketApproved

    def getTicketApproved2(self):
        newTicketApproved = self._ticketApproved.copy()
        return newTicketApproved

    def numberOfTicketApproved(self):
        number = len(self._ticketApproved)
        return number

    def hasTicketApproved(self):
        has = len(self._ticketApproved) > 0
        return has

    def indexOfTicketApproved(self, aTicketApproved):
        index = (-1 if not aTicketApproved in self._ticketApproved else self._ticketApproved.index(aTicketApproved))
        return index

    def delete(self):
        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "]"

    def getTicketApproved(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getTicketApproved1(argv[0])
        if len(argv) == 0 :
            return self.getTicketApproved2()
        raise TypeError("No method matches provided parameters")
