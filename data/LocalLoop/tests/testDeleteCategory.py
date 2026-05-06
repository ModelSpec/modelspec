import pytest

@pytest.fixture
def givenController(modelingTool, mw):
    global Event, Registration
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

    category1 = mw(Category, categoryId="id1", name="Sports", description="Sports related events", categoryViewModel=controller.categoryViewModel)
    category2 = mw(Category, categoryId="id2", name="Music", description="Music and concerts", categoryViewModel=controller.categoryViewModel)
    controller.categories.append(category1.model)
    controller.categories.append(category2.model)

    yield controller

def testDeleteCategoryWithNoEventsAsAdminSuccess(mw, givenController):
    # Act
    givenController.deleteCategory("id1", "id1")

    # Assert
    deletedCategory = None
    for c in givenController.categories:
        c = mw(c)
        if c.getCategoryId() == "id1":
            deletedCategory = c
            break

    assert deletedCategory is None
    assert len(givenController.categories) == 1

def testDeleteCategoryWithEventsWithNoRegistrationsAsAdminSuccess(mw, givenController):
    # Arrange
    category = None
    for c in givenController.categories:
        c = mw(c)
        if c.getCategoryId() == "id2":
            category = c
    organizer = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            organizer = p

    event = mw(Event, eventId="id1", organizerId="id3", name="Summer Concert", description="A summer concert", categoryId="id2", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category.model, organizer=organizer.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event.model)

    # Act
    givenController.deleteCategory("id1", "id2")

    # Assert
    deletedCategory = None
    for c in givenController.categories:
        c = mw(c)
        if c.getCategoryId() == "id2":
            deletedCategory = c
            break

    assert deletedCategory is None
    assert len(givenController.categories) == 1

    assert len(givenController.events) == 0

def testDeleteCategoryWithEventsWithRegistrationsAsAdminSuccess(mw, givenController):
    # Arrange
    category1 = None
    category2 = None
    for c in givenController.categories:
        c = mw(c)
        if c.getCategoryId() == "id1":
            category1 = c
        if c.getCategoryId() == "id2":
            category2 = c
    organizer3 = None
    organizer4 = None
    participant2 = None
    participant5 = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUserID() == "id3":
            organizer3 = p
        if p.getUserID() == "id4":
            organizer4 = p
        if p.getUserID() == "id2":
            participant2 = p
        if p.getUserID() == "id5":
            participant5 = p

    event1 = mw(Event, eventId="id1", organizerId="id3", name="Olympics", description="Summer Olympics", categoryId="id1", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category1.model, organizer=organizer3.getRole().model, eventRepository=givenController.eventRepository)
    event2 = mw(Event, eventId="id2", organizerId="id4", name="Winter Concert", description="A winter concert", categoryId="id2", fee=50.0, eventStart=1735689600000, eventEnd=1735693200000, capacity=2, category=category2.model, organizer=organizer4.getRole().model, eventRepository=givenController.eventRepository)
    givenController.events.append(event1.model)
    givenController.events.append(event2.model)

    registration1 = mw(Registration, registrationId="id1", eventId="id1", participantId="id2", organizerId="id3", status="approved", timestamp=1735600000000, event=event1.model, participant=participant2.getRole().model, registrationRepository=givenController.registrationRepository)
    registration2 = mw(Registration, registrationId="id2", eventId="id2", participantId="id5", organizerId="id4", status="approved", timestamp=1735600000000, event=event2.model, participant=participant5.getRole().model, registrationRepository=givenController.registrationRepository)
    givenController.registrations.append(registration1.model)
    givenController.registrations.append(registration2.model)

    # Act
    givenController.deleteCategory("id1", "id1")

    # Assert
    deletedCategory = None
    for c in givenController.categories:
        c = mw(c)
        if c.getCategoryId() == "id1":
            deletedCategory = c
            break

    assert deletedCategory is None
    assert len(givenController.categories) == 1

    assert len(givenController.events) == 1
    eventDeleted = None
    for e in givenController.events:
        e = mw(e)
        if e.getEventId() == "id1":
            eventDeleted = e
    assert eventDeleted is None

    regsForEvent = [r for r in givenController.registrations if mw(r).getEventId() == "id1"]
    assert len(regsForEvent) == 0

    assert len(givenController.registrations) == 1

@pytest.mark.parametrize(
    "userID",
    [
        ("id2"),
        ("id3"),
    ]
)
def testDeleteCategoryFailNotAdmin(mw, givenController, userID):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteCategory(userID, "id1")

    # Assert
    assert str(errorInfo.value) == "Only admin users can delete categories."

    category = None
    for c in givenController.categories:
        c = mw(c)
        if c.getCategoryId() == "id1":
            category = c
            break

    assert category is not None
    assert len(givenController.categories) == 2

def testDeleteCategoryFailNonExistentAccount(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteCategory("id999", "id1")

    # Assert
    assert str(errorInfo.value) == "Account with ID id999 does not exist."

    category = None
    for c in givenController.categories:
        c = mw(c)
        if c.getCategoryId() == "id1":
            category = c
            break

    assert category is not None
    assert len(givenController.categories) == 2

def testDeleteCategoryFailNonExistentCategory(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.deleteCategory("id1", "id999")

    # Assert
    assert str(errorInfo.value) == "Category with ID id999 does not exist."

    assert len(givenController.categories) == 2