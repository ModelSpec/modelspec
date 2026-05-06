from datetime import datetime

import pytest
from freezegun import freeze_time


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Member, Subscription, SubscriptionPeriod, SubscriptionStatus, MeetingGroupLocation, MeetingGroupMember, MeetingGroupMemberRole, MeetingGroupProposalStatus

    if modelingTool == "umple":
        from ..umple.controller import MeetingGroupsController
        from ..umple.generated_model_layer import (
            Administration,
            Meeting,
            MeetingGroup,
            MeetingGroupLocation,
            MeetingGroupMember,
            MeetingGroupProposal,
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
            Meeting,
            MeetingGroup,
            MeetingGroupLocation,
            MeetingGroupMember,
            MeetingGroupMemberRole,
            MeetingGroupProposal,
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

    mw(Member, id=1, login="user1", email="user1@email.com", firstName="John", lastName="Doe", name="John Doe", userAccess=c.userAccess, meetings=c.meetings)

    yield c


@freeze_time("2025-11-30")
def testCreateProposalSuccessfully(controller, mw):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member1.model, payments=controller.payments)

    # Act
    controller.createMeetingGroupProposal(1, 'meetinggroup1', 'description', 'city', 'ca')

    # Assert
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingGroupProposals() == 1
    proposal = meetings.getMeetingGroupProposal(0)
    assert proposal.getName() == 'meetinggroup1'
    assert proposal.getDescription() == 'description'
    assert proposal.getMeetingGroupLocation().getCity() == 'city'
    assert proposal.getMeetingGroupLocation().getCountryCode() == 'ca'
    assert proposal.getStatus().name == MeetingGroupProposalStatus.ToVerify.name
    assert proposal.getProposalDate().year == datetime(2025, 11, 30).year
    assert proposal.getProposalDate().month == datetime(2025, 11, 30).month
    assert proposal.getProposalDate().day == datetime(2025, 11, 30).day
    assert proposal.getMember().getId() == 1


@freeze_time("2025-11-30")
def testCreateProposalWithUniqueId(controller, mw):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member1.model, payments=controller.payments)
    location = mw(MeetingGroupLocation, city="city", countryCode="ca")
    if hasattr(MeetingGroupProposal, "nextId"):
        proposal = mw(
            MeetingGroupProposal,
            name="proposal1",
            description="description",
            meetingGroupLocation=location.model,
            member=member1.model,
            meetings=controller.meetings,
        )
    else:
        proposal = mw(
            MeetingGroupProposal,
            id=1,
            name="proposal1",
            description="description",
            meetingGroupLocation=location.model,
            member=member1.model,
            meetings=controller.meetings,
        )
    proposal.setStatus(MeetingGroupProposalStatus.ToVerify)
    proposal.setProposalDate(datetime(2025, 11, 30))

    # Act
    controller.createMeetingGroupProposal(1, 'meetinggroup1', 'description', 'city', 'ca')

    # Assert
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingGroupProposals() == 2
    proposal = next(p for p in meetings.getMeetingGroupProposals() if p.getId() != 1)
    assert proposal.getName() == 'meetinggroup1'
    assert proposal.getDescription() == 'description'
    assert proposal.getMeetingGroupLocation().getCity() == 'city'
    assert proposal.getMeetingGroupLocation().getCountryCode() == 'ca'
    assert proposal.getStatus().name == MeetingGroupProposalStatus.ToVerify.name
    assert proposal.getProposalDate().year == datetime(2025, 11, 30).year
    assert proposal.getProposalDate().month == datetime(2025, 11, 30).month
    assert proposal.getProposalDate().day == datetime(2025, 11, 30).day
    assert proposal.getMember().getId() == 1


def testCreateProposalNoSubscription(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.createMeetingGroupProposal(1, 'meetinggroup1', 'description', 'city', 'ca')

    # Assert
    assert str(excInfo.value) == 'Must have an active subscription to create a meeting group proposal.'
    assert mw(controller.meetings).numberOfMeetingGroupProposals() == 0


@pytest.mark.parametrize("name,description,city,countryCode,errorMessage", [
    ('', 'description', 'city', 'ca', 'The name must not be empty.'),
    ('meetinggroup1', '', 'city', 'ca', 'The description must not be empty.'),
    ('meetinggroup1', 'description', '', 'ca', 'The city must not be empty.'),
    ('meetinggroup1', 'description', 'city', '', 'The country code must not be empty.'),
    ('meetinggroup1', 'description', 'city', 'c', 'The country code must be either 2 or 3 characters long.'),
    ('meetinggroup1', 'description', 'city', 'cabd', 'The country code must be either 2 or 3 characters long.'),
])
def testCreateProposalInvalidValues(controller, mw, name, description, city, countryCode, errorMessage):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member1.model, payments=controller.payments)

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.createMeetingGroupProposal(1, name, description, city, countryCode)

    # Assert
    assert str(excInfo.value) == errorMessage
    assert mw(controller.meetings).numberOfMeetingGroupProposals() == 0


def testCreateProposalExceedingMeetingGroupLimit(controller, mw):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    mw(Subscription, countryCode="ca", expirationDate=datetime(2025, 12, 31), subscriptionPeriod=SubscriptionPeriod.Month, status=SubscriptionStatus.Active, subscriber=member1.model, payments=controller.payments)

    for i in range(1, 4):
        loc = mw(MeetingGroupLocation, city="city", countryCode="ca")
        mg = mw(MeetingGroup, id=i, name=f"meetinggroup{i}", description="description", meetingGroupLocation=loc.model, creator=member1.model, meetings=controller.meetings)
        organizer = mw(MeetingGroupMember, role=MeetingGroupMemberRole.Organizer, member=member1.model, meetingGroup=mg.model)
        organizer.setJoinedDate(datetime(2025, 11, 29))
        organizer.setIsActive(True)

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.createMeetingGroupProposal(1, 'meetinggroup4', 'description', 'city', 'ca')

    # Assert
    assert str(excInfo.value) == 'A maximum of 3 meeting groups can be covered by a subscription.'
    assert mw(controller.meetings).numberOfMeetingGroupProposals() == 0


