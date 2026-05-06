import pytest
from datetime import datetime


@pytest.fixture
def controllerWithParticipant(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import User, Guide, Participant, Manager
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Guide, Participant, Manager

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Manager, email="manager@btp.com", password="password", bikeTourPlus=controller.btp)
    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)
    mw(Participant, email="peter@email.com", password="pass1", name="Peter", emergencyContact="(666)555-5555",
       nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
       authorizationCode="None", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    mw(Participant, email="tyler@email.com", password="pass2", name="Tyler", emergencyContact="(777)444-4444",
       nrWeeks=2, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="None", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    yield controller


@pytest.mark.parametrize("email, password, name, emergencyContact, nrWeeks, weeksFrom, weeksUntil, lodge", [
    ("user3@mail.ca", "password3", "User3", "(333)333-3333", 3, 3, 10, True),
    ("user4@mail.ca", "password4", "User4", "(444)444-4444", 4, 4, 7, True),
])
def testRegisterParticipantSuccess(controllerWithParticipant, mw, email, password, name, emergencyContact, nrWeeks,
                                   weeksFrom, weeksUntil, lodge):
    controllerWithParticipant.registerParticipant(email, password, name, emergencyContact, nrWeeks, weeksFrom, weeksUntil, lodge)

    btp = mw(controllerWithParticipant.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is not None
    assert participant.getName() == name
    assert participant.getNrWeeks() == nrWeeks
    assert participant.getLodgeRequired() == lodge

    assert len(btp.getParticipants()) == 3


@pytest.mark.parametrize("email, password, name, emergencyContact, nrWeeks, weeksFrom, weeksUntil, lodge, error", [
    ("manager@btp.com", "password", "User", "(555)555-5555", 5, 2, 6, True, "Email cannot be manager@btp.com"),
    ("john@email.com", "password", "User", "(111)111-1111", 1, 1, 10, True, "Email already linked to a guide account"),
    ("peter@email.com", "password", "User", "(111)111-1111", 1, 1, 10, True,
     "Email already linked to a participant account"),
    ("user@ mail.ca", "password", "User", "(111)222-333", 1, 8, 9, True, "Email must not contain any spaces"),
    ("user@mail@y.ca", "password", "User", "(111)222-333", 1, 3, 10, True, "Invalid email"),
    ("kyle@email.", "password", "User", "(111)222-333", 1, 3, 10, True, "Invalid email"),
    ("user@mail", "password", "User", "(111)222-333", 1, 3, 10, True, "Invalid email"),
    ("@mail.ca", "password", "User", "(111)222-333", 1, 3, 10, True, "Invalid email"),
    ("user@.ca", "password", "User", "(111)222-333", 1, 3, 10, True, "Invalid email"),
    ("", "password", "User", "(111)222-333", 5, 2, 10, False, "Email cannot be empty"),
    ("user@mail.ca", "", "User", "(555)555-5555", 5, 2, 10, False, "Password cannot be empty"),
    ("user@mail.ca", "password", "", "(555)555-5555", 5, 2, 10, False, "Name cannot be empty"),
    ("user@mail.ca", "password", "User", "", 5, 2, 10, False, "Emergency contact cannot be empty"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 0, 5, 8, True, "Number of weeks must be greater than zero"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 11, 5, 8, True,
     "Number of weeks must be less than or equal to the number of biking weeks in the biking season"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 3, 5, 6, True,
     "Number of weeks must be less than or equal to the number of available weeks"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 3, 6, 5, True,
     "Week from which one is available must be less than or equal to the week until which one is available"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 3, 0, 6, True,
     "Available weeks must be within weeks of biking season (1-10)"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 3, 11, 6, True,
     "Available weeks must be within weeks of biking season (1-10)"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 3, -1, 0, True,
     "Available weeks must be within weeks of biking season (1-10)"),
    ("user@mail.ca", "password", "User", "(555)555-5555", 3, 6, 11, True,
     "Available weeks must be within weeks of biking season (1-10)"),
])
def testRegisterParticipantFailure(controllerWithParticipant, mw, email, password, name, emergencyContact, nrWeeks,
                                   weeksFrom, weeksUntil, lodge, error):
    with pytest.raises(Exception) as excInfo:
        controllerWithParticipant.registerParticipant(email, password, name, emergencyContact, nrWeeks, weeksFrom, weeksUntil, lodge)

    assert str(excInfo.value) == error
    assert len(mw(controllerWithParticipant.btp).getParticipants()) == 2
