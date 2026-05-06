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
        User.usersByEmail.clear()
        Farmer.usersByEmail.clear()
        Shelf.shelfsById.clear()
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

def testDisplayCheeseWheels(controllerWithCheese, mw):
    # Arrange
    controller, purchase = controllerWithCheese

    shelfA = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)
    for column in range(1, 6):
        for row in range(1, 3):
            mw(ShelfLocation, column=column, row=row, shelf=shelfA.model)

    cheeseWheel2 = None
    cheeseWheel3 = None
    for cw in mw(controller.cheECSEManager).getCheeseWheels():
        if cw.getId() == 2:
            cheeseWheel2 = cw
        if cw.getId() == 3:
            cheeseWheel3 = cw
            break

    target1 = next(loc for loc in shelfA.getLocations() if loc.getColumn() == 2 and loc.getRow() == 1)
    target2 = next(loc for loc in shelfA.getLocations() if loc.getColumn() == 1 and loc.getRow() == 1)
    target1.setCheeseWheel(cheeseWheel2)
    target2.setCheeseWheel(cheeseWheel3)

    cheesy = mw(WholesaleCompany, name="Cheesy Bites", address="112 Av", cheECSEManager=controller.cheECSEManager)

    order = mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=5, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2026, 4, 4), company=cheesy.model)

    for cw in purchase.getCheeseWheels():
        if not cw.getIsSpoiled():
            order.addCheeseWheel(cw.model)

    # Act
    tos = controller.displayCheeseWheels()

    # Assert
    assert len(tos) == 5
    byId = {mw(to).getId(): mw(to) for to in tos}
    assert byId[1].getId() == 1 and byId[1].getMonthsAged() == MaturationPeriod.Six and byId[1].getIsSpoiled() and byId[1].getPurchaseDate() == datetime(2025, 4, 4) and byId[1].getShelfID() is None and byId[1].getColumn() == -1 and byId[1].getRow() == -1 and not byId[1].getIsOrdered()
    assert byId[2].getId() == 2 and byId[2].getMonthsAged() == MaturationPeriod.Six and not byId[2].getIsSpoiled() and byId[2].getPurchaseDate() == datetime(2025, 4, 4) and byId[2].getShelfID() == "A12" and byId[2].getColumn() == 2 and byId[2].getRow() == 1 and byId[2].getIsOrdered()
    assert byId[3].getId() == 3 and byId[3].getMonthsAged() == MaturationPeriod.Six and not byId[3].getIsSpoiled() and byId[3].getPurchaseDate() == datetime(2025, 4, 4) and byId[3].getShelfID() == "A12" and byId[3].getColumn() == 1 and byId[3].getRow() == 1 and byId[3].getIsOrdered()
    assert byId[4].getId() == 4 and byId[4].getMonthsAged() == MaturationPeriod.Six and not byId[4].getIsSpoiled() and byId[4].getPurchaseDate() == datetime(2025, 4, 4) and byId[4].getShelfID() is None and byId[4].getColumn() == -1 and byId[4].getRow() == -1 and byId[4].getIsOrdered()
    assert byId[5].getId() == 5 and byId[5].getMonthsAged() == MaturationPeriod.Six and not byId[5].getIsSpoiled() and byId[5].getPurchaseDate() == datetime(2025, 4, 4) and byId[5].getShelfID() is None and byId[5].getColumn() == -1 and byId[5].getRow() == -1 and byId[5].getIsOrdered()
    assert mw(controller.cheECSEManager).numberOfCheeseWheels() == 5