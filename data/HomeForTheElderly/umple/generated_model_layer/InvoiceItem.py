# %% NEW FILE InvoiceItem BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 50 "model.ump"
# line 144 "model.ump"

class InvoiceItem():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #InvoiceItem Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aStay):
        self._stay = None
        self._invoiceLine = None
        didAddStay = self.setStay(aStay)
        if not didAddStay :
            raise RuntimeError ("Unable to create invoiceItem due to stay. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getInvoiceLine(self):
        return self._invoiceLine

    def hasInvoiceLine(self):
        has = not (self._invoiceLine is None)
        return has

    # Code from template association_GetOne 
    def getStay(self):
        return self._stay

    # Code from template association_SetOptionalOneToOne 
    def setInvoiceLine(self, aNewInvoiceLine):
        wasSet = False
        if not (self._invoiceLine is None) and not self._invoiceLine == aNewInvoiceLine and self == self._invoiceLine.getInvoiceItem() :
            #Unable to setInvoiceLine, as existing invoiceLine would become an orphan
            return wasSet
        self._invoiceLine = aNewInvoiceLine
        anOldInvoiceItem = (aNewInvoiceLine.getInvoiceItem()) if not (aNewInvoiceLine is None) else None
        if not self == anOldInvoiceItem :
            if not (anOldInvoiceItem is None) :
                anOldInvoiceItem.invoiceLine = None
            if not (self._invoiceLine is None) :
                self._invoiceLine.setInvoiceItem(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setStay(self, aStay):
        wasSet = False
        if aStay is None :
            return wasSet
        existingStay = self._stay
        self._stay = aStay
        if not (existingStay is None) and not existingStay == aStay :
            existingStay.removeInvoiceItem(self)
        self._stay.addInvoiceItem(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingInvoiceLine = self._invoiceLine
        self._invoiceLine = None
        if not (existingInvoiceLine is None) :
            existingInvoiceLine.delete()
        placeholderStay = self._stay
        self._stay = None
        if not (placeholderStay is None) :
            placeholderStay.removeInvoiceItem(self)
