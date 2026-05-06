# %% NEW FILE TicketImage BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 64 "model.ump"
# line 236 "model.ump"
import os

class TicketImage():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TicketImage Attributes
    #TicketImage Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aImageURL, aTicket):
        self._ticket = None
        self._imageURL = None
        self._imageURL = aImageURL
        didAddTicket = self.setTicket(aTicket)
        if not didAddTicket :
            raise RuntimeError ("Unable to create ticketImage due to ticket. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setImageURL(self, aImageURL):
        wasSet = False
        self._imageURL = aImageURL
        wasSet = True
        return wasSet

    def getImageURL(self):
        return self._imageURL

    # Code from template association_GetOne 
    def getTicket(self):
        return self._ticket

    # Code from template association_SetOneToMany 
    def setTicket(self, aTicket):
        wasSet = False
        if aTicket is None :
            return wasSet
        existingTicket = self._ticket
        self._ticket = aTicket
        if not (existingTicket is None) and not existingTicket == aTicket :
            existingTicket.removeTicketImage(self)
        self._ticket.addTicketImage(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderTicket = self._ticket
        self._ticket = None
        if not (placeholderTicket is None) :
            placeholderTicket.removeTicketImage(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "imageURL" + ":" + str(self.getImageURL()) + "]" + str(os.linesep) + "  " + "ticket = " + ((format(id(self.getTicket()), "x")) if not (self.getTicket() is None) else "null")
