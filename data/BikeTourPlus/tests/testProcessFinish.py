import pytest
from datetime import datetime


@pytest.fixture
def controllerWithFinish(modelingTool, mw):
    global Participant, Status, BikeTour
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
        from ..ecore.generated_model_layer import BikeTour, Gear, Combo, ComboItem, Guide, Participant, Status

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

    jeff = mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
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

    alice.setStatus(Status.NotAssigned)
    charlie.setStatus(Status.NotAssigned)
    johndoe.setStatus(Status.NotAssigned)
    emily.setStatus(Status.NotAssigned)
    new.setStatus(Status.NotAssigned)

    tour1 = mw(BikeTour, id=1, startWeek=1, endWeek=3, guide=jeff.model, bikeTourPlus=controller.btp)
    tour1.addParticipant(alice.model)
    tour1.addParticipant(charlie.model)
    tour1.addParticipant(johndoe.model)

    tour2 = mw(BikeTour, id=2, startWeek=4, endWeek=5, guide=jeff.model, bikeTourPlus=controller.btp)
    tour2.addParticipant(emily.model)

    yield controller


@pytest.mark.parametrize("email", [
    ("alice@gmail.com"),
    ("charlie@hotmail.ca"),
])
def testFinishTourSuccess(controllerWithFinish, mw, email):
    btp = mw(controllerWithFinish.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == email)
    participant.setStatus(Status.Started)

    controllerWithFinish.processFinish(email)

    assert participant.getStatus() == Status.Finished
    assert participant.getRefundedPercentageAmount() == 0


@pytest.mark.parametrize("email, error", [
    ("nonexisting@mail.ca", "Participant with email address nonexisting@mail.ca does not exist"),
])
def testFinishTourNonExistentParticipant(controllerWithFinish, mw, email, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithFinish.processFinish(email)

    assert str(error_info.value) == error

    btp = mw(controllerWithFinish.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is None
    assert len(btp.getParticipants()) == 5


@pytest.mark.parametrize("email, error", [
    ("new@hotmail.ca", "Cannot finish a tour for a participant who has not started their tour"),
])
def testFinishTourNotAssigned(controllerWithFinish, mw, email, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithFinish.processFinish(email)

    assert str(error_info.value) == error

    btp = mw(controllerWithFinish.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant.getStatus() == Status.NotAssigned


@pytest.mark.parametrize("email, error", [
    ("alice@gmail.com", "Cannot finish a tour for a participant who has not started their tour"),
])
def testFinishTourAssigned(controllerWithFinish, mw, email, error):
    btp = mw(controllerWithFinish.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == email)
    participant.setStatus(Status.Assigned)

    with pytest.raises(ValueError) as error_info:
        controllerWithFinish.processFinish(email)

    assert str(error_info.value) == error
    assert participant.getStatus() == Status.Assigned


@pytest.mark.parametrize("email, error", [
    ("charlie@hotmail.ca", "Cannot finish a tour for a participant who has not started their tour"),
])
def testFinishTourPaid(controllerWithFinish, mw, email, error):
    btp = mw(controllerWithFinish.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == email)
    participant.setStatus(Status.Paid)

    with pytest.raises(ValueError) as error_info:
        controllerWithFinish.processFinish(email)

    assert str(error_info.value) == error
    assert participant.getStatus() == Status.Paid


@pytest.mark.parametrize("email, error", [
    ("emily@hotmail.ca", "Cannot finish tour because the participant is banned"),
])
def testFinishTourBanned(controllerWithFinish, mw, email, error):
    btp = mw(controllerWithFinish.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == email)
    participant.setStatus(Status.Banned)

    with pytest.raises(ValueError) as error_info:
        controllerWithFinish.processFinish(email)

    assert str(error_info.value) == error
    assert participant.getStatus() == Status.Banned


@pytest.mark.parametrize("email, error", [
    ("alice@gmail.com", "Cannot finish tour because the participant has cancelled their tour"),
])
def testFinishTourCancelled(controllerWithFinish, mw, email, error):
    btp = mw(controllerWithFinish.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == email)
    participant.setStatus(Status.Cancelled)

    with pytest.raises(ValueError) as error_info:
        controllerWithFinish.processFinish(email)

    assert str(error_info.value) == error
    assert participant.getStatus() == Status.Cancelled


@pytest.mark.parametrize("email, error", [
    ("alice@gmail.com", "Cannot finish tour because the participant has already finished their tour"),
])
def testFinishTourAlreadyFinished(controllerWithFinish, mw, email, error):
    btp = mw(controllerWithFinish.btp)
    participant = next(p for p in btp.getParticipants() if p.getEmail() == email)
    participant.setStatus(Status.Finished)

    with pytest.raises(ValueError) as error_info:
        controllerWithFinish.processFinish(email)

    assert str(error_info.value) == error
    assert participant.getStatus() == Status.Finished
