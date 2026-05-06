import pytest
from datetime import datetime


@pytest.fixture
def controllerWithBikeTourPlus(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)
    yield controller


@pytest.mark.parametrize("startDate, nrWeeks, priceOfGuidePerWeek", [
    ("2023-03-14", 10, 100),
    ("2023-03-13", 0, 100),
    ("2023-03-13", 10, 0),
])
def testUpdateBikeTourPlusSuccess(controllerWithBikeTourPlus, mw, startDate, nrWeeks, priceOfGuidePerWeek):
    year, month, day = map(int, startDate.split('-'))
    startDateObj = datetime(year, month, day)

    controllerWithBikeTourPlus.updateBikeTourPlus(startDateObj, nrWeeks, priceOfGuidePerWeek)

    btp = mw(controllerWithBikeTourPlus.btp)
    assert btp.getStartDate() == startDateObj
    assert btp.getNrWeeks() == nrWeeks
    assert btp.getPriceOfGuidePerWeek() == priceOfGuidePerWeek


@pytest.mark.parametrize("startDate, nrWeeks, priceOfGuidePerWeek, error", [
    ("2023-01-13", -1, 100, "The number of riding weeks must be greater than or equal to zero"),
    ("2023-01-13", 10, -1, "The price of guide per week must be greater than or equal to zero"),
    ("2021-01-13", 10, 100, "The start date cannot be from previous year or earlier"),
])
def testUpdateBikeTourPlusUnsuccessful(controllerWithBikeTourPlus, mw, startDate, nrWeeks, priceOfGuidePerWeek, error):
    year, month, day = map(int, startDate.split('-'))
    startDateObj = datetime(year, month, day)

    with pytest.raises(ValueError) as error_info:
        controllerWithBikeTourPlus.updateBikeTourPlus(startDateObj, nrWeeks, priceOfGuidePerWeek)

    assert str(error_info.value) == error

    btp = mw(controllerWithBikeTourPlus.btp)
    assert btp.getStartDate() == datetime(2023, 3, 13)
    assert btp.getNrWeeks() == 10
    assert btp.getPriceOfGuidePerWeek() == 100
