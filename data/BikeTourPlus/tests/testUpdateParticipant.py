import pytest
from datetime import datetime


@pytest.fixture
def controllerWithParticipant(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import User, Guide, Participant
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Guide, Participant

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)
    mw(Participant, email="peter@email.com", password="pass1", name="Peter", emergencyContact="(666)555-5555",
       nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    mw(Participant, email="tyler@email.com", password="pass2", name="Tyler", emergencyContact="(777)444-4444",
       nrWeeks=2, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    yield controller


@pytest.mark.parametrize("email, password, name, emergencyContact, nrWeeks, weeksAvailableFrom, weeksAvailableUntil, lodgeRequired, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired", [
    ("peter@email.com", "pass1", "Peter", "(666)555-5555", 1, 1, 2, True, "password3", "User3", "(333)333-3333", 3, 3, 10, True),
    ("tyler@email.com", "pass2", "Tyler", "(777)444-4444", 2, 2, 5, False, "password4", "User4", "(444)444-4444", 4, 4, 7, True),
])
def testUpdateParticipantSuccess(controllerWithParticipant, mw, email, password, name, emergencyContact, nrWeeks, weeksAvailableFrom, weeksAvailableUntil, lodgeRequired, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired):
    controllerWithParticipant.updateParticipant(email, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired)

    btp = mw(controllerWithParticipant.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is not None
    assert participant.getPassword() == newPassword
    assert participant.getName() == newName
    assert participant.getEmergencyContact() == newEmergencyContact
    assert participant.getNrWeeks() == newNrWeeks
    assert participant.getWeekAvailableFrom() == newWeeksAvailableFrom
    assert participant.getWeekAvailableUntil() == newWeeksAvailableUntil
    assert participant.getLodgeRequired() == newLodgeRequired

    assert len(btp.getParticipants()) == 2


@pytest.mark.parametrize("email, password, name, emergencyContact, nrWeeks, weeksAvailableFrom, weeksAvailableUntil, lodgeRequired, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired, error", [
    ("peter@email.com", "pass1", "Peter", "(666)555-5555", 1, 1, 2, True, "", "User", "(555)555-5555", 5, 2, 10, False, "Password cannot be empty"),
    ("peter@email.com", "pass1", "Peter", "(666)555-5555", 1, 1, 2, True, "password", "", "(555)555-5555", 5, 2, 10, False, "Name cannot be empty"),
    ("peter@email.com", "pass1", "Peter", "(666)555-5555", 1, 1, 2, True, "password", "User", "", 5, 2, 10, False, "Emergency contact cannot be empty"),
    ("peter@email.com", "pass1", "Peter", "(666)555-5555", 1, 1, 2, True, "password", "User", "(555)555-5555", 0, 5, 8, True, "Number of weeks must be greater than zero"),
    ("peter@email.com", "pass1", "Peter", "(666)555-5555", 1, 1, 2, True, "password", "User", "(555)555-5555", 11, 5, 8, True, "Number of weeks must be less than or equal to the number of biking weeks in the biking season"),
    ("tyler@email.com", "pass2", "Tyler", "(777)444-4444", 2, 2, 5, False, "password", "User", "(555)555-5555", 3, 5, 6, True, "Number of weeks must be less than or equal to the number of available weeks"),
    ("tyler@email.com", "pass2", "Tyler", "(777)444-4444", 2, 2, 5, False, "password", "User", "(555)555-5555", 3, 6, 5, True, "Week from which one is available must be less than or equal to the week until which one is available"),
    ("tyler@email.com", "pass2", "Tyler", "(777)444-4444", 2, 2, 5, False, "password", "User", "(555)555-5555", 3, 0, 6, True, "Available weeks must be within weeks of biking season (1-10)"),
    ("tyler@email.com", "pass2", "Tyler", "(777)444-4444", 2, 2, 5, False, "password", "User", "(555)555-5555", 3, 11, 6, True, "Available weeks must be within weeks of biking season (1-10)"),
    ("tyler@email.com", "pass2", "Tyler", "(777)444-4444", 2, 2, 5, False, "password", "User", "(555)555-5555", 3, -1, 0, True, "Available weeks must be within weeks of biking season (1-10)"),
    ("tyler@email.com", "pass2", "Tyler", "(777)444-4444", 2, 2, 5, False, "password", "User", "(555)555-5555", 3, 6, 11, True, "Available weeks must be within weeks of biking season (1-10)"),
])
def testUpdateParticipantUnsuccessful(controllerWithParticipant, mw, email, password, name, emergencyContact, nrWeeks, weeksAvailableFrom, weeksAvailableUntil, lodgeRequired, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithParticipant.updateParticipant(email, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired)

    assert str(error_info.value) == error

    btp = mw(controllerWithParticipant.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is not None
    assert participant.getPassword() == password
    assert participant.getName() == name
    assert participant.getEmergencyContact() == emergencyContact
    assert participant.getNrWeeks() == nrWeeks
    assert participant.getWeekAvailableFrom() == weeksAvailableFrom
    assert participant.getWeekAvailableUntil() == weeksAvailableUntil
    assert participant.getLodgeRequired() == lodgeRequired

    assert len(btp.getParticipants()) == 2


@pytest.mark.parametrize("email, password, name, emergencyContact, nrWeeks, weeksAvailableFrom, weeksAvailableUntil, lodgeRequired, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired, error", [
    ("jane@email.com", "pass1", "Peter", "(666)555-5555", 1, 1, 2, True, "", "User", "(555)555-5555", 5, 2, 10, False, "The participant account does not exist"),
])
def testUpdateParticipantNonExistent(controllerWithParticipant, mw, email, password, name, emergencyContact, nrWeeks, weeksAvailableFrom, weeksAvailableUntil, lodgeRequired, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithParticipant.updateParticipant(email, newPassword, newName, newEmergencyContact, newNrWeeks, newWeeksAvailableFrom, newWeeksAvailableUntil, newLodgeRequired)

    assert str(error_info.value) == error

    btp = mw(controllerWithParticipant.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is None

    assert len(btp.getParticipants()) == 2
