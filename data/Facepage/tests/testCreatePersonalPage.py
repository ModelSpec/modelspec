from datetime import datetime
import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global User, PersonalAccount, BusinessAccount, PersonalPage
    if modelingTool == "umple":
        from ..umple.controller import FacepageController
        from ..umple.generated_model_layer import User, PersonalAccount, BusinessAccount, PersonalPage
        User.usersByUserID.clear()
    else:
        from ..ecore.controller import FacepageController
        from ..ecore.generated_model_layer import User, PersonalAccount, BusinessAccount, PersonalPage

    controller = FacepageController()
    u1 = mw(User, userID=1, name="John Doe", email="john.doe@mail.com", birthDate=datetime(2000, 1, 1), facepage=controller.facepage)
    mw(PersonalAccount, accountNumber=1, facepage=controller.facepage, user=u1.model)
    yield controller


def testCreatePersonalPageNewSuccess(givenController, mw):
    givenController.createPersonalPage("page", 1)

    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    a1 = u1.getAccount()
    assert a1 is not None
    assert isinstance(a1, PersonalAccount)

    created = None
    for p in a1.getAdministrator():
        if p.getPageName() == "page":
            created = p
            break

    assert created is not None
    assert isinstance(created, PersonalPage)
    assert created.getPersonalAccount() == a1

    assert created.getPageName() == "page"
    assert created.getVisits() == 0

    assert a1.numberOfAdministrator() == 1
    assert face.numberOfPages() == 1


def testCreatePersonalPageSameNameDifferentAccountSuccess(givenController, mw):
    u2 = mw(User, userID=2, name="Jane Smith", email="jane.smith@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    a2 = mw(PersonalAccount, accountNumber=2, facepage=givenController.facepage, user=u2.model)
    mw(PersonalPage, pageName="page", visits=0, facepage=givenController.facepage, personalAccount=a2.model)
    givenController.createPersonalPage("page", 1)

    face = mw(givenController.facepage)
    u1 = None
    u2 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
        if u.getUserID() == 2:
            u2 = u
    assert u1 is not None and u2 is not None

    a1 = u1.getAccount()
    a2 = u2.getAccount()
    assert a1 is not None and isinstance(a1, PersonalAccount)
    assert a2 is not None and isinstance(a2, PersonalAccount)

    created1 = None
    for p in a1.getAdministrator():
        if p.getPageName() == "page":
            created1 = p
            break
    assert created1 is not None
    assert created1.getPersonalAccount() == a1
    assert created1.getPageName() == "page"
    assert created1.getVisits() == 0

    created2 = None
    for p in a2.getAdministrator():
        if p.getPageName() == "page":
            created2 = p
            break
    assert created2 is not None
    assert created2.getPersonalAccount() == a2
    assert created2.getPageName() == "page"
    assert created2.getVisits() == 0

    assert a1.numberOfAdministrator() == 1
    assert a2.numberOfAdministrator() == 1
    assert face.numberOfPages() == 2


def testCreatePersonalPageDuplicateNameFail(givenController, mw):
    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    a1 = u1.getAccount()
    assert a1 is not None
    assert isinstance(a1, PersonalAccount)

    mw(PersonalPage, pageName="page", visits=0, facepage=givenController.facepage, personalAccount=a1.model)

    with pytest.raises(ValueError) as err:
        givenController.createPersonalPage("page", 1)

    assert str(err.value) == 'A page with the name "page" already exists.'

    assert a1.numberOfAdministrator() == 1
    assert face.numberOfPages() == 1

    existing = None
    for p in a1.getAdministrator():
        if p.getPageName() == "page":
            existing = p
            break

    assert existing is not None
    assert existing.getPageName() == "page"
    assert existing.getVisits() == 0


def testCreatePersonalPageInvalidPageNameFail(givenController, mw):
    with pytest.raises(ValueError) as err:
        givenController.createPersonalPage("", 1)

    assert str(err.value) == "The page name cannot be empty."

    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    a1 = u1.getAccount()
    assert a1 is not None
    assert isinstance(a1, PersonalAccount)

    assert a1.numberOfAdministrator() == 0
    assert face.numberOfPages() == 0


def testCreatePersonalPageWithBusinessAccountFail(givenController, mw):
    u2 = mw(User, userID=2, name="Jane Smith", email="jane.smith@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    mw(BusinessAccount, accountNumber=2, facepage=givenController.facepage, user=u2.model, companyName="company")

    with pytest.raises(ValueError) as err:
        givenController.createPersonalPage("page", 2)

    assert str(err.value) == "Only personal accounts can create personal pages."

    face = mw(givenController.facepage)
    u2 = None
    for u in face.getUsers():
        if u.getUserID() == 2:
            u2 = u
            break
    assert u2 is not None

    b2 = u2.getAccount()
    assert b2 is not None
    assert isinstance(b2, BusinessAccount)

    assert b2.numberOfAdvertisementPages() == 0
    assert face.numberOfPages() == 0
