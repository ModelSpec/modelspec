from datetime import datetime

import pytest
from freezegun import freeze_time


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global UserRegistrationStatus

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

    if modelingTool == "umple":
        registration1 = mw(
            UserRegistration,
            login="user1",
            email="user1@example.com",
            firstName="John",
            lastName="Doe",
            userAccess=c.userAccess,
        )
        registration1.setName("John Doe")
        registration1.setStatus(UserRegistrationStatus.WaitingForConfirmation)
        registration1.setRegisterDate(datetime(2025, 11, 29))
    else:
        mw(
            UserRegistration,
            id=1,
            login="user1",
            email="user1@example.com",
            firstName="John",
            lastName="Doe",
            name="John Doe",
            status=UserRegistrationStatus.WaitingForConfirmation,
            registerDate=datetime(2025, 11, 29),
            userAccess=c.userAccess,
        )

    yield c


@freeze_time("2025-11-30")
def testUpdateRegistrationSuccessfully(controller, mw):
    # Act
    controller.updateUserRegistration(1, 'user1updated', 'updated@example.com', 'Jane', 'Smith',
                                           'Jane Smith', 'WaitingForConfirmation')

    # Assert
    ua = mw(controller.userAccess)
    assert ua.numberOfUserRegistrations() == 1
    registration = ua.getUserRegistration(0)
    assert registration.getId() == 1
    assert registration.getLogin() == 'user1updated'
    assert registration.getEmail() == 'updated@example.com'
    assert registration.getFirstName() == 'Jane'
    assert registration.getLastName() == 'Smith'
    assert registration.getName() == 'Jane Smith'
    assert registration.getStatus().name == UserRegistrationStatus.WaitingForConfirmation.name
    assert registration.getRegisterDate().year == datetime(2025, 11, 29).year
    assert registration.getRegisterDate().month == datetime(2025, 11, 29).month
    assert registration.getRegisterDate().day == datetime(2025, 11, 29).day
    assert registration.getConfirmedDate() == None
    assert ua.numberOfUsers() == 0


@freeze_time("2025-11-30")
def testConfirmRegistrationSuccessfully(controller, mw):
    # Act
    controller.updateUserRegistration(1, 'user1', 'user1@example.com', 'John', 'Doe', 'John Doe', 'Confirmed')

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
    assert registration.getStatus().name == UserRegistrationStatus.Confirmed.name
    assert registration.getRegisterDate().year == datetime(2025, 11, 29).year
    assert registration.getRegisterDate().month == datetime(2025, 11, 29).month
    assert registration.getRegisterDate().day == datetime(2025, 11, 29).day
    assert registration.getConfirmedDate().year == datetime(2025, 11, 30).year
    assert registration.getConfirmedDate().month == datetime(2025, 11, 30).month
    assert registration.getConfirmedDate().day == datetime(2025, 11, 30).day
    assert ua.numberOfUsers() == 1
    user = ua.getUser(0)
    assert user.getLogin() == 'user1'
    assert user.getEmail() == 'user1@example.com'
    assert user.getFirstName() == 'John'
    assert user.getLastName() == 'Doe'
    assert user.getName() == 'John Doe'
    assert user.getCreateDate().year == datetime(2025, 11, 30).year
    assert user.getCreateDate().month == datetime(2025, 11, 30).month
    assert user.getCreateDate().day == datetime(2025, 11, 30).day


@freeze_time("2025-11-30")
def testExpireRegistrationSuccessfully(controller, mw):
    # Act
    controller.updateUserRegistration(1, 'user1', 'user1@example.com', 'John', 'Doe', 'John Doe', 'Expired')

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
    assert registration.getStatus().name == UserRegistrationStatus.Expired.name
    assert registration.getRegisterDate().year == datetime(2025, 11, 29).year
    assert registration.getRegisterDate().month == datetime(2025, 11, 29).month
    assert registration.getRegisterDate().day == datetime(2025, 11, 29).day
    assert registration.getConfirmedDate() == None
    assert ua.numberOfUsers() == 0


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
@freeze_time("2025-11-30")
def testUpdateRegistrationInvalidValues(controller, mw, login, email, firstName, lastName, name, errorMessage):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.updateUserRegistration(1, login, email, firstName, lastName, name, 'WaitingForConfirmation')

    # Assert
    assert str(excInfo.value) == errorMessage
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


@freeze_time("2025-11-30")
def testUpdateConfirmedRegistration(controller, mw):
    if hasattr(UserRegistration, "nextId"):
        registration2 = mw(
            UserRegistration,
            login="user2",
            email="user2@example.com",
            firstName="Alice",
            lastName="Johnson",
            userAccess=controller.userAccess,
        )
        registration2.setName("Alice Johnson")
    else:
        registration2 = mw(
            UserRegistration,
            id=2,
            login="user2",
            email="user2@example.com",
            firstName="Alice",
            lastName="Johnson",
            name="Alice Johnson",
            userAccess=controller.userAccess,
        )

    ua = mw(controller.userAccess)
    registration2 = next(r for r in ua.getUserRegistrations() if r.getId() == 2)
    registration2.setStatus(UserRegistrationStatus.Confirmed)
    registration2.setRegisterDate(datetime(2025, 11, 28))
    registration2.setConfirmedDate(datetime(2025, 11, 29))

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.updateUserRegistration(2, 'user2', 'user2@example.com', 'Jane', 'Smith',
                               'Jane Smith', 'WaitingForConfirmation')

    # Assert
    assert str(excInfo.value) == 'Cannot update a confirmed user registration.'
    assert ua.numberOfUserRegistrations() == 2
    registration2 = next(r for r in ua.getUserRegistrations() if r.getId() == 2)
    assert registration2.getLogin() == 'user2'
    assert registration2.getEmail() == 'user2@example.com'
    assert registration2.getFirstName() == 'Alice'
    assert registration2.getLastName() == 'Johnson'
    assert registration2.getName() == 'Alice Johnson'
    assert registration2.getStatus().name == UserRegistrationStatus.Confirmed.name


@freeze_time("2025-11-30")
def testUpdateExpiredRegistration(controller, mw):
    if hasattr(UserRegistration, "nextId"):
        registration2 = mw(
            UserRegistration,
            login="user2",
            email="user2@example.com",
            firstName="Alice",
            lastName="Johnson",
            userAccess=controller.userAccess,
        )
        registration2.setName("Alice Johnson")
    else:
        registration2 = mw(
            UserRegistration,
            id=2,
            login="user2",
            email="user2@example.com",
            firstName="Alice",
            lastName="Johnson",
            name="Alice Johnson",
            userAccess=controller.userAccess,
        )

    ua = mw(controller.userAccess)
    registration2 = next(r for r in ua.getUserRegistrations() if r.getId() == 2)
    registration2.setStatus(UserRegistrationStatus.Expired)
    registration2.setRegisterDate(datetime(2025, 11, 27))

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.updateUserRegistration(2, 'user2', 'user2@example.com', 'Jane', 'Smith',
                               'Jane Smith', 'WaitingForConfirmation')

    # Assert
    assert str(excInfo.value) == 'Cannot update an expired user registration.'
    registration2 = next(r for r in ua.getUserRegistrations() if r.getId() == 2)
    assert registration2.getLogin() == 'user2'
    assert registration2.getEmail() == 'user2@example.com'
    assert registration2.getFirstName() == 'Alice'
    assert registration2.getLastName() == 'Johnson'
    assert registration2.getName() == 'Alice Johnson'
    assert registration2.getStatus().name == UserRegistrationStatus.Expired.name


