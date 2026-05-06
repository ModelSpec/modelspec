from datetime import datetime

import pytest

@pytest.fixture
def controllerWithCheese(modelingTool, mw):
    global MaturationPeriod, Shelf, ShelfLocation, WholesaleCompany, Order, Purchase, CheeseWheel
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Shelf, ShelfLocation, Transaction, CheeseWheel, User, Farmer, WholesaleCompany, Purchase, Order

        Shelf.shelfsById.clear()
        ShelfLocation.nextId = 1
        Transaction.nextId = 1
        CheeseWheel.nextId = 1
        User.usersByEmail.clear()
        Farmer.usersByEmail.clear()
        WholesaleCompany.wholesalecompanysByName.clear()
        MaturationPeriod = CheeseWheel.MaturationPeriod

    else:
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Shelf, ShelfLocation, Transaction, CheeseWheel, User, Farmer, WholesaleCompany, Purchase, MaturationPeriod, Order

    controller = CheECSEManagerController()

    farmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")

    purchase = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase.setId(1)

    for i in range(5):
        isSpoiled = True if i == 0 else False
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=isSpoiled, purchase=purchase.model)
        cw.setId(i + 1)

    yield controller, purchase, purchase.getCheeseWheels(), farmer

@pytest.mark.parametrize(
    "wheelId, updatedIsSpoiled, updatedMonthsAged",
    [(1, False, "ThirtySix"), (2, True, "Twelve")],
)
def testUpdateCheeseWheelSuccess(mw, controllerWithCheese, wheelId, updatedIsSpoiled, updatedMonthsAged):
    # Arrange
    controller, purchase, _, _ = controllerWithCheese

    # Act
    controller.updateCheeseWheel(wheelId, updatedMonthsAged, updatedIsSpoiled)

    # Assert
    cheese = next(cw for cw in purchase.getCheeseWheels() if cw.getId() == wheelId)
    assert cheese.getIsSpoiled() == updatedIsSpoiled
    assert cheese.getMonthsAged() == getattr(MaturationPeriod, updatedMonthsAged)
    assert cheese.getPurchase().getId() == 1
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5
    assert purchase.numberOfCheeseWheels() == 5

def testUpdateCheeseWheelSpoilOnShelf(mw, controllerWithCheese):
    # Arrange
    controller, purchase, wheels, _ = controllerWithCheese

    shelf = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)
    for column in range(1, 6):
        for row in range(1, 3):
            mw(ShelfLocation, column=column, row=row, shelf=shelf.model)

    target = next(loc for loc in shelf.getLocations() if loc.getColumn() == 2 and loc.getRow() == 1)
    target.setCheeseWheel(wheels[1].model)

    # Act
    controller.updateCheeseWheel(2, "Six", True)

    # Assert
    cheese = next(cw for cw in purchase.getCheeseWheels() if cw.getId() == 2)
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5
    assert cheese.getIsSpoiled()
    assert cheese.getMonthsAged() == MaturationPeriod.Six
    assert cheese.getPurchase().getId() == 1
    assert purchase.numberOfCheeseWheels() == 5
    
    assert not cheese.hasLocation()
    assert len([loc for loc in shelf.getLocations() if loc.hasCheeseWheel()]) == 0

def testUpdateCheeseWheelSpoilInOrder(mw, controllerWithCheese):
    # Arrange
    controller, purchase, _, _ = controllerWithCheese

    company = mw(WholesaleCompany, name="Cheesy Bites", address="112 Av", cheECSEManager=controller.cheECSEManager)

    order = mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=5, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2025, 10, 10), company=company.model)
    order.setId(2)

    for cw in purchase.getCheeseWheels():
        if not cw.getIsSpoiled() and order.numberOfCheeseWheels() < order.getNrCheeseWheels():
            order.addCheeseWheel(cw.model)

    # Act
    controller.updateCheeseWheel(3, "Six", True)

    # Arrange
    cheese = next(cw for cw in purchase.getCheeseWheels() if cw.getId() == 3)
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5
    assert cheese.getIsSpoiled()
    assert cheese.getMonthsAged() == MaturationPeriod.Six
    assert cheese.getPurchase().getId() == 1
    assert purchase.numberOfCheeseWheels() == 5
    assert cheese.hasOrder() is False
    assert order.numberOfCheeseWheels() == 3

def testUpdateCheeseWheelIncreaseMonthsRemovesFromOrder(mw, controllerWithCheese):
    # Arrange
    controller, purchase, _, _ = controllerWithCheese
    
    company = mw(WholesaleCompany, name="Cheesy Bites", address="112 Av", cheECSEManager=controller.cheECSEManager)

    order = mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=5, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2025, 10, 10), company=company.model)
    order.setId(2)

    for cw in purchase.getCheeseWheels():
        if not cw.getIsSpoiled() and order.numberOfCheeseWheels() < order.getNrCheeseWheels():
            order.addCheeseWheel(cw.model)

    # Act
    controller.updateCheeseWheel(4, "Twelve", False)

    # Assert
    cheese = next(cw for cw in purchase.getCheeseWheels() if cw.getId() == 4)
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5
    assert not cheese.getIsSpoiled()
    assert cheese.getMonthsAged() == MaturationPeriod.Twelve
    assert cheese.getPurchase().getId() == 1
    assert purchase.numberOfCheeseWheels() == 5
    assert cheese.hasOrder() is False
    assert order.numberOfCheeseWheels() == 3

def testUpdateCheeseWheelInvalidMonths(controllerWithCheese):
    # Arrange
    controller, purchase, _, _ = controllerWithCheese

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateCheeseWheel(2, "notALiteral", True)

    # Assert
    assert str(errorInfo.value) == "The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix."
    cheese = next(cw for cw in purchase.getCheeseWheels() if cw.getId() == 2)
    assert not cheese.getIsSpoiled()
    assert cheese.getMonthsAged() == MaturationPeriod.Six
    assert cheese.getPurchase().getId() == 1
    assert purchase.numberOfCheeseWheels() == 5

@pytest.mark.parametrize(
    "updatedIsSpoiled, updatedMonthsAged, originalId",
    [(False, "Twelve", 6), (False, "TwentyFour", 6), (True, "Six", 7)],
)
def testUpdateCheeseWheelDecreaseMonths(mw, controllerWithCheese, updatedIsSpoiled, updatedMonthsAged, originalId):
    # Arrange
    controller, _, _, farmer = controllerWithCheese

    purchase2 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase2.setId(2)

    id = 6
    for _ in range(2):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.ThirtySix, isSpoiled=False, purchase=purchase2.model)
        cw.setId(id)
        id += 1

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateCheeseWheel(originalId, updatedMonthsAged, updatedIsSpoiled)

    # Assert
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 7
    assert str(errorInfo.value) == "Cannot decrease the monthsAged of a cheese wheel."
    cheese = next(cw for cw in mw(controller.cheECSEManager).getCheeseWheels() if cw.getId() == originalId)
    assert not cheese.getIsSpoiled()
    assert cheese.getMonthsAged() == MaturationPeriod.ThirtySix
    assert cheese.getPurchase().getId() == 2
    assert purchase2.numberOfCheeseWheels() == 2

def testUpdateCheeseWheelMissing(mw, controllerWithCheese):
    # Arrange
    controller, purchase, _, _ = controllerWithCheese

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateCheeseWheel(30, "Twelve", False)

    # Assert
    assert str(errorInfo.value) == "The cheese wheel with id 30 does not exist."
    assert purchase.numberOfCheeseWheels() == 5
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5
    cheese = None
    for cw in mw(controller.cheECSEManager).getCheeseWheels():
        if cw.getId() == 30:
            cheese = cw
    assert cheese is None