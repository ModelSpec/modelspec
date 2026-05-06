from datetime import datetime

import pytest

@pytest.fixture
def controllerWithCheese(modelingTool, mw):
    global Order, MaturationPeriod, Shelf, ShelfLocation, WholesaleCompany
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Transaction, CheeseWheel, User, Farmer, WholesaleCompany, Order, Purchase, Shelf, ShelfLocation

        MaturationPeriod = CheeseWheel.MaturationPeriod
        Transaction.nextId = 1
        CheeseWheel.nextId = 1
        Shelf.shelfsById.clear()
        User.usersByEmail.clear()
        Farmer.usersByEmail.clear()
        WholesaleCompany.wholesalecompanysByName.clear()
        
    else: 
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Transaction, CheeseWheel, User, Farmer, WholesaleCompany, MaturationPeriod, Order, Purchase, Shelf, ShelfLocation
   
    controller = CheECSEManagerController()

    farmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")

    purchase = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase.setId(1)

    for i in range(5):
        isSpoiled = False if i != 0 else True
        cw = mw(CheeseWheel, monthsAged=MaturationPeriod.Six, isSpoiled=isSpoiled, purchase=purchase.model, cheECSEManager=controller.cheECSEManager)
        cw.setId(i + 1)

    yield controller, purchase

def testDisplayCheeseWheelBase(controllerWithCheese, mw):
    # Arrange
    controller, _ = controllerWithCheese
    # Act
    display = controller.displayCheeseWheel(1)

    # Assert
    display = mw(display)
    assert display.getId() == 1
    assert display.getMonthsAged() == MaturationPeriod.Six
    assert display.getIsSpoiled()
    assert display.getShelfID() is None
    assert display.getColumn() == -1
    assert display.getRow() == -1
    assert not display.getIsOrdered()
    assert display.getPurchaseDate() == datetime(2025, 4, 4)
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5

def testDisplayCheeseWheelOnShelfAndOrder(controllerWithCheese, mw):
    # Arrange
    controller, purchase = controllerWithCheese

    shelfA = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)
    for column in range(1, 6):
        for row in range(1, 3):
            mw(ShelfLocation, column=column, row=row, shelf=shelfA.model)

    cheeseWheel = None
    for cw in mw(controller.cheECSEManager).getCheeseWheels():
        if cw.getId() == 2:
            cheeseWheel = cw
            break

    target = next(loc for loc in shelfA.getLocations() if loc.getColumn() == 2 and loc.getRow() == 1)
    target.setCheeseWheel(cheeseWheel)

    cheesy = mw(WholesaleCompany, name="Cheesy Bites", address="112 Av", cheECSEManager=controller.cheECSEManager)

    order = mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=5, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2026, 4, 4), company=cheesy.model)

    for cw in purchase.getCheeseWheels():
        if not cw.getIsSpoiled():
            order.addCheeseWheel(cw.model)

    # Act
    display = controller.displayCheeseWheel(2)

    # Assert
    display = mw(display)
    assert display.getId() == 2
    assert display.getMonthsAged() == MaturationPeriod.Six
    assert display.getShelfID() == "A12"
    assert not display.getIsSpoiled()
    assert display.getPurchaseDate() == datetime(2025, 4, 4)
    assert display.getColumn() == 2
    assert display.getRow() == 1
    assert display.getIsOrdered()
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5

def testDisplayCheeseWheelMissing(controllerWithCheese, mw):
    # Arrange
    controller, _ = controllerWithCheese

    # Act
    result = controller.displayCheeseWheel(10)

    # Assert
    assert result is None
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5