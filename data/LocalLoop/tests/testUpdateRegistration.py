import pytest

@pytest.fixture
def givenController(modelingTool, mw):
    global Registration, Event
    if modelingTool == "umple":
        from ..umple.controller import LocalLoopController
        from ..umple.generated_model_layer import Participant, UserAccount, Organizer, Category, Event, Registration
    else:
        from ..ecore.controller import LocalLoopController
        from ..ecore.generated_model_layer import Participant, UserAccount, Organizer, Category, Event, Registration

    controller = LocalLoopController()

    organizerRole = mw(Organizer, companyName="AliceEvents Inc.")
    participant1 = mw(Participant())
    participant2 = mw(Participant())
    organizer = mw(UserAccount, userID="id1", firstName="Alice", lastName="Smith", username="aliceorg", email="alice@organizer.com", phoneNumber="555-0100", role=organizerRole.model, adminViewModel=controller.adminViewModel)
    participant = mw(UserAccount, userID="id2", firstName="Bob", lastName="Johnson", username="bobpart", email="bob@participant.com", phoneNumber="555-0200", role=participant1.model, adminViewModel=controller.adminViewModel)
    account3 = mw(UserAccount, userID="id3", firstName="Alice", lastName="Johnson", username="alicej", email="alice@example.com", phoneNumber="555-0300", role=participant2.model, adminViewModel=controller.adminViewModel)
    controller.accounts.append(organizer.model)
    controller.accounts.append(participant.model)
    controller.accounts.append(account3.model)

    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=controller.categoryViewModel)
    controller.categories.append(category.model)

    event = mw(Event, eventId="id1", organizerId="id1", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer.getRole().model, eventRepository=controller.eventRepository)
    controller.events.append(event.model)

    registration = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id1", status="approved", timestamp=1735600000000, event=event.model, participant=participant.getRole().model, registrationRepository=controller.registrationRepository)
    controller.registrations.append(registration.model)

    yield controller

@pytest.mark.parametrize(
    "userId, registrationId, newStatus",
    [
        ("id1", "id2", "cancelled"),
        ("id3", "id2", "cancelled"),
        ("id1", "id2", "approved"),
        ("id1", "id2", "pending"),
    ]
)
def testUpdateRegistrationSuccess(mw, givenController, userId, registrationId, newStatus):
    # Arrange
    participant = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            participant = p
    event = mw(givenController.events[0])
    newReg = mw(Registration, registrationId="id2", eventId="id1", participantId="id3", organizerId="id1", status="pending", timestamp=1735600000000, event=event.model, participant=participant.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(newReg.model)

    # Act
    givenController.updateRegistration(userId, registrationId, newStatus)

    # Assert
    updatedReg = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == registrationId:
            updatedReg = r
            break

    assert updatedReg is not None
    assert updatedReg.getStatus() == newStatus
    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 2

@pytest.mark.parametrize(
    "currentStatus, newStatus",
    [
        ("approved",  "approved"),
        ("approved",  "cancelled"),
        ("approved",  "pending"),
        ("cancelled", "cancelled"),
        ("cancelled", "approved"),
        ("cancelled", "pending"),
    ]
)
def testUpdateRegistrationFailApprovedOrCancelled(mw, givenController, currentStatus, newStatus):
    # Arrange
    participant = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            participant = p
    event = mw(givenController.events[0])
    newReg = mw(Registration, registrationId="id2", eventId="id1", participantId="id3", organizerId="id1", status=currentStatus, timestamp=1735600000000, event=event.model, participant=participant.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(newReg.model)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateRegistration("id1", "id2", newStatus)

    # Assert
    assert str(errorInfo.value) == f"Cannot update registration with status '{currentStatus}'."

    unchangedReg = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == "id2":
            unchangedReg = r
            break

    assert unchangedReg is not None
    assert unchangedReg.getStatus() == currentStatus
    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 2

def testUpdateRegistrationFailNonOrganizer(mw, givenController):
    # Arrange
    participant = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            participant = p
    event = mw(givenController.events[0])
    newReg = mw(Registration, registrationId="id2", eventId="id1", participantId="id3", organizerId="id1", status="pending", timestamp=1735600000000, event=event.model, participant=participant.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(newReg.model)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateRegistration("id2", "id2", "approved")

    # Assert
    assert str(errorInfo.value) == "User id2 is not authorized to update this registration."

    unchangedReg = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == "id2":
            unchangedReg = r
            break

    assert unchangedReg is not None
    assert unchangedReg.getStatus() == "pending"
    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 2

def testUpdateRegistrationFailAtCapacity(mw, givenController):
    # Arrange
    organizer = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id1":
            organizer = p
    category = mw(givenController.categories[0])
    event = mw(Event, eventId="id2", organizerId="id1", name="Summer Concert 2", description="Another summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=1, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event.model)

    participant2 = None
    participant3 = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id2":
            participant2 = p
        if p.getUserID() == "id3":
            participant3 = p
    reg1 = mw(Registration, registrationId="id2", eventId="id2", participantId="id2", organizerId="id1", status="approved", timestamp=1735600000000, event=event.model, participant=participant2.getRole().model, registrationRepository=givenController.registrationRepository)
    reg2 = mw(Registration, registrationId="id3", eventId="id2", participantId="id3", organizerId="id1", status="pending", timestamp=1735600000000, event=event.model, participant=participant3.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(reg1.model)
    givenController.registrations.append(reg2.model)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateRegistration("id1", "id3", "approved")

    # Assert
    assert str(errorInfo.value) == "Cannot approve registration if event is at full capacity."

    pendingReg = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == "id3":
            pendingReg = r
            break

    assert pendingReg is not None
    assert pendingReg.getStatus() == "pending"

    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id2"]
    assert len(regsForEvent) == 2

@pytest.mark.parametrize(
    "userId, registrationId, newStatus, errorMessage",
    [
        ("id999", "id2",   "approved",  "Invalid user ID."),
        ("id1",   "id999", "cancelled", "Invalid registration ID."),
        ("id1",   "id2",   "",          "Invalid status. Must be pending, approved or cancelled."),
        ("id1",   "id2",   "invalid",   "Invalid status. Must be pending, approved or cancelled."),
    ]
)
def testUpdateRegistrationFailInvalidValues(mw, givenController, userId, registrationId, newStatus, errorMessage):
    # Arrange
    participant = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            participant = p
    event = mw(givenController.events[0])
    newReg = mw(Registration, registrationId="id2", eventId="id1", participantId="id3", organizerId="id1", status="pending", timestamp=1735600000000, event=event.model, participant=participant.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(newReg.model)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateRegistration(userId, registrationId, newStatus)

    # Assert
    assert str(errorInfo.value) == errorMessage
