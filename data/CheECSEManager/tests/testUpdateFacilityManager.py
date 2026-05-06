import pytest

@pytest.fixture
def controllerWithManager(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import User, FacilityManager

        User.usersByEmail.clear()

    else: 
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import User, FacilityManager
   

    controller = CheECSEManagerController()

    mw(FacilityManager, email="manager@cheecse.fr", password="p#Ssw0rd", cheECSEManager=controller.cheECSEManager)

    yield controller


@pytest.mark.parametrize(
    "updatedPassword",
    ["pAssword!", "Pa$$word", "Test#1234", "abcD!"],
)
def testUpdateFacilityManagerSuccess(controllerWithManager, updatedPassword, mw):
    # Act
    controllerWithManager.updateFacilityManager(updatedPassword)

    # Assert
    controllerWithManager.cheECSEManager = mw(controllerWithManager.cheECSEManager)
    manager = controllerWithManager.cheECSEManager.getManager()
    assert manager is not None
    assert manager.getPassword() == updatedPassword


@pytest.mark.parametrize(
    "updatedPassword, errorMessage",
    [
        ("a$D", "Password must be at least 4 characters long."),
        ("Password", "Password must contain a special character from !, #, or $."),
        ("password!", "Password must contain an uppercase character."),
        ("PASSWORD!", "Password must contain a lowercase character."),
    ],
)
def testUpdateFacilityManagerInvalid(controllerWithManager, updatedPassword, errorMessage, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithManager.updateFacilityManager(updatedPassword)

    # Assert
    controllerWithManager.cheECSEManager = mw(controllerWithManager.cheECSEManager)
    assert str(errorInfo.value) == errorMessage
    manager = controllerWithManager.cheECSEManager.getManager()
    assert manager is not None
    assert manager.getPassword() == "p#Ssw0rd"
