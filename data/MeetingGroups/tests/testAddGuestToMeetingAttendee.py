from datetime import datetime

import pytest


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Member, MeetingAttendee, MeetingAttendeeRole, MeetingLocation, MeetingTerm, Term, MeetingLimit

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
            Meetings,
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
            Meetings,
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
    member2 = mw(Member, id=2, login="user2", email="user2@email.com", firstName="Jane", lastName="Smith", name="Jane Smith", userAccess=c.userAccess, meetings=c.meetings)

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

    mw(
        MeetingAttendee,
        guestNumber=0,
        decisionDate=datetime(2025, 11, 29),
        role=MeetingAttendeeRole.Attendee,
        attendee=member2.model,
        meeting=meeting.model,
        meetings=c.meetings,
    )

    yield c


def testAddGuestsSuccessfully3(controller, mw):
    # Act
    controller.addGuestToMeetingAttendee(2, 1, 3)

    # Assert
    meetings = mw(controller.meetings)
    attendee = next(a for a in meetings.getMeetingAttendees()
                    if a.getAttendee().getId() == 2 and a.getMeeting().getId() == 1)
    assert attendee.getGuestNumber() == 3


def testAddGuestsSuccessfully0(controller, mw):
    # Act
    controller.addGuestToMeetingAttendee(2, 1, 0)

    # Assert
    meetings = mw(controller.meetings)
    attendee = next(a for a in meetings.getMeetingAttendees()
                    if a.getAttendee().getId() == 2 and a.getMeeting().getId() == 1)
    assert attendee.getGuestNumber() == 0


def testAddNegativeGuests(controller):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addGuestToMeetingAttendee(2, 1, -1)

    # Assert
    assert str(excInfo.value) == 'The guestNumber must be zero or positive.'


def testAddGuestsNonexistentMeeting(controller):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addGuestToMeetingAttendee(2, 999, 3)

    # Assert
    assert str(excInfo.value) == 'Meeting does not exist.'


def testAddGuestsNonexistentMember(controller):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addGuestToMeetingAttendee(999, 1, 3)

    # Assert
    assert str(excInfo.value) == 'Member does not exist.'


def testAddGuestsMemberNotAttendee(controller, mw):
    mw(
        Member,
        id=3,
        login="user3",
        email="user3@email.com",
        firstName="Alice",
        lastName="Johnson",
        name="Alice Johnson",
        userAccess=controller.userAccess,
        meetings=controller.meetings,
    )

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addGuestToMeetingAttendee(3, 1, 3)

    # Assert
    assert str(excInfo.value) == 'Member is not an attendee of the meeting.'


def testAddGuestsExceedingLimit(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addGuestToMeetingAttendee(2, 1, 6)

    # Assert
    assert str(excInfo.value) == "The guestNumber exceeds the meeting's guestsLimit."
    meetings = mw(controller.meetings)
    attendee = next(a for a in meetings.getMeetingAttendees()
                    if a.getAttendee().getId() == 2 and a.getMeeting().getId() == 1)
    assert attendee.getGuestNumber() == 0


