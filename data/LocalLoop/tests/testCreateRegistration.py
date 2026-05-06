import pytest

@pytest.fixture
def givenController(modelingTool, mw):
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
    account2 = mw(UserAccount, userID="id2", firstName="Bob", lastName="Johnson", username="bobpart", email="bob@participant.com", phoneNumber="555-0200", role=participant1.model, adminViewModel=controller.adminViewModel)
    account3 = mw(UserAccount, userID="id3", firstName="Alice", lastName="Johnson", username="alicej", email="alice@example.com", phoneNumber="555-0300", role=participant2.model, adminViewModel=controller.adminViewModel)
    controller.accounts.append(organizer.model)
    controller.accounts.append(account2.model)
    controller.accounts.append(account3.model)

    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=controller.categoryViewModel)
    controller.categories.append(category.model)

    event = mw(Event, eventId="id1", organizerId="id1", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=100, category=category.model, organizer=organizer.getRole().model, eventRepository=controller.eventRepository)
    controller.events.append(event.model)

    registration = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id1", status="approved", timestamp=1735600000000, event=event.model, participant=account2.getRole().model, registrationRepository=controller.registrationRepository)
    controller.registrations.append(registration.model)

    yield controller


def testCreateRegistrationSuccess(mw, givenController):
    # Act
    givenController.createRegistration("id3", "id1", 1735600000000)

    # Assert
    created = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getParticipantId() == "id3" and r.getEventId() == "id1":
            created = r
            break

    assert created is not None
    assert created.getRegistrationId()
    assert created.getRegistrationId() != "id1"
    assert created.getEventId() == "id1"
    assert created.getParticipantId() == "id3"
    assert created.getOrganizerId() == "id1"
    assert created.getStatus() == "pending"
    assert created.getTimestamp() == 1735600000000

    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 2


def testCreateRegistrationFailNonExistentParticipant(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createRegistration("id999", "id1", 1735600000000)

    assert str(errorInfo.value) == "Participant with ID id999 does not exist."

    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 1


def testCreateRegistrationFailNonExistentEvent(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createRegistration("id2", "id999", 1735600000000)

    # Assert
    assert str(errorInfo.value) == "Event with ID id999 does not exist."

    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 1