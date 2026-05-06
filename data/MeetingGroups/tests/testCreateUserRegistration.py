from datetime import datetime

import pytest
from freezegun import freeze_time


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration, UserRegistrationStatus

    if modelingTool == "umple":
        from ..umple.controller import MeetingGroupsController
        from ..umple.generated_model_layer import (
            Administration,
            Meeting,
            MeetingGroup,
            MeetingGroupProposal,
            Meetings,
            Payments,
            User,
            UserAccess,
            UserRegistration,
        )
        UserRegistrationStatus = UserRegistration.UserRegistrationStatus

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
            MeetingGroupProposal,
            Meetings,
            Payments,
            User,
            UserAccess,
            UserRegistration,
            UserRegistrationStatus,
        )

    c = MeetingGroupsController()
    c.userAccess = mw(UserAccess).model
    c.administration = mw(Administration).model
    c.meetings = mw(Meetings).model
    c.payments = mw(Payments).model

    yield c


@freeze_time("2025-11-30")
def testCreateRegistrationSuccessfully(controller, mw):
    # Act
    controller.createUserRegistration('user1', 'user1@example.com', 'John', 'Doe', 'John Doe')

    # Assert
    ua = mw(controller.userAccess)
    assert ua.numberOfUserRegistrations() == 1
    registration = ua.getUserRegistration(0)
    assert registration.getId() == 1
    assert registration.getLogin() == 'user1'
    assert registration.getEmail() == 'user1@example.com'
    assert registration.getFirstName() == 'John'
    assert registration.getLastName() == 'Doe'
    assert registration.getName() == 'John Doe'
    assert registration.getStatus().name == UserRegistrationStatus.WaitingForConfirmation.name
    assert registration.getRegisterDate().year == datetime(2025, 11, 30).year
    assert registration.getRegisterDate().month == datetime(2025, 11, 30).month
    assert registration.getRegisterDate().day == datetime(2025, 11, 30).day
    assert registration.getConfirmedDate() == None


@freeze_time("2025-11-30")
def testCreateRegistrationWithUniqueId(controller, mw):
    if hasattr(UserRegistration, "nextId"):
        registration = mw(
            UserRegistration,
            login="user2",
            email="user2@email.com",
            firstName="Jane",
            lastName="Smith",
            userAccess=controller.userAccess,
        )
        registration.setName("Jane Smith")
        registration.setStatus(UserRegistrationStatus.WaitingForConfirmation)
        registration.setRegisterDate(datetime(2025, 11, 30))
    else:
        mw(
            UserRegistration,
            id=1,
            login="user2",
            email="user2@email.com",
            firstName="Jane",
            lastName="Smith",
            name="Jane Smith",
            status=UserRegistrationStatus.WaitingForConfirmation,
            registerDate=datetime(2025, 11, 30),
            userAccess=controller.userAccess,
        )

    # Act
    controller.createUserRegistration('user1', 'user1@email.com', 'John', 'Doe', 'John Doe')

    # Assert
    ua = mw(controller.userAccess)
    assert ua.numberOfUserRegistrations() == 2
    registration = next(r for r in ua.getUserRegistrations() if r.getId() != 1)
    assert registration.getLogin() == 'user1'
    assert registration.getEmail() == 'user1@email.com'
    assert registration.getFirstName() == 'John'
    assert registration.getLastName() == 'Doe'
    assert registration.getName() == 'John Doe'
    assert registration.getStatus().name == UserRegistrationStatus.WaitingForConfirmation.name
    assert registration.getRegisterDate().year == datetime(2025, 11, 30).year
    assert registration.getRegisterDate().month == datetime(2025, 11, 30).month
    assert registration.getRegisterDate().day == datetime(2025, 11, 30).day
    assert registration.getConfirmedDate() == None


@pytest.mark.parametrize("login,email,firstName,lastName,name,errorMessage", [
    ('', 'user1@example.com', 'John', 'Doe', 'John Doe', 'The login must not be empty.'),
    ('user1', '', 'John', 'Doe', 'John Doe', 'The email must not be empty.'),
    ('user1', 'user1example.com', 'John', 'Doe', 'John Doe', 'The email must contain exactly one "@" character.'),
    ('user1', 'user1@@example.com', 'John', 'Doe', 'John Doe', 'The email must contain exactly one "@" character.'),
    ('user1', 'user1@examplecom', 'John', 'Doe', 'John Doe',
     'The email must contain a "." character after the "@" character.'),
    ('user1', 'user1@example.', 'John', 'Doe', 'John Doe', 'The email must not end with a "." character.'),
    ('user1', 'user1@example.com', '', 'Doe', 'John Doe', 'The firstName must not be empty.'),
    ('user1', 'user1@example.com', 'John', '', 'John Doe', 'The lastName must not be empty.'),
    ('user1', 'user1@example.com', 'John', 'Doe', '', 'The name must not be empty.'),
])
def testCreateRegistrationInvalidValues(controller, mw, login, email, firstName, lastName, name, errorMessage):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.createUserRegistration(login, email, firstName, lastName, name)

    # Assert
    assert str(excInfo.value) == errorMessage
    assert mw(controller.userAccess).numberOfUserRegistrations() == 0


