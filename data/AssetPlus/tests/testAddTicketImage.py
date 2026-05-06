import pytest
from datetime import datetime


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
        from ..ecore.generated_model_layer import Manager, Employee, AssetType, SpecificAsset, MaintenanceTicket, TicketImage
    controller = AssetPlusController()
    ap = controller.assetPlus
    mgr = mw(Manager, email="manager@ap.com", name="", password="manager", phoneNumber="", assetPlus=ap)
    mw(ap).setManager(mgr.model)
    empJeff = mw(Employee, email="jeff@ap.com", name="Jeff", password="pass1", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addEmployee(empJeff.model)
    smith = mw(Employee, email="smith@ap.com", name="Smith", password="pass2", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addEmployee(smith.model)
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
    img1 = mw(TicketImage, imageURL="https://imageurl.com/i.jpg", ticket=t1.model)
    mw(t1.model).addTicketImage(img1.model)
    img2 = mw(TicketImage, imageURL="http://thisimage.com/1.png", ticket=t1.model)
    mw(t1.model).addTicketImage(img2.model)
    yield controller


@pytest.mark.parametrize(
    "imageUrl, ticketId, numberOfImagesOfTicket",
    [
        ("https://imageurl.com/j.jpg", 1, 3),
        ("http://thisimage.com/2.png", 2, 1),
    ],
)
def testAddTicketImageSuccess(givenController, mw, imageUrl, ticketId, numberOfImagesOfTicket):
    givenController.addTicketImage(ticketId, imageUrl)
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()
    totalImages = 0
    for t in tickets:
        totalImages += len(t.getTicketImages())
    assert totalImages == 3

    ticket = None
    for t in tickets:
        if t.getId() == ticketId:
            ticket = t
            break
    assert ticket is not None
    assert len(ticket.getTicketImages()) == numberOfImagesOfTicket

    found = False
    for img in ticket.getTicketImages():
        if img.getImageURL() == imageUrl:
            found = True
            break
    assert found is True


@pytest.mark.parametrize(
    "imageUrl, ticketId, numberOfImagesOfTicket",
    [
        ("http://thisimage.com/1.png", 2, 1),
    ],
)
def testAddSameTicketImageToSecondTicketSuccess(givenController, mw, imageUrl, ticketId, numberOfImagesOfTicket):
    givenController.addTicketImage(ticketId, imageUrl)
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()
    totalImages = 0
    for t in tickets:
        totalImages += len(t.getTicketImages())
    assert totalImages == 3

    ticket = None
    for t in tickets:
        if t.getId() == ticketId:
            ticket = t
            break
    assert ticket is not None
    assert len(ticket.getTicketImages()) == numberOfImagesOfTicket

    found = False
    for img in ticket.getTicketImages():
        if img.getImageURL() == imageUrl:
            found = True
            break
    assert found is True


@pytest.mark.parametrize(
    "imageUrl, ticketId, errorMessage",
    [
        ("thisisnotanurl", 1, "Image URL must start with http:// or https://"),
        ("htps://image.com/3.png", 2, "Image URL must start with http:// or https://"),
        ("", 2, "Image URL cannot be empty"),
        ("http://thisimage.com/3.png", 3, "Ticket does not exist"),
        ("https://imageurl.com/i.jpg", 1, "Image already exists for the ticket"),
    ],
)
def testAddTicketImageFail(givenController, mw, imageUrl, ticketId, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.addTicketImage(ticketId, imageUrl)

    assert str(errorInfo.value) == errorMessage

    tickets = mw(givenController.assetPlus).getMaintenanceTickets()
    totalImages = 0
    for t in tickets:
        totalImages += len(t.getTicketImages())
    assert totalImages == 2

    t1 = None
    t2 = None
    for t in tickets:
        if t.getId() == 1:
            t1 = t
        if t.getId() == 2:
            t2 = t
    assert t1 is not None
    assert t2 is not None

    urlsT1 = [img.getImageURL() for img in t1.getTicketImages()]
    assert urlsT1 == ["https://imageurl.com/i.jpg", "http://thisimage.com/1.png"]
    assert len(t2.getTicketImages()) == 0
