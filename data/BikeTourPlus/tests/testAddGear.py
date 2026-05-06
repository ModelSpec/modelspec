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
    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)

    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)

    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    yield controller


@pytest.mark.parametrize("name, pricePerWeek", [
    ("mountain bike", 100),
    ("tire kit", 15),
])
def testAddGearSuccess(controllerWithGear, mw, name, pricePerWeek):
    result = controllerWithGear.addGear(name, pricePerWeek)

    assert result is None

    btp = mw(controllerWithGear.btp)
    assert len(btp.getGear()) == 4

    addedGear = next((g for g in btp.getGear() if g.getName() == name), None)
    assert addedGear is not None
    assert addedGear.getPricePerWeek() == pricePerWeek


@pytest.mark.parametrize("name, pricePerWeek, error_message", [
    ("lightweight bike", -35, "The price per week must be greater than or equal to 0"),
    ("", 35, "The name must not be empty"),
    ("helmet", 35, "A piece of gear with the same name already exists"),
    ("small combo", 30, "A combo with the same name already exists"),
])
def testAddGearInvalid(controllerWithGear, mw, name, pricePerWeek, error_message):
    with pytest.raises(ValueError) as error_info:
        controllerWithGear.addGear(name, pricePerWeek)

    assert str(error_info.value) == error_message
    assert len(mw(controllerWithGear.btp).getGear()) == 3
