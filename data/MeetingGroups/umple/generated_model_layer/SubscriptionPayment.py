# %% NEW FILE SubscriptionPayment BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 211 "model.ump"
# line 370 "model.ump"
import os
from enum import Enum, auto

class SubscriptionPayment():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class SubscriptionPeriod(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Month = auto()
        HalfYear = auto()

    class SubscriptionPaymentStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        WaitingForPayment = auto()
        Paid = auto()
        Expired = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #SubscriptionPayment Attributes
    #SubscriptionPayment Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aCountryCode, aSubscriptionPeriod, aPayer, aValue, aPayments):
        self._payments = None
        self._value = None
        self._payer = None
        self._status = None
        self._subscriptionPeriod = None
        self._countryCode = None
        self._countryCode = aCountryCode
        self._subscriptionPeriod = aSubscriptionPeriod
        if not self.setPayer(aPayer) :
            raise RuntimeError ("Unable to create SubscriptionPayment due to aPayer. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setValue(aValue) :
            raise RuntimeError ("Unable to create SubscriptionPayment due to aValue. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddPayments = self.setPayments(aPayments)
        if not didAddPayments :
            raise RuntimeError ("Unable to create subscriptionPayment due to payments. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setCountryCode(self, aCountryCode):
        wasSet = False
        self._countryCode = aCountryCode
        wasSet = True
        return wasSet

    def setSubscriptionPeriod(self, aSubscriptionPeriod):
        wasSet = False
        self._subscriptionPeriod = aSubscriptionPeriod
        wasSet = True
        return wasSet

    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def getCountryCode(self):
        return self._countryCode

    def getSubscriptionPeriod(self):
        return self._subscriptionPeriod

    def getStatus(self):
        return self._status

    # Code from template association_GetOne
    def getPayer(self):
        return self._payer

    # Code from template association_GetOne
    def getValue(self):
        return self._value

    # Code from template association_GetOne
    def getPayments(self):
        return self._payments

    # Code from template association_SetUnidirectionalOne
    def setPayer(self, aNewPayer):
        wasSet = False
        if not (aNewPayer is None) :
            self._payer = aNewPayer
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOne
    def setValue(self, aNewValue):
        wasSet = False
        if not (aNewValue is None) :
            self._value = aNewValue
            wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setPayments(self, aPayments):
        wasSet = False
        if aPayments is None :
            return wasSet
        existingPayments = self._payments
        self._payments = aPayments
        if not (existingPayments is None) and not existingPayments == aPayments :
            existingPayments.removeSubscriptionPayment(self)
        self._payments.addSubscriptionPayment(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._payer = None
        self._value = None
        placeholderPayments = self._payments
        self._payments = None
        if not (placeholderPayments is None) :
            placeholderPayments.removeSubscriptionPayment(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "countryCode" + ":" + str(self.getCountryCode()) + "]" + str(os.linesep) + "  " + "subscriptionPeriod" + "=" + str((((self.getSubscriptionPeriod().__str__().replaceAll("  ", "    ")) if not self.getSubscriptionPeriod() == self else "this") if not (self.getSubscriptionPeriod() is None) else "null")) + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "payer = " + str(((format(id(self.getPayer()), "x")) if not (self.getPayer() is None) else "null")) + str(os.linesep) + "  " + "value = " + str(((format(id(self.getValue()), "x")) if not (self.getValue() is None) else "null")) + str(os.linesep) + "  " + "payments = " + ((format(id(self.getPayments()), "x")) if not (self.getPayments() is None) else "null")
