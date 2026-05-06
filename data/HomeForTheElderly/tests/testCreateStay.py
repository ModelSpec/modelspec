from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool, mw):
    global Proposal, Category, Room, Bed
    with freeze_time("2020-01-01"):
        if modelingTool == "umple":
            from ..umple.controller import HomeForTheElderlyController
            from ..umple.generated_model_layer import Person, Department, Category, Room, Bed, Proposal
            Person.personsById.clear()
            Department.departmentsById.clear()
        else:
            from ..ecore.controller import HomeForTheElderlyController
            from ..ecore.generated_model_layer import Person, Department, Category, Room, Bed, Proposal

        controller = HomeForTheElderlyController()

        dept1 = mw(Department, id="dept1", homeForTheElderly=controller.homeForTheElderly)

        category = mw(Category, price=1000.0, type="RH")
        room1 = mw(Room, roomNumber = 1, department = dept1.model, category = category.model)

        bed = mw(Bed, bedNumber = 1, room = room1.model) 

        person = mw(Person, id="person", name="John Doe", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
        person.setAbilities("requires wheelchair")

        yield controller, person, bed, dept1

def testCreateNewStaySuccess(givenController, mw):
    # Arrange
    controller, person, bed, _ = givenController

    mw(Proposal, status="waiting", validated=False, bed=bed.model, person=person.model)

    # Act
    controller.createStay(1, 1, "dept1", "person", datetime(2020, 1, 2))

    # Assert
    stay = person.getStay(0)
    assert stay.getIntakeDate().date() == datetime(2020, 1, 2).date()
    assert stay.getEndDate() == None
    assert stay.getPerson().getId() == "person"
    stayBed = stay.getBed()
    assert stayBed.getBedNumber() == 1
    bedRoom = stayBed.getRoom()
    assert bedRoom.getRoomNumber() == 1
    roomDepartment = bedRoom.getDepartment()
    assert roomDepartment.getId() == "dept1"

    stayCount = 0
    for p in mw(controller.homeForTheElderly).getPeople():
        stayCount += p.numberOfStaies()
    assert stayCount == 1

def testCreateNewStayWithProposalForDifferentRoomSuccess(givenController, mw):
    # Arrange
    controller, person, bed1, dept1 = givenController

    category = mw(Category, price=3000.0, type="SF")
    room2 = mw(Room, roomNumber = 2, department = dept1.model, category = category.model)

    mw(Bed, bedNumber = 1, room = room2.model)

    mw(Proposal, status="waiting", validated=False, bed=bed1.model, person=person.model)

    # Act
    result = controller.createStay(1, 2, "dept1", "person", datetime(2020, 1, 2))

    # Assert
    assert result is None

    stay = person.getStay(0)
    assert stay.getIntakeDate().date() == datetime(2020, 1, 2).date()
    assert stay.getEndDate() == None
    assert stay.getPerson().getId() == "person"
    stayBed = stay.getBed()
    assert stayBed.getBedNumber() == 1
    bedRoom = stayBed.getRoom()
    assert bedRoom.getRoomNumber() == 2
    roomDepartment = bedRoom.getDepartment()
    assert roomDepartment.getId() == "dept1"

    proposal = person.getProposal(0)
    proposalBed = proposal.getBed()
    assert proposalBed.getBedNumber() == 1
    proposalBedRoom = proposalBed.getRoom()
    assert proposalBedRoom.getRoomNumber() == 1
    proposalRoomDept = proposalBedRoom.getDepartment()
    assert proposalRoomDept.getId() == "dept1"
    assert proposal.getPerson().getId() == "person"

    stayCount = 0
    for p in mw(controller.homeForTheElderly).getPeople():
        stayCount += p.numberOfStaies()
    assert stayCount == 1

def testCreateStayNoProposalFail(mw, givenController):
    # Arrange
    controller, _, _, _ = givenController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.createStay(1, 1, "dept1", "person", datetime(2020, 1, 2))

    # Assert
    assert str(errorInfo.value) == "Cannot create stay for \"person\" without a proposal."
    stayCount = 0
    for p in mw(controller.homeForTheElderly).getPeople():
        stayCount += p.numberOfStaies()
    assert stayCount == 0

@pytest.mark.parametrize(
    "person, bed, date, errorMessage",
    [
        (None, 1, datetime(2020, 1, 2), "Person cannot be empty."),
        ("person", None, datetime(2020, 1, 2), "Bed cannot be empty."),
        ("person2", 1, datetime(2020, 1, 2), "Person \"person2\" does not exist."),
        ("person", 2, datetime(2020, 1, 2), "Bed 2 of room 1 of department \"dept1\" does not exist."),
        ("person", 1, datetime(2019, 12, 31), "Intake date must be on or after the current date.")
    ]
)
def testCreateStayInvalidValuesFail(mw, givenController, person, bed, date, errorMessage):
    # Arrange
    controller, personArrange, bedArrange, _ = givenController

    mw(Proposal, status="waiting", validated=False, bed=bedArrange.model, person=personArrange.model)

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.createStay(bed, 1, "dept1", person, date)

    # Assert
    assert str(errorInfo.value) == errorMessage
    stayCount = 0
    for p in mw(controller.homeForTheElderly).getPeople():
        stayCount += p.numberOfStaies()
    assert stayCount == 0