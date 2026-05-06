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
    img3 = mw(TicketImage, imageURL="http://thisimage.com/2.png", ticket=t2.model)
    mw(t2.model).addTicketImage(img3.model)
    yield controller


@pytest.mark.parametrize(
    "ticketId, imageURL, numberOfImagesOfTicket",
    [
        (1, "http://thisimage.com/1.png", 1),
        (2, "http://thisimage.com/2.png", 0),
    ],
)
def testDeleteTicketImageSuccess(givenController, mw, ticketId, imageURL, numberOfImagesOfTicket):
    givenController.deleteTicketImage(ticketId, imageURL)
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()

    totalImages = 0
    for t in tickets:
        totalImages += len(t.getTicketImages())
    assert totalImages == 2

    target = None
    for t in tickets:
        if t.getId() == ticketId:
            target = t
            break
    assert target is not None

    assert len(target.getTicketImages()) == numberOfImagesOfTicket

    for img in target.getTicketImages():
        assert img.getImageURL() != imageURL


@pytest.mark.parametrize(
    "ticketId, imageURL, numberOfImagesOfTicket",
    [
        (1, "http://thisimage.com/0.png", 2),
        (2, "http://thisimage.com/0.png", 1),
    ],
)
def testDeleteNonExistingTicketImageSuccess(givenController, mw, ticketId, imageURL, numberOfImagesOfTicket):
    givenController.deleteTicketImage(ticketId, imageURL)
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()

    totalImages = 0
    for t in tickets:
        totalImages += len(t.getTicketImages())
    assert totalImages == 3

    target = None
    for t in tickets:
        if t.getId() == ticketId:
            target = t
            break
    assert target is not None

    assert len(target.getTicketImages()) == numberOfImagesOfTicket

    for img in target.getTicketImages():
        assert img.getImageURL() != imageURL


def testDeleteTicketImageForNonExistingTicketSuccess(givenController, mw):
    givenController.deleteTicketImage(3, "http://thisimage.com/1.png")
    tickets = mw(givenController.assetPlus).getMaintenanceTickets()

    totalImages = 0
    for t in tickets:
        totalImages += len(t.getTicketImages())
    assert totalImages == 3
