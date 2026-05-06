from datetime import datetime

import pytest
from freezegun import freeze_time


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Member, MeetingAttendee, MeetingAttendeeRole, MeetingWaitlistMember, MeetingNotAttendee
    global MeetingLocation, MeetingTerm, Term, MeetingLimit

    if modelingTool == "umple":
        from ..umple.controller import MeetingGroupsController
        from ..umple.generated_model_layer import (
            Administration,
            Meeting,
            MeetingAttendee,
            MeetingLimit,
            MeetingLocation,
            MeetingTerm,
            MeetingGroup,
            MeetingGroupProposal,
            MeetingNotAttendee,
            Meetings,
            MeetingWaitlistMember,
            Member,
            Payments,
            Term,
            User,
            UserAccess,
            UserRegistration,
        )
        MeetingAttendeeRole = MeetingAttendee.MeetingAttendeeRole

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
            MeetingAttendee,
            MeetingAttendeeRole,
            MeetingLimit,
            MeetingLocation,
            MeetingTerm,
            MeetingGroup,
            MeetingGroupProposal,
            MeetingNotAttendee,
            Meetings,
            MeetingWaitlistMember,
            Member,
            Payments,
            Term,
            User,
            UserAccess,
            UserRegistration,
        )

    c = MeetingGroupsController()
    c.userAccess = mw(UserAccess).model
    c.administration = mw(Administration).model
    c.meetings = mw(Meetings).model
    c.payments = mw(Payments).model

    member1 = mw(Member, id=1, login="user1", email="user1@email.com", firstName="John", lastName="Doe", name="John Doe", userAccess=c.userAccess, meetings=c.meetings)
    mw(Member, id=2, login="user2", email="user2@email.com", firstName="Jane", lastName="Smith", name="Jane Smith", userAccess=c.userAccess, meetings=c.meetings)
    mw(Member, id=3, login="user3", email="user3@email.com", firstName="Alice", lastName="Johnson", name="Alice Johnson", userAccess=c.userAccess, meetings=c.meetings)

    location = mw(MeetingLocation, name="location", address="address", city="city", countryCode="ca", meetings=c.meetings)
    term = mw(MeetingTerm, startDate=datetime(2025, 12, 1), endDate=datetime(2025, 12, 1))
    rsvpTerm = mw(Term, startDate=datetime(2025, 11, 30), endDate=datetime(2025, 11, 30))
    meetingLimit = mw(MeetingLimit, attendeesLimit=10, guestsLimit=5)
    meeting = mw(
        Meeting,
        title="meeting1",
        description="description",
        term=term.model,
        location=location.model,
        meetingLimit=meetingLimit.model,
        rsvpTerm=rsvpTerm.model,
        creator=member1.model,
        meetings=c.meetings,
    )
    meeting.setId(1)

    yield c


@freeze_time("2025-11-30")
def testAddMemberAsAttendee(controller, mw):
    # Act
    controller.addMemberToMeeting(2, 1)

    # Assert
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingAttendees() == 1
    attendee = meetings.getMeetingAttendee(0)
    assert attendee.getMeeting().getId() == 1
    assert attendee.getAttendee().getId() == 2
    assert attendee.getGuestNumber() == 0
    assert attendee.getRole().name == MeetingAttendeeRole.Attendee.name
    assert attendee.getDecisionDate().year == datetime(2025, 11, 30).year
    assert attendee.getDecisionDate().month == datetime(2025, 11, 30).month
    assert attendee.getDecisionDate().day == datetime(2025, 11, 30).day
    assert meetings.numberOfMeetingWaitlistMembers() == 0


@freeze_time("2025-11-30")
def testAddMemberToWaitlist(controller, mw):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    location = mw(MeetingLocation, name="location", address="address", city="city", countryCode="ca", meetings=controller.meetings)
    term = mw(MeetingTerm, startDate=datetime(2025, 12, 1), endDate=datetime(2025, 12, 1))
    rsvpTerm = mw(Term, startDate=datetime(2025, 11, 30), endDate=datetime(2025, 11, 30))
    limit = mw(MeetingLimit, attendeesLimit=1, guestsLimit=5)
    meeting2 = mw(
        Meeting,
        title="meeting2",
        description="description",
        term=term.model,
        location=location.model,
        meetingLimit=limit.model,
        rsvpTerm=rsvpTerm.model,
        creator=member1.model,
        meetings=controller.meetings,
    )
    meeting2.setId(2)

    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    mw(
        MeetingAttendee,
        guestNumber=0,
        decisionDate=datetime(2025, 11, 29),
        role=MeetingAttendeeRole.Attendee,
        attendee=member2.model,
        meeting=meeting2.model,
        meetings=controller.meetings,
    )

    # Act
    controller.addMemberToMeeting(3, 2)

    # Assert
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingAttendees() == 1
    assert meetings.numberOfMeetingWaitlistMembers() == 1
    wait = meetings.getMeetingWaitlistMember(0)
    assert wait.getMeeting().getId() == 2
    assert wait.getMember().getId() == 3
    assert wait.getDecisionDate().year == datetime(2025, 11, 30).year
    assert wait.getDecisionDate().month == datetime(2025, 11, 30).month
    assert wait.getDecisionDate().day == datetime(2025, 11, 30).day


def testAddMemberNonexistentMeeting(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeeting(2, 999)

    # Assert
    assert str(excInfo.value) == 'Meeting does not exist.'
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingAttendees() == 0
    assert meetings.numberOfMeetingWaitlistMembers() == 0


def testAddNonexistentMemberToMeeting(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeeting(999, 1)

    # Assert
    assert str(excInfo.value) == 'Member does not exist.'
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingAttendees() == 0
    assert meetings.numberOfMeetingWaitlistMembers() == 0


def testAddMemberAlreadyAttendee(controller, mw):
    meetings = mw(controller.meetings)
    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    meeting1 = next(mt for mt in meetings.getMeetings() if mt.getId() == 1)
    mw(
        MeetingAttendee,
        guestNumber=0,
        decisionDate=datetime(2025, 11, 29),
        role=MeetingAttendeeRole.Attendee,
        attendee=member2.model,
        meeting=meeting1.model,
        meetings=controller.meetings,
    )

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeeting(2, 1)

    # Assert
    assert str(excInfo.value) == 'Member is already part of the meeting.'
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingAttendees() == 1
    assert meetings.numberOfMeetingWaitlistMembers() == 0


def testAddMemberAlreadyOnWaitlist(controller, mw):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    location = mw(MeetingLocation, name="location", address="address", city="city", countryCode="ca", meetings=controller.meetings)
    term = mw(MeetingTerm, startDate=datetime(2025, 12, 1), endDate=datetime(2025, 12, 1))
    rsvpTerm = mw(Term, startDate=datetime(2025, 11, 30), endDate=datetime(2025, 11, 30))
    limit = mw(MeetingLimit, attendeesLimit=1, guestsLimit=5)
    meeting2 = mw(
        Meeting,
        title="meeting2",
        description="description",
        term=term.model,
        location=location.model,
        meetingLimit=limit.model,
        rsvpTerm=rsvpTerm.model,
        creator=member1.model,
        meetings=controller.meetings,
    )
    meeting2.setId(2)

    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    member3 = next(m for m in meetings.getMembers() if m.getId() == 3)
    mw(
        MeetingAttendee,
        guestNumber=0,
        decisionDate=datetime(2025, 11, 29),
        role=MeetingAttendeeRole.Attendee,
        attendee=member2.model,
        meeting=meeting2.model,
        meetings=controller.meetings,
    )
    mw(
        MeetingWaitlistMember,
        decisionDate=datetime(2025, 11, 29),
        member=member3.model,
        meeting=meeting2.model,
        meetings=controller.meetings,
    )

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeeting(3, 2)

    # Assert
    assert str(excInfo.value) == 'Member is already part of the meeting.'
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingAttendees() == 1
    assert meetings.numberOfMeetingWaitlistMembers() == 1


def testAddMemberWhoIsNotAttendee(controller, mw):
    meetings = mw(controller.meetings)
    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    meeting1 = next(mt for mt in meetings.getMeetings() if mt.getId() == 1)
    mw(
        MeetingNotAttendee,
        decisionDate=datetime(2025, 11, 29),
        member=member2.model,
        meeting=meeting1.model,
        meetings=controller.meetings,
    )

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeeting(2, 1)

    # Assert
    assert str(excInfo.value) == 'Member is already part of the meeting.'
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetingAttendees() == 0
    assert meetings.numberOfMeetingNotAttendees() == 1
    assert meetings.numberOfMeetingWaitlistMembers() == 0


