import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller.controller import AssetPlusController
        from ..umple.generated_model_layer import (
            User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, TicketImage
        )
        uniqueKeywords = ["byemail", "byname", "byid", "byassetnumber", "byimageurl"]
        for cls in [User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, TicketImage]:
            for attr in dir(cls):
                name = attr.lower()
                if any(k in name for k in uniqueKeywords):
                    mapping = getattr(cls, attr)
                    if isinstance(mapping, dict):
                        mapping.clear()
    else:
        from ..ecore.controller.controller import AssetPlusController
        from ..ecore.generated_model_layer import Manager
    controller = AssetPlusController()
    ap = controller.assetPlus
    mgr = mw(Manager, email="manager@ap.com", name="", password="manager", phoneNumber="", assetPlus=ap)
    mw(ap).setManager(mgr.model)
    yield controller


@pytest.mark.parametrize(
    "email, newPassword",
    [
        ("manager@ap.com", "P!p1"),
        ("manager@ap.com", "p#2P"),
        ("manager@ap.com", "$aA3"),
    ],
)
def testUpdateManagerSuccess(givenController, mw, email, newPassword):
    givenController.updateManager(email, newPassword)
    m = mw(givenController.assetPlus).getManager()
    assert m is not None
    assert m.getEmail() == email
    assert m.getPassword() == newPassword
    assert mw(givenController.assetPlus).getManager() is not None


@pytest.mark.parametrize(
    "email, newPassword, errorMessage",
    [
        ("manager@ap.com", "P!p", "Password must be at least four characters long"),
        ("manager@ap.com", "p2P2", "Password must contain one character out of !#$"),
        ("manager@ap.com", "", "Password cannot be empty"),
        ("manager@ap.com", "!2P2", "Password must contain one lower-case character"),
        ("manager@ap.com", "!2p2", "Password must contain one upper-case character"),
    ],
)
def testUpdateManagerFail(givenController, mw, email, newPassword, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateManager(email, newPassword)
    assert str(errorInfo.value) == errorMessage

    m = mw(givenController.assetPlus).getManager()
    assert m is not None
    assert m.getEmail() == "manager@ap.com"
    assert m.getPassword() == "manager"
    assert mw(givenController.assetPlus).getManager() is not None
