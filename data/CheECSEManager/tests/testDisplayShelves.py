from datetime import datetime

import pytest

@pytest.fixture
def controllerWithShelves(modelingTool, mw):
    global MaturationPeriod
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

    shelfA = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)
    for column in range(1, 6):
        mw(ShelfLocation, column=column, row=1, shelf=shelfA.model)
    shelfB = mw(Shelf, id="B16", cheECSEManager=controller.cheECSEManager)
    for column in range(1, 7):
        for row in range(1, 3):
            mw(ShelfLocation, column=column, row=row, shelf=shelfB.model)

    farmerA = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmerA.setName("Farmer A")

    purchase1 = mw(Purchase, transactionDate=datetime(2025, 9, 1), cheECSEManager=controller.cheECSEManager, farmer=farmerA.model)
    purchase2 = mw(Purchase, transactionDate=datetime(2025, 8, 15), cheECSEManager=controller.cheECSEManager, farmer=farmerA.model)

    id = 1
    for _ in range(2):
        isSpoiled = True if id == 2 else False
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=isSpoiled, purchase=purchase1.model)
        cw.setId(id)
        id += 1
    for _ in range(3):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Twelve, isSpoiled=False, purchase=purchase2.model)
        cw.setId(id)
        id += 1

    cw1 = None
    cw2 = None
    cw3 = None
    for cw in mw(controller.cheECSEManager).getCheeseWheels():
        if cw.getId() == 1:
            cw1 = cw
        if cw.getId() == 2:
            cw2 = cw
        if cw.getId() == 3:
            cw3 = cw

    for loc in shelfA.getLocations():
        if loc.getColumn() == 1:
            loc.setCheeseWheel(cw1.model)
        if loc.getColumn() == 3:
            loc.setCheeseWheel(cw2.model)
        if loc.getColumn() == 4:
            loc.setCheeseWheel(cw3.model)

    yield controller

def testDisplayShelvesSuccess(controllerWithShelves, mw):
    # Act
    shelfTos = controllerWithShelves.displayShelves()

    # Assert
    assert len(shelfTos) == 2
    ids = {mw(to).getShelfID() for to in shelfTos}
    assert ids == {"A12", "B16"}

    shelfA = next(mw(to) for to in shelfTos if mw(to).getShelfID() == "A12")
    assert set(shelfA.getColumnNrs()) == {1, 2, 3, 4, 5}
    assert set(shelfA.getRowNrs()) == {1}
    assert shelfA.getCheeseWheelIDs() == [1, None, 2, 3, None]
    assert shelfA.getMonthsAgeds() == [
        MaturationPeriod.Six,
        None,
        MaturationPeriod.Six,
        MaturationPeriod.Twelve,
        None,
    ]

    shelfB = next(mw(to) for to in shelfTos if mw(to).getShelfID() == "B16")
    assert set(shelfB.getColumnNrs()) == {1, 2, 3, 4, 5, 6}
    assert set(shelfB.getRowNrs()) == {1, 2}
    assert all(cw_id is None for cw_id in shelfB.getCheeseWheelIDs())
