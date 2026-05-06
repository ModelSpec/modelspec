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
        from ..ecore.generated_model_layer import House, ConcreteBasement, BMType

    controller = HouseController()
    yield controller

def testCreateHouseNewSuccess(givenController, mw):
    givenController.createHouse("123 Main St", BMType.WOOD, "", "", 0.0, 0.0, 0.0)
    created = mw(givenController.houses[0])
    assert created is not None
    assert created.getAddress() == "123 Main St"
    assert created.getBuildingMaterial() == BMType.WOOD
    assert created.getBasement() is None
    assert len(givenController.houses) == 1

def testCreateHouseWithConcreteBasementSuccess(givenController, mw):
    givenController.createHouse("123 Main St", BMType.WOOD, "concrete", "basement", 20.0, 0.9, 0.0)
    created = mw(givenController.houses[0])

    assert created is not None
    assert created.getAddress() == "123 Main St"
    assert created.getBuildingMaterial() == BMType.WOOD
    
    basement = created.getBasement()
    assert basement is not None
    assert isinstance(basement, ConcreteBasement)
    assert basement.getName() == "basement"
    assert basement.getSize() == 20.0
    assert basement.getQuality() == 0.9
    assert len(givenController.houses) == 1

@pytest.mark.parametrize(
    "address,material,basementType,basementName,basementSize,basementQuality,basementHumidity,error",
    [
        ("", "WOOD", "concrete", "basement", 20.0, 0.9, 0.0, "The address of a house cannot be empty."),
        ("123 Main St", None, "concrete", "basement", 20.0, 0.9, 0.0, "The building material cannot be empty."),
        ("123 Main St", "WOOD", "concrete", "", 20.0, 0.9, 0.0, "The name of a basement cannot be empty."),
        ("123 Main St", "WOOD", "concrete", "basement", 0.0, 0.9, 0.0, "The size of a basement must be greater than 0."),
        ("123 Main St", "WOOD", "metal", "basement", 20.0, 0.5, 0.5, 'The type of a basement must be either "concrete", "earth" or empty.'),
        ("123 Main St", "WOOD", "concrete", "basement", 20.0, -0.1, 0.0, "The quality of a concrete basement must be between 0 and 1."),
        ("123 Main St", "WOOD", "concrete", "basement", 20.0, 2.0, 0.0, "The quality of a concrete basement must be between 0 and 1."),
        ("123 Main St", "WOOD", "concrete", "basement", 20.0, 0.9, 0.5, "The humidity of a concrete basement must be 0."),
        ("123 Main St", "WOOD", "earth", "basement", 20.0, 0.0, -0.1, "The humidity of an earth basement must be between 0 and 1."),
        ("123 Main St", "WOOD", "earth", "basement", 20.0, 0.0, 2.0, "The humidity of an earth basement must be between 0 and 1."),
        ("123 Main St", "WOOD", "earth", "basement", 20.0, 0.5, 0.9, "The quality of an earth basement must be 0."),
    ],
)
def testCreateHouseInvalidValuesFail(givenController, address, material, basementType, basementName, basementSize, basementQuality, basementHumidity, error):
    if material is not None:
        material_enum = getattr(BMType, material)
    else:
        material_enum = None

    with pytest.raises(ValueError) as err:
        givenController.createHouse(address, material_enum, basementType, basementName, basementSize, basementQuality, basementHumidity)
    assert str(err.value) == error
    assert len(givenController.houses) == 0