import pytest
from datetime import datetime


@pytest.fixture
def controllerWithManager(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, Manager
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Manager

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Manager, email="manager@btp.com", password="manager", bikeTourPlus=controller.btp)

    yield controller


@pytest.mark.parametrize("password", [
    ("P!p1"),
    ("p#2P"),
    ("$aA3"),
])
def testUpdateManagerSuccess(controllerWithManager, mw, password):
    controllerWithManager.updateManager(password)

    btp = mw(controllerWithManager.btp)
    manager = btp.getManager()
    assert manager is not None
    assert manager.getPassword() == password
    assert btp.hasManager()


@pytest.mark.parametrize("password, error", [
    ("P!p", "Password must be at least four characters long"),
    ("p2P2", "Password must contain one character out of !#$"),
    ("", "Password cannot be empty"),
    ("!2P2", "Password must contain one lower-case character"),
    ("!2p2", "Password must contain one upper-case character"),
])
def testUpdateManagerUnsuccessful(controllerWithManager, mw, password, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithManager.updateManager(password)

    assert str(error_info.value) == error

    btp = mw(controllerWithManager.btp)
    manager = btp.getManager()
    assert manager is not None
    assert manager.getPassword() == "manager"
    assert btp.hasManager()
