# %% NEW FILE MeetingFee BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 186 "model.ump"
# line 355 "model.ump"
import os
from enum import Enum, auto

class MeetingFee():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class MeetingFeeStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        WaitingForPayment = auto()
        Paid = auto()
        Expired = auto()
        Canceled = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingFee Attributes
    #MeetingFee Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aPayer, aMeeting, aValue, aPayments):
        self._meetingFeePayments = None
        self._payments = None
        self._value = None
        self._meeting = None
        self._payer = None
        self._status = None
        if not self.setPayer(aPayer) :
            raise RuntimeError ("Unable to create MeetingFee due to aPayer. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeeting = self.setMeeting(aMeeting)
        if not didAddMeeting :
            raise RuntimeError ("Unable to create meetingFee due to meeting. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setValue(aValue) :
            raise RuntimeError ("Unable to create MeetingFee due to aValue. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddPayments = self.setPayments(aPayments)
        if not didAddPayments :
            raise RuntimeError ("Unable to create meetingFee due to payments. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._meetingFeePayments = []

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
    def getPayer(self):
        return self._payer

    # Code from template association_GetOne
    def getMeeting(self):
        return self._meeting

    # Code from template association_GetOne
    def getValue(self):
        return self._value

    # Code from template association_GetOne
    def getPayments(self):
        return self._payments

    # Code from template association_GetMany
    def getMeetingFeePayment(self, index):
        aMeetingFeePayment = self._meetingFeePayments[index]
        return aMeetingFeePayment

    def getMeetingFeePayments(self):
        newMeetingFeePayments = tuple(self._meetingFeePayments)
        return newMeetingFeePayments

    def numberOfMeetingFeePayments(self):
        number = len(self._meetingFeePayments)
        return number

    def hasMeetingFeePayments(self):
        has = len(self._meetingFeePayments) > 0
        return has

    def indexOfMeetingFeePayment(self, aMeetingFeePayment):
        index = (-1 if not aMeetingFeePayment in self._meetingFeePayments else self._meetingFeePayments.index(aMeetingFeePayment))
        return index

    # Code from template association_SetUnidirectionalOne
    def setPayer(self, aNewPayer):
        wasSet = False
        if not (aNewPayer is None) :
            self._payer = aNewPayer
            wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setMeeting(self, aMeeting):
        wasSet = False
        if aMeeting is None :
            return wasSet
        existingMeeting = self._meeting
        self._meeting = aMeeting
        if not (existingMeeting is None) and not existingMeeting == aMeeting :
            existingMeeting.removeMeetingFee(self)
        self._meeting.addMeetingFee(self)
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
            existingPayments.removeMeetingFee(self)
        self._payments.addMeetingFee(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingFeePayments():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingFeePayment1(self, aPayments):
        from .MeetingFeePayment import MeetingFeePayment
        return MeetingFeePayment(self, aPayments)

    def addMeetingFeePayment2(self, aMeetingFeePayment):
        wasAdded = False
        if (aMeetingFeePayment) in self._meetingFeePayments :
            return False
        existingMeetingFee = aMeetingFeePayment.getMeetingFee()
        isNewMeetingFee = not (existingMeetingFee is None) and not self == existingMeetingFee
        if isNewMeetingFee :
            aMeetingFeePayment.setMeetingFee(self)
        else :
            self._meetingFeePayments.append(aMeetingFeePayment)
        wasAdded = True
        return wasAdded

    def removeMeetingFeePayment(self, aMeetingFeePayment):
        wasRemoved = False
        #Unable to remove aMeetingFeePayment, as it must always have a meetingFee
        if not self == aMeetingFeePayment.getMeetingFee() :
            self._meetingFeePayments.remove(aMeetingFeePayment)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingFeePaymentAt(self, aMeetingFeePayment, index):
        wasAdded = False
        if self.addMeetingFeePayment(aMeetingFeePayment) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingFeePayments() :
                index = self.numberOfMeetingFeePayments() - 1
            self._meetingFeePayments.remove(aMeetingFeePayment)
            self._meetingFeePayments.insert(index, aMeetingFeePayment)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingFeePaymentAt(self, aMeetingFeePayment, index):
        wasAdded = False
        if (aMeetingFeePayment) in self._meetingFeePayments :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingFeePayments() :
                index = self.numberOfMeetingFeePayments() - 1
            self._meetingFeePayments.remove(aMeetingFeePayment)
            self._meetingFeePayments.insert(index, aMeetingFeePayment)
            wasAdded = True
        else :
            wasAdded = self.addMeetingFeePaymentAt(aMeetingFeePayment, index)
        return wasAdded

    def delete(self):
        self._payer = None
        placeholderMeeting = self._meeting
        self._meeting = None
        if not (placeholderMeeting is None) :
            placeholderMeeting.removeMeetingFee(self)
        self._value = None
        placeholderPayments = self._payments
        self._payments = None
        if not (placeholderPayments is None) :
            placeholderPayments.removeMeetingFee(self)
        i = len(self._meetingFeePayments)
        while i > 0 :
            aMeetingFeePayment = self._meetingFeePayments[i - 1]
            aMeetingFeePayment.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "payer = " + str(((format(id(self.getPayer()), "x")) if not (self.getPayer() is None) else "null")) + str(os.linesep) + "  " + "meeting = " + str(((format(id(self.getMeeting()), "x")) if not (self.getMeeting() is None) else "null")) + str(os.linesep) + "  " + "value = " + str(((format(id(self.getValue()), "x")) if not (self.getValue() is None) else "null")) + str(os.linesep) + "  " + "payments = " + ((format(id(self.getPayments()), "x")) if not (self.getPayments() is None) else "null")

    def addMeetingFeePayment(self, *argv):
        from .MeetingFeePayment import MeetingFeePayment
        from .Payments import Payments
        if len(argv) == 1 and isinstance(argv[0], Payments) :
            return self.addMeetingFeePayment1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], MeetingFeePayment) :
            return self.addMeetingFeePayment2(argv[0])
        raise TypeError("No method matches provided parameters")
