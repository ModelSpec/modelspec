from datetime import date, datetime  # datetime used for birthdate type normalization
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool):
    global User
    with freeze_time("2020-01-01"):
        if modelingTool == "umple":
            from ..umple.controller import FacepageController
            from ..umple.generated_model_layer import User
            User.usersByUserID.clear()
        else:
            from ..ecore.controller import FacepageController
            from ..ecore.generated_model_layer import User

        controller = FacepageController()
        yield controller


def testCreateUserNewSuccess(givenController, mw):
    givenController.createUser(1, "John Doe", "john.doe@mail.com", date(2000, 1, 1))

    face = mw(givenController.facepage)
    createdUser = None
    for u in face.getUsers():
        if u.getName() == "John Doe":
            createdUser = u
            break

    assert createdUser is not None
    assert createdUser.getUserID() == 1
    assert createdUser.getName() == "John Doe"
    assert createdUser.getEmail() == "john.doe@mail.com"
    birthDate = createdUser.getBirthDate()
    assert (birthDate.date() if isinstance(birthDate, datetime) else birthDate) == date(2000, 1, 1)
    assert face.numberOfUsers() == 1


@pytest.mark.parametrize(
    "userID,name,email,dateOfBirth,error",
    [
        (None, "John Doe", "john.doe@mail.com", date(2000, 1, 1), "The userID of a user must not be empty."),
        (1, "", "john.doe@mail.com", date(2000, 1, 1), "The name of a user must not be empty."),
        (1, "John Doe", "john.doe.mail.com", date(2000, 1, 1), 'The email of a user must contain exactly one "@" character.'),
        (1, "John Doe", "john.doe@@mail.com", date(2000, 1, 1), 'The email of a user must contain exactly one "@" character.'),
        (1, "John Doe", "johndoe@mailcom", date(2000, 1, 1), 'The email of a user must contain at least one "." after the "@" character.'),
        (1, "John Doe", "johndoe@mail.", date(2000, 1, 1), 'The email of a user must not end with a "." character.'),
        (1, "John Doe", "john.doe@mail.com", date(2020, 1, 2), "The date of birth of a user must not be in the future."),
    ],
)
def testCreateUserInvalidValuesFail(givenController, mw, userID, name, email, dateOfBirth, error):
    with pytest.raises(ValueError) as err:
        givenController.createUser(userID, name, email, dateOfBirth)
    assert str(err.value) == error
    assert mw(givenController.facepage).numberOfUsers() == 0


def testCreateUserDuplicateUserIDFail(givenController, mw):
    u1 = mw(User, userID=1, name="John Doe", email="john.doe@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    with pytest.raises(ValueError) as err:
        givenController.createUser(1, "Jane Smith", "jane.smith@mail.com", date(1995, 5, 5))
    assert str(err.value) == 'A user with the ID "1" already exists.'

    face = mw(givenController.facepage)
    assert face.numberOfUsers() == 1
    existing = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            existing = u
            break

    assert existing is not None
    assert existing.getUserID() == 1
    assert existing.getName() == "John Doe"
    assert existing.getEmail() == "john.doe@mail.com"
    birthDate = existing.getBirthDate()
    assert birthDate.year == 2000
    assert birthDate.month == 1
    assert birthDate.day == 1