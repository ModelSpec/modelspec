import pytest
from datetime import date
from freezegun import freeze_time


@pytest.fixture
def givenController(modelingTool):
    global BusVehicle, Route
    if modelingTool == "umple":
        from ..umple.controller.controller import BusTransportationManagementSystemController
        from ..umple.generated_model_layer import BusVehicle, Route
        BusVehicle.busvehiclesByLicencePlate.clear()
        Route.routesByNumber.clear()
        controller = BusTransportationManagementSystemController()
        controller.btms.addVehicle("123456")
        controller.btms.addVehicle("654321")
        controller.btms.addRoute(101)
    else:
        from ..ecore.controller.controller import BusTransportationManagementSystemController
        from ..ecore.generated_model_layer import BusVehicle, Route
        controller = BusTransportationManagementSystemController()
        controller.btms.vehicles.append(BusVehicle(licencePlate="123456"))
        controller.btms.vehicles.append(BusVehicle(licencePlate="654321"))
        controller.btms.routes.append(Route(number=101))

    yield controller


@freeze_time("2021-10-07")
@pytest.mark.parametrize("vehicle, route, assignDate", [
    ("123456", 101, date(2021, 10, 8)),
])
def testAssignBusSuccess(givenController, mw, vehicle, route, assignDate):
    controller = givenController

    controller.createRouteAssignment(vehicle, route, assignDate)

    btms = mw(controller.btms)
    assignments = btms.getAssignments()
    assert len(assignments) == 1

    assignment = assignments[0]
    assert assignment.getBus().getLicencePlate() == vehicle
    assert assignment.getRoute().getNumber() == route
    actualDate = assignment.getDate()
    assert actualDate.year == assignDate.year
    assert actualDate.month == assignDate.month
    assert actualDate.day == assignDate.day


@freeze_time("2021-10-07")
@pytest.mark.parametrize("vehicle, route, assignDate, errorMsg", [
    ("notreal", 101, date(2021, 10, 8), "A bus must be specified for the assignment."),
    ("123456",  201, date(2021, 10, 8), "A route must be specified for the assignment."),
    ("654321",  101, date(2023, 10, 8), "The date must be within a year from today."),
])
def testAssignBusInvalid(givenController, mw, vehicle, route, assignDate, errorMsg):
    controller = givenController

    with pytest.raises(ValueError) as exc_info:
        controller.createRouteAssignment(vehicle, route, assignDate)

    btms = mw(controller.btms)

    assert str(exc_info.value) == errorMsg
    assert len(btms.getAssignments()) == 0
