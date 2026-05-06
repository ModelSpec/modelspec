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
    "email, password, name, phoneNumber",
    [
        ("lisa@gmail.com", "pass4", "Lisa", "(888)888-8888"),
        ("liam@yahoo.com", "pass5", "Liam", "(777)777-7777"),
        ("owen@gmail.com", "pass10", "", "(888)888-5555"),
        ("noah@gmail.com", "pass11", "Noah", ""),
    ],
)
def testRegisterGuestSuccess(givenController, mw, email, password, name, phoneNumber):
    givenController.registerGuest(email, password, name, phoneNumber)
    guests = mw(givenController.assetPlus).getGuests()
    assert len(guests) == 3

    created = None
    for g in guests:
        if g.getEmail() == email:
            created = g
            break

    assert created is not None
    assert created.getEmail() == email
    assert created.getPassword() == password
    assert created.getName() == name
    assert created.getPhoneNumber() == phoneNumber


@pytest.mark.parametrize(
    "email, password, name, phoneNumber, errorMessage",
    [
        ("manager@ap.com", "pass1", "Paul", "(111)111-1111", "Email cannot be manager@ap.com"),
        ("jeff@ap.com", "pass1", "Jeff", "(111)111-1111", "Email domain cannot be @ap.com"),
        ("jeff@gmail.com", "pass2", "Jeff", "(111)777-7777", "Email already linked to a guest account"),
        ("bart @ ap.com", "pass3", "Bart", "(444)666-6666", "Email must not contain any spaces"),
        ("dony@gmail@.com", "pass4", "Dony", "(777)555-7777", "Invalid email"),
        ("kyle@gmail.", "pass5", "Kyle", "(666)777-6666", "Invalid email"),
        ("greg.ap@com", "pass6", "Greg", "(777)888-7777", "Invalid email"),
        ("@gmail.com", "pass7", "Otto", "(111)777-6666", "Invalid email"),
        ("karl@.com", "pass8", "Karl", "(111)777-6661", "Invalid email"),
        ("", "pass9", "Vino", "(777)888-5555", "Email cannot be empty"),
        ("luke@gmail.com", "", "Luke", "(999)888-5555", "Password cannot be empty"),
    ],
)
def testRegisterGuestFail(givenController, mw, email, password, name, phoneNumber, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.registerGuest(email, password, name, phoneNumber)
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
