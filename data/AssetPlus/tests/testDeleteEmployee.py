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
    "email, expectedCount",
    [
        ("jeff@ap.com", 1),
        ("john@ap.com", 1),
        ("kyle@ap.com", 2),
        ("paul@ap.com", 2),
    ],
)
def testDeleteEmployeeScenarioOutline(givenController, mw, email, expectedCount):
    givenController.deleteEmployee(email)
    employees = mw(givenController.assetPlus).getEmployees()
    assert len(employees) == expectedCount

    stillExists = False
    for e in employees:
        if e.getEmail() == email:
            stillExists = True
            break
    assert stillExists is False


def testDeleteEmployeeManagerEmailDoesNotDeleteManager(givenController, mw):
    givenController.deleteEmployee("manager@ap.com")
    employees = mw(givenController.assetPlus).getEmployees()
    assert len(employees) == 2

    manager = mw(givenController.assetPlus).getManager()
    assert manager is not None
    assert manager.getEmail() == "manager@ap.com"
    for e in employees:
        assert e.getEmail() != "manager@ap.com"
