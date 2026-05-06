from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool, mw):
    with freeze_time("2020-01-01"):
        if modelingTool == "umple":
            from ..umple.controller import HomeForTheElderlyController
            from ..umple.generated_model_layer import Person
            Person.personsById.clear()
        else:
            from ..ecore.controller import HomeForTheElderlyController
            from ..ecore.generated_model_layer import Person

        controller = HomeForTheElderlyController()

        person = mw(Person, id="person", name="John Doe", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
        person.setRegistrationDate(datetime.today())
        person.setAbilities("")

        yield controller

@pytest.mark.parametrize(
    "abilities",
    [
        "requires wheelchair",
        "",
    ],
)
def testUpdatePersonAbilitiesSuccess(givenController, abilities, mw):
    # Act
    givenController.updatePersonAbilities("person", abilities)

    # Assert
    updatedPerson = None
    for p in mw(givenController.homeForTheElderly).getPeople():
        if p.getId() == "person":
            updatedPerson = p
    assert updatedPerson.getAbilities() == abilities

def testUpdatePersonAbilitiesInvalid(givenController, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updatePersonAbilities("unknown", "requires wheelchair")

    # Assert
    assert str(errorInfo.value) == 'Person with ID "unknown" does not exist.'

    person = None
    for p in mw(givenController.homeForTheElderly).getPeople():
        if p.getId() == "person":
            person = p
    assert person.getAbilities() == ""