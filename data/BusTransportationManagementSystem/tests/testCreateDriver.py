import pytest


@pytest.fixture
def givenController(modelingTool):
    global Driver
    if modelingTool == "umple":
        from ..umple.controller.controller import BusTransportationManagementSystemController
        from ..umple.generated_model_layer import Driver
        Driver.nextId = 1
    else:
        from ..ecore.controller.controller import BusTransportationManagementSystemController
        from ..ecore.generated_model_layer import Driver

    controller = BusTransportationManagementSystemController()
    yield controller


@pytest.mark.parametrize("driverName, driverCnt, errorCnt, error", [
    ("John Doe", 1, 0, ""),
    ("",         0, 1, "The name of a driver cannot be empty."),
])
def testCreateDriver(givenController, mw, driverName, driverCnt, errorCnt, error):
    controller = givenController

    errors = []

    try:
        controller.createDriver(driverName)
    except ValueError as e:
        errors.append(str(e))

    assert len(mw(controller.btms).getDrivers()) == driverCnt
    assert len(errors) == errorCnt

    if error:
        assert error in errors
