import pytest

@pytest.fixture
def controllerWithBaseCompany(modelingTool, mw):
    global WholesaleCompany
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
    "updatedName, updatedAddress",
    [("Dairy Something", "55 Mtl"), ("Milk Depot", "123 Quebec"), ("Cheesy Bites", "456 Ontario")],
)
def testUpdateWholesaleCompanySuccess(controllerWithBaseCompany, updatedName, updatedAddress, mw):
    # Act
    controllerWithBaseCompany.updateWholesaleCompany("Cheesy Bites", updatedName, updatedAddress)

    # Assert
    controllerWithBaseCompany.cheECSEManager = mw(controllerWithBaseCompany.cheECSEManager)

    assert controllerWithBaseCompany.cheECSEManager.numberOfCompanies() == 1

    updatedCompany = None
    for company in controllerWithBaseCompany.cheECSEManager.getCompanies():
        if company.getName() == updatedName:
            updatedCompany = company

    assert updatedCompany is not None
    assert updatedCompany.getAddress() == updatedAddress

@pytest.mark.parametrize(
    "updatedName, updatedAddress, errorMessage",
    [("Dairy Something", "55 Mtl", "The wholesale company Dairy Something does not exist.")],
)
def testUpdateWholesaleCompanyMissing(controllerWithBaseCompany, updatedName, updatedAddress, errorMessage, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithBaseCompany.updateWholesaleCompany("Dairy Something", updatedName, updatedAddress)

    # Assert
    controllerWithBaseCompany.cheECSEManager = mw(controllerWithBaseCompany.cheECSEManager)
    
    assert str(errorInfo.value) == errorMessage
    assert controllerWithBaseCompany.cheECSEManager.numberOfCompanies() == 1

    existing = None
    for company in controllerWithBaseCompany.cheECSEManager.getCompanies():
        if company.getName() == "Cheesy Bites":
            existing = company

    assert existing is not None
    assert existing.getAddress() == "112 Av"

    nonExisting = None
    for company in controllerWithBaseCompany.cheECSEManager.getCompanies():
        if company.getName() == updatedName:
            nonExisting = company

    assert nonExisting is None

@pytest.mark.parametrize(
    "updatedName, updatedAddress, errorMessage",
    [
        ("Dairy Something", "112 Av", "The wholesale company Dairy Something already exists."),
        ("", "55 Mtl", "The name must not be empty."),
        ("New Cheese Co", "", "The address must not be empty."),
    ],
)
def testUpdateWholesaleCompanyInvalid(controllerWithBaseCompany, updatedName, updatedAddress, errorMessage, mw):
    # Arrange
    mw(WholesaleCompany, name="Dairy Something", address="55 Mtl", cheECSEManager=controllerWithBaseCompany.cheECSEManager)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithBaseCompany.updateWholesaleCompany("Cheesy Bites", updatedName, updatedAddress)

    # Assert
    controllerWithBaseCompany.cheECSEManager = mw(controllerWithBaseCompany.cheECSEManager)

    assert str(errorInfo.value) == errorMessage
    assert controllerWithBaseCompany.cheECSEManager.numberOfCompanies() == 2

    cheesy = None
    for company in controllerWithBaseCompany.cheECSEManager.getCompanies():
        if company.getName() == "Cheesy Bites":
            cheesy = company   
    assert cheesy is not None
    assert cheesy.getAddress() == "112 Av"
    
    dairy = None
    for company in controllerWithBaseCompany.cheECSEManager.getCompanies():
        if company.getName() == "Dairy Something":
            dairy = company
    assert dairy is not None
    assert dairy.getAddress() == "55 Mtl"

    updated = None
    for company in controllerWithBaseCompany.cheECSEManager.getCompanies():
        if company.getName() == updatedName:
            updated = company
    assert updated is None or not (updated.getAddress() == updatedAddress)