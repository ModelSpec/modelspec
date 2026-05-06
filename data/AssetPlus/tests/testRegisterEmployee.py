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
    "email, password, name, phoneNumber",
    [
        ("lisa@ap.com", "pass4", "Lisa", "(888)888-8888"),
        ("liam@ap.com", "pass5", "Liam", "(777)777-7777"),
        ("owen@ap.com", "pass10", "", "(888)888-5555"),
        ("noah@ap.com", "pass11", "Noah", ""),
    ],
)
def testRegisterEmployeeSuccess(givenController, mw, email, password, name, phoneNumber):
    givenController.registerEmployee(email, password, name, phoneNumber)

    employees = mw(givenController.assetPlus).getEmployees()
    assert len(employees) == 3

    created = None
    for e in employees:
        if e.getEmail() == email:
            created = e
            break
    assert created is not None
    assert created.getEmail() == email
    assert created.getPassword() == password
    assert created.getName() == name
    assert created.getPhoneNumber() == phoneNumber


@pytest.mark.parametrize(
    "email, password, name, phoneNumber, errorMessage",
    [
        ("manager@ap.com", "pass1", "Paul", "(111)111-1111", "Email cannot be manager@ap.com"),
        ("jeff@ap.com", "pass2", "Jeff", "(111)777-7777", "Email already linked to an employee account"),
        ("bart @ ap.com", "pass3", "Bart", "(444)666-6666", "Email must not contain any spaces"),
        ("dony@ap@.com", "pass4", "Dony", "(777)555-7777", "Invalid email"),
        ("kyle@ap.", "pass5", "Kyle", "(666)777-6666", "Invalid email"),
        ("greg.ap@com", "pass6", "Greg", "(777)888-7777", "Invalid email"),
        ("@ap.com", "pass7", "Otto", "(111)777-6666", "Invalid email"),
        ("karl@.com", "pass8", "Karl", "(111)777-6661", "Invalid email"),
        ("", "pass9", "Vino", "(777)888-5555", "Email cannot be empty"),
        ("jeff@yahoo.com", "pass11", "Jeff", "(111)111-1111", "Email domain must be @ap.com"),
        ("luke@ap.com", "", "Luke", "(999)888-5555", "Password cannot be empty"),
    ],
)
def testRegisterEmployeeFail(givenController, mw, email, password, name, phoneNumber, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.registerEmployee(email, password, name, phoneNumber)
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
