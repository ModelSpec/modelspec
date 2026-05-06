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
        from ..ecore.generated_model_layer import Shelf, ShelfLocation, Transaction, CheeseWheel, User, Farmer, MaturationPeriod, Purchase

    controller = CheECSEManagerController()

    shelfA = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)

    for column in range(1, 6):
        mw(ShelfLocation, column=column, row=1, shelf=shelfA.model)

    shelfB = mw(Shelf, id="B23", cheECSEManager=controller.cheECSEManager)

    for column in range(1, 7):
        for row in range(1, 3):
            mw(ShelfLocation, column=column, row=row, shelf=shelfB.model)

    farmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")

    purchase = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase.setId(1)

    for i in range(2):
        cw = mw(CheeseWheel, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase.model, cheECSEManager=controller.cheECSEManager)
        cw.setId(i + 1)
    
    yield controller

def testDeleteShelfSuccess(controllerWithShelves, mw):
    # Act
    controllerWithShelves.deleteShelf("A12")

    # Arrange
    controllerWithShelves.cheECSEManager = mw(controllerWithShelves.cheECSEManager)

    shelves = controllerWithShelves.cheECSEManager.getShelves()
    assert len(shelves) == 1

    remainingShelf = None
    for sh in shelves:
        if sh.getId() == "B23":
            remainingShelf = sh

    assert remainingShelf is not None
    assert remainingShelf.numberOfLocations() == 12
    count = 0
    for shelf in shelves:
        for loc in shelf.getLocations():
            if loc.getShelf().getId() == "A12":
                count += 1
    assert count == 0

@pytest.mark.parametrize("shelfId", ["C45", "Z99"])
def testDeleteShelfDoesNotExist(controllerWithShelves, shelfId, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithShelves.deleteShelf(shelfId)

    # Arrange
    controllerWithShelves.cheECSEManager = mw(controllerWithShelves.cheECSEManager)

    assert str(errorInfo.value) == f"The shelf {shelfId} does not exist."
    shelves = controllerWithShelves.cheECSEManager.getShelves()
    assert len(shelves) == 2

    shelfA = None
    shelfB = None
    deletedShelf = None
    for sh in shelves:
        if sh.getId() == "A12":
            shelfA = sh
        if sh.getId() == "B23":
            shelfB = sh
        if sh.getId() == shelfId:
            deletedShelf = sh
    assert shelfA is not None
    assert shelfB is not None
    assert deletedShelf is None

    assert shelfA.numberOfLocations() == 5
    assert shelfB.numberOfLocations() == 12

    count = 0
    for s in shelves:
        for loc in s.getLocations():
            if loc.getShelf().getId() == shelfId:
                count += 1
    assert count == 0

def testDeleteShelfWithCheeseWheel(controllerWithShelves, mw):
    # Arrange
    controllerWithShelves.cheECSEManager = mw(controllerWithShelves.cheECSEManager)

    shelfB = None
    for sh in controllerWithShelves.cheECSEManager.getShelves():
        if sh.getId() == "B23":
            shelfB = sh
            break

    targetLocation = None
    for loc in shelfB.getLocations():
        if loc.getColumn() == 1 and loc.getRow() == 1:
            targetLocation = loc
            break
    
    cheeseWheel = None
    for cw in controllerWithShelves.cheECSEManager.getCheeseWheels():
        if cw.getId() == 1:
            cheeseWheel = cw
    targetLocation.setCheeseWheel(cheeseWheel)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithShelves.deleteShelf("B23")

    # Arrange
    assert str(errorInfo.value) == "Cannot delete a shelf that contains cheese wheels."
    shelvesAssert = controllerWithShelves.cheECSEManager.getShelves()
    assert len(shelvesAssert) == 2

    # shelfA = Shelf.getWithId("A12")
    shelfA = None
    shelfB = None
    for sh in shelvesAssert:
        if sh.getId() == "A12":
            shelfA = sh
        if sh.getId() == "B23":
            shelfB = sh
    assert shelfA is not None
    assert shelfB is not None

    assert shelfA.numberOfLocations() == 5
    assert shelfB.numberOfLocations() == 12

    cw1 = None
    cw2 = None
    for cw in controllerWithShelves.cheECSEManager.getCheeseWheels():
        if cw.getId() == 1:
            cw1 = cw
        if cw.getId() == 2:
            cw2 = cw

    assert cw1.getMonthsAged() == MaturationPeriod.Six
    assert cw2.getMonthsAged() == MaturationPeriod.Six

    assert not cw1.getIsSpoiled()
    assert not cw2.getIsSpoiled()

    assert cw1.getPurchase().getId() == 1
    assert cw2.getPurchase().getId() == 1

    purchase1 = cw1.getPurchase()
    assert purchase1 is not None

    cw1_location = cw1.getLocation()
    assert cw1_location.getShelf().getId() == "B23"
    assert cw1_location.getColumn() == 1
    assert cw1_location.getRow() == 1

    assert cw2.getPurchase() is not None
    assert not cw2.hasLocation() 