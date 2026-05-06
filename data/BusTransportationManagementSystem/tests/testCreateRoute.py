import pytest


@pytest.fixture
def givenController(modelingTool):
    global Route
    if modelingTool == "umple":
        from ..umple.controller.controller import BusTransportationManagementSystemController
        from ..umple.generated_model_layer import Route
        Route.routesByNumber.clear()
    else:
        from ..ecore.controller.controller import BusTransportationManagementSystemController
        from ..ecore.generated_model_layer import Route

    controller = BusTransportationManagementSystemController()
    yield controller


def testCreateRouteSuccess(givenController, mw):
    controller = givenController

    controller.createRoute(3)

    btms = mw(controller.btms)

    assert len(btms.getRoutes()) == 1
    assert btms.getRoutes()[0].getNumber() == 3


def testCreateRouteDuplicate(givenController, mw):
    controller = givenController

    controller.createRoute(3)

    with pytest.raises(ValueError) as exc_info:
        controller.createRoute(3)

    btms = mw(controller.btms)

    assert str(exc_info.value) == "A route with this number already exists. Please use a different number."
    assert len(btms.getRoutes()) == 1


@pytest.mark.parametrize("number", [5, 10])
def testCreateRouteOutlineSuccess(givenController, mw, number):
    controller = givenController

    controller.createRoute(number)

    btms = mw(controller.btms)

    assert len(btms.getRoutes()) == 1
    assert btms.getRoutes()[0].getNumber() == number


@pytest.mark.parametrize("number, errorMsg", [
    (-2,    "The number of a route must be greater than zero."),
    (10000, "The number of a route cannot be greater than 9999."),
])
def testCreateRouteInvalidNumber(givenController, mw, number, errorMsg):
    controller = givenController

    with pytest.raises(ValueError) as exc_info:
        controller.createRoute(number)

    btms = mw(controller.btms)

    assert str(exc_info.value) == errorMsg
    assert len(btms.getRoutes()) == 0
