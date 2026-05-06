from datetime import datetime

import pytest

@pytest.fixture
def controllerWithShelf(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Shelf, ShelfLocation, Transaction, CheeseWheel, User, Farmer, Purchase

        Shelf.shelfsById.clear()
        ShelfLocation.nextId = 1
        Transaction.nextId = 1
        CheeseWheel.nextId = 1
        User.usersByEmail.clear()
        Farmer.usersByEmail.clear()
        MaturationPeriod = CheeseWheel.MaturationPeriod

    else:
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Shelf, ShelfLocation, Transaction, CheeseWheel, User, Farmer, Purchase, MaturationPeriod

    controller = CheECSEManagerController()

    farmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")

    shelf = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)
    for column in range(1, 6):
        for row in range(1, 3):
            mw(ShelfLocation, column=column, row=row, shelf=shelf.model)

    purchase = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase.setId(1)

    for i in range(5):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase.model)
        cw.setId(i + 1)

    yield controller, shelf

def testRemoveCheeseWheelSuccess(controllerWithShelf, mw):
    # Arrange
    controller, shelf = controllerWithShelf
    for loc in shelf.getLocations():
        if loc.getColumn() == 2 and loc.getRow() == 1:
            location = loc
    for cw in mw(controller.cheECSEManager).getCheeseWheels():
        if cw.getId() == 1:
            cw.setLocation(location.model)

    # Act
    controller.removeCheeseWheelFromShelf(1)

    # Assert
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 0
    cheese = next(cw for cw in mw(controller.cheECSEManager).getCheeseWheels() if cw.getId() == 1)
    assert not cheese.hasLocation()

def testRemoveCheeseWheelMissing(controllerWithShelf):
    # Arrange
    controller, shelf = controllerWithShelf

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.removeCheeseWheelFromShelf(10)

    # Assert
    assert str(errorInfo.value) == "The cheese wheel with id 10 does not exist."
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 0

def testRemoveCheeseWheelNotOnShelf(controllerWithShelf):
    # Arrange
    controller, shelf = controllerWithShelf

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.removeCheeseWheelFromShelf(3)

    # Assert
    assert str(errorInfo.value) == "The cheese wheel is not on any shelf."
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 0