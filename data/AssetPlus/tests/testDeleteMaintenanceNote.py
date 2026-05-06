import pytest
from datetime import datetime


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
    note1a = mw(MaintenanceNote, date=datetime(2023, 9, 10), description="This is another dummy note 2 for a ticket", noteTaker=smith.model, ticket=t1.model)
    mw(t1.model).addTicketNote(note1a.model)
    note1b = mw(MaintenanceNote, date=datetime(2023, 9, 23), description="This is a dummy description 1", noteTaker=mgr.model, ticket=t1.model)
    mw(t1.model).addTicketNote(note1b.model)
    note2 = mw(MaintenanceNote, date=datetime(2023, 9, 1), description="This is a dummy note 1 for a ticket", noteTaker=jeff.model, ticket=t2.model)
    mw(t2.model).addTicketNote(note2.model)
    yield controller


@pytest.mark.parametrize(
    "noteIndex, ticketId, numberOfNotes",
    [
        (0, 2, 0),
        (0, 1, 1),
        (1, 1, 1),
    ],
)
def testMaintenanceDeleteNoteSuccess(givenController, mw, noteIndex, ticketId, numberOfNotes):
    beforeTicket = None
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        if t.getId() == ticketId:
            beforeTicket = t
            break
    assert beforeTicket is not None
    beforeNotes = beforeTicket.getTicketNotes()
    deletedNote = beforeNotes[noteIndex] if 0 <= noteIndex < len(beforeNotes) else None
    givenController.deleteMaintenanceNote(ticketId, noteIndex)
    totalNotes = 0
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        totalNotes += len(t.getTicketNotes())
    assert totalNotes == 2
    afterTicket = None
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        if t.getId() == ticketId:
            afterTicket = t
            break
    assert afterTicket is not None
    afterNotes = afterTicket.getTicketNotes()
    assert len(afterNotes) == numberOfNotes
    if deletedNote is not None:
        for n in afterNotes:
            assert n is not deletedNote


@pytest.mark.parametrize(
    "noteIndex, ticketId, numberOfNotes",
    [
        (1, 2, 1),
        (2, 1, 2),
        (3, 1, 2),
    ],
)
def testDeleteNonExistingMaintenanceNoteForExistingTicketSuccess(givenController, mw, noteIndex, ticketId, numberOfNotes):
    beforeTicket = None
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        if t.getId() == ticketId:
            beforeTicket = t
            break
    assert beforeTicket is not None
    beforeNotes = beforeTicket.getTicketNotes()
    givenController.deleteMaintenanceNote(ticketId, noteIndex)
    totalNotes = 0
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        totalNotes += len(t.getTicketNotes())
    assert totalNotes == 3
    afterTicket = None
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        if t.getId() == ticketId:
            afterTicket = t
            break
    assert afterTicket is not None
    afterNotes = afterTicket.getTicketNotes()
    assert len(afterNotes) == numberOfNotes
    assert len(afterNotes) == len(beforeNotes)
    for i in range(len(afterNotes)):
        b = beforeNotes[i]
        a = afterNotes[i]
        assert a.getDate() == b.getDate()
        assert a.getDescription() == b.getDescription()
        assert a.getNoteTaker() is not None
        assert b.getNoteTaker() is not None
        assert a.getNoteTaker().getEmail() == b.getNoteTaker().getEmail()


def testDeleteNonExistingMaintenanceNoteForNonExistingTicketSuccess(givenController, mw):
    givenController.deleteMaintenanceNote(3, 0)
    totalNotes = 0
    for t in mw(givenController.assetPlus).getMaintenanceTickets():
        totalNotes += len(t.getTicketNotes())
    assert totalNotes == 3
