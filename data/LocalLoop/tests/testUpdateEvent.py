import pytest

@pytest.fixture
def givenController(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import LocalLoopController
        from ..umple.generated_model_layer import Participant, UserAccount, Organizer, Category, Event
    else:
        from ..ecore.controller import LocalLoopController
        from ..ecore.generated_model_layer import Participant, UserAccount, Organizer, Category, Event

    controller = LocalLoopController()

    organizer1 = mw(Organizer, companyName="AliceEvents Inc.")
    organizer2 = mw(Organizer, companyName="CarolEvents Co.")
    participant = mw(Participant())
    organizer = mw(UserAccount, userID="id1", firstName="ALice", lastName="Smith", username="aliceorg", email="alice@organizer.com", phoneNumber="555-0100", role=organizer1.model, adminViewModel=controller.adminViewModel)
    account2 = mw(UserAccount, userID="id2", firstName="Bob", lastName="Johnson", username="bobpart", email="bob@participant.com", phoneNumber="555-0200", role=participant.model, adminViewModel=controller.adminViewModel)
    account3 = mw(UserAccount, userID="id3", firstName="Carol", lastName="White", username="carolorg", email="carol@organizer.com", phoneNumber="555-0300", role=organizer2.model, adminViewModel=controller.adminViewModel)
    controller.accounts.append(organizer.model)
    controller.accounts.append(account2.model)
    controller.accounts.append(account3.model)

    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=controller.categoryViewModel)
    controller.categories.append(category.model)

    event = mw(Event, eventId="id1", organizerId="id1", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=100, category=category.model, organizer=organizer.getRole().model, eventRepository=controller.eventRepository)
    controller.events.append(event.model)

    yield controller


@pytest.mark.parametrize(
    "organizerId, eventId, name, description, categoryId, fee, eventStart, eventEnd, capacity",
    [
        ("id1", "id1", "Updated Concert", "Updated summer concert", "id1",  60.0, 1735689600000, 1735693200000, 120),
        ("id1", "id1", "Updated Concert", "Updated summer concert", "id1",   0.0, 1735689600000, 1735693200000, 120),
        ("id1", "id1", "Updated Concert", "Updated summer concert", "id1",  60.0, 1735689600000, 1735693200000, 0)
    ]
)
def testUpdateEventSuccess(mw, givenController, organizerId, eventId, name, description, categoryId, fee, eventStart, eventEnd, capacity):
    # Act
    givenController.updateEvent(organizerId, eventId, name, description, categoryId, fee, eventStart, eventEnd, capacity)

    # Assert
    assert len(givenController.events) == 1

    updatedEvent = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == eventId:
            updatedEvent = e
            break

    assert updatedEvent is not None
    assert updatedEvent.getName() == name
    assert updatedEvent.getDescription() == description
    assert updatedEvent.getCategoryId() == categoryId
    assert updatedEvent.getFee() == fee
    assert updatedEvent.getEventStart() == eventStart
    assert updatedEvent.getEventEnd() == eventEnd
    assert updatedEvent.getCapacity() == capacity
    assert updatedEvent.getOrganizerId() == organizerId

@pytest.mark.parametrize(
    "organizerId, eventId, name, description, categoryId, fee, eventStart, eventEnd, capacity, errorMessage",
    [
        ("id1", "id1", "",               "Annual winter festival", "id1",   25.5, 1740000000000, 1740010000000,  200, "Event name must not be empty."),
        ("id1", "id1", "Winter Festival", "",                      "id1",   25.5, 1740000000000, 1740010000000,  200, "Event description must not be empty."),
        ("id1", "id1", "Winter Festival", "Annual winter festival", "id1", -10.0, 1740000000000, 1740010000000,  200, "Fee must be 0 or a positive number."),
        ("id1", "id1", "Winter Festival", "Annual winter festival", "id1",  25.5, 1740000000000, 1740010000000,   -5, "Capacity must be 0 or a positive integer."),
        ("id1", "id1", "Winter Festival", "Annual winter festival", "id1",  25.5, 1740010000000, 1740000000000,  200, "Event end time must be after start time."),
        ("id1", "id1", "Winter Festival", "Annual winter festival", "id1",  25.5,             0, 1740010000000,  200, "Event start time must not be empty."),
        ("id1", "id1", "Winter Festival", "Annual winter festival", "id1",  25.5, 1740000000000,             0,  200, "Event end time must not be empty."),
        ("id1", "id1", "Winter Festival", "Annual winter festival", "id999", 25.5, 1740000000000, 1740010000000, 200, "Category with the given ID does not exist."),
    ]
)
def testUpdateEventFailInvalidValues(mw, givenController, organizerId, eventId, name, description, categoryId, fee, eventStart, eventEnd, capacity, errorMessage):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateEvent(organizerId, eventId, name, description, categoryId, fee, eventStart, eventEnd, capacity)

    # Assert
    assert str(errorInfo.value) == errorMessage
    assert len(givenController.events) == 1

    originalEvent = mw(givenController.events[0])
    assert originalEvent.getName() == "Summer Concert"
    assert originalEvent.getDescription() == "A summer concert"
    assert originalEvent.getFee() == 50.0
    assert originalEvent.getEventStart() == 1735689600000
    assert originalEvent.getEventEnd() == 1735693200000
    assert originalEvent.getCapacity() == 100


def testUpdateEventFailNotOrganizer(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateEvent("id2", "id1", "Spring Concert", "A beautiful concert", "id1", 30.0, 1740000000000, 1740010000000, 150)

    # Assert
    assert str(errorInfo.value) == "Only organizers can update events."
    assert len(givenController.events) == 1
    assert mw(givenController.events[0]).getName() == "Summer Concert"


def testUpdateEventFailWrongOrganizer(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateEvent("id3", "id1", "Spring Concert", "A beautiful concert", "id1", 30.0, 1740000000000, 1740010000000, 150)

    # Assert
    assert str(errorInfo.value) == "Only the event organizer can update this event."
    assert len(givenController.events) == 1
    assert mw(givenController.events[0]).getName() == "Summer Concert"


def testUpdateEventFailNonExistentEvent(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateEvent("id1", "id999", "Spring Concert", "A beautiful concert", "id1", 30.0, 1740000000000, 1740010000000, 150)

    # Assert
    assert str(errorInfo.value) == "Event with ID id999 does not exist."
    assert len(givenController.events) == 1
