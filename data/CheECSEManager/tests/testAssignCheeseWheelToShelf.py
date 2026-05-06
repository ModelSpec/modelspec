from datetime import datetime

import pytest

@pytest.fixture
def populatedController(modelingTool, mw):
    global Shelf, ShelfLocation
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

    sh = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)

    for column in range(1, 6):
        for row in range(1, 3):
            mw(ShelfLocation, column=column, row=row, shelf=sh.model)

    farmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")

    purchase = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)

    for i in range(5):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase.model)
        cw.setId(i + 1)

    yield controller, sh, purchase.getCheeseWheels()

def testAssignCheeseWheelEmptyLocation(populatedController, mw):
    # Arrange
    controller, shelf, _ = populatedController

    # Act
    controller.assignCheeseWheelToShelf(1, "A12", 2, 1)

    # Assert
    controller.cheECSEManager = mw(controller.cheECSEManager)
    target = None
    for loc in shelf.getLocations():
        if loc.getColumn() == 2 and loc.getRow() == 1:
            target = loc
            break

    assert target.hasCheeseWheel()
    targetCheese = target.getCheeseWheel()
    assert targetCheese.getId() == 1
    count = 0
    for location in shelf.getLocations():
        if location.hasCheeseWheel():
            count += 1
    assert count == 1

def testAssignCheeseWheelMoveSameShelf(populatedController, mw):
    # Arrange
    controller, shelf, wheels = populatedController

    wheel = wheels[0]
    for loc in shelf.getLocations():
        if loc.getColumn() == 2 and loc.getRow() == 1:
            wheel.setLocation(loc)
            break

    # Act
    controller.assignCheeseWheelToShelf(1, "A12", 1, 1)

    # Assert
    target = next(loc for loc in shelf.getLocations() if loc.getColumn() == 1 and loc.getRow() == 1)

    assert target.hasCheeseWheel()
    assert target.getCheeseWheel().getId() == 1

    count = 0
    for location in shelf.getLocations():
        if location.hasCheeseWheel():
            count += 1
    assert count == 1

def testAssignCheeseWheelMoveDifferentShelf(populatedController, mw):
    # Arrange
    controller, shelf, wheels = populatedController

    wheel = wheels[0]
    for loc in shelf.getLocations():
        if loc.getColumn() == 2 and loc.getRow() == 1:
            wheel.setLocation(loc)
            break

    shelfB = mw(Shelf, id="B11", cheECSEManager=controller.cheECSEManager)
    mw(ShelfLocation, column=1, row=1, shelf=shelfB.model)
    
    # Act
    controller.assignCheeseWheelToShelf(1, "B11", 1, 1)

    # Assert
    locB = next(loc for loc in shelfB.getLocations() if loc.getColumn() == 1 and loc.getRow() == 1)

    assert locB.hasCheeseWheel()
    assert locB.getCheeseWheel().getId() == 1

    countA = 0
    for location in shelf.getLocations():
        if location.hasCheeseWheel():
            countA += 1
    assert countA == 0

    countB = 0
    for location in shelfB.getLocations():
        if location.hasCheeseWheel():
            countB += 1
    assert countB == 1

def testAssignCheeseWheelMissing(populatedController, mw):
    # Arrange
    controller, shelf, _ = populatedController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.assignCheeseWheelToShelf(10, "A12", 2, 1)

    # Assert
    assert str(errorInfo.value) == "The cheese wheel with id 10 does not exist."
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 0

def testAssignCheeseWheelSpoiled(populatedController, mw):
    # Arrange
    controller, shelf, wheels = populatedController
    wheels[1].setIsSpoiled(True)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.assignCheeseWheelToShelf(2, "A12", 2, 1)

    # Assert
    assert str(errorInfo.value) == "Cannot place a spoiled cheese wheel on a shelf."
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 0

def testAssignCheeseWheelInvalidLocation(populatedController, mw):
    # Arrange
    controller, shelf, _ = populatedController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.assignCheeseWheelToShelf(1, "A12", 6, 1)

    # Assert
    assert str(errorInfo.value) == "The shelf location does not exist."
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 0

def testAssignCheeseWheelOccupied(populatedController, mw):
    # Arrange
    controller, shelf, wheels = populatedController
    wheel = wheels[0]
    for loc in shelf.getLocations():
        if loc.getColumn() == 2 and loc.getRow() == 1:
            wheel.setLocation(loc)
            break

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.assignCheeseWheelToShelf(3, "A12", 2, 1)

    # Assert
    assert str(errorInfo.value) == "The shelf location is already occupied."

    target = next(loc for loc in shelf.getLocations() if loc.getColumn() == 2 and loc.getRow() == 1)
    assert target.hasCheeseWheel()
    assert target.getCheeseWheel().getId() == 1
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 1