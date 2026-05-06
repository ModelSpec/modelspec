import pytest

@pytest.fixture
def givenController(modelingTool):
    global ConcreteBasement, BMType
    if modelingTool == "umple":
        from ..umple.controller import HouseController
        from ..umple.generated_model_layer import House, ConcreteBasement
        BMType = House.BMType
    else:
        from ..ecore.controller import HouseController
        from ..ecore.generated_model_layer import ConcreteBasement, BMType

    controller = HouseController()
    yield controller

def testCreateSemiDetachedWithGarageNewSuccess(givenController, mw):
    givenController.createSemiDetachedWithGarage("123 Main St", BMType.WOOD, 4, True, True, "", "", 0.0, 0.0, 0.0)

    created = mw(givenController.houses[0])
    assert created is not None
    assert created.getAddress() == "123 Main St"
    assert created.getBuildingMaterial() == BMType.WOOD
    assert created.getWindows() == 4
    assert created.getGarden() is True

    garage = created.getGarage()
    assert garage is not None
    assert garage.getAutomatic() is True
    assert created.getBasement() is None
    assert len(givenController.houses) == 1


def testCreateSemiDetachedWithGarageAndBasementSuccess(givenController, mw):
    givenController.createSemiDetachedWithGarage("123 Main St", BMType.WOOD, 4, True, True, "concrete", "North", 20.0, 0.9, 0.0)
    created = mw(givenController.houses[0])
    assert created is not None
    assert created.getAddress() == "123 Main St"
    assert created.getBuildingMaterial() == BMType.WOOD
    assert created.getWindows() == 4
    assert created.getGarden() is True

    garage = created.getGarage()
    assert garage is not None
    assert garage.getAutomatic() is True

    basement = created.getBasement()
    assert basement is not None
    assert isinstance(basement, ConcreteBasement)
    assert basement.getName() == "North"
    assert basement.getSize() == 20.0
    assert basement.getQuality() == 0.9
    assert len(givenController.houses) == 1


@pytest.mark.parametrize(
    "address,buildingMaterial,windows,garden,automatic,basementType,basementName,basementSize,basementQuality,basementHumidity,error",
    [
        ("", "WOOD", 4, True, True, "concrete", "basement", 20.0, 0.9, 0.0, "The address of a house cannot be empty."),
        ("123 Main St", None, 4, True, True, "concrete", "basement", 20.0, 0.9, 0.0, "The building material cannot be empty."),
        ("123 Main St", "WOOD", -1, True, True, "concrete", "basement", 20.0, 0.9, 0.0, "The number of windows must be non-negative."),
        ("123 Main St", "WOOD", 4, False, True, "concrete", "", 20.0, 0.9, 0.0, "The name of a basement cannot be empty."),
        ("123 Main St", "WOOD", 4, True, True, "concrete", "basement", -1.0, 0.9, 0.0, "The size of a basement must be greater than 0."),
        ("123 Main St", "WOOD", 4, True, True, "metal", "basement", 20.0, 0.5, 0.5, 'The type of a basement must be either "concrete", "earth" or empty.'),
        ("123 Main St", "WOOD", 4, True, True, "concrete", "basement", 20.0, -0.1, 0.0, "The quality of a concrete basement must be between 0 and 1."),
        ("123 Main St", "WOOD", 4, True, True, "concrete", "basement", 20.0, 2.0, 0.0, "The quality of a concrete basement must be between 0 and 1."),
        ("123 Main St", "WOOD", 4, True, True, "concrete", "basement", 20.0, 0.9, 0.5, "The humidity of a concrete basement must be 0."),
        ("123 Main St", "WOOD", 4, True, True, "earth", "basement", 20.0, 0.0, -0.1, "The humidity of an earth basement must be between 0 and 1."),
        ("123 Main St", "WOOD", 4, True, True, "earth", "basement", 20.0, 0.0, 2.0, "The humidity of an earth basement must be between 0 and 1."),
        ("123 Main St", "WOOD", 4, True, True, "earth", "basement", 20.0, 0.5, 0.9, "The quality of an earth basement must be 0."),
    ]
)
def testCreateSemiDetachedWithGarageInvalidValuesFail(givenController, address, buildingMaterial, windows, garden, automatic, basementType, basementName, basementSize, basementQuality, basementHumidity, error):
    if buildingMaterial is not None:
        buildingMaterial = getattr(BMType, buildingMaterial)
    else:
        buildingMaterial = None

    with pytest.raises(ValueError) as err:
        givenController.createSemiDetachedWithGarage(address,  buildingMaterial,  windows,  garden,  automatic,  basementType,  basementName,  basementSize,  basementQuality,  basementHumidity)
    assert str(err.value) == error
    assert len(givenController.houses) == 0