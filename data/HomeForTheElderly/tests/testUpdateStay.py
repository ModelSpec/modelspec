from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool, mw):
    global Person
    with freeze_time("2020-01-01"):
        if modelingTool == "umple":
            from ..umple.controller import HomeForTheElderlyController
            from ..umple.generated_model_layer import Person, Department, Category, Room, Bed, Proposal, Stay
            Person.personsById.clear()
            Department.departmentsById.clear()
        else:
            from ..ecore.controller import HomeForTheElderlyController
            from ..ecore.generated_model_layer import Person, Department, Category, Room, Bed, Proposal, Stay

        controller = HomeForTheElderlyController()

        dept1 = mw(Department, id="dept1", homeForTheElderly=controller.homeForTheElderly)

        category = mw(Category, price=1000.0, type="RH")
        room1 = mw(Room, roomNumber = 1, department = dept1.model, category = category.model)

        bed = mw(Bed, bedNumber = 1, room = room1.model) 

        person = mw(Person, id="person", name="John Doe", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
        person.setAbilities("requires wheelchair")

        mw(Proposal, status="waiting", validated=False, bed=bed.model, person=person.model)

        stay = mw(Stay, intakeDate=datetime(2020, 1, 2), endDate=None, person=person.model, bed=bed.model)

        yield controller, stay

def testUpdateStayIntakeDateSuccess(givenController):
    # Arrange
    controller, stay = givenController

    # Act
    result = controller.updateStay(1, 1, "dept1", "person", datetime(2020, 1, 15))

    # Assert
    assert result is None
    assert stay.getIntakeDate().date() == datetime(2020, 1, 15).date()

@pytest.mark.parametrize(
    "intakeDate, errorMessage",
    [
        ("", "Intake date must not be empty."),
        (datetime(2019, 12, 31), "Intake date must be on or after the current date.")
    ]
)
def testUpdateStayInvalidIntakeDateFail(givenController, intakeDate, errorMessage):
    # Arrange
    controller, stay = givenController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateStay(1, 1, "dept1", "person", intakeDate)

    # Assert
    assert str(errorInfo.value) == errorMessage
    assert stay.getIntakeDate().date() == datetime(2020, 1, 2).date()

@pytest.mark.parametrize(
    "endDate",
    [
        (""),
        (datetime(2019, 12, 31)),
        (datetime(2021, 1, 1)),
        (datetime(2020, 1, 15))
    ]
)
def testUpdateStayEndDateSuccess(givenController, endDate):
    # Arrange
    controller, stay = givenController

    # Act
    result = controller.updateStay(1, 1, "dept1", "person", endDate=endDate)

    # Assert
    assert result is None
    if endDate == "":
        assert stay.getEndDate() == None
    else:
        assert stay.getEndDate().date() == endDate.date()

def testUpdateStayNonExistentStayFail(mw, givenController):
    # Arrange
    controller, _, = givenController

    person = mw(Person, id="person2", name="Jane Smith", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
    person.setAbilities("requires wheelchair")

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateStay(1, 1, "dept1", "person2", datetime(2020, 1, 3))

    # Assert
    assert str(errorInfo.value) == "Stay for person \"person2\" and bed 1 of room 1 of department \"dept1\" does not exist."