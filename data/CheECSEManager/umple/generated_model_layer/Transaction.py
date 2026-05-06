#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 60 "../model.ump"
# line 194 "../model.ump"
from abc import ABC, abstractmethod
import os

class Transaction(ABC):
    nextId = 1
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Transaction Attributes
    #Autounique Attributes
    #Transaction Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTransactionDate, aCheECSEManager):
        self._cheECSEManager = None
        self._id = None
        self._transactionDate = None
        self._transactionDate = aTransactionDate
        self._id, Transaction.nextId = Transaction.nextId, Transaction.nextId + 1
        didAddCheECSEManager = self.setCheECSEManager(aCheECSEManager)
        if not didAddCheECSEManager :
            raise RuntimeError ("Unable to create transaction due to cheECSEManager. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setTransactionDate(self, aTransactionDate):
        wasSet = False
        self._transactionDate = aTransactionDate
        wasSet = True
        return wasSet

    def getTransactionDate(self):
        return self._transactionDate

    def getId(self):
        return self._id

    # Code from template association_GetOne 
    def getCheECSEManager(self):
        return self._cheECSEManager

    # Code from template association_SetOneToMany 
    def setCheECSEManager(self, aCheECSEManager):
        wasSet = False
        if aCheECSEManager is None :
            return wasSet
        existingCheECSEManager = self._cheECSEManager
        self._cheECSEManager = aCheECSEManager
        if not (existingCheECSEManager is None) and not existingCheECSEManager == aCheECSEManager :
            existingCheECSEManager.removeTransaction(self)
        self._cheECSEManager.addTransaction(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderCheECSEManager = self._cheECSEManager
        self._cheECSEManager = None
        if not (placeholderCheECSEManager is None) :
            placeholderCheECSEManager.removeTransaction(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "]" + str(os.linesep) + "  " + "transactionDate" + "=" + str((((self.getTransactionDate().__str__().replaceAll("  ", "    ")) if not self.getTransactionDate() == self else "this") if not (self.getTransactionDate() is None) else "null")) + str(os.linesep) + "  " + "cheECSEManager = " + ((format(id(self.getCheECSEManager()), "x")) if not (self.getCheECSEManager() is None) else "null")

