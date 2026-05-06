import pytest
from datetime import datetime


@pytest.fixture
def controllerWithCombo(modelingTool, mw):
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


@pytest.mark.parametrize("oldName, oldDiscount, newName, newDiscount, numberOfGearInCombo", [
    ("small combo", 10, "deluxe combo", 40, 2),
    ("large combo", 25, "combo plus", 10, 3),
])
def testUpdateComboSuccess(controllerWithCombo, mw, oldName, oldDiscount, newName, newDiscount, numberOfGearInCombo):
    controllerWithCombo.updateCombo(oldName, newName, newDiscount)

    btp = mw(controllerWithCombo.btp)
    newCombo = next((c for c in btp.getCombos() if c.getName() == newName), None)
    assert newCombo is not None
    assert newCombo.getDiscount() == newDiscount
    assert len(newCombo.getComboItems()) == numberOfGearInCombo

    oldCombo = next((c for c in btp.getCombos() if c.getName() == oldName), None)
    assert oldCombo is None

    assert len(btp.getCombos()) == 2


@pytest.mark.parametrize("oldName, oldDiscount, newName, newDiscount, numberOfGearInCombo, error", [
    ("small combo", 10, "deluxe combo", -1, 2, "Discount must be at least 0"),
    ("small combo", 10, "combo plus", 101, 2, "Discount must be no more than 100"),
    ("small combo", 10, "", 0, 2, "The name must not be empty"),
    ("large combo", 25, "helmet", 35, 3, "A piece of gear with the same name already exists"),
    ("large combo", 25, "small combo", 30, 3, "A combo with the same name already exists"),
])
def testUpdateComboUnsuccessful(controllerWithCombo, mw, oldName, oldDiscount, newName, newDiscount, numberOfGearInCombo, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithCombo.updateCombo(oldName, newName, newDiscount)

    assert str(error_info.value) == error

    btp = mw(controllerWithCombo.btp)
    oldCombo = next((c for c in btp.getCombos() if c.getName() == oldName), None)
    assert oldCombo is not None
    assert oldCombo.getDiscount() == oldDiscount
    assert len(oldCombo.getComboItems()) == numberOfGearInCombo

    assert len(btp.getCombos()) == 2


@pytest.mark.parametrize("oldName, oldDiscount, newName, newDiscount, error", [
    ("combo plus", 10, "deluxe combo", 15, "The combo does not exist"),
])
def testUpdateComboNonExistent(controllerWithCombo, mw, oldName, oldDiscount, newName, newDiscount, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithCombo.updateCombo(oldName, newName, newDiscount)

    assert str(error_info.value) == error

    btp = mw(controllerWithCombo.btp)
    oldCombo = next((c for c in btp.getCombos() if c.getName() == oldName), None)
    assert oldCombo is None

    newCombo = next((c for c in btp.getCombos() if c.getName() == newName), None)
    assert newCombo is None

    assert len(btp.getCombos()) == 2
