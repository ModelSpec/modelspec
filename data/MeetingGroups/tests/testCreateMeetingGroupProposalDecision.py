from datetime import datetime

import pytest
from freezegun import freeze_time


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Administrator, Member, MeetingGroupLocation, MeetingGroupMember, MeetingGroupMemberRole
    global Subscription, SubscriptionPeriod, SubscriptionStatus
    global MeetingGroupProposalDecision, MeetingGroupProposalDecisionCode, MeetingGroupProposalStatus

    if modelingTool == "umple":
        from ..umple.controller import MeetingGroupsController
        from ..umple.generated_model_layer import (
            Administration,
            Administrator,
            Meeting,
            MeetingGroup,
            MeetingGroupLocation,
            MeetingGroupMember,
            MeetingGroupProposal,
            MeetingGroupProposalDecision,
            Meetings,
            Member,
            Payments,
            Subscription,
            User,
            UserAccess,
            UserRegistration,
        )
        SubscriptionPeriod = Subscription.SubscriptionPeriod
        SubscriptionStatus = Subscription.SubscriptionStatus
        MeetingGroupMemberRole = MeetingGroupMember.MeetingGroupMemberRole
        MeetingGroupProposalDecisionCode = MeetingGroupProposalDecision.MeetingGroupProposalDecisionCode
        MeetingGroupProposalStatus = MeetingGroupProposal.MeetingGroupProposalStatus

        User.usersById.clear()
        MeetingGroup.meetinggroupsById.clear()
        MeetingGroupProposal.nextId = 1
        Meeting.nextId = 1
        UserRegistration.nextId = 1
    else:
        from ..ecore.controller import MeetingGroupsController
        from ..ecore.generated_model_layer import (
            Administration,
            Administrator,
            Meeting,
            MeetingGroup,
            MeetingGroupLocation,
            MeetingGroupMember,
            MeetingGroupMemberRole,
            MeetingGroupProposal,
            MeetingGroupProposalDecision,
            MeetingGroupProposalDecisionCode,
            MeetingGroupProposalStatus,
            Meetings,
            Member,
            Payments,
            Subscription,
            SubscriptionPeriod,
            SubscriptionStatus,
            User,
            UserAccess,
            UserRegistration,
        )

    c = MeetingGroupsController()
    c.userAccess = mw(UserAccess).model
    c.administration = mw(Administration).model
    c.meetings = mw(Meetings).model
    c.payments = mw(Payments).model

    mw(Administrator, id=1, login="user1", email="user1@email.com", firstName="John", lastName="Doe", name="John Doe", userAccess=c.userAccess, administration=c.administration)
    member2 = mw(Member, id=2, login="user2", email="user2@email.com", firstName="Jane", lastName="Smith", name="Jane Smith", userAccess=c.userAccess, meetings=c.meetings)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member2.model, payments=c.payments)
    location = mw(MeetingGroupLocation, city="city", countryCode="ca")
    if modelingTool == "umple":
        proposal = mw(
            MeetingGroupProposal,
            name="meetinggroup1",
            description="description",
            meetingGroupLocation=location.model,
            member=member2.model,
            meetings=c.meetings,
        )
    else:
        proposal = mw(
            MeetingGroupProposal,
            id=1,
            name="meetinggroup1",
            description="description",
            meetingGroupLocation=location.model,
            member=member2.model,
            meetings=c.meetings,
        )
    proposal.setStatus(MeetingGroupProposalStatus.ToVerify)
    proposal.setProposalDate(datetime(2025, 11, 30))

    yield c


@freeze_time("2025-11-30")
def testVerifyProposalSuccessfully(controller, mw):
    meetings = mw(controller.meetings)
    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member2.model, payments=controller.payments)

    # Act
    controller.createMeetingGroupProposalDecision(1, 1, 'Accept', '')

    # Assert
    meetings = mw(controller.meetings)
    proposal = meetings.getMeetingGroupProposal(0)
    assert len(proposal.getDecisions()) == 1
    decision = proposal.getDecision(0)
    assert decision.getAdministrator().getId() == 1
    assert decision.getCode().name == MeetingGroupProposalDecisionCode.Accept.name
    assert decision.getRejectReason() == ''
    assert decision.getDate().year == datetime(2025, 11, 30).year
    assert decision.getDate().month == datetime(2025, 11, 30).month
    assert decision.getDate().day == datetime(2025, 11, 30).day
    assert meetings.numberOfMeetingGroups() == 1
    meetingGroup = meetings.getMeetingGroup(0)
    assert meetingGroup.getName() == 'meetinggroup1'
    assert meetingGroup.getDescription() == 'description'
    assert meetingGroup.getMeetingGroupLocation().getCity() == 'city'
    assert meetingGroup.getMeetingGroupLocation().getCountryCode() == 'ca'
    assert meetingGroup.getCreator().getId() == 2
    assert meetingGroup.getCreateDate().year == datetime(2025, 11, 30).year
    assert meetingGroup.getCreateDate().month == datetime(2025, 11, 30).month
    assert meetingGroup.getCreateDate().day == datetime(2025, 11, 30).day
    assert len(meetingGroup.getMembers()) == 1
    mgMember = meetingGroup.getMember(0)
    assert mgMember.getMember().getId() == 2
    assert mgMember.getJoinedDate().year == datetime(2025, 11, 30).year
    assert mgMember.getJoinedDate().month == datetime(2025, 11, 30).month
    assert mgMember.getJoinedDate().day == datetime(2025, 11, 30).day
    assert mgMember.getRole().name == MeetingGroupMemberRole.Organizer.name


@freeze_time("2025-11-30")
def testRejectProposalSuccessfully(controller, mw):
    meetings = mw(controller.meetings)
    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member2.model, payments=controller.payments)

    # Act
    controller.createMeetingGroupProposalDecision(1, 1, 'Reject', 'reason')

    # Assert
    meetings = mw(controller.meetings)
    proposal = meetings.getMeetingGroupProposal(0)
    assert len(proposal.getDecisions()) == 1
    decision = proposal.getDecision(0)
    assert decision.getAdministrator().getId() == 1
    assert decision.getCode().name == MeetingGroupProposalDecisionCode.Reject.name
    assert decision.getRejectReason() == 'reason'
    assert decision.getDate().year == datetime(2025, 11, 30).year
    assert decision.getDate().month == datetime(2025, 11, 30).month
    assert decision.getDate().day == datetime(2025, 11, 30).day
    assert proposal.getStatus().name == MeetingGroupProposalStatus.Rejected.name
    assert meetings.numberOfMeetingGroups() == 0


def testVerifyProposalMemberWithoutSubscription(controller, mw):
    if hasattr(controller.payments, "subscriptions"):
        controller.payments.subscriptions.clear()
    else:
        payments = mw(controller.payments)
        while payments.numberOfSubscriptions() > 0:
            s = payments.getSubscription(0)
            s.delete()

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.createMeetingGroupProposalDecision(1, 1, 'Accept', '')

    # Assert
    assert str(excInfo.value) == 'Member does not have an active subscription'
    meetings = mw(controller.meetings)
    proposal = meetings.getMeetingGroupProposal(0)
    assert len(proposal.getDecisions()) == 0
    assert meetings.numberOfMeetingGroups() == 0


def testVerifyProposalMemberWith3MeetingGroups(controller, mw):
    meetings = mw(controller.meetings)
    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member2.model, payments=controller.payments)

    for i in range(1, 4):
        loc = mw(MeetingGroupLocation, city="city", countryCode="ca")
        mg = mw(MeetingGroup, id=i, name=f"meetinggroup{i}", description="description", meetingGroupLocation=loc.model, creator=member2.model, meetings=controller.meetings)
        organizer = mw(MeetingGroupMember, role=MeetingGroupMemberRole.Organizer, member=member2.model, meetingGroup=mg.model)
        organizer.setJoinedDate(datetime(2025, 11, 29))
        organizer.setIsActive(True)

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.createMeetingGroupProposalDecision(1, 1, 'Accept', '')

    # Assert
    assert str(excInfo.value) == 'A maximum of 3 meeting groups can be covered by a subscription.'
    proposal = meetings.getMeetingGroupProposal(0)
    assert len(proposal.getDecisions()) == 0
    assert meetings.numberOfMeetingGroups() == 3


