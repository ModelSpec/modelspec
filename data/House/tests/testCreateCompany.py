import pytest

@pytest.fixture
def givenController(modelingTool):
    if modelingTool == "umple":
        from ..umple.controller import HouseController
    else:
        from ..ecore.controller import HouseController
    controller = HouseController()
    yield controller

def testCreateCompanyNewSuccess(givenController, mw):
    givenController.createCompany("FixIt Co", "456 Oak Ave")
    created = mw(givenController.companies[0])
    assert created is not None
    assert created.getName() == "FixIt Co"
    assert created.getAddress() == "456 Oak Ave"
    assert len(givenController.companies) == 1


@pytest.mark.parametrize(
    "name,address,companyCnt,error",
    [
        ("", "456 Oak Ave", 0, "The name of a company cannot be empty."),
        ("FixIt Co", "", 0, "The address of a company cannot be empty."),
    ],
)
def testCreateCompanyInvalidValuesFail(givenController, name, address, companyCnt, error):
    with pytest.raises(ValueError) as err:
        givenController.createCompany(name, address)
    assert str(err.value) == error
    assert len(givenController.companies) == companyCnt