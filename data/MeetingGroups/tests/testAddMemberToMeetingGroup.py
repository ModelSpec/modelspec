from datetime import datetime

import pytest
from freezegun import freeze_time


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Member, MeetingGroupLocation, MeetingGroupMember, MeetingGroupMemberRole

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
            User,
            UserAccess,
            UserRegistration,
        )
        MeetingGroupMemberRole = MeetingGroupMember.MeetingGroupMemberRole

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
            Meetings,
            Member,
            Payments,
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
    location = mw(MeetingGroupLocation, city="city", countryCode="ca")
    mw(MeetingGroup, id=1, name="meetinggroup1", description="description", meetingGroupLocation=location.model, creator=member1.model, meetings=c.meetings)

    yield c


@freeze_time("2025-11-30")
def testAddMemberSuccessfully(controller, mw):
    # Act
    controller.addMemberToMeetingGroup(2, 1)

    # Assert
    meetings = mw(controller.meetings)
    assert sum(len(mt.getMembers()) for mt in meetings.getMeetingGroups()) == 1
    mgMember = meetings.getMeetingGroup(0).getMember(0)
    assert mgMember.getMeetingGroup().getId() == 1
    assert mgMember.getMember().getId() == 2
    assert mgMember.getJoinedDate().year == datetime(2025, 11, 30).year
    assert mgMember.getJoinedDate().month == datetime(2025, 11, 30).month
    assert mgMember.getJoinedDate().day == datetime(2025, 11, 30).day
    assert mgMember.getRole().name == MeetingGroupMemberRole.Member.name
    assert mgMember.getIsActive() is True


def testAddMemberNonexistentMeetingGroup(controller):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeetingGroup(2, 999)

    # Assert
    assert str(excInfo.value) == 'Meeting group does not exist.'


def testAddNonexistentMemberToMeetingGroup(controller):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeetingGroup(999, 1)

    # Assert
    assert str(excInfo.value) == 'Member does not exist.'


def testAddMemberAlreadyInGroup(controller, mw):
    meetings = mw(controller.meetings)
    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    meetinggroup1 = next(mg for mg in meetings.getMeetingGroups() if mg.getId() == 1)
    mw(
        MeetingGroupMember,
        role=MeetingGroupMemberRole.Member,
        member=member2.model,
        meetingGroup=meetinggroup1.model,
    )
    existing = meetinggroup1.getMember(0)
    existing.setJoinedDate(datetime(2025, 11, 29))
    existing.setIsActive(True)

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addMemberToMeetingGroup(2, 1)

    # Assert
    assert str(excInfo.value) == 'Member is already part of the meeting group.'
    meetings = mw(controller.meetings)
    assert sum(len(mt.getMembers()) for mt in meetings.getMeetingGroups()) == 1


