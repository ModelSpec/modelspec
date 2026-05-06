import pytest

@pytest.fixture
def givenController(modelingTool, mw):
    global Participant, Organizer
    if modelingTool == "umple":
        from ..umple.controller import LocalLoopController
        from ..umple.generated_model_layer import Participant, UserAccount, Organizer
    else:
        from ..ecore.controller import LocalLoopController
        from ..ecore.generated_model_layer import Participant, UserAccount, Organizer

    controller = LocalLoopController()

    participant = mw(Participant())
    account = mw(UserAccount, userID="id1", firstName="John", lastName="Doe", username="johndoe", email="john@example.com", phoneNumber="555-0100", role=participant.model, adminViewModel=controller.adminViewModel)
    controller.accounts.append(account.model)

    yield controller

@pytest.mark.parametrize(
    "firstName, lastName, username, email, phoneNumber, password, confirmPassword, isOrganizer, companyName",
    [
        ("Alice", "Johnson", "alicej", "alice@example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, ""),
        ("Bob", "Williams", "bobw", "bob@example.com", "", "Pass$123", "Pass$123", False, ""),
        ("Charlie", "Brown", "charlieb", "charlie@example.com", "555-0400", "Secure#45", "Secure#45", True, "BrownEvents Inc."),
        ("Diana", "Lee", "dianalee", "diana@example.com", "", "MyP@ss99", "MyP@ss99", True, "Lee Organizers"),
    ]
)
def testCreateNewAccountSuccess(mw, givenController, firstName, lastName, username, email, phoneNumber, password, confirmPassword, isOrganizer, companyName):
    # Act
    givenController.createAccount(firstName, lastName, username, email, phoneNumber, password, confirmPassword, isOrganizer, companyName)

    # Assert
    createdPerson = None
    for p in givenController.accounts:
        p = mw(p)
        if p.getUsername() == username:
            createdPerson = p
            break

    assert createdPerson is not None
    assert createdPerson.getUserID()
    assert createdPerson.getUserID() != "id1"
    assert createdPerson.getFirstName() == firstName
    assert createdPerson.getLastName() == lastName
    assert createdPerson.getUsername() == username
    assert createdPerson.getEmail() == email
    assert createdPerson.getPhoneNumber() == phoneNumber

    role = createdPerson.getRole()
    if isOrganizer:
        assert role is not None
        assert isinstance(role, Organizer)
        assert role.getCompanyName() == companyName
    else:
        assert isinstance(role, Participant)

    assert len(givenController.accounts) == 2

@pytest.mark.parametrize(
    "firstName, lastName, username, email, phoneNumber, password, confirmPassword, isOrganizer, companyName, errorMessage",
    [
        ("" , "Johnson", "alicej", "alice@example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "First name must not be empty."),
        ("Alice" , "", "alicej", "alice@example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Last name must not be empty."),
        ("Alice" , "Johnson", "", "alice@example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Username must not be empty."),
        ("Alice" , "Johnson", "alicej", "", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Email must not be empty."),
        ("Alice" , "Johnson", "alicej", "alice.example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Email must contain @ symbol."),
        ("Alice" , "Johnson", "alicej", "@example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Email must have characters before @."),
        ("Alice" , "Johnson", "alicej", "alice@", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Email must contain a dot after @."),
        ("Alice" , "Johnson", "alicej", "alice@example", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Email must contain a dot after @."),
        ("Alice" , "Johnson", "alicej", "alice@example.", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Email must have characters after dot."),
        ("Alice" , "Johnson", "alicej", "alice @example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "Email must not contain spaces."),
        ("Alice" , "Johnson", "alicej", "john@example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "The email already exists."),
        ("Alice" , "Johnson", "johndoe", "alice@example.com", "555-0300", "P@ssw0rd1", "P@ssw0rd1", False, "", "The username already exists."),
        ("Alice" , "Johnson", "alicej", "alice@example.com", "555-0300", "", "P@ssw0rd1", False, "", "Password must not be empty."),
        ("Alice" , "Johnson", "alicej", "alice@example.com", "555-0300", "P@ssw0rd1", "", False, "", "Confirm password must not be empty."),
        ("Alice" , "Johnson", "alicej", "alice@example.com", "555-0300", "P@ssw0rd1", "DifferentPass", False, "", "Passwords must match."),
        ("Charlie" , "Brown", "charlieb", "charlie@example.com", "555-0400", "Secure#45", "Secure#45", True, "", "Company name must be provided for organizers."),
    ]
)
def testCreateNewAccountFail(givenController, firstName, lastName, username, email, phoneNumber, password, confirmPassword, isOrganizer, companyName, errorMessage):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createAccount(firstName, lastName, username, email, phoneNumber, password, confirmPassword, isOrganizer, companyName)

    # Assert
    assert str(errorInfo.value) == errorMessage

    assert len(givenController.accounts) == 1