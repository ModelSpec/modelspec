import pytest

@pytest.fixture
def givenController(modelingTool, mw):
    global Category, Event, Registration
    if modelingTool == "umple":
        from ..umple.controller import LocalLoopController
        from ..umple.generated_model_layer import Participant, UserAccount, Organizer, Admin, Category, Event, Registration
    else:
        from ..ecore.controller import LocalLoopController
        from ..ecore.generated_model_layer import Participant, UserAccount, Organizer, Admin, Category, Event, Registration

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

    yield controller

def testDeleteOrganizerAccountWithNoEventsAsAdminSuccess(mw, givenController):
    # Act
    givenController.deleteAccount("id1", "id3")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4
    assert len(givenController.events) == 0

def testDeleteOrganizerAccountWithEventsWithNoRegistrationsAsAdminSuccess(mw, givenController):
    # Arrange
    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=givenController.categoryViewModel)
    givenController.categories.append(category.model)

    organizer = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID()== "id3":
            organizer = p
    event = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=1, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event.model)
    
    # Act
    givenController.deleteAccount("id1", "id3")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4

    event = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            event = e
    
    assert event is None
    assert len(givenController.events) == 0

def testDeleteOrganizerAccountWithEventsWithRegistrationsAsAdminSuccess(mw, givenController):
    # Arrange
    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=givenController.categoryViewModel)
    givenController.categories.append(category.model)

    organizer = None
    organizer2 = None
    participant2 = None
    participant5 = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID()== "id3":
            organizer = p
        if p.getUserID()== "id4":
            organizer2 = p
        if p.getUserID()== "id2":
            participant2 = p
        if p.getUserID()== "id5":
            participant5 = p

    event1 = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    event2 = mw(Event, eventId="id2", organizerId="id4", name="Winter Concert", description="A winter concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer2.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event1.model)
    givenController.events.append(event2.model)

    registration1 = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id3", status="approved", timestamp=1735600000000, event=event1.model, participant=participant2.getRole().model, registrationRepository=givenController.registrationRepository)
    registration2 = mw(Registration, registrationId="id2", eventId="id2", participantId="id5", organizerId="id4", status="approved", timestamp=1735600000000, event=event2.model, participant=participant5.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(registration1.model)
    givenController.registrations.append(registration2.model)

    # Act
    givenController.deleteAccount("id1", "id3")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4

    event = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            event = e
    
    assert event is None
    assert len(givenController.events) == 1

    reg1 = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == "id1":
            reg1 = r
    
    assert reg1 is None
    assert len(givenController.registrations) == 1
    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 0

def testDeleteParticipantAccountWithNoRegistrationsAsAdminSuccess(mw, givenController):
    # Act
    givenController.deleteAccount("id1", "id2")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id2":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4
    assert len(givenController.registrations) == 0

def testDeleteParticipantAccountWithRegistrationsAsAdminSuccess(mw, givenController):
    # Arrange
    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=givenController.categoryViewModel)
    givenController.categories.append(category.model)

    organizer = None
    organizer2 = None
    participant2 = None
    participant5 = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID()== "id3":
            organizer = p
        if p.getUserID()== "id4":
            organizer2 = p
        if p.getUserID()== "id2":
            participant2 = p
        if p.getUserID()== "id5":
            participant5 = p

    event1 = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    event2 = mw(Event, eventId="id2", organizerId="id4", name="Winter Concert", description="A winter concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer2.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event1.model)
    givenController.events.append(event2.model)

    registration1 = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id3", status="approved", timestamp=1735600000000, event=event1.model, participant=participant2.getRole().model, registrationRepository=givenController.registrationRepository)
    registration2 = mw(Registration, registrationId="id2", eventId="id2", participantId="id5", organizerId="id4", status="approved", timestamp=1735600000000, event=event2.model, participant=participant5.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(registration1.model)
    givenController.registrations.append(registration2.model)

    # Act
    givenController.deleteAccount("id1", "id2")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id2":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4

    reg1 = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == "id1":
            reg1 = r
    
    assert reg1 is None
    assert len(givenController.registrations) == 1
    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 0

def testDeleteOrganizerAccountWithNoEventsAsSelfSuccess(mw, givenController):
    # Act
    givenController.deleteAccount("id3", "id3")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4
    assert len(givenController.events) == 0

def testDeleteOrganizerAccountWithEventsWithNoRegistrationsAsSelfSuccess(mw, givenController):
    # Arrange
    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=givenController.categoryViewModel)
    givenController.categories.append(category.model)

    organizer = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID()== "id3":
            organizer = p
    event = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=1, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event.model)

    # Act
    givenController.deleteAccount("id3", "id3")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4

    event = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            event = e
    
    assert event is None
    assert len(givenController.events) == 0

def testDeleteOrganizerAccountWithEventsWithRegistrationsAsSelfSuccess(mw, givenController):
    # Arrange
    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=givenController.categoryViewModel)
    givenController.categories.append(category.model)

    organizer = None
    organizer2 = None
    participant2 = None
    participant5 = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID()== "id3":
            organizer = p
        if p.getUserID()== "id4":
            organizer2 = p
        if p.getUserID()== "id2":
            participant2 = p
        if p.getUserID()== "id5":
            participant5 = p

    event1 = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    event2 = mw(Event, eventId="id2", organizerId="id4", name="Winter Concert", description="A winter concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer2.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event1.model)
    givenController.events.append(event2.model)

    registration1 = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id3", status="approved", timestamp=1735600000000, event=event1.model, participant=participant2.getRole().model, registrationRepository=givenController.registrationRepository)
    registration2 = mw(Registration, registrationId="id2", eventId="id2", participantId="id5", organizerId="id4", status="approved", timestamp=1735600000000, event=event2.model, participant=participant5.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(registration1.model)
    givenController.registrations.append(registration2.model)

    # Act
    givenController.deleteAccount("id3", "id3")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4

    event = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            event = e
    
    assert event is None
    assert len(givenController.events) == 1

    reg1 = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == "id1":
            reg1 = r
    
    assert reg1 is None
    assert len(givenController.registrations) == 1
    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 0

def testDeleteParticipantAccountWithNoRegistrationsAsSelfSuccess(mw, givenController):
    # Act
    givenController.deleteAccount("id2", "id2")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id2":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4
    assert len(givenController.registrations) == 0

def testDeleteParticipantAccountWithRegistrationsAsSelfSuccess(mw, givenController):
    # Arrange
    category = mw(Category, categoryId="id1", name="Music", description="Music and concerts", categoryViewModel=givenController.categoryViewModel)
    givenController.categories.append(category.model)

    organizer = None
    organizer2 = None
    participant2 = None
    participant5 = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID()== "id3":
            organizer = p
        if p.getUserID()== "id4":
            organizer2 = p
        if p.getUserID()== "id2":
            participant2 = p
        if p.getUserID()== "id5":
            participant5 = p

    event1 = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    event2 = mw(Event, eventId="id2", organizerId="id4", name="Winter Concert", description="A winter concert", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer2.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event1.model)
    givenController.events.append(event2.model)

    registration1 = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id3", status="approved", timestamp=1735600000000, event=event1.model, participant=participant2.getRole().model, registrationRepository=givenController.registrationRepository)
    registration2 = mw(Registration, registrationId="id2", eventId="id2", participantId="id5", organizerId="id4", status="approved", timestamp=1735600000000, event=event2.model, participant=participant5.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(registration1.model)
    givenController.registrations.append(registration2.model)

    # Act
    givenController.deleteAccount("id2", "id2")

    # Assert
    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id2":
            account = p
            break
    
    assert account is None

    assert len(givenController.accounts) == 4

    reg1 = None
    for r in givenController.registrations:
        r = mw(r)
        if r.getRegistrationId() == "id1":
            reg1 = r
    
    assert reg1 is None
    assert len(givenController.registrations) == 1
    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 0

@pytest.mark.parametrize(
    "requestingUserID, targetUserID, errorMessage",
    [
        ("id2" , "id3", "Only admins or account owners can delete the account."),
        ("id3" , "id2", "Only admins or account owners can delete the account."),
    ]
)
def testDeleteAccountFailNotAdminOrSelf(mw, givenController, requestingUserID, targetUserID, errorMessage):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteAccount(requestingUserID, targetUserID)

    # Assert
    assert str(errorInfo.value) == errorMessage

    assert len(givenController.accounts) == 5

    account = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == targetUserID:
            account = p
            break
    
    assert account is not None

def testDeleteAccountFailNonExistentDeleter(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteAccount("id999", "id1")

    # Assert
    assert str(errorInfo.value) == "Account does not exist."

    assert len(givenController.accounts) == 5

def testDeleteAccountFailNonExistentDeletee(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteAccount("id1", "id999")

    # Assert
    assert str(errorInfo.value) == "User account does not exist."

    assert len(givenController.accounts) == 5