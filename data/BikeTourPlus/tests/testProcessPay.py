import pytest
from datetime import datetime


@pytest.fixture
def controllerWithPay(modelingTool, mw):
    global Participant, Status
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, BikeTour, Gear, Combo, ComboItem, Guide, Participant
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
        if hasattr(BikeTour, "biketoursById"):
            BikeTour.biketoursById.clear()
        Status = Participant.Status
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Gear, Combo, ComboItem, Guide, Participant, Status

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    h = mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    e = mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    b = mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)
    mw(Gear, name="tire kit", pricePerWeek=15, bikeTourPlus=controller.btp)

    s = mw(Combo, name="small combo", discount=10, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)

    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)

    alice = mw(Participant, email="alice@gmail.com", password="pass123", name="Alice Jones", emergencyContact="(200)5551234",
               nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=True,
               authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    charlie = mw(Participant, email="charlie@hotmail.ca", password="charlie", name="Charles Tremblay", emergencyContact="(200)5559876",
                 nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
                 authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    johndoe = mw(Participant, email="john@hotmail.ca", password="john123", name="John Doe", emergencyContact="(200)5551234",
                 nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=False,
                 authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    emily = mw(Participant, email="emily@hotmail.ca", password="emily007", name="Emily Green", emergencyContact="(200)5559876",
               nrWeeks=2, weekAvailableFrom=4, weekAvailableUntil=5, lodgeRequired=False,
               authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    new = mw(Participant, email="new@hotmail.ca", password="newnew", name="Johnny New", emergencyContact="(200)5559999",
             nrWeeks=5, weekAvailableFrom=6, weekAvailableUntil=10, lodgeRequired=True,
             authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    alice.setStatus(Status.Assigned)
    charlie.setStatus(Status.Assigned)
    johndoe.setStatus(Status.Assigned)
    emily.setStatus(Status.Assigned)
    new.setStatus(Status.NotAssigned)

    yield controller


@pytest.mark.parametrize("email, code", [
    ("alice@gmail.com", "BIKETOUR200"),
    ("charlie@hotmail.ca", "CODE321"),
])
def testPayForParticipantSuccess(controllerWithPay, mw, email, code):
    controllerWithPay.processPay(email, code)

    btp = mw(controllerWithPay.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant.getStatus() == Status.Paid
    assert participant.getAuthorizationCode() == code


@pytest.mark.parametrize("email, code, error", [
    ("steve@yahoo.com", "BIKETOUR200", "Participant with email address steve@yahoo.com does not exist"),
    ("dave@hotmail.com", "CODE321", "Participant with email address dave@hotmail.com does not exist"),
])
def testPayForNonExistentParticipant(controllerWithPay, mw, email, code, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay(email, code)

    assert str(error_info.value) == error

    btp = mw(controllerWithPay.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is None
    assert len(btp.getParticipants()) == 5


@pytest.mark.parametrize("email, code, error", [
    ("alice@gmail.com", "", "Invalid authorization code"),
    ("charlie@hotmail.ca", "", "Invalid authorization code"),
])
def testPayForParticipantInvalidCode(controllerWithPay, mw, email, code, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay(email, code)

    assert str(error_info.value) == error

    btp = mw(controllerWithPay.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant.getStatus() == Status.Assigned


def testPayForParticipantNotAssigned(controllerWithPay, mw):
    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay("new@hotmail.ca", "PAYup")

    assert str(error_info.value) == "The participant has not been assigned to their tour"

    btp = mw(controllerWithPay.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == "new@hotmail.ca"), None)
    assert participant.getStatus() == Status.NotAssigned


def testPayForParticipantAlreadyPaid(controllerWithPay, mw):
    btp = mw(controllerWithPay.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == "charlie@hotmail.ca")
    participant.setStatus(Status.Paid)

    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay("charlie@hotmail.ca", "PAYup")

    assert str(error_info.value) == "The participant has already paid for their tour"
    assert participant.getStatus() == Status.Paid


def testPayForParticipantStarted(controllerWithPay, mw):
    btp = mw(controllerWithPay.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == "john@hotmail.ca")
    participant.setStatus(Status.Started)

    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay("john@hotmail.ca", "PAYup")

    assert str(error_info.value) == "The participant has already paid for their tour"
    assert participant.getStatus() == Status.Started


def testPayForParticipantBanned(controllerWithPay, mw):
    btp = mw(controllerWithPay.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == "emily@hotmail.ca")
    participant.setStatus(Status.Banned)

    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay("emily@hotmail.ca", "PAYup")

    assert str(error_info.value) == "Cannot pay for tour because the participant is banned"
    assert participant.getStatus() == Status.Banned


def testPayForParticipantCancelled(controllerWithPay, mw):
    btp = mw(controllerWithPay.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == "alice@gmail.com")
    participant.setStatus(Status.Cancelled)

    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay("alice@gmail.com", "PAYup")

    assert str(error_info.value) == "Cannot pay for tour because the participant has cancelled their tour"
    assert participant.getStatus() == Status.Cancelled


def testPayForParticipantFinished(controllerWithPay, mw):
    btp = mw(controllerWithPay.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == "charlie@hotmail.ca")
    participant.setStatus(Status.Finished)

    with pytest.raises(ValueError) as error_info:
        controllerWithPay.processPay("charlie@hotmail.ca", "PAYup")

    assert str(error_info.value) == "The participant has already paid for their tour"
    assert participant.getStatus() == Status.Finished
