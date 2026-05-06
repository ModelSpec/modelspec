from datetime import datetime

import pytest

@pytest.fixture
def controllerWithShelf(modelingTool, mw):
    global MaturationPeriod, Purchase, CheeseWheel, Order
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Transaction, CheeseWheel, User, Farmer, WholesaleCompany, Purchase, Order

        Transaction.nextId = 1
        CheeseWheel.nextId = 1
        User.usersByEmail.clear()
        Farmer.usersByEmail.clear()
        WholesaleCompany.wholesalecompanysByName.clear()
        MaturationPeriod = CheeseWheel.MaturationPeriod

    else:
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Transaction, CheeseWheel, User, Farmer, WholesaleCompany, Purchase, MaturationPeriod, Order

    controller = CheECSEManagerController()

    cheesy = mw(WholesaleCompany, name="Cheesy Bites", address="112 Av", cheECSEManager=controller.cheECSEManager)

    farmer = mw(Farmer,  email="farmer@cheesy.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")

    yield controller, farmer, cheesy

@pytest.mark.parametrize(
    "transactionDate, nrCheeseWheels, monthsAged, deliveryDate, company, addedCheeseWheels, purchaseId",
    [
        (datetime(2025, 9, 1), 22, "Twelve", datetime(2026, 5, 1), "Cheesy Bites", 5, 1),
        (datetime(2025, 9, 1), 10, "Six", datetime(2025, 11, 1), "Cheesy Bites", 1, 3),
        (datetime(2025, 9, 1), 5, "TwentyFour", datetime(2027, 5, 1), "Cheesy Bites", 5, 4),
        (datetime(2025, 9, 1), 5, "ThirtySix", datetime(2028, 5, 1), "Cheesy Bites", 0, -1),
    ],
)
def testSellCheeseWheelsSuccess(mw, controllerWithShelf, transactionDate, nrCheeseWheels, monthsAged, deliveryDate, company, addedCheeseWheels, purchaseId):
    # Arrange
    controller, farmer, cheesy = controllerWithShelf

    purchase1 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase1.setId(1)
    purchase2 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase2.setId(2)
    purchase3 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase3.setId(3)
    purchase4 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase4.setId(4)

    id = 1
    for _ in range(5):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Twelve, isSpoiled=False, purchase=purchase1.model)
        cw.setId(id)
        id += 1
    for _ in range(10):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase2.model)
        cw.setId(id)
        id += 1
    cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase3.model)
    cw.setId(id)
    id += 1
    for _ in range(10):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.TwentyFour, isSpoiled=False, purchase=purchase4.model)
        cw.setId(id)
        id += 1

    order = mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=10, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2025, 12, 1), company=cheesy.model)
    order.setId(5)

    for cw in purchase2.getCheeseWheels():
        if not cw.getIsSpoiled() and order.numberOfCheeseWheels() < order.getNrCheeseWheels():
            order.addCheeseWheel(cw.model)

    # Act
    controller.sellCheeseWheelsToWholesaleCompany(company, transactionDate, nrCheeseWheels, monthsAged, deliveryDate)

    # Assert
    orders = [tx for tx in mw(controller.cheECSEManager).getTransactions() if isinstance(tx.model, Order)]
    assert len(orders) == 2
    newOrder = orders[1]
    assert newOrder.getId() == 6
    assert newOrder.getTransactionDate() == transactionDate
    assert newOrder.getNrCheeseWheels() == nrCheeseWheels
    assert newOrder.getMonthsAged() == getattr(MaturationPeriod, monthsAged)
    assert newOrder.getDeliveryDate() == deliveryDate
    assert newOrder.getCompany() == cheesy
    assert newOrder.numberOfCheeseWheels() == addedCheeseWheels
    if purchaseId > 0:
        assert newOrder.numberOfCheeseWheels() == addedCheeseWheels
    else:
        assert newOrder.numberOfCheeseWheels() == 0

@pytest.mark.parametrize(
    "transactionDate, nrCheeseWheels, monthsAged, deliveryDate, company, addedCheeseWheels, purchaseId",
    [
        (datetime(2025, 11, 1), 22, "Twelve", datetime(2026, 5, 1), "Cheesy Bites", 4, 1),
        (datetime(2025, 11, 1), 10, "Six", datetime(2025, 11, 1), "Cheesy Bites", 0, -1),
        (datetime(2025, 11, 1), 5, "TwentyFour", datetime(2027, 5, 1), "Cheesy Bites", 5, 3),
    ],
)
def testSellCheeseWheelsSuccessWithSpoiled(mw, controllerWithShelf, transactionDate, nrCheeseWheels, monthsAged, deliveryDate, company, addedCheeseWheels, purchaseId):
    # Arrange
    controller, farmer, cheesy = controllerWithShelf

    purchase1 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase1.setId(1)
    purchase2 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase2.setId(2)
    purchase3 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase3.setId(3)

    id = 1
    for _ in range(5):
        isSpoiled = True if id == 1 else False
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Twelve, isSpoiled=isSpoiled, purchase=purchase1.model)
        cw.setId(id)
        id += 1
    for _ in range(2):
        isSpoiled = True if id == 6 else False
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=isSpoiled, purchase=purchase2.model)
        cw.setId(id)
        id += 1
    for _ in range(10):
        isSpoiled = True if id == 10 else False
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.TwentyFour, isSpoiled=isSpoiled, purchase=purchase3.model)
        cw.setId(id)
        id += 1

    order = mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=10, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2025, 12, 1), company=cheesy.model)
    order.setId(4)

    for cw in purchase2.getCheeseWheels():
        if not cw.getIsSpoiled() and order.numberOfCheeseWheels() < order.getNrCheeseWheels():
            order.addCheeseWheel(cw.model)

    # Act
    controller.sellCheeseWheelsToWholesaleCompany(company, transactionDate, nrCheeseWheels, monthsAged, deliveryDate)

    # Assert
    orders = [tx for tx in mw(controller.cheECSEManager).getTransactions() if isinstance(tx.model, Order)]
    assert len(orders) == 2
    newOrder = orders[1]
    assert newOrder.getId() == 5
    assert newOrder.getTransactionDate() == transactionDate
    assert newOrder.getNrCheeseWheels() == nrCheeseWheels
    assert newOrder.getMonthsAged() == getattr(MaturationPeriod, monthsAged)
    assert newOrder.numberOfCheeseWheels() == addedCheeseWheels
    assert newOrder.getCompany() == cheesy
    if purchaseId > 0:
        assert newOrder.numberOfCheeseWheels() == addedCheeseWheels
    else:
        assert newOrder.numberOfCheeseWheels() == 0

@pytest.mark.parametrize(
    "transactionDate, nrCheeseWheels, monthsAged, deliveryDate, company, addedCheeseWheels, purchaseId",
    [
        (datetime(2025, 9, 1), 22, "Six", datetime(2025, 11, 1), "Cheesy Bites", 1, 2),
        (datetime(2025, 9, 1), 10, "ThirtySix", datetime(2028, 5, 1), "Cheesy Bites", 1, 4),
    ],
)
def testSellCheeseWheelsSuccessWithVariedMonths(mw, controllerWithShelf, transactionDate, nrCheeseWheels, monthsAged, deliveryDate, company, addedCheeseWheels, purchaseId):
    # Arrange
    controller, farmer, cheesy = controllerWithShelf

    purchase1 = mw(Purchase, transactionDate=datetime(2025, 8, 1), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase1.setId(1)
    purchase2 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase2.setId(2)
    purchase3 = mw(Purchase, transactionDate=datetime(2025, 8, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase3.setId(3)
    purchase4 = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase4.setId(4)

    id = 1
    for _ in range(3):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase1.model)
        cw.setId(id)
        id += 1
    for _ in range(11):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase2.model)
        cw.setId(id)
        id += 1
    for _ in range(3):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.ThirtySix, isSpoiled=False, purchase=purchase3.model)
        cw.setId(id)
        id += 1
    cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.ThirtySix, isSpoiled=False, purchase=purchase4.model)
    cw.setId(id)

    order = mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=10, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2025, 12, 1), company=cheesy.model)
    order.setId(5)

    for cw in purchase2.getCheeseWheels():
        if not cw.getIsSpoiled() and order.numberOfCheeseWheels() < order.getNrCheeseWheels():
            order.addCheeseWheel(cw.model)

    # Act
    controller.sellCheeseWheelsToWholesaleCompany(company, transactionDate, nrCheeseWheels, monthsAged, deliveryDate)

    # Assert
    orders = [tx for tx in mw(controller.cheECSEManager).getTransactions() if isinstance(tx.model, Order)]
    assert len(orders) == 2
    newOrder = orders[1]
    assert newOrder.getId() == 6
    assert newOrder.getTransactionDate() == transactionDate
    assert newOrder.getNrCheeseWheels() == nrCheeseWheels
    assert newOrder.getMonthsAged() == getattr(MaturationPeriod, monthsAged)
    assert newOrder.numberOfCheeseWheels() == addedCheeseWheels
    assert newOrder.getCompany() == cheesy
    count = 0

    for cw in newOrder.getCheeseWheels():
        if cw.getPurchase().getId() == purchaseId:
            count += 1
    assert count == addedCheeseWheels

@pytest.mark.parametrize(
    "nrCheeseWheels, monthsAged, company, deliveryDate, errorMessage",
    [
        (0, "Twelve", "Cheesy Bites", datetime(2026, 11, 1), "nrCheeseWheels must be greater than zero."),
        (-5, "Six", "Cheesy Bites", datetime(2026, 5, 1), "nrCheeseWheels must be greater than zero."),
        (22, "Invalid", "Cheesy Bites", datetime(2026, 11, 1), "The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix."),
        (22, "Twelve", "Dairy Something", datetime(2026, 11, 1), "The wholesale company Dairy Something does not exist."),
        (22, "Twelve", "Cheesy Bites", datetime(2025, 10, 1), "The delivery date must be on or after the transaction date."),
    ],
)
def testSellCheeseWheelsInvalid(mw, controllerWithShelf, nrCheeseWheels, monthsAged, company, deliveryDate, errorMessage):
    # Arrange
    controller, _, _ = controllerWithShelf

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.sellCheeseWheelsToWholesaleCompany(company, datetime(2025, 11, 1), nrCheeseWheels, monthsAged, deliveryDate)

    # Assert
    assert str(errorInfo.value) == errorMessage
    orders = [tx for tx in mw(controller.cheECSEManager).getTransactions() if isinstance(tx.model, Order)]
    assert len(orders) == 0