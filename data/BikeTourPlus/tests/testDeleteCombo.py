import pytest
from datetime import datetime


@pytest.fixture
def controllerWithCombos(modelingTool, mw):
    global Participant, BookedItem
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, Gear, Combo, ComboItem, Participant, BookedItem
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Gear, Combo, ComboItem, Participant, BookedItem

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    h = mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    e = mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    b = mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)

    s = mw(Combo, name="small combo", discount=10, bikeTourPlus=controller.btp)
    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    yield controller


@pytest.mark.parametrize("name, numberOfCombos", [
    ("small combo", 1),
    ("large combo", 1),
    ("deluxe combo", 2),
    ("combo plus", 2),
])
def testDeleteComboSuccess(controllerWithCombos, mw, name, numberOfCombos):
    controllerWithCombos.deleteCombo(name)

    btp = mw(controllerWithCombos.btp)
    currentCombos = btp.getCombos()
    assert not any(c.getName() == name for c in currentCombos)
    assert len(currentCombos) == numberOfCombos


@pytest.mark.parametrize("name, email, requestedComboName, quantity, numberOfRequestedCombos", [
    ("small combo", "peter@email.com", "large combo", 2, 1),
    ("large combo", "peter@email.com", "small combo", 1, 1),
])
def testDeleteRequestedCombo(controllerWithCombos, mw, name, email, requestedComboName, quantity, numberOfRequestedCombos):
    btp = mw(controllerWithCombos.btp)

    p1 = mw(Participant, email=email, password="pass1", name="Peter", emergencyContact="(666)555-5555",
             nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
             authorizationCode="no-lodge", refundedPercentageAmount=0, bikeTourPlus=controllerWithCombos.btp)

    sCombo = next((c for c in btp.getCombos() if c.getName() == "small combo"), None)
    lCombo = next((c for c in btp.getCombos() if c.getName() == "large combo"), None)
    mw(BookedItem, quantity=1, bikeTourPlus=controllerWithCombos.btp, participant=p1.model, item=sCombo.model)
    mw(BookedItem, quantity=2, bikeTourPlus=controllerWithCombos.btp, participant=p1.model, item=lCombo.model)

    controllerWithCombos.deleteCombo(name)

    assert not any(c.getName() == name for c in btp.getCombos())
    assert len(btp.getCombos()) == 1

    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    bookedItems = participant.getBookedItems()

    remaining = next((bi for bi in bookedItems if bi.getItem().getName() == requestedComboName), None)
    assert remaining is not None
    assert remaining.getQuantity() == quantity

    assert not any(bi.getItem().getName() == name for bi in bookedItems)
    assert len(bookedItems) == numberOfRequestedCombos
