import pytest
from datetime import date, datetime


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
        from ..ecore.generated_model_layer import Manager, Employee, Guest, AssetType, SpecificAsset, MaintenanceTicket
    controller = AssetPlusController()
    ap = controller.assetPlus
    mgr = mw(Manager, email="manager@ap.com", name="", password="manager", phoneNumber="", assetPlus=ap)
    mw(ap).setManager(mgr.model)
    smith = mw(Employee, email="smith@ap.com", name="Smith", password="pass2", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addEmployee(smith.model)
    empJeff = mw(Employee, email="jeff@ap.com", name="Jeff", password="pass1", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addEmployee(empJeff.model)
    g1 = mw(Guest, email="jeff@gmail.com", name="Jeff", password="pass1", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addGuest(g1.model)
    g2 = mw(Guest, email="john@gmail.com", name="John", password="pass2", phoneNumber="(444)444-4444", assetPlus=ap)
    mw(ap).addGuest(g2.model)
    atLamp = mw(AssetType, name="lamp", expectedLifeSpan=1800, assetPlus=ap)
    mw(ap).addAssetType(atLamp.model)
    atBed = mw(AssetType, name="bed", expectedLifeSpan=5000, assetPlus=ap)
    mw(ap).addAssetType(atBed.model)
    sa1 = mw(SpecificAsset, assetNumber=1, floorNumber=9, roomNumber=23, purchaseDate=datetime(2022, 3, 20), assetType=atLamp.model, assetPlus=ap)
    mw(ap).addSpecificAsset(sa1.model)
    sa2 = mw(SpecificAsset, assetNumber=2, floorNumber=10, roomNumber=35, purchaseDate=datetime(2010, 1, 30), assetType=atBed.model, assetPlus=ap)
    mw(ap).addSpecificAsset(sa2.model)
    t1 = mw(MaintenanceTicket, id=1, raisedOnDate=datetime(2023, 7, 20), description="This is a dummy description 1", ticketRaiser=mgr.model, assetPlus=ap)
    mw(ap).addMaintenanceTicket(t1.model)
    t1.setAsset(sa2.model)
    t2 = mw(MaintenanceTicket, id=2, raisedOnDate=datetime(2023, 7, 10), description="This is a dummy description 2", ticketRaiser=smith.model, assetPlus=ap)
    mw(ap).addMaintenanceTicket(t2.model)
    t2.setAsset(sa1.model)
    yield controller


@pytest.mark.parametrize(
    "id_, ticketRaiser, raisedOnDate, description, assetNumber",
    [
        (3, "john@gmail.com", date(2023, 9, 23), "This is a dummy description 3", 2),
        (4, "smith@ap.com", date(2023, 10, 5), "This is a dummy description 2", 1),
        (3, "manager@ap.com", date(2023, 9, 23), "This is a dummy description 1", 1),
    ],
)
def testAddMaintenanceTicketWithAssetSuccess(givenController, mw, id_, ticketRaiser, raisedOnDate, description, assetNumber):
    givenController.addMaintenanceTicket(id_, ticketRaiser, raisedOnDate, description, assetNumber)
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()
    assert len(tickets) == 3
    created = None
    for t in tickets:
        if t.getId() == id_:
            created = t
            break
    assert created is not None
    d = created.getRaisedOnDate()
    assert d.year == raisedOnDate.year
    assert d.month == raisedOnDate.month
    assert d.day == raisedOnDate.day
    assert created.getDescription() == description
    raiser = created.getTicketRaiser()
    assert raiser is not None
    assert raiser.getEmail() == ticketRaiser
    a = created.getAsset()
    assert a is not None
    assert a.getAssetNumber() == assetNumber


@pytest.mark.parametrize(
    "id_, ticketRaiser, raisedOnDate, description",
    [
        (3, "john@gmail.com", date(2023, 9, 23), "it is noisy"),
        (4, "smith@ap.com", date(2023, 10, 5), "it smells"),
        (3, "manager@ap.com", date(2023, 9, 23), "it smells and it is noisy"),
    ],
)
def testAddMaintenanceTicketWithoutAssetSuccess(givenController, mw, id_, ticketRaiser, raisedOnDate, description):
    givenController.addMaintenanceTicket(id_, ticketRaiser, raisedOnDate, description, None)
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()
    assert len(tickets) == 3
    created = None
    for t in tickets:
        if t.getId() == id_:
            created = t
            break
    assert created is not None
    d = created.getRaisedOnDate()
    assert d.year == raisedOnDate.year
    assert d.month == raisedOnDate.month
    assert d.day == raisedOnDate.day
    assert created.getDescription() == description
    raiser = created.getTicketRaiser()
    assert raiser is not None
    assert raiser.getEmail() == ticketRaiser
    assert created.getAsset() is None


@pytest.mark.parametrize(
    "id_, ticketRaiser, raisedOnDate, description, assetNumber, errorMessage",
    [
        (2, "smith@ap.com", date(2023, 9, 23), "This is a dummy description 1", 2, "Ticket id already exists"),
        (3, "manager@ap.com", date(2023, 9, 23), "This is a dummy description 1", 3, "The asset does not exist"),
        (3, "none@ap.com", date(2023, 9, 23), "This is a dummy description 1", 1, "The ticket raiser does not exist"),
        (3, "smith@ap.com", date(2023, 9, 23), "", 1, "Ticket description cannot be empty"),
    ],
)
def testAddMaintenanceTicketInvalidValuesFail(givenController, mw, id_, ticketRaiser, raisedOnDate, description, assetNumber, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.addMaintenanceTicket(id_, ticketRaiser, raisedOnDate, description, assetNumber)
    assert str(errorInfo.value) == errorMessage
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()
    assert len(tickets) == 2
    byId = {t.getId(): t for t in tickets}
    assert set(byId.keys()) == {1, 2}
    t1 = byId[1]
    assert t1.getTicketRaiser().getEmail() == "manager@ap.com"
    d1 = t1.getRaisedOnDate()
    assert d1.year == 2023
    assert d1.month == 7
    assert d1.day == 20
    assert t1.getDescription() == "This is a dummy description 1"
    asset1 = t1.getAsset()
    assert asset1 is not None
    assert asset1.getAssetNumber() == 2
    t2 = byId[2]
    assert t2.getTicketRaiser().getEmail() == "smith@ap.com"
    d2 = t2.getRaisedOnDate()
    assert d2.year == 2023
    assert d2.month == 7
    assert d2.day == 10
    assert t2.getDescription() == "This is a dummy description 2"
    asset2 = t2.getAsset()
    assert asset2 is not None
    assert asset2.getAssetNumber() == 1
