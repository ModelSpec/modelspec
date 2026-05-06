from datetime import datetime

import pytest

@pytest.fixture
def controllerWithCompanies(modelingTool, mw):
    global MaturationPeriod, WholesaleCompany, Purchase, CheeseWheel, Order
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

    yield controller, cheesy, farmer


def testDisplayWholesaleCompaniesSuccess(controllerWithCompanies, mw):
    # Arrange
    controller, cheesy, farmer = controllerWithCompanies

    dairy = mw(WholesaleCompany, name="Dairy something", address="55 Mtl", cheECSEManager=controller.cheECSEManager)
    masters = mw(WholesaleCompany, name="Cheese Masters", address="456 Ontario", cheECSEManager=controller.cheECSEManager)

    purchase2 = mw(Purchase, transactionDate=datetime(2025, 2, 1), cheECSEManager=controller.cheECSEManager, farmer=farmer.model)
    purchase2.setId(4)
    id = 6
    for _ in range(3):
        cw = mw(CheeseWheel, cheECSEManager=controller.cheECSEManager, monthsAged=MaturationPeriod.TwentyFour, isSpoiled=False, purchase=purchase2.model)
        cw.setId(id)
        id += 1
    
    order3 = mw(Order, transactionDate=datetime(2025, 10, 1), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=15, monthsAged=MaturationPeriod.TwentyFour, deliveryDate=datetime(2027, 2, 2), company=masters.model)
    order3.setId(5)

    for cw in purchase2.getCheeseWheels():
        if not cw.getIsSpoiled():
            order3.addCheeseWheel(cw.model)
    
    # Act
    companyTOs = controller.displayWholesaleCompanies()

    # Assert
    assert len(companyTOs) == 3
    names = {mw(to).getName() for to in companyTOs}
    assert names == {cheesy.getName(), dairy.getName(), masters.getName()}

    cheesyTO = next(mw(to) for to in companyTOs if mw(to).getName() == cheesy.getName())
    assert cheesyTO.getAddress() == "112 Av"

    assert cheesyTO.getOrderDates() == [datetime(2025, 8, 15), datetime(2025, 9, 1)]
    assert cheesyTO.getDeliveryDates() == [datetime(2025, 12, 15), datetime(2026, 3, 1)]
    assert cheesyTO.getMonthsAgeds() == [MaturationPeriod.Six, MaturationPeriod.Twelve]
    assert cheesyTO.getNrCheeseWheelsOrdereds() == [10, 3]
    assert cheesyTO.getNrCheeseWheelsMissings() == [5, 3]

    dairyTO = next(mw(to) for to in companyTOs if mw(to).getName() == dairy.getName())
    assert dairyTO.getAddress() == "55 Mtl"
    assert len(dairyTO.getOrderDates()) == 0
    assert len(dairyTO.getDeliveryDates()) == 0
    assert len(dairyTO.getMonthsAgeds()) == 0
    assert len(dairyTO.getNrCheeseWheelsOrdereds()) == 0
    assert len(dairyTO.getNrCheeseWheelsMissings()) == 0

    cheeseMastersTO = next(mw(to) for to in companyTOs if mw(to).getName() == masters.getName())
    assert cheeseMastersTO.getAddress() == "456 Ontario"
    assert cheeseMastersTO.getOrderDates() == [datetime(2025, 10, 1)]
    assert cheeseMastersTO.getDeliveryDates() == [datetime(2027, 2, 2)]
    assert cheeseMastersTO.getMonthsAgeds() == [MaturationPeriod.TwentyFour]
    assert cheeseMastersTO.getNrCheeseWheelsOrdereds() == [15]
    assert cheeseMastersTO.getNrCheeseWheelsMissings() == [12]
