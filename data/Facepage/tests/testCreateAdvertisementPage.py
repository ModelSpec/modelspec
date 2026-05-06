from datetime import datetime
import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global User, PersonalAccount, BusinessAccount, AdvertisementPage
    if modelingTool == "umple":
        from ..umple.controller import FacepageController
        from ..umple.generated_model_layer import User, PersonalAccount, BusinessAccount, AdvertisementPage
        User.usersByUserID.clear()
    else:
        from ..ecore.controller import FacepageController
        from ..ecore.generated_model_layer import User, PersonalAccount, BusinessAccount, AdvertisementPage

    controller = FacepageController()
    u1 = mw(User, userID=1, name="John Doe", email="john.doe@mail.com", birthDate=datetime(2000, 1, 1), facepage=controller.facepage)
    mw(BusinessAccount, accountNumber=1, facepage=controller.facepage, user=u1.model, companyName="company")
    yield controller


def testCreateAdvertisementPageNewSuccess(givenController, mw):
    givenController.createAdvertisementPage("page", 1)

    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    a1 = u1.getAccount()
    assert a1 is not None
    assert isinstance(a1, BusinessAccount)

    assert a1.numberOfAdvertisementPages() == 1

    created = None
    for p in a1.getAdvertisementPages():
        if p.getPageName() == "page":
            created = p
            break

    assert created is not None
    assert isinstance(created, AdvertisementPage)
    assert created.getBusinessAccount() == a1

    assert created.getPageName() == "page"
    assert created.getVisits() == 0
    assert created.getBounceRate() == 0.0
    assert created.getClickThroughRate() == 0.0
    assert created.getConversionRate() == 0.0

    assert a1.numberOfAdvertisementPages() == 1
    assert face.numberOfPages() == 1


def testCreateAdvertisementPageSameNameDifferentAccountSuccess(givenController, mw):
    u2 = mw(User, userID=2, name="Jane Smith", email="jane.smith@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    a2 = mw(BusinessAccount, accountNumber=2, facepage=givenController.facepage, user=u2.model, companyName="company2")
    mw(AdvertisementPage, pageName="page", visits=0, facepage=givenController.facepage, businessAccount=a2.model, bounceRate=0.0, clickThroughRate=0.0, conversionRate=0.0)
    givenController.createAdvertisementPage("page", 1)

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
    assert a1 is not None and isinstance(a1, BusinessAccount)
    assert a2 is not None and isinstance(a2, BusinessAccount)

    assert a1.numberOfAdvertisementPages() == 1
    assert a2.numberOfAdvertisementPages() == 1

    created1 = None
    for p in a1.getAdvertisementPages():
        if p.getPageName() == "page":
            created1 = p
            break
    assert created1 is not None
    assert created1.getBusinessAccount() == a1
    assert created1.getPageName() == "page"
    assert created1.getVisits() == 0
    assert created1.getBounceRate() == 0.0
    assert created1.getClickThroughRate() == 0.0
    assert created1.getConversionRate() == 0.0

    created2 = None
    for p in a2.getAdvertisementPages():
        if p.getPageName() == "page":
            created2 = p
            break
    assert created2 is not None
    assert created2.getBusinessAccount() == a2
    assert created2.getPageName() == "page"
    assert created2.getVisits() == 0
    assert created2.getBounceRate() == 0.0
    assert created2.getClickThroughRate() == 0.0
    assert created2.getConversionRate() == 0.0

    assert a1.numberOfAdvertisementPages() == 1
    assert a2.numberOfAdvertisementPages() == 1
    assert face.numberOfPages() == 2


def testCreateAdvertisementPageDuplicateNameFail(givenController, mw):
    face = mw(givenController.facepage)
    u1 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
            break
    assert u1 is not None

    a1 = u1.getAccount()
    assert a1 is not None
    assert isinstance(a1, BusinessAccount)

    mw(AdvertisementPage, pageName="page", visits=0, facepage=givenController.facepage, businessAccount=a1.model, bounceRate=0.0, clickThroughRate=0.0, conversionRate=0.0)

    with pytest.raises(ValueError) as err:
        givenController.createAdvertisementPage("page", 1)

    assert str(err.value) == 'A page with the name "page" already exists.'

    assert a1.numberOfAdvertisementPages() == 1
    assert face.numberOfPages() == 1

    existing = None
    for p in a1.getAdvertisementPages():
        if p.getPageName() == "page":
            existing = p
            break

    assert existing is not None
    assert existing.getPageName() == "page"
    assert existing.getVisits() == 0
    assert existing.getBounceRate() == 0.0
    assert existing.getClickThroughRate() == 0.0
    assert existing.getConversionRate() == 0.0


def testCreateAdvertisementPageInvalidPageNameFail(givenController, mw):
    with pytest.raises(ValueError) as err:
        givenController.createAdvertisementPage("", 1)

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
    assert isinstance(a1, BusinessAccount)

    assert a1.numberOfAdvertisementPages() == 0
    assert face.numberOfPages() == 0


def testCreateAdvertisementPageWithPersonalAccountFail(givenController, mw):
    u2 = mw(User, userID=2, name="Jane Smith", email="jane.smith@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    mw(PersonalAccount, accountNumber=2, facepage=givenController.facepage, user=u2.model)

    with pytest.raises(ValueError) as err:
        givenController.createAdvertisementPage("page", 2)

    assert str(err.value) == "Only business accounts can create advertisement pages."

    face = mw(givenController.facepage)
    u2 = None
    for u in face.getUsers():
        if u.getUserID() == 2:
            u2 = u
            break
    assert u2 is not None

    a2 = u2.getAccount()
    assert a2 is not None
    assert isinstance(a2, PersonalAccount)

    assert a2.numberOfAdministrator() == 0
    assert face.numberOfPages() == 0
