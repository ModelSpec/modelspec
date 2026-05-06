import pytest

@pytest.fixture
def givenController(modelingTool):
    if modelingTool == "umple":
        from ..umple.controller import HouseController
        from ..umple.generated_model_layer import House, Company
        BMType = House.BMType
        house = House("123 Main St", BMType.WOOD)
        company = Company("FixIt Co", "456 Oak Ave")
    else:
        from ..ecore.controller import HouseController
        from ..ecore.generated_model_layer import House, Company, BMType
        house = House(address="123 Main St", buildingMaterial=BMType.WOOD)
        company = Company(name="FixIt Co", address="456 Oak Ave")

    controller = HouseController()
    controller.houses.append(house)
    controller.companies.append(company)
    
    yield controller

def testCreateJobLogNewSuccess(givenController, mw):
    givenController.createJobLog(5, 100.00, "123 Main St", "FixIt Co")
    house = mw(givenController.houses[0])
    created = house.getJobLogs()[0]
    assert created is not None
    assert created.getHours() == 5
    assert created.getPrice() == 100.00
    assert house.numberOfJobLogs() == 1

@pytest.mark.parametrize(
    "houseAddress,companyName,hours,price,error",
    [
        ("123 Main St", "FixIt Co", 0, 100.00, "The number of hours must be greater than 0."),
        ("123 Main St", "FixIt Co", 5, -1.00, "The price must be at least 0."),
        ("999 Fake St", "FixIt Co", 5, 100.00, "The house does not exist."),
        ("123 Main St", "Fake Co", 5, 100.00, "The company does not exist."),
    ],
)
def testCreateJobLogInvalidValuesFail(givenController, mw, houseAddress, companyName, hours, price, error):
    with pytest.raises(ValueError) as err:
        givenController.createJobLog(hours, price, houseAddress, companyName)

    assert str(err.value) == error
    house = mw(givenController.houses[0])
    assert house.numberOfJobLogs() == 0