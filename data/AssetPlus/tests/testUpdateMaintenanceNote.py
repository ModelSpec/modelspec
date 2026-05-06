import pytest
from datetime import date, datetime


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
        from ..ecore.generated_model_layer import Manager, Employee, AssetType, SpecificAsset, MaintenanceTicket, MaintenanceNote
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
    t1 = mw(MaintenanceTicket, id=1, raisedOnDate=datetime(2023, 7, 20), description="This is a dummy description 1", ticketRaiser=mgr.model, assetPlus=ap)
    mw(ap).addMaintenanceTicket(t1.model)
    t1.setAsset(sa2.model)
    t2 = mw(MaintenanceTicket, id=2, raisedOnDate=datetime(2023, 7, 10), description="This is a dummy description 2", ticketRaiser=smith.model, assetPlus=ap)
    mw(ap).addMaintenanceTicket(t2.model)
    t2.setAsset(sa1.model)
    note2 = mw(MaintenanceNote, date=datetime(2023, 9, 1), description="This is a dummy note 1 for a ticket", noteTaker=jeff.model, ticket=t2.model)
    mw(t2.model).addTicketNote(note2.model)
    note1 = mw(MaintenanceNote, date=datetime(2023, 9, 10), description="This is another dummy note 2 for a ticket", noteTaker=smith.model, ticket=t1.model)
    mw(t1.model).addTicketNote(note1.model)
    yield controller


@pytest.mark.parametrize(
    "ticketId, newNoteTaker, newDate, newDescription, noteIndex, numberOfNotes",
    [
        (1, "jeff@ap.com", date(2023, 9, 23), "This is a dummy description 1", 0, 1),
        (1, "manager@ap.com", date(2023, 10, 5), "This is a dummy description 2", 0, 1),
    ],
)
def testUpdateMaintenanceNoteSuccess(givenController, mw, ticketId, newNoteTaker, newDate, newDescription, noteIndex, numberOfNotes):
    givenController.updateMaintenanceNote(ticketId, noteIndex, newNoteTaker, newDate, newDescription)
    totalNotes = 0
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        totalNotes += len(t.getTicketNotes())
    assert totalNotes == 2

    ticket = None
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        if t.getId() == ticketId:
            ticket = t
            break
    assert ticket is not None

    notes = ticket.getTicketNotes()
    assert len(notes) == numberOfNotes
    assert 0 <= noteIndex < len(notes)

    n = notes[noteIndex]
    nt = n.getNoteTaker()
    assert nt is not None
    assert nt.getEmail() == newNoteTaker
    d = n.getDate()
    assert d.year == newDate.year
    assert d.month == newDate.month
    assert d.day == newDate.day
    assert n.getDescription() == newDescription


@pytest.mark.parametrize(
    "ticketId, newNoteTaker, newDate, newDescription, noteIndex, errorMessage",
    [
        (1, "abdul@ap.com", date(2023, 9, 23), "This is a dummy description 1", 0, "Hotel staff does not exist"),
        (3, "manager@ap.com", date(2023, 10, 5), "This is a dummy description 2", 0, "Ticket does not exist"),
        (1, "manager@ap.com", date(2023, 10, 5), "This is a dummy description 2", 1, "Note does not exist"),
        (1, "manager@ap.com", date(2023, 10, 5), "", 0, "Ticket description cannot be empty"),
    ],
)
def testUpdateMaintenanceNoteInvalidValuesFail(givenController, mw, ticketId, newNoteTaker, newDate, newDescription, noteIndex, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateMaintenanceNote(ticketId, noteIndex, newNoteTaker, newDate, newDescription)
    assert str(errorInfo.value) == errorMessage

    totalNotes = 0
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        totalNotes += len(t.getTicketNotes())
    assert totalNotes == 2

    t1 = None
    t2 = None
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        if t.getId() == 1:
            t1 = t
        if t.getId() == 2:
            t2 = t
    assert t1 is not None
    assert t2 is not None

    notes1 = t1.getTicketNotes()
    notes2 = t2.getTicketNotes()
    assert len(notes1) == 1
    assert len(notes2) == 1

    n1 = notes1[0]
    nt1 = n1.getNoteTaker()
    assert nt1 is not None
    assert nt1.getEmail() == "smith@ap.com"
    d1 = n1.getDate()
    assert d1.year == 2023
    assert d1.month == 9
    assert d1.day == 10
    assert n1.getDescription() == "This is another dummy note 2 for a ticket"

    n2 = notes2[0]
    nt2 = n2.getNoteTaker()
    assert nt2 is not None
    assert nt2.getEmail() == "jeff@ap.com"
    d2 = n2.getDate()
    assert d2.year == 2023
    assert d2.month == 9
    assert d2.day == 1
    assert n2.getDescription() == "This is a dummy note 1 for a ticket"
