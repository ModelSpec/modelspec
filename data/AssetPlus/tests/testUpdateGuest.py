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
    g1 = mw(Guest, email="jeff@gmail.com", name="Jeff", password="pass1", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addGuest(g1.model)
    g2 = mw(Guest, email="john@gmail.com", name="John", password="pass2", phoneNumber="(444)444-4444", assetPlus=ap)
    mw(ap).addGuest(g2.model)
    yield controller


@pytest.mark.parametrize(
    "email, newPassword, newName, newPhoneNumber",
    [
        ("jeff@gmail.com", "pass5", "Jake", "(111)111-1111"),
        ("john@gmail.com", "pass6", "Johnny", "(111)777-7777"),
        ("john@gmail.com", "pass2", "", "(444)444-7777"),
        ("john@gmail.com", "pass2", "Jon", ""),
    ],
)
def testUpdateGuestSuccess(givenController, mw, email, newPassword, newName, newPhoneNumber):
    givenController.updateGuest(email, newPassword, newName, newPhoneNumber)
    guests = mw(givenController.assetPlus).getGuests()
    assert len(guests) == 2

    updated = None
    for g in guests:
        if g.getEmail() == email:
            updated = g
            break

    assert updated is not None
    assert updated.getEmail() == email
    assert updated.getPassword() == newPassword
    assert updated.getName() == newName
    assert updated.getPhoneNumber() == newPhoneNumber


@pytest.mark.parametrize(
    "email, newPassword, newName, newPhoneNumber, errorMessage",
    [
        ("jeff@gmail.com", "", "Jeff", "(555)666-5555", "Password cannot be empty"),
    ],
)
def testUpdateGuestFail(givenController, mw, email, newPassword, newName, newPhoneNumber, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateGuest(email, newPassword, newName, newPhoneNumber)
    assert str(errorInfo.value) == errorMessage

    guests = mw(givenController.assetPlus).getGuests()
    assert len(guests) == 2

    byEmail = {g.getEmail(): g for g in guests}
    assert set(byEmail.keys()) == {"jeff@gmail.com", "john@gmail.com"}

    g1 = byEmail["jeff@gmail.com"]
    assert g1.getPassword() == "pass1"
    assert g1.getName() == "Jeff"
    assert g1.getPhoneNumber() == "(555)555-5555"

    g2 = byEmail["john@gmail.com"]
    assert g2.getPassword() == "pass2"
    assert g2.getName() == "John"
    assert g2.getPhoneNumber() == "(444)444-4444"
