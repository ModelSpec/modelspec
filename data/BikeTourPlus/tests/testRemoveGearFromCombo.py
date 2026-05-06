import pytest
from datetime import datetime


@pytest.fixture
def controllerWithCombosAndGear(modelingTool, mw):
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
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)

    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    yield controller


@pytest.mark.parametrize("gearName, quantity, comboName, numberOfGearInCombo", [
    ("helmet", 1, "small combo", 2),
    ("helmet", 1, "large combo", 3),
    ("bike bag", 1, "large combo", 3),
])
def testRemoveGearSuccess(controllerWithCombosAndGear, mw, gearName, quantity, comboName, numberOfGearInCombo):
    controllerWithCombosAndGear.removeGearFromCombo(gearName, comboName)

    btp = mw(controllerWithCombosAndGear.btp)
    combo = next((c for c in btp.getCombos() if c.getName() == comboName), None)
    assert combo is not None

    targetItem = next((item for item in combo.getComboItems() if item.getGear().getName() == gearName), None)
    assert targetItem is not None
    assert targetItem.getQuantity() == quantity

    assert len(combo.getComboItems()) == numberOfGearInCombo
    assert len(btp.getCombos()) == 2


@pytest.mark.parametrize("gearName, comboName, numberOfGearInCombo", [
    ("e-bike", "large combo", 2),
    ("spare tire", "small combo", 2),
    ("spare tire", "large combo", 3),
])
def testRemoveLastItemOrNonExistentGear(controllerWithCombosAndGear, mw, gearName, comboName, numberOfGearInCombo):
    controllerWithCombosAndGear.removeGearFromCombo(gearName, comboName)

    btp = mw(controllerWithCombosAndGear.btp)
    combo = next((c for c in btp.getCombos() if c.getName() == comboName), None)
    items = combo.getComboItems()
    assert not any(item.getGear().getName() == gearName for item in items)
    assert len(items) == numberOfGearInCombo
    assert len(btp.getCombos()) == 2


@pytest.mark.parametrize("gearName, quantity, comboName, numberOfGearInCombo, error", [
    ("e-bike", 1, "small combo", 2, "A combo must have at least two pieces of gear"),
])
def testRemoveGearInvalidConstraint(controllerWithCombosAndGear, mw, gearName, quantity, comboName, numberOfGearInCombo, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithCombosAndGear.removeGearFromCombo(gearName, comboName)

    assert str(error_info.value) == error

    btp = mw(controllerWithCombosAndGear.btp)
    combo = next((c for c in btp.getCombos() if c.getName() == comboName), None)
    targetItem = next((item for item in combo.getComboItems() if item.getGear().getName() == gearName), None)
    assert targetItem.getQuantity() == quantity
    assert len(combo.getComboItems()) == numberOfGearInCombo
    assert len(btp.getCombos()) == 2


@pytest.mark.parametrize("gearName, comboName, error", [
    ("e-bike", "deluxe combo", "The combo does not exist"),
    ("helmet", "deluxe combo", "The combo does not exist"),
    ("e-bike", "combo plus", "The combo does not exist"),
    ("helmet", "combo plus", "The combo does not exist"),
    ("bike bag", "combo plus", "The combo does not exist"),
])
def testRemoveGearNonExistentCombo(controllerWithCombosAndGear, mw, gearName, comboName, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithCombosAndGear.removeGearFromCombo(gearName, comboName)

    assert str(error_info.value) == error
    assert len(mw(controllerWithCombosAndGear.btp).getCombos()) == 2
