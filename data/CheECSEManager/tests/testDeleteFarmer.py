from datetime import datetime

import pytest

@pytest.fixture
def controllerWithFarmers(modelingTool, mw):
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
        from ..ecore.generated_model_layer import Transaction, CheeseWheel, User, Farmer, MaturationPeriod, Purchase
   
    controller = CheECSEManagerController()

    farmerA = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmerA.setName("Farmer A")
    
    farmerB = mw(Farmer, email="farmer2@domain.com", password="P4$$w0rd", address="123 St", cheECSEManager=controller.cheECSEManager)
    farmerB.setName("Farmer B")

    purchase = mw(Purchase, transactionDate=datetime(2025, 9, 1), cheECSEManager=controller.cheECSEManager, farmer=farmerB.model)

    for i in range(2):
        cw = mw(CheeseWheel, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase.model, cheECSEManager=controller.cheECSEManager)
        cw.setId(i + 1)

    yield controller

def testDeleteFarmerSuccess(controllerWithFarmers, mw):
    # Act
    controllerWithFarmers.deleteFarmer("farmer@cheecse.fr")

    # Assert
    controllerWithFarmers.cheECSEManager = mw(controllerWithFarmers.cheECSEManager)

    farmers = controllerWithFarmers.cheECSEManager.getFarmers()
    assert len(farmers) == 1

    remaining  = None
    for user in farmers:
        if user.getEmail() == "farmer2@domain.com":
            remaining = user

    assert remaining.getEmail() == "farmer2@domain.com"
    assert remaining.getPassword() == "P4$$w0rd"
    assert remaining.getAddress() == "123 St"
    assert remaining.getName() == "Farmer B"
    
    assert amountOfCheeseWheels(controllerWithFarmers, "farmer2@domain.com") == 2

def testDeleteFarmerWithPurchases(controllerWithFarmers, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithFarmers.deleteFarmer("farmer2@domain.com")

    # Assert
    controllerWithFarmers.cheECSEManager = mw(controllerWithFarmers.cheECSEManager)

    assert str(errorInfo.value) == "Cannot delete farmer who has supplied cheese."
    farmers = controllerWithFarmers.cheECSEManager.getFarmers()
    assert len(farmers) == 2

    farmerA = None
    for user in farmers:
        if user.getEmail() == "farmer@cheecse.fr":
            farmerA = user
        if user.getEmail() == "farmer2@domain.com":
            farmerB = user
    assert farmerA is not None
    assert farmerB is not None

    assert farmerA.getEmail() == "farmer@cheecse.fr"
    assert farmerA.getPassword() == "P@ssw0rd"
    assert farmerA.getAddress() == "112 Av"
    assert farmerA.getName() == "Farmer A"
    assert farmerB.getEmail() == "farmer2@domain.com"
    assert farmerB.getPassword() == "P4$$w0rd"
    assert farmerB.getAddress() == "123 St"
    assert farmerB.getName() == "Farmer B"
        
    assert amountOfCheeseWheels(controllerWithFarmers, "farmer@cheecse.fr") == 0
    assert amountOfCheeseWheels(controllerWithFarmers, "farmer2@domain.com") == 2


def testDeleteFarmerMissing(controllerWithFarmers, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithFarmers.deleteFarmer("farmer@cheecse.ca")

    # Assert
    controllerWithFarmers.cheECSEManager = mw(controllerWithFarmers.cheECSEManager)

    assert str(errorInfo.value) == "The farmer with email farmer@cheecse.ca does not exist."
    farmers = controllerWithFarmers.cheECSEManager.getFarmers()
    assert len(farmers) == 2

    farmerA = None
    for user in farmers:
        if user.getEmail() == "farmer@cheecse.fr":
            farmerA = user
        if user.getEmail() == "farmer2@domain.com":
            farmerB = user
    assert farmerA is not None
    assert farmerB is not None

    assert farmerA.getEmail() == "farmer@cheecse.fr"
    assert farmerA.getPassword() == "P@ssw0rd"
    assert farmerA.getAddress() == "112 Av"
    assert farmerA.getName() == "Farmer A"
    assert farmerB.getEmail() == "farmer2@domain.com"
    assert farmerB.getPassword() == "P4$$w0rd"
    assert farmerB.getAddress() == "123 St"
    assert farmerB.getName() == "Farmer B"
        
    assert amountOfCheeseWheels(controllerWithFarmers, "farmer@cheecse.fr") == 0
    assert amountOfCheeseWheels(controllerWithFarmers, "farmer2@domain.com") == 2


def amountOfCheeseWheels(controller, farmerEmail):
    count = 0
    for transaction in controller.cheECSEManager.getTransactions():
        farmer = transaction.getFarmer()
        if farmer is None:
            continue
        if farmer.getEmail() == farmerEmail:
            count += transaction.numberOfCheeseWheels()
    return count