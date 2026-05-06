from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool):
    with freeze_time("2020-01-01"):
        if modelingTool == "umple":
            from ..umple.controller import HomeForTheElderlyController
            from ..umple.generated_model_layer import Person
        else:
            from ..ecore.controller import HomeForTheElderlyController as HomeForTheElderlyController
            from ..ecore.generated_model_layer import Person
        if modelingTool == "umple":
            Person.personsById.clear()

        controller = HomeForTheElderlyController()

        yield controller

def testCreateNewPersonSuccess(givenController, mw):
    # Act
    result = givenController.createPerson("John Doe", datetime(1950, 1, 1))

    # Assert
    assert result is None

    createdPerson = None
    home = mw(givenController.homeForTheElderly)
    for p in home.getPeople():
        if p.getName() == "John Doe":
            createdPerson = p
            break

    assert createdPerson is not None
    assert createdPerson.getId()
    assert createdPerson.getName() == "John Doe"
    assert createdPerson.getBirthdate() == datetime(1950, 1, 1)
    assert createdPerson.getRegistrationDate().date() == datetime(2020, 1, 1).date()
    assert createdPerson.getAbilities() == ""

    assert home.numberOfPeople() == 1

@pytest.mark.parametrize(
    "name, birthdate, errorMessage",
    [
        ("", datetime(1950, 1, 1), "The name of a person must not be empty."),
        ("John Doe", None, "The birthdate of a person must not be empty."),
        ("John Doe", datetime(2020, 1, 2), "The birthdate of a person must not be in the future.")
    ]
)
def testCreateNewPersonInvalidValuesFail(givenController, name, birthdate, errorMessage, mw):

    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.createPerson(name, birthdate)

    # Assert
    assert str(errorInfo.value) == errorMessage
    home = mw(givenController.homeForTheElderly)
    assert home.numberOfPeople() == 0