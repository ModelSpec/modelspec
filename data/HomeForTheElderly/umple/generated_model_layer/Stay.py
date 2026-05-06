# %% NEW FILE Stay BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 31 "model.ump"
# line 129 "model.ump"
import os

class Stay():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Stay Attributes
    #Stay Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aIntakeDate, aEndDate, aPerson, aBed):
        self._invoiceItems = None
        self._bed = None
        self._person = None
        self._endDate = None
        self._intakeDate = None
        self._intakeDate = aIntakeDate
        self._endDate = aEndDate
        didAddPerson = self.setPerson(aPerson)
        if not didAddPerson :
            raise RuntimeError ("Unable to create stay due to person. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddBed = self.setBed(aBed)
        if not didAddBed :
            raise RuntimeError ("Unable to create stay due to bed. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._invoiceItems = []

    #------------------------
    # INTERFACE
    #------------------------
    def setIntakeDate(self, aIntakeDate):
        wasSet = False
        self._intakeDate = aIntakeDate
        wasSet = True
        return wasSet

    def setEndDate(self, aEndDate):
        wasSet = False
        self._endDate = aEndDate
        wasSet = True
        return wasSet

    def getIntakeDate(self):
        return self._intakeDate

    def getEndDate(self):
        return self._endDate

    # Code from template association_GetOne 
    def getPerson(self):
        return self._person

    # Code from template association_GetOne 
    def getBed(self):
        return self._bed

    # Code from template association_GetMany 
    def getInvoiceItem(self, index):
        aInvoiceItem = self._invoiceItems[index]
        return aInvoiceItem

    def getInvoiceItems(self):
        newInvoiceItems = tuple(self._invoiceItems)
        return newInvoiceItems

    def numberOfInvoiceItems(self):
        number = len(self._invoiceItems)
        return number

    def hasInvoiceItems(self):
        has = len(self._invoiceItems) > 0
        return has

    def indexOfInvoiceItem(self, aInvoiceItem):
        index = (-1 if not aInvoiceItem in self._invoiceItems else self._invoiceItems.index(aInvoiceItem))
        return index

    # Code from template association_SetOneToMany 
    def setPerson(self, aPerson):
        wasSet = False
        if aPerson is None :
            return wasSet
        existingPerson = self._person
        self._person = aPerson
        if not (existingPerson is None) and not existingPerson == aPerson :
            existingPerson.removeStay(self)
        self._person.addStay(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setBed(self, aBed):
        wasSet = False
        if aBed is None :
            return wasSet
        existingBed = self._bed
        self._bed = aBed
        if not (existingBed is None) and not existingBed == aBed :
            existingBed.removeStay(self)
        self._bed.addStay(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfInvoiceItems():
        return 0

    # Code from template association_AddManyToOne 
    def addInvoiceItem1(self):
        from .InvoiceItem import InvoiceItem
        return InvoiceItem(self)

    def addInvoiceItem2(self, aInvoiceItem):
        wasAdded = False
        if (aInvoiceItem) in self._invoiceItems :
            return False
        existingStay = aInvoiceItem.getStay()
        isNewStay = not (existingStay is None) and not self == existingStay
        if isNewStay :
            aInvoiceItem.setStay(self)
        else :
            self._invoiceItems.append(aInvoiceItem)
        wasAdded = True
        return wasAdded

    def removeInvoiceItem(self, aInvoiceItem):
        wasRemoved = False
        #Unable to remove aInvoiceItem, as it must always have a stay
        if not self == aInvoiceItem.getStay() :
            self._invoiceItems.remove(aInvoiceItem)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addInvoiceItemAt(self, aInvoiceItem, index):
        wasAdded = False
        if self.addInvoiceItem(aInvoiceItem) :
            if index < 0 :
                index = 0
            if index > self.numberOfInvoiceItems() :
                index = self.numberOfInvoiceItems() - 1
            self._invoiceItems.remove(aInvoiceItem)
            self._invoiceItems.insert(index, aInvoiceItem)
            wasAdded = True
        return wasAdded

    def addOrMoveInvoiceItemAt(self, aInvoiceItem, index):
        wasAdded = False
        if (aInvoiceItem) in self._invoiceItems :
            if index < 0 :
                index = 0
            if index > self.numberOfInvoiceItems() :
                index = self.numberOfInvoiceItems() - 1
            self._invoiceItems.remove(aInvoiceItem)
            self._invoiceItems.insert(index, aInvoiceItem)
            wasAdded = True
        else :
            wasAdded = self.addInvoiceItemAt(aInvoiceItem, index)
        return wasAdded

    def delete(self):
        placeholderPerson = self._person
        self._person = None
        if not (placeholderPerson is None) :
            placeholderPerson.removeStay(self)
        placeholderBed = self._bed
        self._bed = None
        if not (placeholderBed is None) :
            placeholderBed.removeStay(self)
        i = len(self._invoiceItems)
        while i > 0 :
            aInvoiceItem = self._invoiceItems[i - 1]
            aInvoiceItem.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "intakeDate" + "=" + str((((self.getIntakeDate().__str__().replaceAll("  ", "    ")) if not self.getIntakeDate() == self else "this") if not (self.getIntakeDate() is None) else "null")) + str(os.linesep) + "  " + "endDate" + "=" + str((((self.getEndDate().__str__().replaceAll("  ", "    ")) if not self.getEndDate() == self else "this") if not (self.getEndDate() is None) else "null")) + str(os.linesep) + "  " + "person = " + str(((format(id(self.getPerson()), "x")) if not (self.getPerson() is None) else "null")) + str(os.linesep) + "  " + "bed = " + ((format(id(self.getBed()), "x")) if not (self.getBed() is None) else "null")

    def addInvoiceItem(self, *argv):
        from .InvoiceItem import InvoiceItem
        if len(argv) == 0 :
            return self.addInvoiceItem1()
        if len(argv) == 1 and isinstance(argv[0], InvoiceItem) :
            return self.addInvoiceItem2(argv[0])
        raise TypeError("No method matches provided parameters")