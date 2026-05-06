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
    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)

    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)

    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    yield controller


@pytest.mark.parametrize("name, discount", [
    ("deluxe combo", 40),
    ("combo plus", 10),
])
def testAddComboSuccess(controllerWithCombo, mw, name, discount):
    result = controllerWithCombo.addCombo(name, discount)

    assert result is None

    btp = mw(controllerWithCombo.btp)
    assert len(btp.getCombos()) == 3

    addedCombo = next((c for c in btp.getCombos() if c.getName() == name), None)
    assert addedCombo is not None
    assert addedCombo.getDiscount() == discount
    assert len(addedCombo.getComboItems()) == 0


@pytest.mark.parametrize("name, discount, error_message", [
    ("deluxe combo", -1, "Discount must be at least 0"),
    ("combo plus", 101, "Discount must be no more than 100"),
    ("", 0, "The name must not be empty"),
    ("helmet", 35, "A piece of gear with the same name already exists"),
    ("small combo", 30, "A combo with the same name already exists"),
])
def testAddComboInvalidInputs(controllerWithCombo, mw, name, discount, error_message):
    with pytest.raises(ValueError) as error_info:
        controllerWithCombo.addCombo(name, discount)

    assert str(error_info.value) == error_message
    assert len(mw(controllerWithCombo.btp).getCombos()) == 2
