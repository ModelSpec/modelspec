from datetime import datetime
import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global User, PersonalAccount, BusinessAccount, AdvertisementPage
    if modelingTool == "umple":
        from ..umple.controller import FacepageController
        from ..umple.generated_model_layer import User, PersonalAccount, BusinessAccount, PersonalPage, AdvertisementPage
        User.usersByUserID.clear()
    else:
        from ..ecore.controller import FacepageController
        from ..ecore.generated_model_layer import User, PersonalAccount, BusinessAccount, PersonalPage, AdvertisementPage

    controller = FacepageController()
    u1 = mw(User, userID=1, name="John Doe", email="john.doe@mail.com", birthDate=datetime(2000, 1, 1), facepage=controller.facepage)
    u2 = mw(User, userID=2, name="Jane Smith", email="jane.smith@mail.com", birthDate=datetime(2000, 1, 1), facepage=controller.facepage)
    a1 = mw(PersonalAccount, accountNumber=1, facepage=controller.facepage, user=u1.model)
    mw(PersonalAccount, accountNumber=2, facepage=controller.facepage, user=u2.model)
    mw(PersonalPage, pageName="page", visits=0, facepage=controller.facepage, personalAccount=a1.model)
    yield controller


def testCreatePrivilegeNewSuccess(givenController, mw):
    givenController.createPrivilege("write", "page", 1, 2)

    face = mw(givenController.facepage)
    u1 = None
    u2 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
        elif u.getUserID() == 2:
            u2 = u

    assert u1 is not None and u2 is not None

    a1 = u1.getAccount()
    a2 = u2.getAccount()
    assert a1 is not None and isinstance(a1, PersonalAccount)
    assert a2 is not None and isinstance(a2, PersonalAccount)

    page = None
    for p in a1.getAdministrator():
        if p.getPageName() == "page":
            page = p
            break

    assert page is not None

    created = None
    for pr in a2.getPrivileges():
        if pr.getPersonalAccount() == a2 and pr.getPersonalPage() == page:
            created = pr
            break

    assert created is not None
    assert created.getPersonalAccount() == a2
    assert created.getPersonalPage() == page
    assert created.getTypeOfPrivilege() == "write"

    assert a2.numberOfPrivileges() == 1

    all_privileges = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for pr in acc.getPrivileges():
                all_privileges.add(pr)

    assert len(all_privileges) == 1


@pytest.mark.parametrize(
    "privilegeType,page,pageOwner,targetUser,error",
    [
        ("", "page", 1, 2, "The type of privilege cannot be empty."),
        ("write", "", 1, 1, "Page cannot be empty."),
        ("write", "page", None, 2, "Owner of the page cannot be empty."),
        ("write", "page", 1, None, "Target user cannot be empty."),
        ("write", "page", 3, 1, 'User "3" does not exist.'),
        ("write", "page", 1, 3, 'User "3" does not exist.'),
        ("write", "page2", 1, 1, 'Page "page2" does not exist for user "1".'),
        ("write", "page", 1, 1, "Cannot grant privilege to the owner of the page."),
    ],
)
def testCreatePrivilegeInvalidValuesFail(givenController, mw, privilegeType, page, pageOwner, targetUser, error):
    with pytest.raises(ValueError) as err:
        givenController.createPrivilege(privilegeType, page, pageOwner, targetUser)

    assert str(err.value) == error

    face = mw(givenController.facepage)
    if targetUser is not None:
        target = None
        for u in face.getUsers():
            if u.getUserID() == targetUser:
                target = u
                break
        if target is not None:
            acc = target.getAccount()
            if isinstance(acc, PersonalAccount):
                assert acc.numberOfPrivileges() == 0

    all_privileges = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for pr in acc.getPrivileges():
                all_privileges.add(pr)
    assert len(all_privileges) == 0


def testCreatePrivilegeForBusinessAccountFail(givenController, mw):
    u3 = mw(User, userID=3, name="Bob Johnson", email="bob.johnson@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    mw(BusinessAccount, accountNumber=3, facepage=givenController.facepage, user=u3.model, companyName="company")

    with pytest.raises(ValueError) as err:
        givenController.createPrivilege("write", "page", 1, 3)

    assert str(err.value) == "Cannot grant privilege to a business account."

    face = mw(givenController.facepage)
    all_privileges = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for pr in acc.getPrivileges():
                all_privileges.add(pr)
    assert len(all_privileges) == 0


def testCreatePrivilegeForAdvertisementPageFail(givenController, mw):
    u3 = mw(User, userID=3, name="Bob Johnson", email="bob.johnson@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    b3 = mw(BusinessAccount, accountNumber=3, facepage=givenController.facepage, user=u3.model, companyName="company")
    mw(AdvertisementPage, pageName="page", visits=0, facepage=givenController.facepage, businessAccount=b3.model, bounceRate=0.0, clickThroughRate=0.0, conversionRate=0.0)

    with pytest.raises(ValueError) as err:
        givenController.createPrivilege("write", "page", 3, 1)

    assert str(err.value) == "Cannot grant privilege on an advertisement page."

    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    a1 = u1.getAccount()
    assert a1 is not None and isinstance(a1, PersonalAccount)

    assert a1.numberOfPrivileges() == 0

    all_privileges = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for pr in acc.getPrivileges():
                all_privileges.add(pr)
    assert len(all_privileges) == 0
