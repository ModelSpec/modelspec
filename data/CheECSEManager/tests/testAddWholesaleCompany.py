import pytest

@pytest.fixture
def controllerWithCompany(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import WholesaleCompany

        WholesaleCompany.wholesalecompanysByName.clear()
    else: 
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import WholesaleCompany

    controller = CheECSEManagerController()

    mw(WholesaleCompany, name="Cheesy Bites", address="112 Av", cheECSEManager=controller.cheECSEManager)

    yield controller

@pytest.mark.parametrize(
    "name,address",
    [("Dairy Something", "55 Mtl"), ("Cheese Masters", "123 Rue")],
)
def testAddWholesaleCompanySuccess(controllerWithCompany, name, address, mw):
    # Act
    controllerWithCompany.addWholesaleCompany(name, address)

    # Assert
    controllerWithCompany.cheECSEManager = mw(controllerWithCompany.cheECSEManager)

    companies = controllerWithCompany.cheECSEManager.getCompanies()
    assert len(companies) == 2

    addedCompany = None
    for company in controllerWithCompany.cheECSEManager.getCompanies():
        if company.getName() == name:
            addedCompany = company

    assert addedCompany is not None
    assert addedCompany.getName() == name
    assert addedCompany.getAddress() == address


@pytest.mark.parametrize(
    "name,address,errorMessage",
    [
        ("Cheesy Bites", "55 Mtl", "The wholesale company already exists."),
        ("", "55 Mtl", "Name must not be empty."),
        ("New Company", "", "Address must not be empty."),
    ],
)
def testAddWholesaleCompanyInvalid(controllerWithCompany, name, address, errorMessage, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithCompany.addWholesaleCompany(name, address)

    # Assert
    controllerWithCompany.cheECSEManager = mw(controllerWithCompany.cheECSEManager)

    assert str(errorInfo.value) == errorMessage
    companies = controllerWithCompany.cheECSEManager.getCompanies()
    assert len(companies) == 1

    existingCompany = None
    for company in controllerWithCompany.cheECSEManager.getCompanies():
        if company.getName() == "Cheesy Bites":
            existingCompany = company

    assert existingCompany is not None
    assert existingCompany.getAddress() == "112 Av"
