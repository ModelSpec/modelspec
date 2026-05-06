import pytest
from datetime import datetime


@pytest.fixture
def controllerWithGear(modelingTool, mw):
    global Participant, BookedItem, Combo, ComboItem
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

    mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)
    mw(Gear, name="tire kit", pricePerWeek=15, bikeTourPlus=controller.btp)

    yield controller


@pytest.mark.parametrize("name, numberOfGear", [
    ("helmet", 3),
    ("bike bag", 3),
    ("mountain bike", 4),
    ("spare tire", 4),
])
def testDeleteGearSuccess(controllerWithGear, mw, name, numberOfGear):
    controllerWithGear.deleteGear(name)

    btp = mw(controllerWithGear.btp)
    gears = btp.getGear()
    assert not any(g.getName() == name for g in gears)
    assert len(gears) == numberOfGear


@pytest.mark.parametrize("name, email, requestedGearName, quantity, numberOfRequestedGear", [
    ("helmet", "peter@email.com", "bike bag", 2, 1),
    ("bike bag", "peter@email.com", "helmet", 1, 1),
])
def testDeleteRequestedGear(controllerWithGear, mw, name, email, requestedGearName, quantity, numberOfRequestedGear):
    btp = mw(controllerWithGear.btp)

    p1 = mw(Participant, email=email, password="pass1", name="Peter", emergencyContact="(666)555-5555",
             nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
             authorizationCode="no-lodge", refundedPercentageAmount=0, bikeTourPlus=controllerWithGear.btp)

    helmet = next((g for g in btp.getGear() if g.getName() == "helmet"), None)
    bikeBag = next((g for g in btp.getGear() if g.getName() == "bike bag"), None)
    mw(BookedItem, quantity=1, bikeTourPlus=controllerWithGear.btp, participant=p1.model, item=helmet.model)
    mw(BookedItem, quantity=2, bikeTourPlus=controllerWithGear.btp, participant=p1.model, item=bikeBag.model)

    controllerWithGear.deleteGear(name)

    gears = btp.getGear()
    assert not any(g.getName() == name for g in gears)
    assert len(gears) == 3

    bookedItems = p1.getBookedItems()
    remaining = next((bi for bi in bookedItems if bi.getItem().getName() == requestedGearName), None)
    assert remaining is not None
    assert remaining.getQuantity() == quantity
    assert len(bookedItems) == numberOfRequestedGear


@pytest.mark.parametrize("name, pricePerWeek, comboName, quantity, numberOfGearInCombo", [
    ("helmet", 25, "small combo", 2, 2),
    ("e-bike", 150, "small combo", 1, 2),
])
def testDeleteGearUnsuccessful(controllerWithGear, mw, name, pricePerWeek, comboName, quantity, numberOfGearInCombo):
    btp = mw(controllerWithGear.btp)

    helmet = next((g for g in btp.getGear() if g.getName() == "helmet"), None)
    ebike = next((g for g in btp.getGear() if g.getName() == "e-bike"), None)

    sCombo = mw(Combo, name=comboName, discount=10, bikeTourPlus=controllerWithGear.btp)
    mw(ComboItem, quantity=2, bikeTourPlus=controllerWithGear.btp, combo=sCombo.model, gear=helmet.model)
    mw(ComboItem, quantity=1, bikeTourPlus=controllerWithGear.btp, combo=sCombo.model, gear=ebike.model)

    with pytest.raises(ValueError) as excinfo:
        controllerWithGear.deleteGear(name)

    assert str(excinfo.value) == "The piece of gear is in a combo and cannot be deleted"

    gears = btp.getGear()
    targetGear = next((g for g in gears if g.getName() == name), None)
    assert targetGear is not None
    assert targetGear.getPricePerWeek() == pricePerWeek
    assert len(gears) == 4

    combo = next((c for c in btp.getCombos() if c.getName() == comboName), None)
    comboItems = combo.getComboItems()
    targetCi = next((ci for ci in comboItems if ci.getGear().getName() == name), None)
    assert targetCi.getQuantity() == quantity
    assert len(comboItems) == numberOfGearInCombo
