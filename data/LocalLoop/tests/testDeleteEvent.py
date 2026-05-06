import pytest

@pytest.fixture
def givenController(modelingTool, mw):
    global Registration
    if modelingTool == "umple":
        from ..umple.controller import LocalLoopController
        from ..umple.generated_model_layer import Participant, UserAccount, Organizer, Category, Event, Registration, Admin
    else:
        from ..ecore.controller import LocalLoopController
        from ..ecore.generated_model_layer import Participant, UserAccount, Organizer, Category, Event, Registration, Admin

    controller = LocalLoopController()

    admin = mw(Admin())
    organizer1 = mw(Organizer, companyName="AliceEvents Inc.")
    organizer2 = mw(Organizer, companyName="CarolEvents Co.")
    participant1 = mw(Participant())
    participant2 = mw(Participant())
    account1 = mw(UserAccount, userID="id1", firstName="Admin", lastName="User", username="adminuser", email="admin@example.com", phoneNumber="555-0100", role=admin.model, adminViewModel=controller.adminViewModel)
    account2 = mw(UserAccount, userID="id2", firstName="John", lastName="Doe", username="johndoe", email="john@example.com", phoneNumber="555-0200", role=participant1.model, adminViewModel=controller.adminViewModel)
    account3 = mw(UserAccount, userID="id3", firstName="Alice", lastName="Johnson", username="alicej", email="alice@example.com", phoneNumber="555-0300", role=organizer1.model, adminViewModel=controller.adminViewModel)
    account4 = mw(UserAccount, userID="id4", firstName="Carol", lastName="White", username="carolorg", email="carol@organizer.com", phoneNumber="555-0400", role=organizer2.model, adminViewModel=controller.adminViewModel)
    account5 = mw(UserAccount, userID="id5", firstName="Peter", lastName="Poe", username="ppoe", email="peter@example.com", phoneNumber="555-0500", role=participant2.model, adminViewModel=controller.adminViewModel)
    controller.accounts.append(account1.model)
    controller.accounts.append(account2.model)
    controller.accounts.append(account3.model)
    controller.accounts.append(account4.model)
    controller.accounts.append(account5.model)

    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=controller.categoryViewModel)
    controller.categories.append(category.model)

    event1 = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=100, category=category.model, organizer=account3.getRole().model, eventRepository=controller.eventRepository)
    event2 = mw(Event, eventId="id2", organizerId="id3", name="Winter Concert", description="A winter concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=100, category=category.model, organizer=account3.getRole().model, eventRepository=controller.eventRepository)
    controller.events.append(event1.model)
    controller.events.append(event2.model)

    yield controller

def testDeleteEventThatHasNoRegistrationsAsOrganizerSuccess(mw, givenController):
    # Act
    givenController.deleteEvent("id3", "id1")

    # Assert
    deletedEvent = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            deletedEvent = e
            break

    assert deletedEvent is None
    assert len(givenController.events) == 1
    assert len(givenController.registrations) == 0

def testDeleteEventThatHasRegistrationsAsOrganizerSuccess(mw, givenController):
    # Arrange
    event1 = None
    event2 = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            event1 = e
        if e.getEventId() == "id2":
            event2 = e
    participant2 = None
    participant5 = None
    for a in givenController.accounts:
        a = mw(a)
        if a.getUserID() == "id2":
            participant2 = a
        if a.getUserID() == "id5":
            participant5 = a

    registration1 = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id3", status="approved", timestamp=1735600000000, event=event1.model, participant=participant2.getRole().model, registrationRepository=givenController.registrationRepository)
    registration2 = mw(Registration, registrationId="id2", eventId="id2", participantId="id5", organizerId="id3", status="approved", timestamp=1735600000000, event=event2.model, participant=participant5.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(registration1.model)
    givenController.registrations.append(registration2.model)

    # Act
    givenController.deleteEvent("id3", "id1")

    # Assert
    deletedEvent = None
    for a in givenController.events:
        a = mw(a)
        if a.getEventId() == "id1":
            deletedEvent = a
            break

    assert deletedEvent is None
    assert len(givenController.events) == 1
    assert len(givenController.registrations) == 1

    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 0


def testDeleteEventFailNotOrganizer(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteEvent("id2", "id1")

    # Assert
    assert str(errorInfo.value) == "Only organizers can delete events."

    event = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            event = e
            break

    assert event is not None
    assert len(givenController.events) == 2


def testDeleteEventFailWrongOrganizer(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteEvent("id4", "id1")

    # Assert
    assert str(errorInfo.value) == "Only the event organizer can delete this event."

    event = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            event = e
            break

    assert event is not None
    assert len(givenController.events) == 2


def testDeleteEventFailNonExistentEvent(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteEvent("id3", "id999")

    # Assert
    assert str(errorInfo.value) == "Event with ID id999 does not exist."
    assert len(givenController.events) == 2
