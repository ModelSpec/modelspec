# %% NEW FILE InvoiceLine BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 52 "model.ump"
# line 149 "model.ump"

class InvoiceLine():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #InvoiceLine Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aInvoice, aInvoiceItem):
        self._invoiceItem = None
        self._invoice = None
        didAddInvoice = self.setInvoice(aInvoice)
        if not didAddInvoice :
            raise RuntimeError ("Unable to create invoiceLine due to invoice. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddInvoiceItem = self.setInvoiceItem(aInvoiceItem)
        if not didAddInvoiceItem :
            raise RuntimeError ("Unable to create invoiceLine due to invoiceItem. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getInvoice(self):
        return self._invoice

    # Code from template association_GetOne 
    def getInvoiceItem(self):
        return self._invoiceItem

    # Code from template association_SetOneToMany 
    def setInvoice(self, aInvoice):
        wasSet = False
        if aInvoice is None :
            return wasSet
        existingInvoice = self._invoice
        self._invoice = aInvoice
        if not (existingInvoice is None) and not existingInvoice == aInvoice :
            existingInvoice.removeInvoiceLine(self)
        self._invoice.addInvoiceLine(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToOptionalOne 
    def setInvoiceItem(self, aNewInvoiceItem):
        wasSet = False
        if aNewInvoiceItem is None :
            #Unable to setInvoiceItem to null, as invoiceLine must always be associated to a invoiceItem
            return wasSet
        existingInvoiceLine = aNewInvoiceItem.getInvoiceLine()
        if not (existingInvoiceLine is None) and not self == existingInvoiceLine :
            #Unable to setInvoiceItem, the current invoiceItem already has a invoiceLine, which would be orphaned if it were re-assigned
            return wasSet
        anOldInvoiceItem = self._invoiceItem
        self._invoiceItem = aNewInvoiceItem
        self._invoiceItem.setInvoiceLine(self)
        if not (anOldInvoiceItem is None) :
            anOldInvoiceItem.setInvoiceLine(None)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderInvoice = self._invoice
        self._invoice = None
        if not (placeholderInvoice is None) :
            placeholderInvoice.removeInvoiceLine(self)
        existingInvoiceItem = self._invoiceItem
        self._invoiceItem = None
        if not (existingInvoiceItem is None) :
            existingInvoiceItem.setInvoiceLine(None)
