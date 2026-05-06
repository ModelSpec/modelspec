import pytest

@pytest.fixture
def controllerWithFarmer(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Farmer

        Farmer.usersByEmail.clear()        
    else: 
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Farmer
   
    controller = CheECSEManagerController()

    baseFarmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    baseFarmer.setName("Farmer A")

    yield controller


@pytest.mark.parametrize(
    "email,password,address,name",
    [
        ("farmer@cheecse.ca", "Pass$word", "55 Mtl", "Farmer B"),
        ("farmer2@domain.com", "P4$$w0rd", "123 St", "Farmer C"),
        ("john@farming.org", "Ab#1234", "Farm Rd", "Farmer D"),
        ("jane@farming.org", "Ab#1234", "Farm Rd", ""),
    ],
)
def testRegisterFarmerSuccess(controllerWithFarmer, email, password, address, name, mw):
    # Act
    controllerWithFarmer.registerFarmer(email, password, name, address)

    # Assert
    controllerWithFarmer.cheECSEManager = mw(controllerWithFarmer.cheECSEManager)

    assert controllerWithFarmer.cheECSEManager.numberOfFarmers() == 2

    added = None
    for user in controllerWithFarmer.cheECSEManager.getFarmers():
        if user.getEmail() == email:
            added = user

    assert added is not None
    assert added.getEmail() == email
    assert added.getPassword() == password
    assert added.getAddress() == address
    assert added.getName() == name


@pytest.mark.parametrize(
    "email,password,address,name,errorMessage",
    [
        ("farmer@cheecse.fr", "Pass$word", "55 Mtl", "Farmer B", "The farmer email already exists."),
        ("farmer.without.at", "Pass$word", "55 Mtl", "Farmer B", "Email must contain @ symbol."),
        ("@nodomain.com", "Pass$word", "55 Mtl", "Farmer B", "Email must have characters before @."),
        ("invalid@", "Pass$word", "55 Mtl", "Farmer B", "Email must contain a dot after @."),
        ("invalid@domain", "Pass$word", "55 Mtl", "Farmer B", "Email must contain a dot after @."),
        ("invalid@domain.", "Pass$word", "55 Mtl", "Farmer B", "Email must have characters after dot."),
        ("farmer email@with.sp", "Pass$word", "55 Mtl", "Farmer B", "Email must not contain spaces."),
        ("manager@cheecse.fr", "Pass$word", "55 Mtl", "Farmer B", "Email cannot be manager@cheecse.fr."),
        ("farmer@cheecse.ca", None, "55 Mtl", "Farmer B", "Password must not be empty."),
        ("farmer@cheecse.ca", "Pass$word", None, "Farmer B", "Address must not be empty."),
    ],
)
def testRegisterFarmerInvalid(controllerWithFarmer, email, password, address, name, errorMessage, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithFarmer.registerFarmer(email, password, name, address)

    # Assert
    controllerWithFarmer.cheECSEManager = mw(controllerWithFarmer.cheECSEManager)

    assert str(errorInfo.value) == errorMessage
    assert controllerWithFarmer.cheECSEManager.numberOfFarmers() == 1

    farmer = None
    for user in controllerWithFarmer.cheECSEManager.getFarmers():
        if user.getEmail() == "farmer@cheecse.fr":
            farmer = user

    assert farmer is not None
    assert farmer.getEmail() == "farmer@cheecse.fr"
    assert farmer.getPassword() == "P@ssw0rd"
    assert farmer.getAddress() == "112 Av"
    assert farmer.getName() == "Farmer A"
