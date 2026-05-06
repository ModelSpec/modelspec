from datetime import datetime

import pytest

@pytest.fixture
def controllerWithCompanies(modelingTool, mw):
    global Order, MaturationPeriod
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Transaction, WholesaleCompany, Order, CheeseWheel

        MaturationPeriod = CheeseWheel.MaturationPeriod
        Transaction.nextId = 1
        WholesaleCompany.wholesalecompanysByName.clear()
        
    else: 
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Transaction, WholesaleCompany, MaturationPeriod, Order
   
    controller = CheECSEManagerController()

    cheesy = mw(WholesaleCompany, name="Cheesy Bites", address="112 Av", cheECSEManager=controller.cheECSEManager)
    mw(WholesaleCompany, name="Dairy World", address="55 Mtl", cheECSEManager=controller.cheECSEManager)

    yield controller, cheesy

def testDeleteWholesaleCompanySuccess(controllerWithCompanies, mw):
    # Arrange
    controller, _ = controllerWithCompanies

    # Act
    controller.deleteWholesaleCompany("Cheesy Bites")

    # Assert
    controller.cheECSEManager = mw(controller.cheECSEManager)

    companies = controller.cheECSEManager.getCompanies()
    assert len(companies) == 1

    company0 = companies[0]
    assert company0.getName() == "Dairy World"
    assert company0.getAddress() == "55 Mtl"

@pytest.mark.parametrize("name", ["Unknown Company"])
def testDeleteWholesaleCompanyMissing(controllerWithCompanies, name, mw):
    # Arrange
    controller, _ = controllerWithCompanies

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.deleteWholesaleCompany(name)

    # Assert
    controller.cheECSEManager = mw(controller.cheECSEManager)

    assert str(errorInfo.value) == f"The wholesale company {name} does not exist."
    companies = controller.cheECSEManager.getCompanies()
    assert len(companies) == 2

    companyA = None
    companyB = None
    for company in companies:
        if company.getName() == "Cheesy Bites":
            companyA = company
        if company.getName() == "Dairy World":
            companyB = company

    assert companyA is not None
    assert companyB is not None
    assert companyA.getName() == "Cheesy Bites"
    assert companyA.getAddress() == "112 Av"
    assert companyB.getName() == "Dairy World"
    assert companyB.getAddress() == "55 Mtl"

def testDeleteWholesaleCompanyWithOrders(controllerWithCompanies, mw):
    # Arrange
    controller, cheesy = controllerWithCompanies

    mw(Order, transactionDate=datetime(2025, 4, 4), cheECSEManager=controller.cheECSEManager, nrCheeseWheels=5, monthsAged=MaturationPeriod.Six, deliveryDate=datetime(2025, 12, 1), company=cheesy.model)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.deleteWholesaleCompany("Cheesy Bites")

    # Assert
    controller.cheECSEManager = mw(controller.cheECSEManager)

    assert str(errorInfo.value) == "Cannot delete a wholesale company that has ordered cheese."
    companies = controller.cheECSEManager.getCompanies()
    assert len(companies) == 2

    companyA = None
    companyB = None
    for company in companies:
        if company.getName() == "Cheesy Bites":
            companyA = company
        if company.getName() == "Dairy World":
            companyB = company

    assert companyA is not None
    assert companyB is not None
    assert companyA.getName() == "Cheesy Bites"
    assert companyA.getAddress() == "112 Av"
    assert companyB.getName() == "Dairy World"
    assert companyB.getAddress() == "55 Mtl"