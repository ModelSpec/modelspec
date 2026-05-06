from datetime import datetime

import pytest

@pytest.fixture
def controllerWithFarmers(modelingTool, mw):
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

    farmerA = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmerA.setName("Farmer A")
    farmerB = mw(Farmer,  email="farmer2@cheecse.ca", password="Pass$word", address="55 Mtl", cheECSEManager=controller.cheECSEManager)
    farmerB.setName("Farmer B")

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

    yield controller

def testDisplayFarmers(controllerWithFarmers, mw):
    # Act
    farmerTOs = controllerWithFarmers.displayFarmers()

    # Assert
    assert len(farmerTOs) == 2
    byEmail = {mw(to).getEmail(): mw(to) for to in farmerTOs}
    aTO = byEmail["farmer@cheecse.fr"]
    bTO = byEmail["farmer2@cheecse.ca"]

    assert aTO.getPassword() == "P@ssw0rd"
    assert aTO.getAddress() == "112 Av"
    assert aTO.getName() == "Farmer A"
    assert aTO.getCheeseWheelIDs() == [1, 2, 3, 4, 5]
    assert aTO.getMonthsAgeds() == [
        MaturationPeriod.Six,
        MaturationPeriod.Six,
        MaturationPeriod.Twelve,
        MaturationPeriod.Twelve,
        MaturationPeriod.Twelve,
    ]
    assert aTO.getIsSpoileds() == [False, True, False, False, False]
    assert aTO.getPurchaseDates() == [
        datetime(2025, 9, 1),
        datetime(2025, 9, 1),
        datetime(2025, 8, 15),
        datetime(2025, 8, 15),
        datetime(2025, 8, 15),
    ]

    assert bTO.getCheeseWheelIDs() == []
    assert bTO.getPassword() == "Pass$word"
    assert bTO.getAddress() == "55 Mtl"
    assert bTO.getName() == "Farmer B"
    assert mw(controllerWithFarmers.cheECSEManager).numberOfFarmers() == 2