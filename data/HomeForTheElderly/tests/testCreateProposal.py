from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool, mw):
    with freeze_time("2020-01-01"):
        if modelingTool == "umple":
            from ..umple.controller import HomeForTheElderlyController
            from ..umple.generated_model_layer import Person, Department, Category, Room, Bed
            Person.personsById.clear()
            Department.departmentsById.clear()
        else:
            from ..ecore.controller import HomeForTheElderlyController
            from ..ecore.generated_model_layer import Person, Department, Category, Room, Bed

        controller = HomeForTheElderlyController()

        dept1 = mw(Department, id="dept1", homeForTheElderly=controller.homeForTheElderly)

        category = mw(Category, price=1000.0, type="RH")
        room1 = mw(Room, roomNumber = 1, department = dept1.model, category = category.model)

        mw(Bed, bedNumber = 1, room = room1.model)

        person = mw(Person, id="person", name="John Doe", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
        person.setAbilities("requires wheelchair")

        yield controller

def testCreateNewProposalSuccess(givenController, mw):
    # Act
    givenController.createProposal(1, 1, "dept1", "person")

    # Assert
    proposalCount = 0
    person = None
    for p in mw(givenController.homeForTheElderly).getPeople():
        proposalCount += p.numberOfProposals()
        if p.getId() == "person":
            person = p
    assert proposalCount == 1

    proposal = person.getProposal(0)

    proposalBed = proposal.getBed()

    assert proposalBed.getBedNumber() == 1
    bedRoom = proposalBed.getRoom()
    assert bedRoom.getRoomNumber() == 1
    roomDepartment = bedRoom.getDepartment()
    assert roomDepartment.getId() == "dept1"

    proposalPerson = proposal.getPerson()
    assert proposalPerson.getId() == "person"

    assert proposal.getStatus() == "waiting"
    assert not proposal.getValidated()

@pytest.mark.parametrize(
    "bed, person, errorMessage",
    [
        (None, "person", "Bed cannot be empty."),
        (1, None, "Person cannot be empty."),
        (2, "person", "Bed \"bed2\" does not exist."),
        (1, "person2", "Person \"person2\" does not exist.")
    ]
)
def testCreateNewProposalInvalidValuesFail(givenController, bed, person, errorMessage, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createProposal(bed, 1, "dept1", person)

    # Assert
    assert str(errorInfo.value) == errorMessage
    proposalCount = 0
    for p in mw(givenController.homeForTheElderly).getPeople():
        proposalCount += p.numberOfProposals()
    assert proposalCount == 0