import pytest
from datetime import datetime


@pytest.fixture
def controllerWithComboAndGear(modelingTool, mw):
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
    mw(Gear, name="tire kit", pricePerWeek=15, bikeTourPlus=controller.btp)

    s = mw(Combo, name="small combo", discount=10, bikeTourPlus=controller.btp)
    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)

    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)

    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    yield controller


@pytest.mark.parametrize("gearName, quantity, comboName, numberOfGearInCombo", [
    ("bike bag", 1, "small combo", 3),
    ("bike bag", 3, "large combo", 3),
    ("e-bike", 2, "small combo", 2),
    ("e-bike", 2, "large combo", 3),
    ("tire kit", 1, "small combo", 3),
    ("tire kit", 1, "large combo", 4),
])
def testAddGearToComboSuccess(controllerWithComboAndGear, mw, gearName, quantity, comboName, numberOfGearInCombo):
    result = controllerWithComboAndGear.addGearToCombo(gearName, comboName)

    assert result is None

    btp = mw(controllerWithComboAndGear.btp)
    assert len(btp.getCombos()) == 2
    combo = next((c for c in btp.getCombos() if c.getName() == comboName), None)

    assert combo is not None
    assert len(combo.getComboItems()) == numberOfGearInCombo

    found = any(
        item.getGear().getName() == gearName and item.getQuantity() == quantity
        for item in combo.getComboItems()
    )
    assert found


@pytest.mark.parametrize("nonExistingGearName, gearName, quantity, comboName, numberOfGearInCombo, error", [
    ("spare tire", "e-bike",   1, "small combo", 2, "The piece of gear does not exist"),
    ("bike lock",  "helmet",   2, "small combo", 2, "The piece of gear does not exist"),
    ("spare tire", "e-bike",   1, "large combo", 3, "The piece of gear does not exist"),
    ("bike lock",  "helmet",   2, "large combo", 3, "The piece of gear does not exist"),
    ("bike lock",  "bike bag", 2, "large combo", 3, "The piece of gear does not exist"),
])
def testAddNonExistingGearToCombo(controllerWithComboAndGear, mw, nonExistingGearName, gearName, quantity, comboName, numberOfGearInCombo, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithComboAndGear.addGearToCombo(nonExistingGearName, comboName)

    assert str(error_info.value) == error

    btp = mw(controllerWithComboAndGear.btp)
    assert len(btp.getCombos()) == 2
    combo = next((c for c in btp.getCombos() if c.getName() == comboName), None)
    assert combo is not None
    assert len(combo.getComboItems()) == numberOfGearInCombo
    found = any(
        item.getGear().getName() == gearName and item.getQuantity() == quantity
        for item in combo.getComboItems()
    )
    assert found


@pytest.mark.parametrize("gearName, comboName, error", [
    ("e-bike", "deluxe combo", "The combo does not exist"),
    ("helmet", "deluxe combo", "The combo does not exist"),
    ("e-bike", "combo plus", "The combo does not exist"),
    ("helmet", "combo plus", "The combo does not exist"),
    ("bike bag", "combo plus", "The combo does not exist"),
])
def testAddGearToNonExistingCombo(controllerWithComboAndGear, gearName, comboName, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithComboAndGear.addGearToCombo(gearName, comboName)

    assert str(error_info.value) == error
