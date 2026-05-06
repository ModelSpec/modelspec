import pytest
from datetime import datetime


@pytest.fixture
def controllerWithGear(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, Gear, Combo, ComboItem
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Gear, Combo, ComboItem

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

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

    yield controller


@pytest.mark.parametrize("oldName, oldPricePerWeek, newName, newPricePerWeek", [
    ("e-bike", 150, "lightweight e-bike", 175),
    ("helmet", 25, "bike helmet", 25),
    ("bike bag", 19, "bike bag", 17),
])
def testUpdateGearSuccess(controllerWithGear, mw, oldName, oldPricePerWeek, newName, newPricePerWeek):
    controllerWithGear.updateGear(oldName, newName, newPricePerWeek)

    btp = mw(controllerWithGear.btp)
    newGear = next((g for g in btp.getGear() if g.getName() == newName), None)
    assert newGear is not None
    assert newGear.getPricePerWeek() == newPricePerWeek

    if oldName != newName:
        oldGear = next((g for g in btp.getGear() if g.getName() == oldName), None)
        assert oldGear is None

    assert len(btp.getGear()) == 3


@pytest.mark.parametrize("oldName, oldPricePerWeek, newName, newPricePerWeek, error", [
    ("e-bike", 150, "lighweight e-bike", -35, "The price per week must be greater than or equal to 0"),
    ("e-bike", 150, "", 35, "The name must not be empty"),
    ("e-bike", 150, "helmet", 150, "A piece of gear with the same name already exists"),
    ("e-bike", 150, "small combo", 150, "A combo with the same name already exists"),
])
def testUpdateGearUnsuccessful(controllerWithGear, mw, oldName, oldPricePerWeek, newName, newPricePerWeek, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithGear.updateGear(oldName, newName, newPricePerWeek)

    assert str(error_info.value) == error

    btp = mw(controllerWithGear.btp)
    oldGear = next((g for g in btp.getGear() if g.getName() == oldName), None)
    assert oldGear is not None
    assert oldGear.getPricePerWeek() == oldPricePerWeek
    assert len(btp.getGear()) == 3


@pytest.mark.parametrize("oldName, oldPricePerWeek, newName, newPricePerWeek, error", [
    ("bike", 150, "mountain bike", 35, "The piece of gear does not exist"),
])
def testUpdateGearNonExistent(controllerWithGear, mw, oldName, oldPricePerWeek, newName, newPricePerWeek, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithGear.updateGear(oldName, newName, newPricePerWeek)

    assert str(error_info.value) == error

    btp = mw(controllerWithGear.btp)
    oldGear = next((g for g in btp.getGear() if g.getName() == oldName), None)
    assert oldGear is None

    newGear = next((g for g in btp.getGear() if g.getName() == newName), None)
    assert newGear is None

    assert len(btp.getGear()) == 3
