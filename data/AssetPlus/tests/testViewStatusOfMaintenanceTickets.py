from datetime import datetime
import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller.controller import AssetPlusController
        from ..umple.generated_model_layer import (
            User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, MaintenanceNote, TicketImage
        )
        uniqueKeywords = ["byemail", "byname", "byid", "byassetnumber", "byimageurl"]
        for cls in [User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, MaintenanceNote, TicketImage]:
            for attr in dir(cls):
                name = attr.lower()
                if any(k in name for k in uniqueKeywords):
                    mapping = getattr(cls, attr)
                    if isinstance(mapping, dict):
                        mapping.clear()
    else:
        from ..ecore.controller.controller import AssetPlusController
        from ..ecore.generated_model_layer import Manager, Employee, AssetType, SpecificAsset, MaintenanceTicket, MaintenanceNote, TicketImage
    controller = AssetPlusController()
    ap = controller.assetPlus
    mgr = mw(Manager, email="manager@ap.com", name="", password="manager", phoneNumber="", assetPlus=ap)
    mw(ap).setManager(mgr.model)
    jeff = mw(Employee, email="jeff@ap.com", name="Jeff", password="pass1", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addEmployee(jeff.model)
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
    sa3 = mw(SpecificAsset, assetNumber=3, floorNumber=1, roomNumber=35, purchaseDate=datetime(2010, 1, 30), assetType=atBed.model, assetPlus=ap)
    mw(ap).addSpecificAsset(sa3.model)
    t1 = mw(MaintenanceTicket, id=1, raisedOnDate=datetime(2023, 7, 20), description="This is a dummy description 1", ticketRaiser=mgr.model, assetPlus=ap)
    mw(ap).addMaintenanceTicket(t1.model)
    t1.setAsset(sa2.model)
    t2 = mw(MaintenanceTicket, id=2, raisedOnDate=datetime(2023, 7, 10), description="This is a dummy description 2", ticketRaiser=smith.model, assetPlus=ap)
    mw(ap).addMaintenanceTicket(t2.model)
    t2.setAsset(sa1.model)
    t3 = mw(MaintenanceTicket, id=3, raisedOnDate=datetime(2023, 7, 20), description="It is noisy", ticketRaiser=mgr.model, assetPlus=ap)
    mw(ap).addMaintenanceTicket(t3.model)
    note1a = mw(MaintenanceNote, date=datetime(2023, 9, 10), description="This is another dummy note 2 for a ticket", noteTaker=smith.model, ticket=t1.model)
    mw(t1.model).addTicketNote(note1a.model)
    note1b = mw(MaintenanceNote, date=datetime(2023, 9, 23), description="This is a dummy description 1", noteTaker=mgr.model, ticket=t1.model)
    mw(t1.model).addTicketNote(note1b.model)
    note2 = mw(MaintenanceNote, date=datetime(2023, 9, 1), description="This is a dummy note 1 for a ticket", noteTaker=jeff.model, ticket=t2.model)
    mw(t2.model).addTicketNote(note2.model)
    img1 = mw(TicketImage, imageURL="https://imageurl.com/i.jpg", ticket=t1.model)
    mw(t1.model).addTicketImage(img1.model)
    img2 = mw(TicketImage, imageURL="http://thisimage.com/1.png", ticket=t1.model)
    mw(t1.model).addTicketImage(img2.model)
    img3 = mw(TicketImage, imageURL="http://thisimage.com/2.png", ticket=t2.model)
    mw(t2.model).addTicketImage(img3.model)
    yield controller


def testViewStatusOfMaintenanceTicketsSuccess(givenController, mw):
    result = givenController.viewStatusOfMaintenanceTickets()
    assert result is not None
    assert len(result) == 3
    ticketsById = {mw(t).getId(): t for t in result}
    assert set(ticketsById.keys()) == {1, 2, 3}

    t1 = ticketsById[1]
    assert mw(t1).getRaisedByEmail() == "manager@ap.com"
    d1 = mw(t1).getRaisedOnDate()
    assert d1.year == 2023
    assert d1.month == 7
    assert d1.day == 20
    assert mw(t1).getDescription() == "This is a dummy description 1"
    assert mw(t1).getAssetName() == "bed"
    assert mw(t1).getExpectedLifeSpanInDays() == 5000
    pd1 = mw(t1).getPurchaseDate()
    assert pd1.year == 2010
    assert pd1.month == 1
    assert pd1.day == 30
    assert mw(t1).getFloorNumber() == 10
    assert mw(t1).getRoomNumber() == 35
    assert mw(t1).getNoteTakerEmails() == ["smith@ap.com", "manager@ap.com"]
    noteDates1 = mw(t1).getNoteDates()
    assert len(noteDates1) == 2
    assert noteDates1[0].year == 2023
    assert noteDates1[0].month == 9
    assert noteDates1[0].day == 10
    assert noteDates1[1].year == 2023
    assert noteDates1[1].month == 9
    assert noteDates1[1].day == 23
    assert mw(t1).getNoteDescriptions() == ["This is another dummy note 2 for a ticket", "This is a dummy description 1"]
    assert mw(t1).getImageURLs() == ["https://imageurl.com/i.jpg", "http://thisimage.com/1.png"]

    t2 = ticketsById[2]
    assert mw(t2).getRaisedByEmail() == "smith@ap.com"
    d2 = mw(t2).getRaisedOnDate()
    assert d2.year == 2023
    assert d2.month == 7
    assert d2.day == 10
    assert mw(t2).getDescription() == "This is a dummy description 2"
    assert mw(t2).getAssetName() == "lamp"
    assert mw(t2).getExpectedLifeSpanInDays() == 1800
    pd2 = mw(t2).getPurchaseDate()
    assert pd2.year == 2022
    assert pd2.month == 3
    assert pd2.day == 20
    assert mw(t2).getFloorNumber() == 9
    assert mw(t2).getRoomNumber() == 23
    assert mw(t2).getNoteTakerEmails() == ["jeff@ap.com"]
    noteDates2 = mw(t2).getNoteDates()
    assert len(noteDates2) == 1
    assert noteDates2[0].year == 2023
    assert noteDates2[0].month == 9
    assert noteDates2[0].day == 1
    assert mw(t2).getNoteDescriptions() == ["This is a dummy note 1 for a ticket"]
    assert mw(t2).getImageURLs() == ["http://thisimage.com/2.png"]

    t3 = ticketsById[3]
    assert mw(t3).getRaisedByEmail() == "manager@ap.com"
    d3 = mw(t3).getRaisedOnDate()
    assert d3.year == 2023
    assert d3.month == 7
    assert d3.day == 20
    assert mw(t3).getDescription() == "It is noisy"
    assert mw(t3).getAssetName() is None
    assert not mw(t3).getExpectedLifeSpanInDays()
    assert mw(t3).getPurchaseDate() is None
    assert not mw(t3).getFloorNumber()
    assert not mw(t3).getRoomNumber()
    assert mw(t3).getNoteTakerEmails() == []
    assert mw(t3).getNoteDates() == []
    assert mw(t3).getNoteDescriptions() == []
    assert mw(t3).getImageURLs() == []
