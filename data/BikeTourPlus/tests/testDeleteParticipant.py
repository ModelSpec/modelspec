import pytest
from datetime import datetime


@pytest.fixture
def controllerWithParticipant(modelingTool, mw):
    global BookedItem
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, Gear, Combo, ComboItem, Guide, Participant, Manager, BookedItem
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Gear, Combo, ComboItem, Guide, Participant, Manager, BookedItem

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Manager, email="manager@btp.com", password="password", bikeTourPlus=controller.btp)

    h = mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    e = mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    b = mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)

    s = mw(Combo, name="small combo", discount=10, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)

    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)

    mw(Participant, email="peter@email.com", password="pass1", name="Peter", emergencyContact="(666)555-5555",
       nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
       authorizationCode="None", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    mw(Participant, email="tyler@email.com", password="pass2", name="Tyler", emergencyContact="(777)444-4444",
       nrWeeks=2, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="None", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    mw(Participant, email="mary@email.com", password="pass3", name="Mary", emergencyContact="(555)666-6666",
       nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=False,
       authorizationCode="None", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    yield controller


@pytest.mark.parametrize("email, numberOfParticipants", [
    ("peter@email.com", 2),
    ("tyler@email.com", 2),
    ("usernotfound@mail.ca", 3),
])
def testDeleteParticipantSuccess(controllerWithParticipant, mw, email, numberOfParticipants):
    controllerWithParticipant.deleteParticipant(email)

    btp = mw(controllerWithParticipant.btp)
    assert not any(p.getEmail() == email for p in btp.getParticipants())
    assert len(btp.getParticipants()) == numberOfParticipants


@pytest.mark.parametrize("email", ["jeff@email.com", "john@email.com"])
def testDeleteNonExistingParticipantGuideExists(controllerWithParticipant, mw, email):
    controllerWithParticipant.deleteParticipant(email)

    btp = mw(controllerWithParticipant.btp)
    assert any(g.getEmail() == email for g in btp.getGuides())
    assert len(btp.getGuides()) == 2
    assert len(btp.getParticipants()) == 3


def testDeleteNonExistingParticipantManagerExists(controllerWithParticipant, mw):
    controllerWithParticipant.deleteParticipant("manager@btp.com")

    btp = mw(controllerWithParticipant.btp)
    assert btp.getManager() is not None
    assert btp.getManager().getEmail() == "manager@btp.com"
    assert len(btp.getGuides()) == 2
    assert len(btp.getParticipants()) == 3


@pytest.mark.parametrize("email, gearName, gearCount, comboName, comboCount", [
    ("peter@email.com", "helmet", 0, "small combo", 0),
    ("peter@email.com", "bike bag", 0, "large combo", 2),
    ("tyler@email.com", "bike bag", 1, "large combo", 1),
    ("mary@email.com", "helmet", 1, "large combo", 1),
])
def testDeleteParticipantWithRequests(controllerWithParticipant, mw, email, gearName, gearCount, comboName, comboCount):
    btp = mw(controllerWithParticipant.btp)

    peter = next(p for p in btp.getParticipants() if p.getEmail() == "peter@email.com")
    tyler = next(p for p in btp.getParticipants() if p.getEmail() == "tyler@email.com")
    mary = next(p for p in btp.getParticipants() if p.getEmail() == "mary@email.com")

    helmet = next(g for g in btp.getGear() if g.getName() == "helmet")
    bikebag = next(g for g in btp.getGear() if g.getName() == "bike bag")
    small = next(c for c in btp.getCombos() if c.getName() == "small combo")
    large = next(c for c in btp.getCombos() if c.getName() == "large combo")

    mw(BookedItem, quantity=1, bikeTourPlus=controllerWithParticipant.btp, participant=peter.model, item=helmet.model)
    mw(BookedItem, quantity=2, bikeTourPlus=controllerWithParticipant.btp, participant=peter.model, item=bikebag.model)
    mw(BookedItem, quantity=1, bikeTourPlus=controllerWithParticipant.btp, participant=peter.model, item=small.model)
    mw(BookedItem, quantity=2, bikeTourPlus=controllerWithParticipant.btp, participant=tyler.model, item=large.model)
    mw(BookedItem, quantity=1, bikeTourPlus=controllerWithParticipant.btp, participant=mary.model, item=large.model)

    controllerWithParticipant.deleteParticipant(email)

    assert not any(p.getEmail() == email for p in btp.getParticipants())
    assert len(btp.getParticipants()) == 2

    participantsWithGear = set()
    for bi in btp.getBookedItems():
        if bi.getItem().getName() == gearName:
            participantsWithGear.add(bi.getParticipant().getEmail())
    assert len(participantsWithGear) == gearCount

    participantsWithCombo = set()
    for bi in btp.getBookedItems():
        if bi.getItem().getName() == comboName:
            participantsWithCombo.add(bi.getParticipant().getEmail())
    assert len(participantsWithCombo) == comboCount
