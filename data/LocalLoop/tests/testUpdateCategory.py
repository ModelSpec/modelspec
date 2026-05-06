import pytest

@pytest.fixture
def givenController(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import LocalLoopController
        from ..umple.generated_model_layer import Participant, UserAccount, Organizer, Admin, Category
    else:
        from ..ecore.controller import LocalLoopController
        from ..ecore.generated_model_layer import Participant, UserAccount, Organizer, Admin, Category

    controller = LocalLoopController()

    admin = mw(Admin())
    organizer = mw(Organizer, companyName="Name")
    participant = mw(Participant())
    account1 = mw(UserAccount, userID="id1", firstName="Admin", lastName="User", username="adminuser", email="admin@example.com", phoneNumber="555-0100", role=admin.model, adminViewModel=controller.adminViewModel)
    account2 = mw(UserAccount, userID="id2", firstName="Bob", lastName="Smith", username="bobsmith", email="bob@example.com", phoneNumber="555-0200", role=organizer.model, adminViewModel=controller.adminViewModel)
    account3 = mw(UserAccount, userID="id3", firstName="Jane", lastName="Doe", username="janedoe", email="jane@example.com", phoneNumber="555-0300", role=participant.model, adminViewModel=controller.adminViewModel)
    controller.accounts.append(account1.model)
    controller.accounts.append(account2.model)
    controller.accounts.append(account3.model)

    category = mw(Category, categoryId="id1", name="Sports", description="Sports related events", categoryViewModel=controller.categoryViewModel)
    controller.categories.append(category.model)
    yield controller

def testUpdateCategorySuccess(mw, givenController):
    # Act
    givenController.updateCategory("id1", "id1", "Athletics", "Athletic competitions and sports events")

    # Assert
    createdCategory = None
    for p in givenController.categories:
        p = mw(p)
        if p.getCategoryId() == "id1":
            createdCategory = p
            break

    assert createdCategory is not None
    assert createdCategory.getCategoryId() == "id1"
    assert createdCategory.getName() == "Athletics"
    assert createdCategory.getDescription() == "Athletic competitions and sports events"

    assert len(givenController.categories) == 1

@pytest.mark.parametrize(
    "name, description, errorMessage",
    [
        ("" , "Updated sports description", "Name must not be empty."),
        ("Sports" , "", "Description must not be empty.")
    ]
)
def testUpdateCategoryFailInvalidValues(mw, givenController, name, description, errorMessage):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateCategory("id1", "id1", name, description)

    # Assert
    assert str(errorInfo.value) == errorMessage

    assert len(givenController.categories) == 1

    createdCategory = None
    for p in givenController.categories:
        p = mw(p)
        if p.getCategoryId() == "id1":
            createdCategory = p
            break

    assert createdCategory is not None
    assert createdCategory.getCategoryId() == "id1"
    assert createdCategory.getName() == "Sports"
    assert createdCategory.getDescription() == "Sports related events"

@pytest.mark.parametrize(
    "userID",
    [
        ("id2"),
        ("id3")
    ]
)
def testUpdateCategoryFailNotAdmin(mw, givenController, userID):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateCategory(userID, "id1", "Updated Sports", "Updated description")

    # Assert
    assert str(errorInfo.value) == "Only admin users can update categories."

    assert len(givenController.categories) == 1

    createdCategory = None
    for p in givenController.categories:
        p = mw(p)
        if p.getCategoryId() == "id1":
            createdCategory = p
            break

    assert createdCategory is not None
    assert createdCategory.getCategoryId() == "id1"
    assert createdCategory.getName() == "Sports"
    assert createdCategory.getDescription() == "Sports related events"

def testUpdateCategoryFailNonExistentAccount(mw, givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateCategory("id999", "id1", "Updated Sports", "Updated description")

    # Assert
    assert str(errorInfo.value) == "Account with ID id999 does not exist."

    assert len(givenController.categories) == 1

    createdCategory = None
    for p in givenController.categories:
        p = mw(p)
        if p.getCategoryId() == "id1":
            createdCategory = p
            break

    assert createdCategory is not None
    assert createdCategory.getCategoryId() == "id1"
    assert createdCategory.getName() == "Sports"
    assert createdCategory.getDescription() == "Sports related events"

def testUpdateCategoryFailNonExistentCategory(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateCategory("id1", "id999", "NonExistent", "This category does not exist")

    # Assert
    assert str(errorInfo.value) == "Category with ID id999 does not exist."

    assert len(givenController.categories) == 1