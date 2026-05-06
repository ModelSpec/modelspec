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

    member1 = mw(
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
    mw(
        Member,
        id=2,
        login="user2",
        email="user2@email.com",
        firstName="Jane",
        lastName="Smith",
        name="Jane Smith",
        userAccess=c.userAccess,
        meetings=c.meetings,
    )

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


def testEditMeetingSuccessfully(controller, mw):
    # Act
    controller.editMeeting(
        1,
        1,
        "meeting2",
        "new description",
        "location2",
        "address2",
        "city2",
        "us",
        datetime(2025, 12, 2),
        datetime(2025, 12, 2),
        datetime(2025, 12, 1),
        datetime(2025, 12, 1),
        20,
        10,
    )

    # Assert
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetings() == 1
    meeting = meetings.getMeeting(0)
    assert meeting.getTitle() == "meeting2"
    assert meeting.getDescription() == "new description"
    assert meeting.getLocation().getName() == "location2"
    assert meeting.getLocation().getAddress() == "address2"
    assert meeting.getLocation().getCity() == "city2"
    assert meeting.getLocation().getCountryCode() == "us"
    assert meeting.getTerm().getStartDate().year == datetime(2025, 12, 2).year
    assert meeting.getTerm().getStartDate().month == datetime(2025, 12, 2).month
    assert meeting.getTerm().getStartDate().day == datetime(2025, 12, 2).day
    assert meeting.getTerm().getEndDate().year == datetime(2025, 12, 2).year
    assert meeting.getTerm().getEndDate().month == datetime(2025, 12, 2).month
    assert meeting.getTerm().getEndDate().day == datetime(2025, 12, 2).day
    assert meeting.getRsvpTerm().getStartDate().year == datetime(2025, 12, 1).year
    assert meeting.getRsvpTerm().getStartDate().month == datetime(2025, 12, 1).month
    assert meeting.getRsvpTerm().getStartDate().day == datetime(2025, 12, 1).day
    assert meeting.getRsvpTerm().getEndDate().year == datetime(2025, 12, 1).year
    assert meeting.getRsvpTerm().getEndDate().month == datetime(2025, 12, 1).month
    assert meeting.getRsvpTerm().getEndDate().day == datetime(2025, 12, 1).day
    assert meeting.getMeetingLimit().getAttendeesLimit() == 20
    assert meeting.getMeetingLimit().getGuestsLimit() == 10


@pytest.mark.parametrize(
    "title,description,locationName,locationAddress,locationCity,locationCountryCode,startDate,endDate,rsvpStartDate,rsvpEndDate,attendeesLimit,guestsLimit,errorMessage",
    [
        ('', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The title must not be empty.'),
        ('meeting2', '', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The description must not be empty.'),
        ('meeting2', 'new description', '', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The locationName must not be empty.'),
        ('meeting2', 'new description', 'location', '', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The locationAddress must not be empty.'),
        ('meeting2', 'new description', 'location', 'address', '', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The locationCity must not be empty.'),
        ('meeting2', 'new description', 'location', 'address', 'city', '', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The locationCountryCode must not be empty.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'c', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5,
         'The locationCountryCode must be either 2 or 3 characters long.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'cabd', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5,
         'The locationCountryCode must be either 2 or 3 characters long.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', None, datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The startDate must not be empty.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), None,
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The endDate must not be empty.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         None, datetime(2025, 11, 30), 10, 5, 'The rsvpStartDate must not be empty.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), None, 10, 5, 'The rsvpEndDate must not be empty.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 2), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 5, 'The startDate must be before or equal to endDate.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 12, 2), datetime(2025, 11, 30), 10, 5, 'The rsvpStartDate must be before or equal to rsvpEndDate.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 0, 5, 'The attendeesLimit must be greater than 0.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), -1, 5, 'The attendeesLimit must be greater than 0.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, 0, 'The guestsLimit must be greater than 0.'),
        ('meeting2', 'new description', 'location', 'address', 'city', 'ca', datetime(2025, 12, 1), datetime(2025, 12, 1),
         datetime(2025, 11, 30), datetime(2025, 11, 30), 10, -1, 'The guestsLimit must be greater than 0.'),
    ])
def testEditMeetingInvalidValues(controller, mw, title, description, locationName, locationAddress, locationCity,
                                 locationCountryCode, startDate, endDate, rsvpStartDate, rsvpEndDate,
                                 attendeesLimit, guestsLimit, errorMessage):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.editMeeting(1, 1, title, description, locationName, locationAddress, locationCity,
                        locationCountryCode, startDate, endDate, rsvpStartDate, rsvpEndDate,
                        attendeesLimit, guestsLimit)

    # Assert
    assert str(excInfo.value) == errorMessage
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetings() == 1
    meeting = meetings.getMeeting(0)
    assert meeting.getTitle() == "meeting1"
    assert meeting.getDescription() == "description"


def testEditMeetingNotCreator(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.editMeeting(
            2,
            1,
            "meeting2",
            "new description",
            "location2",
            "address2",
            "city2",
            "us",
            datetime(2025, 12, 2),
            datetime(2025, 12, 3),
            datetime(2025, 11, 28),
            datetime(2025, 11, 29),
            20,
            10,
        )

    # Assert
    assert str(excInfo.value) == 'Only the creator of the meeting can edit it.'
    meetings = mw(controller.meetings)
    assert meetings.numberOfMeetings() == 1
    meeting = meetings.getMeeting(0)
    assert meeting.getTitle() == "meeting1"
    assert meeting.getDescription() == "description"


