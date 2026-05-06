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

def testCreateNewCategorySuccess(mw, givenController):
    # Act
    givenController.createCategory("id1", "Music", "Music concerts and performances")

    # Assert
    createdCategory = None
    for c in givenController.categories:
        c = mw(c)
        if c.getName() == "Music":
            createdCategory = c
            break

    assert createdCategory is not None
    assert createdCategory.getCategoryId()
    assert createdCategory.getCategoryId() != "id1"
    assert createdCategory.getName() == "Music"
    assert createdCategory.getDescription() == "Music concerts and performances"

    assert len(givenController.categories) == 2

@pytest.mark.parametrize(
    "name, description, errorMessage",
    [
        ("" , "Music concerts and performances", "Name must not be empty."),
        ("Music" , "", "Description must not be empty."),
    ]
)
def testCreateNewCategoryFailInvalidValues(givenController, name, description, errorMessage):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createCategory("id1", name, description)

    # Assert
    assert str(errorInfo.value) == errorMessage

    assert len(givenController.categories) == 1

@pytest.mark.parametrize(
    "userID",
    [
        ("id2"),
        ("id3"),
    ]
)
def testCreateNewCategoryFailNotAdmin(givenController, userID):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createCategory(userID, "Music", "Music concerts and performances")

    # Assert
    assert str(errorInfo.value) == "Only admin users can update categories."

    assert len(givenController.categories) == 1