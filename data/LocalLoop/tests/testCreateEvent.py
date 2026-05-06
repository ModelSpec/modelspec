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

    organizerRole = mw(Organizer, companyName="AliceEvents Inc.")
    participantRole = mw(Participant())
    organizer = mw(UserAccount, userID="id1", firstName="Alice", lastName="Smith", username="aliceorg", email="alice@organizer.com", phoneNumber="555-0100", role=organizerRole.model, adminViewModel=controller.adminViewModel)
    participant = mw(UserAccount, userID="id2", firstName="Bob", lastName="Johnson", username="bobpart", email="bob@participant.com", phoneNumber="555-0200", role=participantRole.model, adminViewModel=controller.adminViewModel)
    controller.accounts.append(organizer.model)
    controller.accounts.append(participant.model)

    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=controller.categoryViewModel)
    controller.categories.append(category.model)

    event = mw(Event, eventId="id1", organizerId="id1", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=100, category=category.model, organizer=organizer.getRole().model, eventRepository=controller.eventRepository)
    controller.events.append(event.model)

    yield controller


@pytest.mark.parametrize(
    "organizerId, name, description, categoryId, fee, eventStart, eventEnd, capacity",
    [
        ("id1", "Winter Festival", "Annual winter festival", "id1", 25.5, 1740000000000, 1740010000000, 200),
        ("id1", "Winter Festival", "Annual winter festival", "id1", 0.0, 1740000000000, 1740010000000, 200),
        ("id1", "Winter Festival", "Annual winter festival", "id1", 25.5, 1740000000000, 1740010000000, 0),
    ],
)
def testCreateEventSuccess(mw, givenController, organizerId, name, description, categoryId, fee, eventStart, eventEnd, capacity):
    # Act
    givenController.createEvent(organizerId, name, description, categoryId, fee, eventStart, eventEnd, capacity)

    # Assert
    created = None
    for e in givenController.events:
        e = mw(e)
        if e.getName() == name:
            created = e
            break

    assert created is not None
    assert created.getEventId()
    assert created.getEventId() != "id1"
    assert created.getOrganizerId() == organizerId
    assert created.getName() == name
    assert created.getDescription() == description
    assert created.getCategoryId() == categoryId
    assert created.getFee() == pytest.approx(float(fee))
    assert created.getEventStart() == eventStart
    assert created.getEventEnd() == eventEnd
    assert created.getCapacity() == capacity

    assert len(givenController.events) == 2


@pytest.mark.parametrize(
    "organizerId, name, description, categoryId, fee, eventStart, eventEnd, capacity, error",
    [
        ("id1", "", "Annual winter festival", "id1", 25.5, 1740000000000, 1740010000000, 200, "Event name must not be empty."),
        ("id1", "Winter Festival", "", "id1", 25.5, 1740000000000, 1740010000000, 200, "Event description must not be empty."),
        ("id1", "Winter Festival", "Annual winter festival", "id1", -10.0, 1740000000000, 1740010000000, 200, "Fee must be 0 or a positive number."),
        ("id1", "Winter Festival", "Annual winter festival", "id1", 25.5, 1740000000000, 1740010000000, -5, "Capacity must be 0 or a positive integer."),
        ("id1", "Winter Festival", "Annual winter festival", "id1", 25.5, 1740010000000, 1740000000000, 200, "Event end time must be after start time."),
        ("id1", "Winter Festival", "Annual winter festival", "id1", 25.5, 0, 1740010000000, 200, "Event start time must not be empty."),
        ("id1", "Winter Festival", "Annual winter festival", "id1", 25.5, 1740000000000, 0, 200, "Event end time must not be empty."),
        ("id1", "Winter Festival", "Annual winter festival", "id999", 25.5, 1740000000000, 1740010000000, 200, "Category with the given ID does not exist."),
    ],
)
def testCreateEventFailInvalidValues(givenController, organizerId, name, description, categoryId, fee, eventStart, eventEnd, capacity, error):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createEvent(organizerId, name, description, categoryId, fee, eventStart, eventEnd, capacity)

    # Assert
    assert str(errorInfo.value) == error
    assert len(givenController.events) == 1


def testCreateEventFailNonOrganizer(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createEvent("id2", "Spring Concert", "A beautiful concert", "id1", 30.0, 1740000000000, 1740010000000, 150)

    # Assert
    assert str(errorInfo.value) == "Only organizers can create events."
    assert len(givenController.events) == 1


def testCreateEventFailNonExistentAccount(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createEvent("id999", "Spring Concert", "A beautiful concert", "id1", 30.0, 1740000000000, 1740010000000, 150)

    # Assert
    assert str(errorInfo.value) == "Account with ID id999 does not exist."
    assert len(givenController.events) == 1