from datetime import datetime
import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global User, PersonalAccount, BusinessAccount
    if modelingTool == "umple":
        from ..umple.controller import FacepageController
        from ..umple.generated_model_layer import User, PersonalAccount, BusinessAccount
        User.usersByUserID.clear()
    else:
        from ..ecore.controller import FacepageController
        from ..ecore.generated_model_layer import User, PersonalAccount, BusinessAccount

    controller = FacepageController()
    mw(User, userID=1, name="John Doe", email="john.doe@mail.com", birthDate=datetime(2000, 1, 1), facepage=controller.facepage)
    yield controller


def testCreatePersonalAccountNewSuccess(givenController, mw):
    givenController.createPersonalAccount(1)

    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    created = u1.getAccount()
    assert created is not None
    assert isinstance(created, PersonalAccount)

    assert created.getUser() == u1

    account_number = created.getAccountNumber()
    assert account_number is not None
    assert str(account_number).strip() != ""

    assert face.numberOfAccounts() == 1


@pytest.mark.parametrize("accountType,companyName", [("BusinessAccount", "company1"), ("PersonalAccount", ""),])
def testCreatePersonalAccountAutoUniqueAccountNumberSuccess(givenController, mw, accountType, companyName):
    u2 = mw(User, userID=2, name="Jane Smith", email="jane.smith@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)

    if accountType == "BusinessAccount":
        a2 = mw(BusinessAccount, accountNumber=2, facepage=givenController.facepage, user=u2.model, companyName=companyName)
    elif accountType == "PersonalAccount":
        a2 = mw(PersonalAccount, accountNumber=2, facepage=givenController.facepage, user=u2.model)
    else:
        raise AssertionError("Unexpected accountType in test parameters")

    a2_number = a2.getAccountNumber()

    givenController.createPersonalAccount(1)

    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    created = u1.getAccount()
    assert created is not None
    assert isinstance(created, PersonalAccount)

    assert created.getUser() == u1
    assert created.getAccountNumber() != a2_number

    assert face.numberOfAccounts() == 2


@pytest.mark.parametrize("accountType,companyName", [("BusinessAccount", "company1"), ("PersonalAccount", ""),])
def testCreatePersonalAccountDuplicateUserIDFail(givenController, mw, accountType, companyName):
    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    if accountType == "BusinessAccount":
        mw(BusinessAccount, accountNumber=1, facepage=givenController.facepage, user=u1.model, companyName=companyName)
    elif accountType == "PersonalAccount":
        mw(PersonalAccount, accountNumber=1, facepage=givenController.facepage, user=u1.model)
    else:
        raise AssertionError("Unexpected accountType in test parameters")

    with pytest.raises(ValueError) as err:
        givenController.createPersonalAccount(1)

    assert str(err.value) == 'A user with the ID "1" already has an account.'
    assert face.numberOfAccounts() == 1

    assert u1.getAccount() is not None
