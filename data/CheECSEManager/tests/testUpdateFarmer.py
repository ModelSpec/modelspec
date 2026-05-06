import pytest

@pytest.fixture
def controllerWithFarmer(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import User, Farmer

        User.usersByEmail.clear()
        Farmer.usersByEmail.clear()

    else: 
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import User, Farmer
   
    controller = CheECSEManagerController()

    farmer = mw(Farmer,  email="farmer@cheecse.fr", password="P@ssw0rd", address="112 Av", cheECSEManager=controller.cheECSEManager)
    farmer.setName("Farmer A")
    yield controller


@pytest.mark.parametrize(
    "email, updatedPassword, updatedName, updatedAddress",
    [
        ("farmer@cheecse.fr", "Password$", "Jericho", "55 Mtl"),
        ("farmer@cheecse.fr", "P4$$w0rd", "John Smith", "123 Farm St"),
        ("farmer@cheecse.fr", "Ab#1234", "Farmer B", "42 Main Rd"),
        ("farmer@cheecse.fr", "P@ssw0rd!", "", "112 Av"),
    ],
)
def testUpdateFarmerSuccess(controllerWithFarmer, email, updatedPassword, updatedName, updatedAddress, mw):
    # Act
    controllerWithFarmer.updateFarmer(email, updatedPassword, updatedName, updatedAddress)

    # Assert
    controllerWithFarmer.cheECSEManager = mw(controllerWithFarmer.cheECSEManager)
    assert controllerWithFarmer.cheECSEManager.numberOfFarmers() == 1

    farmer  = None
    for user in controllerWithFarmer.cheECSEManager.getFarmers():
        if user.getEmail() == email:
            farmer = user

    assert farmer is not None
    assert farmer.getPassword() == updatedPassword
    assert farmer.getName() == updatedName
    assert farmer.getAddress() == updatedAddress


@pytest.mark.parametrize(
    "email, updatedPassword, updatedName, updatedAddress, errorMessage",
    [
        ("farmer@cheecse.ca", "Password$", "Jericho", "55 Mtl", "The farmer with email farmer@cheecse.ca does not exist."),
        ("farmer@cheecse.fr", None, "Jericho", "55 Mtl", "Password must not be empty."),
        ("farmer@cheecse.fr", "Password$", "Jericho", None, "Address must not be empty."),
    ],
)
def testUpdateFarmerInvalid(controllerWithFarmer, email, updatedPassword, updatedName, updatedAddress, errorMessage, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithFarmer.updateFarmer(email, updatedPassword, updatedName, updatedAddress)

    # Assert
    controllerWithFarmer.cheECSEManager = mw(controllerWithFarmer.cheECSEManager)
    assert str(errorInfo.value) == errorMessage
    farmers = controllerWithFarmer.cheECSEManager.getFarmers()
    assert len(farmers) == 1

    farmer = None
    for user in farmers:

        if user.getEmail() == "farmer@cheecse.fr":
            farmer = user

    assert farmer is not None and farmer.getAddress() == "112 Av" and farmer.getPassword() == "P@ssw0rd" and farmer.getName() == "Farmer A"

    updated = None
    for user in farmers:

        if user.getEmail() == email:
            updated = user

    assert updated is None or not (updated.getAddress() == updatedAddress and updated.getPassword() == updatedPassword and updated.getName() == updatedName)