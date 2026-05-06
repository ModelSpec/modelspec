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
        from ..ecore.generated_model_layer import Manager, Guest
    controller = AssetPlusController()
    ap = controller.assetPlus
    mgr = mw(Manager, email="manager@ap.com", name="", password="manager", phoneNumber="", assetPlus=ap)
    mw(ap).setManager(mgr.model)
    g1 = mw(Guest, email="jeff@yahoo.com", name="Jeff", password="pass1", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addGuest(g1.model)
    g2 = mw(Guest, email="john@gmail.com", name="John", password="pass2", phoneNumber="(444)444-4444", assetPlus=ap)
    mw(ap).addGuest(g2.model)
    yield controller


@pytest.mark.parametrize(
    "email, expectedCount",
    [
        ("jeff@yahoo.com", 1),
        ("john@gmail.com", 1),
        ("kyle@yahoo.com", 2),
        ("paul@yahoo.com", 2),
    ],
)
def testDeleteGuestSuccess(givenController, mw, email, expectedCount):
    givenController.deleteGuest(email)
    guests = mw(givenController.assetPlus).getGuests()
    assert len(guests) == expectedCount
    assert email not in {g.getEmail() for g in guests}


def testDeleteGuestManagerStillExists(givenController, mw):
    givenController.deleteGuest("manager@ap.com")
    guests = mw(givenController.assetPlus).getGuests()
    assert len(guests) == 2
    assert "manager@ap.com" not in {g.getEmail() for g in guests}

    m = mw(givenController.assetPlus).getManager()
    assert m is not None
    assert m.getEmail() == "manager@ap.com"
