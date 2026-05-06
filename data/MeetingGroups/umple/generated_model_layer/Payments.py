# %% NEW FILE Payments BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 22 "model.ump"
# line 260 "model.ump"
from enum import Enum, auto
from datetime import date

class Payments():
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

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Payments Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._priceLists = None
        self._subscriptionRenewalPayments = None
        self._subscriptionPayments = None
        self._subscriptions = None
        self._meetingFeePayments = None
        self._meetingFees = None
        self._meetingFees = []
        self._meetingFeePayments = []
        self._subscriptions = []
        self._subscriptionPayments = []
        self._subscriptionRenewalPayments = []
        self._priceLists = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany
    def getMeetingFee(self, index):
        aMeetingFee = self._meetingFees[index]
        return aMeetingFee

    def getMeetingFees(self):
        newMeetingFees = tuple(self._meetingFees)
        return newMeetingFees

    def numberOfMeetingFees(self):
        number = len(self._meetingFees)
        return number

    def hasMeetingFees(self):
        has = len(self._meetingFees) > 0
        return has

    def indexOfMeetingFee(self, aMeetingFee):
        index = (-1 if not aMeetingFee in self._meetingFees else self._meetingFees.index(aMeetingFee))
        return index

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

    # Code from template association_GetMany
    def getSubscription(self, index):
        aSubscription = self._subscriptions[index]
        return aSubscription

    def getSubscriptions(self):
        newSubscriptions = tuple(self._subscriptions)
        return newSubscriptions

    def numberOfSubscriptions(self):
        number = len(self._subscriptions)
        return number

    def hasSubscriptions(self):
        has = len(self._subscriptions) > 0
        return has

    def indexOfSubscription(self, aSubscription):
        index = (-1 if not aSubscription in self._subscriptions else self._subscriptions.index(aSubscription))
        return index

    # Code from template association_GetMany
    def getSubscriptionPayment(self, index):
        aSubscriptionPayment = self._subscriptionPayments[index]
        return aSubscriptionPayment

    def getSubscriptionPayments(self):
        newSubscriptionPayments = tuple(self._subscriptionPayments)
        return newSubscriptionPayments

    def numberOfSubscriptionPayments(self):
        number = len(self._subscriptionPayments)
        return number

    def hasSubscriptionPayments(self):
        has = len(self._subscriptionPayments) > 0
        return has

    def indexOfSubscriptionPayment(self, aSubscriptionPayment):
        index = (-1 if not aSubscriptionPayment in self._subscriptionPayments else self._subscriptionPayments.index(aSubscriptionPayment))
        return index

    # Code from template association_GetMany
    def getSubscriptionRenewalPayment(self, index):
        aSubscriptionRenewalPayment = self._subscriptionRenewalPayments[index]
        return aSubscriptionRenewalPayment

    def getSubscriptionRenewalPayments(self):
        newSubscriptionRenewalPayments = tuple(self._subscriptionRenewalPayments)
        return newSubscriptionRenewalPayments

    def numberOfSubscriptionRenewalPayments(self):
        number = len(self._subscriptionRenewalPayments)
        return number

    def hasSubscriptionRenewalPayments(self):
        has = len(self._subscriptionRenewalPayments) > 0
        return has

    def indexOfSubscriptionRenewalPayment(self, aSubscriptionRenewalPayment):
        index = (-1 if not aSubscriptionRenewalPayment in self._subscriptionRenewalPayments else self._subscriptionRenewalPayments.index(aSubscriptionRenewalPayment))
        return index

    # Code from template association_GetMany
    def getPriceList(self, index):
        aPriceList = self._priceLists[index]
        return aPriceList

    def getPriceLists(self):
        newPriceLists = tuple(self._priceLists)
        return newPriceLists

    def numberOfPriceLists(self):
        number = len(self._priceLists)
        return number

    def hasPriceLists(self):
        has = len(self._priceLists) > 0
        return has

    def indexOfPriceList(self, aPriceList):
        index = (-1 if not aPriceList in self._priceLists else self._priceLists.index(aPriceList))
        return index

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingFees():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingFee1(self, aPayer, aMeeting, aValue):
        from .MeetingFee import MeetingFee
        return MeetingFee(aPayer, aMeeting, aValue, self)

    def addMeetingFee2(self, aMeetingFee):
        wasAdded = False
        if (aMeetingFee) in self._meetingFees :
            return False
        existingPayments = aMeetingFee.getPayments()
        isNewPayments = not (existingPayments is None) and not self == existingPayments
        if isNewPayments :
            aMeetingFee.setPayments(self)
        else :
            self._meetingFees.append(aMeetingFee)
        wasAdded = True
        return wasAdded

    def removeMeetingFee(self, aMeetingFee):
        wasRemoved = False
        #Unable to remove aMeetingFee, as it must always have a payments
        if not self == aMeetingFee.getPayments() :
            self._meetingFees.remove(aMeetingFee)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingFeeAt(self, aMeetingFee, index):
        wasAdded = False
        if self.addMeetingFee(aMeetingFee) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingFees() :
                index = self.numberOfMeetingFees() - 1
            self._meetingFees.remove(aMeetingFee)
            self._meetingFees.insert(index, aMeetingFee)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingFeeAt(self, aMeetingFee, index):
        wasAdded = False
        if (aMeetingFee) in self._meetingFees :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingFees() :
                index = self.numberOfMeetingFees() - 1
            self._meetingFees.remove(aMeetingFee)
            self._meetingFees.insert(index, aMeetingFee)
            wasAdded = True
        else :
            wasAdded = self.addMeetingFeeAt(aMeetingFee, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingFeePayments():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingFeePayment1(self, aMeetingFee):
        from .MeetingFeePayment import MeetingFeePayment
        return MeetingFeePayment(aMeetingFee, self)

    def addMeetingFeePayment2(self, aMeetingFeePayment):
        wasAdded = False
        if (aMeetingFeePayment) in self._meetingFeePayments :
            return False
        existingPayments = aMeetingFeePayment.getPayments()
        isNewPayments = not (existingPayments is None) and not self == existingPayments
        if isNewPayments :
            aMeetingFeePayment.setPayments(self)
        else :
            self._meetingFeePayments.append(aMeetingFeePayment)
        wasAdded = True
        return wasAdded

    def removeMeetingFeePayment(self, aMeetingFeePayment):
        wasRemoved = False
        #Unable to remove aMeetingFeePayment, as it must always have a payments
        if not self == aMeetingFeePayment.getPayments() :
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

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfSubscriptions():
        return 0

    # Code from template association_AddManyToOne
    def addSubscription1(self, aCountryCode, aExpirationDate, aSubscriptionPeriod, aStatus, aSubscriber):
        from .Subscription import Subscription
        return Subscription(aCountryCode, aExpirationDate, aSubscriptionPeriod, aStatus, aSubscriber, self)

    def addSubscription2(self, aSubscription):
        wasAdded = False
        if (aSubscription) in self._subscriptions :
            return False
        existingPayments = aSubscription.getPayments()
        isNewPayments = not (existingPayments is None) and not self == existingPayments
        if isNewPayments :
            aSubscription.setPayments(self)
        else :
            self._subscriptions.append(aSubscription)
        wasAdded = True
        return wasAdded

    def removeSubscription(self, aSubscription):
        wasRemoved = False
        #Unable to remove aSubscription, as it must always have a payments
        if not self == aSubscription.getPayments() :
            self._subscriptions.remove(aSubscription)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addSubscriptionAt(self, aSubscription, index):
        wasAdded = False
        if self.addSubscription(aSubscription) :
            if index < 0 :
                index = 0
            if index > self.numberOfSubscriptions() :
                index = self.numberOfSubscriptions() - 1
            self._subscriptions.remove(aSubscription)
            self._subscriptions.insert(index, aSubscription)
            wasAdded = True
        return wasAdded

    def addOrMoveSubscriptionAt(self, aSubscription, index):
        wasAdded = False
        if (aSubscription) in self._subscriptions :
            if index < 0 :
                index = 0
            if index > self.numberOfSubscriptions() :
                index = self.numberOfSubscriptions() - 1
            self._subscriptions.remove(aSubscription)
            self._subscriptions.insert(index, aSubscription)
            wasAdded = True
        else :
            wasAdded = self.addSubscriptionAt(aSubscription, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfSubscriptionPayments():
        return 0

    # Code from template association_AddManyToOne
    def addSubscriptionPayment1(self, aCountryCode, aSubscriptionPeriod, aPayer, aValue):
        from .SubscriptionPayment import SubscriptionPayment
        return SubscriptionPayment(aCountryCode, aSubscriptionPeriod, aPayer, aValue, self)

    def addSubscriptionPayment2(self, aSubscriptionPayment):
        wasAdded = False
        if (aSubscriptionPayment) in self._subscriptionPayments :
            return False
        existingPayments = aSubscriptionPayment.getPayments()
        isNewPayments = not (existingPayments is None) and not self == existingPayments
        if isNewPayments :
            aSubscriptionPayment.setPayments(self)
        else :
            self._subscriptionPayments.append(aSubscriptionPayment)
        wasAdded = True
        return wasAdded

    def removeSubscriptionPayment(self, aSubscriptionPayment):
        wasRemoved = False
        #Unable to remove aSubscriptionPayment, as it must always have a payments
        if not self == aSubscriptionPayment.getPayments() :
            self._subscriptionPayments.remove(aSubscriptionPayment)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addSubscriptionPaymentAt(self, aSubscriptionPayment, index):
        wasAdded = False
        if self.addSubscriptionPayment(aSubscriptionPayment) :
            if index < 0 :
                index = 0
            if index > self.numberOfSubscriptionPayments() :
                index = self.numberOfSubscriptionPayments() - 1
            self._subscriptionPayments.remove(aSubscriptionPayment)
            self._subscriptionPayments.insert(index, aSubscriptionPayment)
            wasAdded = True
        return wasAdded

    def addOrMoveSubscriptionPaymentAt(self, aSubscriptionPayment, index):
        wasAdded = False
        if (aSubscriptionPayment) in self._subscriptionPayments :
            if index < 0 :
                index = 0
            if index > self.numberOfSubscriptionPayments() :
                index = self.numberOfSubscriptionPayments() - 1
            self._subscriptionPayments.remove(aSubscriptionPayment)
            self._subscriptionPayments.insert(index, aSubscriptionPayment)
            wasAdded = True
        else :
            wasAdded = self.addSubscriptionPaymentAt(aSubscriptionPayment, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfSubscriptionRenewalPayments():
        return 0

    # Code from template association_AddManyToOne
    def addSubscriptionRenewalPayment1(self, aCountryCode, aSubscriptionPeriod, aPayer, aValue):
        from .SubscriptionRenewalPayment import SubscriptionRenewalPayment
        return SubscriptionRenewalPayment(aCountryCode, aSubscriptionPeriod, aPayer, aValue, self)

    def addSubscriptionRenewalPayment2(self, aSubscriptionRenewalPayment):
        wasAdded = False
        if (aSubscriptionRenewalPayment) in self._subscriptionRenewalPayments :
            return False
        existingPayments = aSubscriptionRenewalPayment.getPayments()
        isNewPayments = not (existingPayments is None) and not self == existingPayments
        if isNewPayments :
            aSubscriptionRenewalPayment.setPayments(self)
        else :
            self._subscriptionRenewalPayments.append(aSubscriptionRenewalPayment)
        wasAdded = True
        return wasAdded

    def removeSubscriptionRenewalPayment(self, aSubscriptionRenewalPayment):
        wasRemoved = False
        #Unable to remove aSubscriptionRenewalPayment, as it must always have a payments
        if not self == aSubscriptionRenewalPayment.getPayments() :
            self._subscriptionRenewalPayments.remove(aSubscriptionRenewalPayment)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addSubscriptionRenewalPaymentAt(self, aSubscriptionRenewalPayment, index):
        wasAdded = False
        if self.addSubscriptionRenewalPayment(aSubscriptionRenewalPayment) :
            if index < 0 :
                index = 0
            if index > self.numberOfSubscriptionRenewalPayments() :
                index = self.numberOfSubscriptionRenewalPayments() - 1
            self._subscriptionRenewalPayments.remove(aSubscriptionRenewalPayment)
            self._subscriptionRenewalPayments.insert(index, aSubscriptionRenewalPayment)
            wasAdded = True
        return wasAdded

    def addOrMoveSubscriptionRenewalPaymentAt(self, aSubscriptionRenewalPayment, index):
        wasAdded = False
        if (aSubscriptionRenewalPayment) in self._subscriptionRenewalPayments :
            if index < 0 :
                index = 0
            if index > self.numberOfSubscriptionRenewalPayments() :
                index = self.numberOfSubscriptionRenewalPayments() - 1
            self._subscriptionRenewalPayments.remove(aSubscriptionRenewalPayment)
            self._subscriptionRenewalPayments.insert(index, aSubscriptionRenewalPayment)
            wasAdded = True
        else :
            wasAdded = self.addSubscriptionRenewalPaymentAt(aSubscriptionRenewalPayment, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfPriceLists():
        return 0

    # Code from template association_AddManyToOne
    def addPriceList1(self, aPricingStrategy):
        from .PriceList import PriceList
        return PriceList(aPricingStrategy, self)

    def addPriceList2(self, aPriceList):
        wasAdded = False
        if (aPriceList) in self._priceLists :
            return False
        existingPayments = aPriceList.getPayments()
        isNewPayments = not (existingPayments is None) and not self == existingPayments
        if isNewPayments :
            aPriceList.setPayments(self)
        else :
            self._priceLists.append(aPriceList)
        wasAdded = True
        return wasAdded

    def removePriceList(self, aPriceList):
        wasRemoved = False
        #Unable to remove aPriceList, as it must always have a payments
        if not self == aPriceList.getPayments() :
            self._priceLists.remove(aPriceList)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addPriceListAt(self, aPriceList, index):
        wasAdded = False
        if self.addPriceList(aPriceList) :
            if index < 0 :
                index = 0
            if index > self.numberOfPriceLists() :
                index = self.numberOfPriceLists() - 1
            self._priceLists.remove(aPriceList)
            self._priceLists.insert(index, aPriceList)
            wasAdded = True
        return wasAdded

    def addOrMovePriceListAt(self, aPriceList, index):
        wasAdded = False
        if (aPriceList) in self._priceLists :
            if index < 0 :
                index = 0
            if index > self.numberOfPriceLists() :
                index = self.numberOfPriceLists() - 1
            self._priceLists.remove(aPriceList)
            self._priceLists.insert(index, aPriceList)
            wasAdded = True
        else :
            wasAdded = self.addPriceListAt(aPriceList, index)
        return wasAdded

    def delete(self):

        while len(self._meetingFees) > 0 :
            aMeetingFee = self._meetingFees[len(self._meetingFees) - 1]
            aMeetingFee.delete()
            self._meetingFees.remove(aMeetingFee)

        while len(self._meetingFeePayments) > 0 :
            aMeetingFeePayment = self._meetingFeePayments[len(self._meetingFeePayments) - 1]
            aMeetingFeePayment.delete()
            self._meetingFeePayments.remove(aMeetingFeePayment)

        while len(self._subscriptions) > 0 :
            aSubscription = self._subscriptions[len(self._subscriptions) - 1]
            aSubscription.delete()
            self._subscriptions.remove(aSubscription)

        while len(self._subscriptionPayments) > 0 :
            aSubscriptionPayment = self._subscriptionPayments[len(self._subscriptionPayments) - 1]
            aSubscriptionPayment.delete()
            self._subscriptionPayments.remove(aSubscriptionPayment)

        while len(self._subscriptionRenewalPayments) > 0 :
            aSubscriptionRenewalPayment = self._subscriptionRenewalPayments[len(self._subscriptionRenewalPayments) - 1]
            aSubscriptionRenewalPayment.delete()
            self._subscriptionRenewalPayments.remove(aSubscriptionRenewalPayment)

        while len(self._priceLists) > 0 :
            aPriceList = self._priceLists[len(self._priceLists) - 1]
            aPriceList.delete()
            self._priceLists.remove(aPriceList)

    def addMeetingFee(self, *argv):
        from .MeetingFee import MeetingFee
        from .Member import Member
        from .Meeting import Meeting
        from .MoneyValue import MoneyValue
        if len(argv) == 3 and isinstance(argv[0], Member) and isinstance(argv[1], Meeting) and isinstance(argv[2], MoneyValue) :
            return self.addMeetingFee1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MeetingFee) :
            return self.addMeetingFee2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingFeePayment(self, *argv):
        from .MeetingFeePayment import MeetingFeePayment
        from .MeetingFee import MeetingFee
        if len(argv) == 1 and isinstance(argv[0], MeetingFee) :
            return self.addMeetingFeePayment1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], MeetingFeePayment) :
            return self.addMeetingFeePayment2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addSubscription(self, *argv):
        from .Subscription import Subscription
        from .Member import Member
        if len(argv) == 5 and isinstance(argv[0], str) and isinstance(argv[1], date) and isinstance(argv[2], Subscription.SubscriptionPeriod) and isinstance(argv[3], Subscription.SubscriptionStatus) and isinstance(argv[4], Member) :
            return self.addSubscription1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], Subscription) :
            return self.addSubscription2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addSubscriptionPayment(self, *argv):
        from .Subscription import Subscription
        from .SubscriptionPayment import SubscriptionPayment
        from .Member import Member
        from .MoneyValue import MoneyValue
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], Subscription.SubscriptionPeriod) and isinstance(argv[2], Member) and isinstance(argv[3], MoneyValue) :
            return self.addSubscriptionPayment1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], SubscriptionPayment) :
            return self.addSubscriptionPayment2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addSubscriptionRenewalPayment(self, *argv):
        from .Subscription import Subscription
        from .SubscriptionRenewalPayment import SubscriptionRenewalPayment
        from .Member import Member
        from .MoneyValue import MoneyValue
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], Subscription.SubscriptionPeriod) and isinstance(argv[2], Member) and isinstance(argv[3], MoneyValue) :
            return self.addSubscriptionRenewalPayment1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], SubscriptionRenewalPayment) :
            return self.addSubscriptionRenewalPayment2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addPriceList(self, *argv):
        from .PriceList import PriceList
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addPriceList1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], PriceList) :
            return self.addPriceList2(argv[0])
        raise TypeError("No method matches provided parameters")
