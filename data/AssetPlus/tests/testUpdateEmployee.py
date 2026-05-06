import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller.controller import AssetPlusController
        from ..umple.generated_model_layer import (
            User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, TicketImage
        )
        uniqueKeywords = ["byemail", "byname", "byid", "byassetnumber", "byimageurl"]
        for cls in [User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, TicketImage]:
            for attr in dir(cls):
                name = attr.lower()
                if any(k in name for k in uniqueKeywords):
                    mapping = getattr(cls, attr)
                    if isinstance(mapping, dict):
                        mapping.clear()
    else:
        from ..ecore.controller.controller import AssetPlusController
        from ..ecore.generated_model_layer import Manager, Employee
    controller = AssetPlusController()
    ap = controller.assetPlus
    mgr = mw(Manager, email="manager@ap.com", name="", password="manager", phoneNumber="", assetPlus=ap)
    mw(ap).setManager(mgr.model)
    emp1 = mw(Employee, email="jeff@ap.com", name="Jeff", password="pass1", phoneNumber="(555)555-5555", assetPlus=ap)
    mw(ap).addEmployee(emp1.model)
    emp2 = mw(Employee, email="john@ap.com", name="John", password="pass2", phoneNumber="(444)444-4444", assetPlus=ap)
    mw(ap).addEmployee(emp2.model)
    yield controller


@pytest.mark.parametrize(
    "email, newPassword, newName, newPhoneNumber",
    [
        ("jeff@ap.com", "pass5", "Jake", "(111)111-1111"),
        ("john@ap.com", "pass6", "Johnny", "(111)777-7777"),
        ("john@ap.com", "pass2", "", "(444)444-7777"),
        ("john@ap.com", "pass2", "Jon", ""),
    ],
)
def testUpdateEmployeeSuccess(givenController, mw, email, newPassword, newName, newPhoneNumber):
    givenController.updateEmployee(email, newPassword, newName, newPhoneNumber)
    employees = mw(givenController.assetPlus).getEmployees()
    assert len(employees) == 2

    updated = None
    for e in employees:
        if e.getEmail() == email:
            updated = e
            break
    assert updated is not None
    assert updated.getEmail() == email
    assert updated.getPassword() == newPassword
    assert updated.getName() == newName
    assert updated.getPhoneNumber() == newPhoneNumber


@pytest.mark.parametrize(
    "email, newPassword, newName, newPhoneNumber, errorMessage",
    [
        ("jeff@ap.com", "", "Jeff", "(555)666-5555", "Password cannot be empty"),
    ],
)
def testUpdateEmployeeFail(givenController, mw, email, newPassword, newName, newPhoneNumber, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateEmployee(email, newPassword, newName, newPhoneNumber)
    assert str(errorInfo.value) == errorMessage

    employees = mw(givenController.assetPlus).getEmployees()
    assert len(employees) == 2

    byEmail = {e.getEmail(): e for e in employees}
    assert set(byEmail.keys()) == {"jeff@ap.com", "john@ap.com"}

    jeff = byEmail["jeff@ap.com"]
    assert jeff.getEmail() == "jeff@ap.com"
    assert jeff.getPassword() == "pass1"
    assert jeff.getName() == "Jeff"
    assert jeff.getPhoneNumber() == "(555)555-5555"

    john = byEmail["john@ap.com"]
    assert john.getEmail() == "john@ap.com"
    assert john.getPassword() == "pass2"
    assert john.getName() == "John"
    assert john.getPhoneNumber() == "(444)444-4444"
