# %% NEW FILE MeetingFeePayment BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 194 "model.ump"
# line 360 "model.ump"
import os
from enum import Enum, auto

class MeetingFeePayment():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class MeetingFeePaymentStatus(Enum):
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
    #MeetingFeePayment Attributes
    #MeetingFeePayment Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aMeetingFee, aPayments):
        self._payments = None
        self._meetingFee = None
        self._status = None
        didAddMeetingFee = self.setMeetingFee(aMeetingFee)
        if not didAddMeetingFee :
            raise RuntimeError ("Unable to create meetingFeePayment due to meetingFee. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddPayments = self.setPayments(aPayments)
        if not didAddPayments :
            raise RuntimeError ("Unable to create meetingFeePayment due to payments. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def getStatus(self):
        return self._status

    # Code from template association_GetOne
    def getMeetingFee(self):
        return self._meetingFee

    # Code from template association_GetOne
    def getPayments(self):
        return self._payments

    # Code from template association_SetOneToMany
    def setMeetingFee(self, aMeetingFee):
        wasSet = False
        if aMeetingFee is None :
            return wasSet
        existingMeetingFee = self._meetingFee
        self._meetingFee = aMeetingFee
        if not (existingMeetingFee is None) and not existingMeetingFee == aMeetingFee :
            existingMeetingFee.removeMeetingFeePayment(self)
        self._meetingFee.addMeetingFeePayment(self)
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
            existingPayments.removeMeetingFeePayment(self)
        self._payments.addMeetingFeePayment(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderMeetingFee = self._meetingFee
        self._meetingFee = None
        if not (placeholderMeetingFee is None) :
            placeholderMeetingFee.removeMeetingFeePayment(self)
        placeholderPayments = self._payments
        self._payments = None
        if not (placeholderPayments is None) :
            placeholderPayments.removeMeetingFeePayment(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "meetingFee = " + str(((format(id(self.getMeetingFee()), "x")) if not (self.getMeetingFee() is None) else "null")) + str(os.linesep) + "  " + "payments = " + ((format(id(self.getPayments()), "x")) if not (self.getPayments() is None) else "null")
