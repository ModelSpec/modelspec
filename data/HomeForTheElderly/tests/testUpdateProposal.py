from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool, mw):
    global Bed, Person
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

        mw(Bed, bedNumber = 1, room = room1.model)

        person = mw(Person, id="person", name="John Doe", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
        person.setAbilities("requires wheelchair")

        proposal = mw(Proposal, status="waiting", validated=False, bed=room1.getBed(0).model, person=person.model)

        yield controller, proposal, room1

@pytest.mark.parametrize(
    "status",
    [
        ("waiting"),
        ("accepted"),
        ("refused"),
        ("invalidated")
    ]
)
def testUpdateProposalStatusSuccess(givenController, status):
    # Arrange
    controller, proposal, _ = givenController

    # Act
    controller.updateProposal(1, 1, "dept1", "person", status=status)

    # Assert
    assert proposal.getStatus() == status

@pytest.mark.parametrize(
    "status, errorNessage",
    [
        ("", "The status of a proposal must not be empty."),
        ("unknown", "The status of a proposal must be one of: waiting, accepted, refused, invalidated.")
    ]
)
def testUpdateProposalStatusFail(givenController, status, errorNessage):
    # Arrange
    controller, proposal, _ = givenController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateProposal(1, 1, "dept1", "person", status=status)

    # Assert
    assert str(errorInfo.value) == errorNessage
    assert proposal.getStatus() == "waiting"

@pytest.mark.parametrize(
    "currentValidated, newValidated",
    [
        (False, True),
        (True, False),
        (False, False),
        (True, True)
    ]
)
def testUpdateProposalValidatedSuccess(givenController, currentValidated, newValidated):
    # Arrange
    controller, proposal, _ = givenController

    proposal.setValidated(currentValidated)

    # Act
    controller.updateProposal(1, 1, "dept1", "person", validated=newValidated)

    # Assert
    assert proposal.getValidated() == newValidated

def testUpdateProposalBedSuccess(givenController, mw):
    # Arrange
    controller, proposal, room = givenController

    mw(Bed, bedNumber = 2, room = room.model)

    # Act
    controller.updateProposal(1, 1, "dept1", "person", newBedNumber=2, newRoomNumber=1, newDepartment="dept1")

    # Assert
    assert proposal.getBed().getBedNumber() == 2
    proposalBed1 = None
    proposalBed2 = None
    for person in mw(controller.homeForTheElderly).getPeople():
        for prop in person.getProposals():
            bed = prop.getBed()
            if bed.getBedNumber() == 1:
                proposalBed1 = prop
            elif bed.getBedNumber() == 2:
                proposalBed2 = prop
    assert proposalBed1 is None
    assert proposalBed2 is not None

    bedRoom = proposalBed2.getBed().getRoom()
    assert bedRoom.getRoomNumber() == 1
    roomDepartment = bedRoom.getDepartment()
    assert roomDepartment.getId() == "dept1"
    assert proposalBed2.getPerson().getId() == "person"

def testUpdateProposalBedFail(givenController, mw):
    # Arrange
    controller, proposal, _ = givenController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateProposal(1, 1, "dept1", "person", newBedNumber=3, newRoomNumber=1, newDepartment="dept1")

    # Assert
    assert str(errorInfo.value) == "Bed 3 of room 1 of department \"dept1\" does not exist."
    assert proposal.getPerson().getId() == "person"
    assert proposal.getBed().getBedNumber() == 1
    bedRoom = proposal.getBed().getRoom()
    assert bedRoom.getRoomNumber() == 1
    roomDepartment = bedRoom.getDepartment()
    assert roomDepartment.getId() == "dept1"

def testUpdateProposalPersonSuccess(givenController, mw):
    # Arrange
    controller, proposal, _ = givenController

    person = mw(Person, id="person2", name="Jane Smith", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
    person.setAbilities("requires wheelchair")

    # Act
    controller.updateProposal(1, 1, "dept1", "person", newPerson="person2")

    # Assert
    assert proposal.getPerson().getId() == "person2"
    personOne = None
    personTwo = None
    for p in mw(controller.homeForTheElderly).getPeople():
        if p.getId() == "person":
            personOne = p
        elif p.getId() == "person2":
            personTwo = p
    assert personOne.numberOfProposals() == 0
    assert personTwo.numberOfProposals() == 1

    proposalPerson2 = personTwo.getProposal(0)
    
    assert proposalPerson2 is not None
    assert proposalPerson2.getBed().getBedNumber() == 1

    bedRoom = proposalPerson2.getBed().getRoom()
    assert bedRoom.getRoomNumber() == 1

    roomDepartment = bedRoom.getDepartment()
    assert roomDepartment.getId() == "dept1"

def testUpdateProposalPersonFail(givenController, mw):
    # Arrange
    controller, proposal, _ = givenController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateProposal(1, 1, "dept1", "person", newPerson="person3")

    # Assert
    assert str(errorInfo.value) == "Person \"person3\" does not exist."
    assert proposal.getPerson().getId() == "person"
    assert proposal.getBed().getBedNumber() == 1
    bedRoom = proposal.getBed().getRoom()
    assert bedRoom.getRoomNumber() == 1
    roomDepartment = bedRoom.getDepartment()
    assert roomDepartment.getId() == "dept1"

def testUpdateProposalNotFoundFail(givenController):
    # Arrange
    controller, _, _ = givenController

    # Act
    with pytest.raises(ValueError) as errorInfo:
        controller.updateProposal(1, 1, "dept1", "person2", status="accepted")

    # Assert
    assert str(errorInfo.value) == "Proposal for bed 1 of room 1 of department \"dept1\" to person \"person2\" does not exist."