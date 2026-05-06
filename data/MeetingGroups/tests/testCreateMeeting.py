from datetime import datetime

import pytest


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Member, MeetingLocation, MeetingTerm, Term, MeetingLimit

    if modelingTool == "umple":
        from ..umple.controller import MeetingGroupsController
        from ..umple.generated_model_layer import (
            Administration,
            Meeting,
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

    mw(
        Member,
        id=1,
        login="user1",
        email="user1@email.com",
        firstName="John",
        lastName="Doe",
        name="John Doe",
        userAccess=c.userAccess,
        meetings=c.meetings,
    )

    yield c


def testCreateMeetingSuccessfully(controller, mw):
    # Act
    controller.createMeeting(
        1,
        "meeting1",
        "description",
        "location",
        "address",
        "city",
        "ca",
        datetime(2025, 12, 1),
        datetime(2025, 12, 1),
        datetime(2025, 11, 30),
        datetime(2025, 11, 30),
        10,
        5,
    )

    # Assert
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetings() == 1
    meeting = meetings.getMeeting(0)
    assert meeting.getTitle() == "meeting1"
    assert meeting.getDescription() == "description"
    assert meeting.getLocation().getName() == "location"
    assert meeting.getLocation().getAddress() == "address"
    assert meeting.getLocation().getCity() == "city"
    assert meeting.getLocation().getCountryCode() == "ca"
    assert meeting.getTerm().getStartDate().year == datetime(2025, 12, 1).year
    assert meeting.getTerm().getStartDate().month == datetime(2025, 12, 1).month
    assert meeting.getTerm().getStartDate().day == datetime(2025, 12, 1).day
    assert meeting.getTerm().getEndDate().year == datetime(2025, 12, 1).year
    assert meeting.getTerm().getEndDate().month == datetime(2025, 12, 1).month
    assert meeting.getTerm().getEndDate().day == datetime(2025, 12, 1).day
    assert meeting.getRsvpTerm().getStartDate().year == datetime(2025, 11, 30).year
    assert meeting.getRsvpTerm().getStartDate().month == datetime(2025, 11, 30).month
    assert meeting.getRsvpTerm().getStartDate().day == datetime(2025, 11, 30).day
    assert meeting.getRsvpTerm().getEndDate().year == datetime(2025, 11, 30).year
    assert meeting.getRsvpTerm().getEndDate().month == datetime(2025, 11, 30).month
    assert meeting.getRsvpTerm().getEndDate().day == datetime(2025, 11, 30).day
    assert meeting.getMeetingLimit().getAttendeesLimit() == 10
    assert meeting.getMeetingLimit().getGuestsLimit() == 5


def testCreateMeetingSuccessfullyWithUniqueId(controller, mw):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    location = mw(MeetingLocation, name="location", address="address", city="city", countryCode="ca", meetings=controller.meetings)
    term = mw(MeetingTerm, startDate=datetime(2025, 12, 1), endDate=datetime(2025, 12, 1))
    rsvpTerm = mw(Term, startDate=datetime(2025, 11, 30), endDate=datetime(2025, 11, 30))
    limit = mw(MeetingLimit, attendeesLimit=10, guestsLimit=5)
    firstMeeting = mw(
        Meeting,
        title="meeting1",
        description="description",
        term=term.model,
        location=location.model,
        meetingLimit=limit.model,
        rsvpTerm=rsvpTerm.model,
        creator=member1.model,
        meetings=controller.meetings,
    )
    firstMeeting.setId(1)

    # Act
    controller.createMeeting(
        1,
        "meeting1",
        "description",
        "location",
        "address",
        "city",
        "ca",
        datetime(2025, 12, 1),
        datetime(2025, 12, 1),
        datetime(2025, 11, 30),
        datetime(2025, 11, 30),
        10,
        5,
    )

    # Assert
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetings() == 2
    meeting = next(mt for mt in meetings.getMeetings() if mt.getId() != 1)
    assert meeting.getTitle() == "meeting1"
    assert meeting.getDescription() == "description"
    assert meeting.getLocation().getName() == "location"
    assert meeting.getLocation().getAddress() == "address"
    assert meeting.getLocation().getCity() == "city"
    assert meeting.getLocation().getCountryCode() == "ca"
    assert meeting.getTerm().getStartDate().year == datetime(2025, 12, 1).year
    assert meeting.getTerm().getStartDate().month == datetime(2025, 12, 1).month
    assert meeting.getTerm().getStartDate().day == datetime(2025, 12, 1).day
    assert meeting.getTerm().getEndDate().year == datetime(2025, 12, 1).year
    assert meeting.getTerm().getEndDate().month == datetime(2025, 12, 1).month
    assert meeting.getTerm().getEndDate().day == datetime(2025, 12, 1).day
    assert meeting.getRsvpTerm().getStartDate().year == datetime(2025, 11, 30).year
    assert meeting.getRsvpTerm().getStartDate().month == datetime(2025, 11, 30).month
    assert meeting.getRsvpTerm().getStartDate().day == datetime(2025, 11, 30).day
    assert meeting.getRsvpTerm().getEndDate().year == datetime(2025, 11, 30).year
    assert meeting.getRsvpTerm().getEndDate().month == datetime(2025, 11, 30).month
    assert meeting.getRsvpTerm().getEndDate().day == datetime(2025, 11, 30).day
    assert meeting.getMeetingLimit().getAttendeesLimit() == 10
    assert meeting.getMeetingLimit().getGuestsLimit() == 5


@pytest.mark.parametrize(
    "title,description,locationName,locationAddress,locationCity,countryCode,startDate,endDate,rsvpStart,rsvpEnd,attendees,guests,errorMessage",
    [
        ('', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The title must not be empty.'),
        ('meeting', '', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The description must not be empty.'),
        ('meeting', 'desc', '', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The locationName must not be empty.'),
        ('meeting', 'desc', 'loc', '', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The locationAddress must not be empty.'),
        ('meeting', 'desc', 'loc', 'addr', '', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The locationCity must not be empty.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', '', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The locationCountryCode must not be empty.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'c', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The locationCountryCode must be either 2 or 3 characters long.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'cabd', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The locationCountryCode must be either 2 or 3 characters long.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The startDate must not be empty.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '', '2025-11-30', '2025-11-30', 10, 5,
         'The endDate must not be empty.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '', '2025-11-30', 10, 5,
         'The rsvpStartDate must not be empty.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '', 10, 5,
         'The rsvpEndDate must not be empty.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-02', '2025-12-01', '2025-11-30', '2025-11-30', 10, 5,
         'The startDate must be before or equal to endDate.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-12-02', '2025-11-30', 10, 5,
         'The rsvpStartDate must be before or equal to rsvpEndDate.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 0, 5,
         'The attendeesLimit must be greater than 0.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', -1, 5,
         'The attendeesLimit must be greater than 0.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, 0,
         'The guestsLimit must be greater than 0.'),
        ('meeting', 'desc', 'loc', 'addr', 'city', 'ca', '2025-12-01', '2025-12-01', '2025-11-30', '2025-11-30', 10, -1,
         'The guestsLimit must be greater than 0.'),
    ])
def testCreateMeetingInvalidValues(controller, title, description, locationName, locationAddress, locationCity,
                                   countryCode, startDate, endDate, rsvpStart, rsvpEnd, attendees, guests,
                                   errorMessage):
    startDate = None if startDate == '' else datetime.fromisoformat(startDate)
    endDate = None if endDate == '' else datetime.fromisoformat(endDate)
    rsvpStart = None if rsvpStart == '' else datetime.fromisoformat(rsvpStart)
    rsvpEnd = None if rsvpEnd == '' else datetime.fromisoformat(rsvpEnd)

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.createMeeting(1, title, description, locationName, locationAddress, locationCity, countryCode,
                          startDate, endDate, rsvpStart, rsvpEnd, attendees, guests)

    # Assert
    assert str(excInfo.value) == errorMessage


