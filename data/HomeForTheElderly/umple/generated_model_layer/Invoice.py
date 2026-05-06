# %% NEW FILE Invoice BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 44 "model.ump"
# line 139 "model.ump"
import os

class Invoice():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Invoice Attributes
    #Invoice Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aInvoiceDate, aOutstandingAmount, aStatus, aPerson):
        self._invoiceLines = None
        self._person = None
        self._status = None
        self._outstandingAmount = None
        self._invoiceDate = None
        self._invoiceDate = aInvoiceDate
        self._outstandingAmount = aOutstandingAmount
        self._status = aStatus
        didAddPerson = self.setPerson(aPerson)
        if not didAddPerson :
            raise RuntimeError ("Unable to create invoice due to person. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._invoiceLines = []

    #------------------------
    # INTERFACE
    #------------------------
    def setInvoiceDate(self, aInvoiceDate):
        wasSet = False
        self._invoiceDate = aInvoiceDate
        wasSet = True
        return wasSet

    def setOutstandingAmount(self, aOutstandingAmount):
        wasSet = False
        self._outstandingAmount = aOutstandingAmount
        wasSet = True
        return wasSet

    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def getInvoiceDate(self):
        return self._invoiceDate

    def getOutstandingAmount(self):
        return self._outstandingAmount

    def getStatus(self):
        return self._status

    # Code from template association_GetOne 
    def getPerson(self):
        return self._person

    # Code from template association_GetMany 
    def getInvoiceLine(self, index):
        aInvoiceLine = self._invoiceLines[index]
        return aInvoiceLine

    def getInvoiceLines(self):
        newInvoiceLines = tuple(self._invoiceLines)
        return newInvoiceLines

    def numberOfInvoiceLines(self):
        number = len(self._invoiceLines)
        return number

    def hasInvoiceLines(self):
        has = len(self._invoiceLines) > 0
        return has

    def indexOfInvoiceLine(self, aInvoiceLine):
        index = (-1 if not aInvoiceLine in self._invoiceLines else self._invoiceLines.index(aInvoiceLine))
        return index

    # Code from template association_SetOneToMany 
    def setPerson(self, aPerson):
        wasSet = False
        if aPerson is None :
            return wasSet
        existingPerson = self._person
        self._person = aPerson
        if not (existingPerson is None) and not existingPerson == aPerson :
            existingPerson.removeInvoice(self)
        self._person.addInvoice(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfInvoiceLines():
        return 0

    # Code from template association_AddManyToOne 
    def addInvoiceLine1(self, aInvoiceItem):
        from .InvoiceLine import InvoiceLine
        return InvoiceLine(self, aInvoiceItem)

    def addInvoiceLine2(self, aInvoiceLine):
        wasAdded = False
        if (aInvoiceLine) in self._invoiceLines :
            return False
        existingInvoice = aInvoiceLine.getInvoice()
        isNewInvoice = not (existingInvoice is None) and not self == existingInvoice
        if isNewInvoice :
            aInvoiceLine.setInvoice(self)
        else :
            self._invoiceLines.append(aInvoiceLine)
        wasAdded = True
        return wasAdded

    def removeInvoiceLine(self, aInvoiceLine):
        wasRemoved = False
        #Unable to remove aInvoiceLine, as it must always have a invoice
        if not self == aInvoiceLine.getInvoice() :
            self._invoiceLines.remove(aInvoiceLine)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addInvoiceLineAt(self, aInvoiceLine, index):
        wasAdded = False
        if self.addInvoiceLine(aInvoiceLine) :
            if index < 0 :
                index = 0
            if index > self.numberOfInvoiceLines() :
                index = self.numberOfInvoiceLines() - 1
            self._invoiceLines.remove(aInvoiceLine)
            self._invoiceLines.insert(index, aInvoiceLine)
            wasAdded = True
        return wasAdded

    def addOrMoveInvoiceLineAt(self, aInvoiceLine, index):
        wasAdded = False
        if (aInvoiceLine) in self._invoiceLines :
            if index < 0 :
                index = 0
            if index > self.numberOfInvoiceLines() :
                index = self.numberOfInvoiceLines() - 1
            self._invoiceLines.remove(aInvoiceLine)
            self._invoiceLines.insert(index, aInvoiceLine)
            wasAdded = True
        else :
            wasAdded = self.addInvoiceLineAt(aInvoiceLine, index)
        return wasAdded

    def delete(self):
        placeholderPerson = self._person
        self._person = None
        if not (placeholderPerson is None) :
            placeholderPerson.removeInvoice(self)
        i = len(self._invoiceLines)
        while i > 0 :
            aInvoiceLine = self._invoiceLines[i - 1]
            aInvoiceLine.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "outstandingAmount" + ":" + str(self.getOutstandingAmount()) + "," + "status" + ":" + str(self.getStatus()) + "]" + str(os.linesep) + "  " + "invoiceDate" + "=" + str((((self.getInvoiceDate().__str__().replaceAll("  ", "    ")) if not self.getInvoiceDate() == self else "this") if not (self.getInvoiceDate() is None) else "null")) + str(os.linesep) + "  " + "person = " + ((format(id(self.getPerson()), "x")) if not (self.getPerson() is None) else "null")

    def addInvoiceLine(self, *argv):
        from .InvoiceLine import InvoiceLine
        from .InvoiceItem import InvoiceItem
        if len(argv) == 1 and isinstance(argv[0], InvoiceItem) :
            return self.addInvoiceLine1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], InvoiceLine) :
            return self.addInvoiceLine2(argv[0])
        raise TypeError("No method matches provided parameters")
