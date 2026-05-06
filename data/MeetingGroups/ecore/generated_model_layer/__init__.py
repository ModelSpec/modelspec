
from .meetinggroups import getEClassifier, eClassifiers
from .meetinggroups import name, nsURI, nsPrefix, eClass
from .meetinggroups import UserAccess, Administration, Meetings, Payments, UserRegistration, User, Administrator, Member, MeetingGroupLocation, MeetingGroupProposal, MeetingGroupProposalDecision, MeetingGroup, MeetingGroupMember, MeetingLocation, Term, MeetingTerm, Meeting, MeetingAttendee, MeetingNotAttendee, MeetingWaitlistMember, MeetingLimit, MoneyValue, MeetingFee, MeetingFeePayment, Subscription, SubscriptionPayment, SubscriptionRenewalPayment, PriceListItem, PriceList, UserRegistrationStatus, MeetingGroupProposalStatus, MeetingGroupProposalDecisionCode, MeetingGroupMemberRole, MeetingAttendeeRole, MeetingFeeStatus, MeetingFeePaymentStatus, SubscriptionPeriod, SubscriptionStatus, SubscriptionPaymentStatus, SubscriptionRenewalPaymentStatus, PriceListItemCategory


from . import meetinggroups

__all__ = ['UserAccess', 'Administration', 'Meetings', 'Payments', 'UserRegistration', 'User', 'Administrator', 'Member', 'MeetingGroupLocation', 'MeetingGroupProposal', 'MeetingGroupProposalDecision', 'MeetingGroup', 'MeetingGroupMember', 'MeetingLocation', 'Term', 'MeetingTerm', 'Meeting', 'MeetingAttendee', 'MeetingNotAttendee', 'MeetingWaitlistMember', 'MeetingLimit', 'MoneyValue', 'MeetingFee', 'MeetingFeePayment',
           'Subscription', 'SubscriptionPayment', 'SubscriptionRenewalPayment', 'PriceListItem', 'PriceList', 'UserRegistrationStatus', 'MeetingGroupProposalStatus', 'MeetingGroupProposalDecisionCode', 'MeetingGroupMemberRole', 'MeetingAttendeeRole', 'MeetingFeeStatus', 'MeetingFeePaymentStatus', 'SubscriptionPeriod', 'SubscriptionStatus', 'SubscriptionPaymentStatus', 'SubscriptionRenewalPaymentStatus', 'PriceListItemCategory']

eSubpackages = []
eSuperPackage = None
meetinggroups.eSubpackages = eSubpackages
meetinggroups.eSuperPackage = eSuperPackage

MeetingGroupProposal.meetingGroupLocation.eType = MeetingGroupLocation
MeetingGroupProposalDecision.administrator.eType = Administrator
MeetingGroup.meetingGroupLocation.eType = MeetingGroupLocation
MeetingGroupMember.member.eType = Member
Meeting.term.eType = MeetingTerm
Meeting.location.eType = MeetingLocation
Meeting.rsvpTerm.eType = Term
Meeting.creator.eType = Member
Meeting.changeMember.eType = Member
Meeting.cancelMember.eType = Member
Meeting.meetingLimit.eType = MeetingLimit
MeetingAttendee.attendee.eType = Member
MeetingAttendee.fee.eType = MeetingFee
MeetingAttendee.removingMember.eType = Member
MeetingNotAttendee.member.eType = Member
MeetingWaitlistMember.member.eType = Member
MeetingFee.payer.eType = Member
MeetingFee.value.eType = MoneyValue
Subscription.subscriber.eType = Member
SubscriptionPayment.payer.eType = Member
SubscriptionPayment.value.eType = MoneyValue
SubscriptionRenewalPayment.payer.eType = Member
SubscriptionRenewalPayment.value.eType = MoneyValue
PriceListItem.price.eType = MoneyValue
PriceList.items.eType = PriceListItem
UserAccess.users.eType = User
UserAccess.userRegistrations.eType = UserRegistration
Administration.administrators.eType = Administrator
Meetings.members.eType = Member
Meetings.meetingGroupProposals.eType = MeetingGroupProposal
Meetings.meetingGroups.eType = MeetingGroup
Meetings.meetings.eType = Meeting
Meetings.meetingLocations.eType = MeetingLocation
Meetings.meetingAttendees.eType = MeetingAttendee
Meetings.meetingNotAttendees.eType = MeetingNotAttendee
Meetings.meetingWaitlistMembers.eType = MeetingWaitlistMember
Payments.meetingFees.eType = MeetingFee
Payments.meetingFeePayments.eType = MeetingFeePayment
Payments.subscriptions.eType = Subscription
Payments.subscriptionPayments.eType = SubscriptionPayment
Payments.subscriptionRenewalPayments.eType = SubscriptionRenewalPayment
Payments.priceLists.eType = PriceList
UserRegistration.userAccess.eType = UserAccess
UserRegistration.userAccess.eOpposite = UserAccess.userRegistrations
User.userAccess.eType = UserAccess
User.userAccess.eOpposite = UserAccess.users
Administrator.administration.eType = Administration
Administrator.administration.eOpposite = Administration.administrators
Member.meetings.eType = Meetings
Member.meetings.eOpposite = Meetings.members
Member.meetingGroups.eType = MeetingGroup
Member.meetingGroupProposals.eType = MeetingGroupProposal
MeetingGroupProposal.member.eType = Member
MeetingGroupProposal.member.eOpposite = Member.meetingGroupProposals
MeetingGroupProposal.decisions.eType = MeetingGroupProposalDecision
MeetingGroupProposal.meetings.eType = Meetings
MeetingGroupProposal.meetings.eOpposite = Meetings.meetingGroupProposals
MeetingGroupProposalDecision.proposal.eType = MeetingGroupProposal
MeetingGroupProposalDecision.proposal.eOpposite = MeetingGroupProposal.decisions
MeetingGroup.creator.eType = Member
MeetingGroup.creator.eOpposite = Member.meetingGroups
MeetingGroup.members.eType = MeetingGroupMember
MeetingGroup.meetings.eType = Meetings
MeetingGroup.meetings.eOpposite = Meetings.meetingGroups
MeetingGroupMember.meetingGroup.eType = MeetingGroup
MeetingGroupMember.meetingGroup.eOpposite = MeetingGroup.members
MeetingLocation.meetings.eType = Meetings
MeetingLocation.meetings.eOpposite = Meetings.meetingLocations
Meeting.meetingAttendees.eType = MeetingAttendee
Meeting.meetingNotAttendees.eType = MeetingNotAttendee
Meeting.meetingWaitlistMembers.eType = MeetingWaitlistMember
Meeting.meetingFees.eType = MeetingFee
Meeting.meetings.eType = Meetings
Meeting.meetings.eOpposite = Meetings.meetings
MeetingAttendee.meeting.eType = Meeting
MeetingAttendee.meeting.eOpposite = Meeting.meetingAttendees
MeetingAttendee.meetings.eType = Meetings
MeetingAttendee.meetings.eOpposite = Meetings.meetingAttendees
MeetingNotAttendee.meeting.eType = Meeting
MeetingNotAttendee.meeting.eOpposite = Meeting.meetingNotAttendees
MeetingNotAttendee.meetings.eType = Meetings
MeetingNotAttendee.meetings.eOpposite = Meetings.meetingNotAttendees
MeetingWaitlistMember.meeting.eType = Meeting
MeetingWaitlistMember.meeting.eOpposite = Meeting.meetingWaitlistMembers
MeetingWaitlistMember.meetings.eType = Meetings
MeetingWaitlistMember.meetings.eOpposite = Meetings.meetingWaitlistMembers
MeetingFee.meeting.eType = Meeting
MeetingFee.meeting.eOpposite = Meeting.meetingFees
MeetingFee.meetingFeePayments.eType = MeetingFeePayment
MeetingFee.payments.eType = Payments
MeetingFee.payments.eOpposite = Payments.meetingFees
MeetingFeePayment.meetingFee.eType = MeetingFee
MeetingFeePayment.meetingFee.eOpposite = MeetingFee.meetingFeePayments
MeetingFeePayment.payments.eType = Payments
MeetingFeePayment.payments.eOpposite = Payments.meetingFeePayments
Subscription.payments.eType = Payments
Subscription.payments.eOpposite = Payments.subscriptions
SubscriptionPayment.payments.eType = Payments
SubscriptionPayment.payments.eOpposite = Payments.subscriptionPayments
SubscriptionRenewalPayment.payments.eType = Payments
SubscriptionRenewalPayment.payments.eOpposite = Payments.subscriptionRenewalPayments
PriceList.payments.eType = Payments
PriceList.payments.eOpposite = Payments.priceLists

otherClassifiers = [UserRegistrationStatus, MeetingGroupProposalStatus, MeetingGroupProposalDecisionCode, MeetingGroupMemberRole, MeetingAttendeeRole,
                    MeetingFeeStatus, MeetingFeePaymentStatus, SubscriptionPeriod, SubscriptionStatus, SubscriptionPaymentStatus, SubscriptionRenewalPaymentStatus, PriceListItemCategory]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
