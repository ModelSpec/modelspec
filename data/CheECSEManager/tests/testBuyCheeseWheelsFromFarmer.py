from datetime import datetime

import pytest

@pytest.fixture
def populatedController(modelingTool, mw):
    global MaturationPeriod
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Transaction, CheeseWheel, User, Farmer, Purchase

        Transaction.nextId = 1
        CheeseWheel.nextId = 1
        User.usersByEmail.clear()
        Farmer.usersByEmail.clear()
        MaturationPeriod = CheeseWheel.MaturationPeriod

    else:
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Transaction, CheeseWheel, User, Farmer, Purchase, MaturationPeriod

    controller = CheECSEManagerController()

    farmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")

    purchase = mw(Purchase, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)

    for i in range(5):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase.model)
        cw.setId(i + 1)

    yield controller

@pytest.mark.parametrize(
    "purchaseDate, nrCheeseWheels, monthsAged, farmerEmail, totalCheeseWheels",
    [
        (datetime(2025, 11, 1), 5, "Twelve", "farmer@cheecse.fr", 10),
        (datetime(2025, 11, 2), 3, "Six", "farmer@cheecse.fr", 8),
        (datetime(2025, 11, 3), 10, "TwentyFour", "farmer@cheecse.fr", 15),
        (datetime(2025, 11, 4), 8, "ThirtySix", "farmer@cheecse.fr", 13),
    ],
)
def testBuyCheeseWheelsSuccess(mw, populatedController, purchaseDate, nrCheeseWheels, monthsAged, farmerEmail, totalCheeseWheels):
    # Act
    populatedController.buyCheeseWheelsFromFarmer(farmerEmail, purchaseDate, nrCheeseWheels, monthsAged)

    # Assert
    populatedController.cheECSEManager = mw(populatedController.cheECSEManager)

    purchases = populatedController.cheECSEManager.getTransactions()
    assert len(purchases) == 2

    purchase = None
    for p in purchases:
        if p.getId() == 2:
            purchase = p
    assert purchase is not None
    assert purchase.getTransactionDate() == purchaseDate
    assert purchase.getFarmer().getEmail() == farmerEmail
    assert purchase.numberOfCheeseWheels() == nrCheeseWheels
    assert all(cw.getMonthsAged() == getattr(MaturationPeriod, monthsAged) for cw in purchase.getCheeseWheels())
    assert populatedController.cheECSEManager.numberOfCheeseWheels() == totalCheeseWheels

@pytest.mark.parametrize(
    "nrCheeseWheels, monthsAged, farmerEmail, errorMessage",
    [
        (0, "Twelve", "farmer@cheecse.fr", "nrCheeseWheels must be greater than zero."),
        (-5, "Twelve", "farmer@cheecse.fr", "nrCheeseWheels must be greater than zero."),
        (5, "notALiteral", "farmer@cheecse.fr", "The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix."),
        (5, "Twelve", "farmer@cheecse.ca", "The farmer with email farmer@cheecse.ca does not exist."),
        (5, "Twelve", "manager@cheecse.com", "The farmer with email manager@cheecse.com does not exist."),
    ],
)
def testBuyCheeseWheelsInvalid(mw, populatedController, nrCheeseWheels, monthsAged, farmerEmail, errorMessage):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        populatedController.buyCheeseWheelsFromFarmer(farmerEmail, datetime(2025, 11, 1), nrCheeseWheels, monthsAged)

    # Assert
    populatedController.cheECSEManager = mw(populatedController.cheECSEManager)

    assert str(errorInfo.value) == errorMessage
    purchases = populatedController.cheECSEManager.getTransactions()
    assert len(purchases) == 1
    assert purchases[0].getTransactionDate() == datetime(2025, 4, 4)
    assert purchases[0].numberOfCheeseWheels() == 5
    assert all(cw.getMonthsAged() == MaturationPeriod.Six for cw in purchases[0].getCheeseWheels())
    assert purchases[0].getFarmer().getEmail() == "farmer@cheecse.fr"
    assert populatedController.cheECSEManager.numberOfCheeseWheels() == 5

    purchase2 = None
    for p in purchases:
        if p.getId() == 2:
            purchase2 = p
            break
    assert purchase2 is None