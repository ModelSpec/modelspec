from datetime import datetime

import pytest

@pytest.fixture
def controllerWithCompany(modelingTool, mw):
    global MaturationPeriod
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

    farmer = mw(Farmer,  email="farmer1@example.com", password="pass123", address="123 Farm", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer 1")

    purchase1 = mw(Purchase, transactionDate=datetime(2025, 1, 1), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase1.setId(1)

    id = 1
    for _ in range(5):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.Six, isSpoiled=False, purchase=purchase1.model)
        cw.setId(id)
        id += 1

    order1 = mw(Order, transactionDate=datetime(2025, 8, 15), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=10, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2025, 12, 15), company=cheesy.model)
    order1.setId(2)
    order2 = mw(Order, transactionDate=datetime(2025, 9, 1), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=3, monthsAged=MaturationPeriod.Twelve, deliveryDate=datetime(2026, 3, 1), company=cheesy.model)
    order2.setId(3)

    for cw in purchase1.getCheeseWheels():
        if not cw.getIsSpoiled():
            order1.addCheeseWheel(cw.model)

    yield controller


def testDisplayWholesaleCompanySuccess(controllerWithCompany, mw):
    # Act
    companyTO = controllerWithCompany.displayWholesaleCompany("Cheesy Bites")

    # Assert
    companyTO = mw(companyTO)
    assert companyTO.getName() == "Cheesy Bites"
    assert companyTO.getAddress() == "112 Av"
    assert companyTO.getOrderDates() == [datetime(2025, 8, 15), datetime(2025, 9, 1)]
    assert companyTO.getDeliveryDates() == [datetime(2025, 12, 15), datetime(2026, 3, 1)]
    assert companyTO.getMonthsAgeds() == [MaturationPeriod.Six, MaturationPeriod.Twelve]
    assert companyTO.getNrCheeseWheelsOrdereds() == [10, 3]
    assert companyTO.getNrCheeseWheelsMissings() == [5, 3]
    assert mw(controllerWithCompany.cheECSEManager).numberOfCompanies() == 1


def testDisplayWholesaleCompanyMissing(controllerWithCompany, mw):
    # Act
    result = controllerWithCompany.displayWholesaleCompany("Cheese Paradise")

    # Assert
    assert result is None
    assert mw(controllerWithCompany.cheECSEManager).numberOfCompanies() == 1
