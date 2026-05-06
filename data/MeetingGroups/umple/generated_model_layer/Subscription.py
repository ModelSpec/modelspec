# %% NEW FILE Subscription BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 202 "model.ump"
# line 365 "model.ump"
import os
from enum import Enum, auto

class Subscription():
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

    class SubscriptionStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Active = auto()
        Expired = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Subscription Attributes
    #Subscription Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aCountryCode, aExpirationDate, aSubscriptionPeriod, aStatus, aSubscriber, aPayments):
        self._payments = None
        self._subscriber = None
        self._status = None
        self._subscriptionPeriod = None
        self._expirationDate = None
        self._countryCode = None
        self._countryCode = aCountryCode
        self._expirationDate = aExpirationDate
        self._subscriptionPeriod = aSubscriptionPeriod
        self._status = aStatus
        if not self.setSubscriber(aSubscriber) :
            raise RuntimeError ("Unable to create Subscription due to aSubscriber. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddPayments = self.setPayments(aPayments)
        if not didAddPayments :
            raise RuntimeError ("Unable to create subscription due to payments. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setCountryCode(self, aCountryCode):
        wasSet = False
        self._countryCode = aCountryCode
        wasSet = True
        return wasSet

    def setExpirationDate(self, aExpirationDate):
        wasSet = False
        self._expirationDate = aExpirationDate
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

    def getExpirationDate(self):
        return self._expirationDate

    def getSubscriptionPeriod(self):
        return self._subscriptionPeriod

    def getStatus(self):
        return self._status

    # Code from template association_GetOne
    def getSubscriber(self):
        return self._subscriber

    # Code from template association_GetOne
    def getPayments(self):
        return self._payments

    # Code from template association_SetUnidirectionalOne
    def setSubscriber(self, aNewSubscriber):
        wasSet = False
        if not (aNewSubscriber is None) :
            self._subscriber = aNewSubscriber
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
            existingPayments.removeSubscription(self)
        self._payments.addSubscription(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._subscriber = None
        placeholderPayments = self._payments
        self._payments = None
        if not (placeholderPayments is None) :
            placeholderPayments.removeSubscription(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "countryCode" + ":" + str(self.getCountryCode()) + "]" + str(os.linesep) + "  " + "expirationDate" + "=" + str((((self.getExpirationDate().__str__().replaceAll("  ", "    ")) if not self.getExpirationDate() == self else "this") if not (self.getExpirationDate() is None) else "null")) + str(os.linesep) + "  " + "subscriptionPeriod" + "=" + str((((self.getSubscriptionPeriod().__str__().replaceAll("  ", "    ")) if not self.getSubscriptionPeriod() == self else "this") if not (self.getSubscriptionPeriod() is None) else "null")) + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "subscriber = " + str(((format(id(self.getSubscriber()), "x")) if not (self.getSubscriber() is None) else "null")) + str(os.linesep) + "  " + "payments = " + ((format(id(self.getPayments()), "x")) if not (self.getPayments() is None) else "null")
