"""Definition of meta model 'meetinggroups'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'meetinggroups'
nsURI = 'meetinggroups'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
UserRegistrationStatus = EEnum('UserRegistrationStatus', literals=[
                               'WaitingForConfirmation', 'Confirmed', 'Expired'])

MeetingGroupProposalStatus = EEnum('MeetingGroupProposalStatus', literals=[
                                   'ToVerify', 'Verified', 'Rejected'])

MeetingGroupProposalDecisionCode = EEnum('MeetingGroupProposalDecisionCode', literals=[
                                         'NoDecision', 'Accept', 'Reject'])

MeetingGroupMemberRole = EEnum('MeetingGroupMemberRole', literals=['Organizer', 'Member'])

MeetingAttendeeRole = EEnum('MeetingAttendeeRole', literals=['Host', 'Attendee'])

MeetingFeeStatus = EEnum('MeetingFeeStatus', literals=[
                         'WaitingForPayment', 'Paid', 'Expired', 'Canceled'])

MeetingFeePaymentStatus = EEnum('MeetingFeePaymentStatus', literals=[
                                'WaitingForPayment', 'Paid', 'Expired'])

SubscriptionPeriod = EEnum('SubscriptionPeriod', literals=['Month', 'HalfYear'])

SubscriptionStatus = EEnum('SubscriptionStatus', literals=['Active', 'Expired'])

SubscriptionPaymentStatus = EEnum('SubscriptionPaymentStatus', literals=[
                                  'WaitingForPayment', 'Paid', 'Expired'])

SubscriptionRenewalPaymentStatus = EEnum('SubscriptionRenewalPaymentStatus', literals=[
                                         'WaitingForPayment', 'Paid', 'Expired'])

PriceListItemCategory = EEnum('PriceListItemCategory', literals=['New', 'Renewal'])


class UserAccess(EObject, metaclass=MetaEClass):

    users = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    userRegistrations = EReference(ordered=True, unique=True,
                                   containment=True, derived=False, upper=-1)

    def __init__(self, *, users=None, userRegistrations=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if users:
            self.users.extend(users)

        if userRegistrations:
            self.userRegistrations.extend(userRegistrations)


class Administration(EObject, metaclass=MetaEClass):

    administrators = EReference(ordered=True, unique=True,
                                containment=True, derived=False, upper=-1)

    def __init__(self, *, administrators=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if administrators:
            self.administrators.extend(administrators)


class Meetings(EObject, metaclass=MetaEClass):

    members = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    meetingGroupProposals = EReference(ordered=True, unique=True,
                                       containment=True, derived=False, upper=-1)
    meetingGroups = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    meetings = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    meetingLocations = EReference(ordered=True, unique=True,
                                  containment=True, derived=False, upper=-1)
    meetingAttendees = EReference(ordered=True, unique=True,
                                  containment=True, derived=False, upper=-1)
    meetingNotAttendees = EReference(ordered=True, unique=True,
                                     containment=True, derived=False, upper=-1)
    meetingWaitlistMembers = EReference(
        ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, members=None, meetingGroupProposals=None, meetingGroups=None, meetings=None, meetingLocations=None, meetingAttendees=None, meetingNotAttendees=None, meetingWaitlistMembers=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if members:
            self.members.extend(members)

        if meetingGroupProposals:
            self.meetingGroupProposals.extend(meetingGroupProposals)

        if meetingGroups:
            self.meetingGroups.extend(meetingGroups)

        if meetings:
            self.meetings.extend(meetings)

        if meetingLocations:
            self.meetingLocations.extend(meetingLocations)

        if meetingAttendees:
            self.meetingAttendees.extend(meetingAttendees)

        if meetingNotAttendees:
            self.meetingNotAttendees.extend(meetingNotAttendees)

        if meetingWaitlistMembers:
            self.meetingWaitlistMembers.extend(meetingWaitlistMembers)


class Payments(EObject, metaclass=MetaEClass):

    meetingFees = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    meetingFeePayments = EReference(ordered=True, unique=True,
                                    containment=True, derived=False, upper=-1)
    subscriptions = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    subscriptionPayments = EReference(ordered=True, unique=True,
                                      containment=True, derived=False, upper=-1)
    subscriptionRenewalPayments = EReference(
        ordered=True, unique=True, containment=True, derived=False, upper=-1)
    priceLists = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, meetingFees=None, meetingFeePayments=None, subscriptions=None, subscriptionPayments=None, subscriptionRenewalPayments=None, priceLists=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if meetingFees:
            self.meetingFees.extend(meetingFees)

        if meetingFeePayments:
            self.meetingFeePayments.extend(meetingFeePayments)

        if subscriptions:
            self.subscriptions.extend(subscriptions)

        if subscriptionPayments:
            self.subscriptionPayments.extend(subscriptionPayments)

        if subscriptionRenewalPayments:
            self.subscriptionRenewalPayments.extend(subscriptionRenewalPayments)

        if priceLists:
            self.priceLists.extend(priceLists)


class UserRegistration(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    login = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    firstName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    lastName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    registerDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    confirmedDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=UserRegistrationStatus, unique=True, derived=False, changeable=True)
    userAccess = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, userAccess=None, id=None, login=None, email=None, firstName=None, lastName=None, name=None, registerDate=None, confirmedDate=None, status=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if login is not None:
            self.login = login

        if email is not None:
            self.email = email

        if firstName is not None:
            self.firstName = firstName

        if lastName is not None:
            self.lastName = lastName

        if name is not None:
            self.name = name

        if registerDate is not None:
            self.registerDate = registerDate

        if confirmedDate is not None:
            self.confirmedDate = confirmedDate

        if status is not None:
            self.status = status

        if userAccess is not None:
            self.userAccess = userAccess


class User(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    login = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    firstName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    lastName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    createDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    userAccess = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, userAccess=None, id=None, login=None, email=None, firstName=None, lastName=None, name=None, createDate=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if login is not None:
            self.login = login

        if email is not None:
            self.email = email

        if firstName is not None:
            self.firstName = firstName

        if lastName is not None:
            self.lastName = lastName

        if name is not None:
            self.name = name

        if createDate is not None:
            self.createDate = createDate

        if userAccess is not None:
            self.userAccess = userAccess


class MeetingGroupLocation(EObject, metaclass=MetaEClass):

    city = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    countryCode = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, city=None, countryCode=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if city is not None:
            self.city = city

        if countryCode is not None:
            self.countryCode = countryCode


class MeetingGroupProposal(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    proposalDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=MeetingGroupProposalStatus,
                        unique=True, derived=False, changeable=True)
    meetingGroupLocation = EReference(ordered=True, unique=True, containment=False, derived=False)
    member = EReference(ordered=True, unique=True, containment=False, derived=False)
    decisions = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, name=None, description=None, proposalDate=None, status=None, meetingGroupLocation=None, member=None, decisions=None, meetings=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if proposalDate is not None:
            self.proposalDate = proposalDate

        if status is not None:
            self.status = status

        if meetingGroupLocation is not None:
            self.meetingGroupLocation = meetingGroupLocation

        if member is not None:
            self.member = member

        if decisions:
            self.decisions.extend(decisions)

        if meetings is not None:
            self.meetings = meetings


class MeetingGroupProposalDecision(EObject, metaclass=MetaEClass):

    rejectReason = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    date = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    code = EAttribute(eType=MeetingGroupProposalDecisionCode,
                      unique=True, derived=False, changeable=True)
    proposal = EReference(ordered=True, unique=True, containment=False, derived=False)
    administrator = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, rejectReason=None, date=None, code=None, proposal=None, administrator=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if rejectReason is not None:
            self.rejectReason = rejectReason

        if date is not None:
            self.date = date

        if code is not None:
            self.code = code

        if proposal is not None:
            self.proposal = proposal

        if administrator is not None:
            self.administrator = administrator


class MeetingGroup(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    createDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    paymentDateTo = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    meetingGroupLocation = EReference(ordered=True, unique=True, containment=False, derived=False)
    creator = EReference(ordered=True, unique=True, containment=False, derived=False)
    members = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, name=None, description=None, createDate=None, paymentDateTo=None, meetingGroupLocation=None, creator=None, members=None, meetings=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if createDate is not None:
            self.createDate = createDate

        if paymentDateTo is not None:
            self.paymentDateTo = paymentDateTo

        if meetingGroupLocation is not None:
            self.meetingGroupLocation = meetingGroupLocation

        if creator is not None:
            self.creator = creator

        if members:
            self.members.extend(members)

        if meetings is not None:
            self.meetings = meetings


class MeetingGroupMember(EObject, metaclass=MetaEClass):

    joinedDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    isActive = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    role = EAttribute(eType=MeetingGroupMemberRole, unique=True, derived=False, changeable=True)
    member = EReference(ordered=True, unique=True, containment=False, derived=False)
    meetingGroup = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, joinedDate=None, isActive=None, role=None, member=None, meetingGroup=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if joinedDate is not None:
            self.joinedDate = joinedDate

        if isActive is not None:
            self.isActive = isActive

        if role is not None:
            self.role = role

        if member is not None:
            self.member = member

        if meetingGroup is not None:
            self.meetingGroup = meetingGroup


class MeetingLocation(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    city = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    countryCode = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, name=None, address=None, city=None, countryCode=None, meetings=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if address is not None:
            self.address = address

        if city is not None:
            self.city = city

        if countryCode is not None:
            self.countryCode = countryCode

        if meetings is not None:
            self.meetings = meetings


class Term(EObject, metaclass=MetaEClass):

    startDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    endDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)

    def __init__(self, *, startDate=None, endDate=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if startDate is not None:
            self.startDate = startDate

        if endDate is not None:
            self.endDate = endDate


class MeetingTerm(EObject, metaclass=MetaEClass):

    startDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    endDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)

    def __init__(self, *, startDate=None, endDate=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if startDate is not None:
            self.startDate = startDate

        if endDate is not None:
            self.endDate = endDate


class Meeting(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    title = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    createDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    changeDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    cancelDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    isCanceled = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    term = EReference(ordered=True, unique=True, containment=True, derived=False)
    location = EReference(ordered=True, unique=True, containment=False, derived=False)
    rsvpTerm = EReference(ordered=True, unique=True, containment=True, derived=False)
    creator = EReference(ordered=True, unique=True, containment=False, derived=False)
    changeMember = EReference(ordered=True, unique=True, containment=False, derived=False)
    cancelMember = EReference(ordered=True, unique=True, containment=False, derived=False)
    meetingAttendees = EReference(ordered=True, unique=True,
                                  containment=False, derived=False, upper=-1)
    meetingNotAttendees = EReference(ordered=True, unique=True,
                                     containment=False, derived=False, upper=-1)
    meetingWaitlistMembers = EReference(
        ordered=True, unique=True, containment=False, derived=False, upper=-1)
    meetingLimit = EReference(ordered=True, unique=True, containment=False, derived=False)
    meetingFees = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, title=None, description=None, createDate=None, changeDate=None, cancelDate=None, isCanceled=None, term=None, location=None, rsvpTerm=None, creator=None, changeMember=None, cancelMember=None, meetingAttendees=None, meetingNotAttendees=None, meetingWaitlistMembers=None, meetingLimit=None, meetingFees=None, meetings=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if createDate is not None:
            self.createDate = createDate

        if changeDate is not None:
            self.changeDate = changeDate

        if cancelDate is not None:
            self.cancelDate = cancelDate

        if isCanceled is not None:
            self.isCanceled = isCanceled

        if term is not None:
            self.term = term

        if location is not None:
            self.location = location

        if rsvpTerm is not None:
            self.rsvpTerm = rsvpTerm

        if creator is not None:
            self.creator = creator

        if changeMember is not None:
            self.changeMember = changeMember

        if cancelMember is not None:
            self.cancelMember = cancelMember

        if meetingAttendees:
            self.meetingAttendees.extend(meetingAttendees)

        if meetingNotAttendees:
            self.meetingNotAttendees.extend(meetingNotAttendees)

        if meetingWaitlistMembers:
            self.meetingWaitlistMembers.extend(meetingWaitlistMembers)

        if meetingLimit is not None:
            self.meetingLimit = meetingLimit

        if meetingFees:
            self.meetingFees.extend(meetingFees)

        if meetings is not None:
            self.meetings = meetings


class MeetingAttendee(EObject, metaclass=MetaEClass):

    guestNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    decisionChanged = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    isFeePaid = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    isRemoved = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    removingReason = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    decisionDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    decisionChangeDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    removedDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    role = EAttribute(eType=MeetingAttendeeRole, unique=True, derived=False, changeable=True)
    attendee = EReference(ordered=True, unique=True, containment=False, derived=False)
    fee = EReference(ordered=True, unique=True, containment=False, derived=False)
    removingMember = EReference(ordered=True, unique=True, containment=False, derived=False)
    meeting = EReference(ordered=True, unique=True, containment=False, derived=False)
    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, guestNumber=None, decisionChanged=None, isFeePaid=None, isRemoved=None, removingReason=None, decisionDate=None, decisionChangeDate=None, removedDate=None, role=None, attendee=None, fee=None, removingMember=None, meeting=None, meetings=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if guestNumber is not None:
            self.guestNumber = guestNumber

        if decisionChanged is not None:
            self.decisionChanged = decisionChanged

        if isFeePaid is not None:
            self.isFeePaid = isFeePaid

        if isRemoved is not None:
            self.isRemoved = isRemoved

        if removingReason is not None:
            self.removingReason = removingReason

        if decisionDate is not None:
            self.decisionDate = decisionDate

        if decisionChangeDate is not None:
            self.decisionChangeDate = decisionChangeDate

        if removedDate is not None:
            self.removedDate = removedDate

        if role is not None:
            self.role = role

        if attendee is not None:
            self.attendee = attendee

        if fee is not None:
            self.fee = fee

        if removingMember is not None:
            self.removingMember = removingMember

        if meeting is not None:
            self.meeting = meeting

        if meetings is not None:
            self.meetings = meetings


class MeetingNotAttendee(EObject, metaclass=MetaEClass):

    decisionChanged = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    decisionDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    decisionChangeDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    member = EReference(ordered=True, unique=True, containment=False, derived=False)
    meeting = EReference(ordered=True, unique=True, containment=False, derived=False)
    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, decisionChanged=None, decisionDate=None, decisionChangeDate=None, member=None, meeting=None, meetings=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if decisionChanged is not None:
            self.decisionChanged = decisionChanged

        if decisionDate is not None:
            self.decisionDate = decisionDate

        if decisionChangeDate is not None:
            self.decisionChangeDate = decisionChangeDate

        if member is not None:
            self.member = member

        if meeting is not None:
            self.meeting = meeting

        if meetings is not None:
            self.meetings = meetings


class MeetingWaitlistMember(EObject, metaclass=MetaEClass):

    decisionChanged = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    decisionDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    signUpDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    signOffDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    movedToAttendeesDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    isMovedToAttendees = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    member = EReference(ordered=True, unique=True, containment=False, derived=False)
    meeting = EReference(ordered=True, unique=True, containment=False, derived=False)
    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, decisionChanged=None, decisionDate=None, signUpDate=None, signOffDate=None, movedToAttendeesDate=None, isMovedToAttendees=None, member=None, meeting=None, meetings=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if decisionChanged is not None:
            self.decisionChanged = decisionChanged

        if decisionDate is not None:
            self.decisionDate = decisionDate

        if signUpDate is not None:
            self.signUpDate = signUpDate

        if signOffDate is not None:
            self.signOffDate = signOffDate

        if movedToAttendeesDate is not None:
            self.movedToAttendeesDate = movedToAttendeesDate

        if isMovedToAttendees is not None:
            self.isMovedToAttendees = isMovedToAttendees

        if member is not None:
            self.member = member

        if meeting is not None:
            self.meeting = meeting

        if meetings is not None:
            self.meetings = meetings


class MeetingLimit(EObject, metaclass=MetaEClass):

    attendeesLimit = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    guestsLimit = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)

    def __init__(self, *, attendeesLimit=None, guestsLimit=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if attendeesLimit is not None:
            self.attendeesLimit = attendeesLimit

        if guestsLimit is not None:
            self.guestsLimit = guestsLimit


class MoneyValue(EObject, metaclass=MetaEClass):

    value = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    currency = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, value=None, currency=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if value is not None:
            self.value = value

        if currency is not None:
            self.currency = currency


class MeetingFee(EObject, metaclass=MetaEClass):

    status = EAttribute(eType=MeetingFeeStatus, unique=True, derived=False, changeable=True)
    payer = EReference(ordered=True, unique=True, containment=False, derived=False)
    meeting = EReference(ordered=True, unique=True, containment=False, derived=False)
    value = EReference(ordered=True, unique=True, containment=True, derived=False)
    meetingFeePayments = EReference(ordered=True, unique=True,
                                    containment=False, derived=False, upper=-1)
    payments = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, status=None, payer=None, meeting=None, value=None, meetingFeePayments=None, payments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if status is not None:
            self.status = status

        if payer is not None:
            self.payer = payer

        if meeting is not None:
            self.meeting = meeting

        if value is not None:
            self.value = value

        if meetingFeePayments:
            self.meetingFeePayments.extend(meetingFeePayments)

        if payments is not None:
            self.payments = payments


class MeetingFeePayment(EObject, metaclass=MetaEClass):

    status = EAttribute(eType=MeetingFeePaymentStatus, unique=True, derived=False, changeable=True)
    meetingFee = EReference(ordered=True, unique=True, containment=False, derived=False)
    payments = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, status=None, meetingFee=None, payments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if status is not None:
            self.status = status

        if meetingFee is not None:
            self.meetingFee = meetingFee

        if payments is not None:
            self.payments = payments


class Subscription(EObject, metaclass=MetaEClass):

    countryCode = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    expirationDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    subscriptionPeriod = EAttribute(eType=SubscriptionPeriod,
                                    unique=True, derived=False, changeable=True)
    status = EAttribute(eType=SubscriptionStatus, unique=True, derived=False, changeable=True)
    subscriber = EReference(ordered=True, unique=True, containment=False, derived=False)
    payments = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, countryCode=None, expirationDate=None, subscriptionPeriod=None, status=None, subscriber=None, payments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if countryCode is not None:
            self.countryCode = countryCode

        if expirationDate is not None:
            self.expirationDate = expirationDate

        if subscriptionPeriod is not None:
            self.subscriptionPeriod = subscriptionPeriod

        if status is not None:
            self.status = status

        if subscriber is not None:
            self.subscriber = subscriber

        if payments is not None:
            self.payments = payments


class SubscriptionPayment(EObject, metaclass=MetaEClass):

    countryCode = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    subscriptionPeriod = EAttribute(eType=SubscriptionPeriod,
                                    unique=True, derived=False, changeable=True)
    status = EAttribute(eType=SubscriptionPaymentStatus,
                        unique=True, derived=False, changeable=True)
    payer = EReference(ordered=True, unique=True, containment=False, derived=False)
    value = EReference(ordered=True, unique=True, containment=True, derived=False)
    payments = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, countryCode=None, subscriptionPeriod=None, status=None, payer=None, value=None, payments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if countryCode is not None:
            self.countryCode = countryCode

        if subscriptionPeriod is not None:
            self.subscriptionPeriod = subscriptionPeriod

        if status is not None:
            self.status = status

        if payer is not None:
            self.payer = payer

        if value is not None:
            self.value = value

        if payments is not None:
            self.payments = payments


class SubscriptionRenewalPayment(EObject, metaclass=MetaEClass):

    countryCode = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    subscriptionPeriod = EAttribute(eType=SubscriptionPeriod,
                                    unique=True, derived=False, changeable=True)
    status = EAttribute(eType=SubscriptionRenewalPaymentStatus,
                        unique=True, derived=False, changeable=True)
    payer = EReference(ordered=True, unique=True, containment=False, derived=False)
    value = EReference(ordered=True, unique=True, containment=True, derived=False)
    payments = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, countryCode=None, subscriptionPeriod=None, status=None, payer=None, value=None, payments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if countryCode is not None:
            self.countryCode = countryCode

        if subscriptionPeriod is not None:
            self.subscriptionPeriod = subscriptionPeriod

        if status is not None:
            self.status = status

        if payer is not None:
            self.payer = payer

        if value is not None:
            self.value = value

        if payments is not None:
            self.payments = payments


class PriceListItem(EObject, metaclass=MetaEClass):

    isActive = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    countryCode = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    subscriptionPeriod = EAttribute(eType=SubscriptionPeriod,
                                    unique=True, derived=False, changeable=True)
    category = EAttribute(eType=PriceListItemCategory, unique=True, derived=False, changeable=True)
    price = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, isActive=None, countryCode=None, subscriptionPeriod=None, category=None, price=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if isActive is not None:
            self.isActive = isActive

        if countryCode is not None:
            self.countryCode = countryCode

        if subscriptionPeriod is not None:
            self.subscriptionPeriod = subscriptionPeriod

        if category is not None:
            self.category = category

        if price is not None:
            self.price = price


class PriceList(EObject, metaclass=MetaEClass):

    pricingStrategy = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    items = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    payments = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, pricingStrategy=None, items=None, payments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if pricingStrategy is not None:
            self.pricingStrategy = pricingStrategy

        if items:
            self.items.extend(items)

        if payments is not None:
            self.payments = payments


class Administrator(User):

    administration = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, administration=None, **kwargs):

        super().__init__(**kwargs)

        if administration is not None:
            self.administration = administration


class Member(User):

    meetings = EReference(ordered=True, unique=True, containment=False, derived=False)
    meetingGroups = EReference(ordered=True, unique=True,
                               containment=False, derived=False, upper=-1)
    meetingGroupProposals = EReference(ordered=True, unique=True,
                                       containment=False, derived=False, upper=-1)

    def __init__(self, *, meetings=None, meetingGroups=None, meetingGroupProposals=None, **kwargs):

        super().__init__(**kwargs)

        if meetings is not None:
            self.meetings = meetings

        if meetingGroups:
            self.meetingGroups.extend(meetingGroups)

        if meetingGroupProposals:
            self.meetingGroupProposals.extend(meetingGroupProposals)
